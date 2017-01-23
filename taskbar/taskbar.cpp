#ifndef _WIN32_IE // 允许使用 IE 4.0 或更高版本的特定功能。
    #define _WIN32_IE 0x0500 //为 IE 5.0 及更新版本改变为适当的值。
#endif

#include <windows.h>
#include <shellapi.h>
#include <stdio.h>
#include <io.h>

#include "psapi.h"
#include "resource.h"

#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "psapi.lib")

#ifndef INTERNET_OPTION_PER_CONNECTION_OPTION
    #define INTERNET_OPTION_PER_CONNECTION_OPTION           75
    // Options used in INTERNET_PER_CONN_OPTON struct
    #define INTERNET_PER_CONN_FLAGS                         1
    #define INTERNET_PER_CONN_SubMenu_SERVER                  2
    #define INTERNET_PER_CONN_SubMenu_BYPASS                  3
    #define INTERNET_PER_CONN_AUTOCONFIG_URL                4
    #define INTERNET_PER_CONN_AUTODISCOVERY_FLAGS           5
    // PER_CONN_FLAGS
    #define SubMenu_TYPE_DIRECT                               0x00000001
    #define SubMenu_TYPE_SubMenu                                0x00000002
    #define SubMenu_TYPE_AUTO_SubMenu_URL                       0x00000004
    #define SubMenu_TYPE_AUTO_DETECT                          0x00000008

    typedef struct {
      DWORD dwOption;
      union {
        DWORD    dwValue;
        LPTSTR   pszValue;
        FILETIME ftValue;
      } Value;
    } INTERNET_PER_CONN_OPTION, *LPINTERNET_PER_CONN_OPTION;

    typedef struct {
      DWORD                      dwSize;
      LPTSTR                     pszConnection;
      DWORD                      dwOptionCount;
      DWORD                      dwOptionError;
      LPINTERNET_PER_CONN_OPTION pOptions;
    } INTERNET_PER_CONN_OPTION_LIST, *LPINTERNET_PER_CONN_OPTION_LIST;
#endif

extern "C" WINBASEAPI HWND WINAPI GetConsoleWindow();

#define NID_UID 123
#define WM_TASKBARNOTIFY WM_USER+20
#define WM_TASKBARNOTIFY_MENUITEM_SHOW (WM_USER + 21)
#define WM_TASKBARNOTIFY_MENUITEM_HIDE (WM_USER + 22)
#define WM_TASKBARNOTIFY_MENUITEM_RELOAD (WM_USER + 23)
#define WM_TASKBARNOTIFY_MENUITEM_ABOUT (WM_USER + 24)
#define WM_TASKBARNOTIFY_MENUITEM_EXIT (WM_USER + 25)
#define WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE (WM_USER + 26)

HINSTANCE hInst;
HWND hWnd;
HWND hConsole;

WCHAR szWindowClass[16] = L"taskbar";

WCHAR szVisible[8] = L"";
WCHAR szTooltip[512] = L"";
WCHAR szTitle[64] = L"";
WCHAR szBalloon[512] = L"";
WCHAR szPath[2048] = L"";

WCHAR szCommand[1024] = L"python";
WCHAR szEnvironment[1024] = L"ENV_VISIBLE=0\nENV_TOOLTIP=GoProxy\nENV_TITLE=GoProxy Notify\nENV_BALLOON=GoProxy 已经启动，单击托盘图标可以最小化。\n";
WCHAR szSubMenuTitle[2048] = L"RunPython\nRunPip\n";
WCHAR szSubMenuCmd[2048] = L"python\npip\n";
WCHAR szSubMenuPath[2048] = L"";

WCHAR szPathLast[2048] = L"";
WCHAR szCommandLast[1024] = L"";

WCHAR *lpSubMenuTitleList[8] = {0};
WCHAR *lpSubMenuCmdList[8] = {0};
WCHAR *lpSubMenuPathList[8] = {0};

volatile DWORD dwChildrenPid;

static DWORD MyGetProcessId(HANDLE hProcess)
{
    typedef DWORD (WINAPI *pfnGPI)(HANDLE);
    typedef ULONG (WINAPI *pfnNTQIP)(HANDLE, ULONG, PVOID, ULONG, PULONG);

    static int first = 1;
    static pfnGPI pfnGetProcessId;
    static pfnNTQIP ZwQueryInformationProcess;
    if (first){
        first = 0;
        pfnGetProcessId = (pfnGPI)GetProcAddress(GetModuleHandleW(L"KERNEL32.DLL"), "GetProcessId");
        if (!pfnGetProcessId){
            ZwQueryInformationProcess = (pfnNTQIP)GetProcAddress(GetModuleHandleW(L"NTDLL.DLL"), "ZwQueryInformationProcess");
        }

    }
    if (pfnGetProcessId){
        return pfnGetProcessId(hProcess);
    }
    if (ZwQueryInformationProcess){
        struct {
            PVOID Reserved1;
            PVOID PebBaseAddress;
            PVOID Reserved2[2];
            ULONG UniqueProcessId;
            PVOID Reserved3;
        } pbi;
        ZwQueryInformationProcess(hProcess, 0, &pbi, sizeof(pbi), 0);
        return pbi.UniqueProcessId;
    }
    return 0;
}


static BOOL MyEndTask(DWORD pid)
{
    WCHAR szCmd[1024] = {0};
    wsprintf(szCmd, L"taskkill /f /pid %d", pid);
    return _wsystem(szCmd) == 0;
}

BOOL ShowTrayIcon(LPCTSTR lpszSubMenu, DWORD dwMessage=NIM_ADD)
{
    NOTIFYICONDATA nid;
    ZeroMemory(&nid, sizeof(NOTIFYICONDATA));
    nid.cbSize = (DWORD)sizeof(NOTIFYICONDATA);
    nid.hWnd   = hWnd;
    nid.uID       = NID_UID;
    nid.uFlags = NIF_ICON|NIF_MESSAGE;
    nid.dwInfoFlags=NIIF_INFO;
    nid.uCallbackMessage = WM_TASKBARNOTIFY;
    nid.hIcon = LoadIcon(hInst, (LPCTSTR)IDI_SMALL);
    nid.uTimeoutAndVersion = 3 * 1000 | NOTIFYICON_VERSION;
    lstrcpy(nid.szInfoTitle, szTitle);
    if (lpszSubMenu){
        nid.uFlags |= NIF_INFO|NIF_TIP;
        if (lstrlen(lpszSubMenu) > 0){
            lstrcpy(nid.szTip, lpszSubMenu);
            lstrcpy(nid.szInfo, lpszSubMenu);
        } else {
            lstrcpy(nid.szInfo, szBalloon);
            lstrcpy(nid.szTip, szTooltip);
        }
    }
    Shell_NotifyIcon(dwMessage, &nid);
    return TRUE;
}

BOOL DeleteTrayIcon()
{
    NOTIFYICONDATA nid;
    nid.cbSize = (DWORD)sizeof(NOTIFYICONDATA);
    nid.hWnd   = hWnd;
    nid.uID       = NID_UID;
    Shell_NotifyIcon(NIM_DELETE, &nid);
    return TRUE;
}

BOOL ShowPopupMenu()
{
    POINT pt;
    HMENU hSubMenu = NULL;
    BOOL isZHCN = GetSystemDefaultLCID() == 2052;
    LPCTSTR lpCurrentSubMenu = L"";
    if (lpSubMenuTitleList[1] != NULL){
        hSubMenu = CreatePopupMenu();
        for (int i = 0; lpSubMenuTitleList[i]; i++){
            UINT uFlags = wcscmp(lpSubMenuTitleList[i], lpCurrentSubMenu) == 0 ? MF_STRING | MF_CHECKED : MF_STRING;
            LPCTSTR lpText = wcslen(lpSubMenuTitleList[i]) ? lpSubMenuTitleList[i] : ( isZHCN ? L"默认" : L"<None>");
            AppendMenu(hSubMenu, uFlags, WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE+i, lpText);
        }
    }

    HMENU hMenu = CreatePopupMenu();
    AppendMenu(hMenu, MF_STRING, WM_TASKBARNOTIFY_MENUITEM_SHOW, ( isZHCN ? L"显示" : L"Show") );
    AppendMenu(hMenu, MF_STRING, WM_TASKBARNOTIFY_MENUITEM_HIDE, ( isZHCN ? L"隐藏" : L"Hide") );
    if (hSubMenu != NULL)
    {
        AppendMenu(hMenu, MF_STRING | MF_POPUP, (UINT_PTR)hSubMenu, ( isZHCN ? L"常用命令" : L"SubMenu") );
    }
    AppendMenu(hMenu, MF_STRING, WM_TASKBARNOTIFY_MENUITEM_RELOAD, ( isZHCN ? L"重新运行" : L"Reload") );
    AppendMenu(hMenu, MF_STRING, WM_TASKBARNOTIFY_MENUITEM_EXIT,   ( isZHCN ? L"退出" : L"Exit") );
    GetCursorPos(&pt);
    TrackPopupMenu(hMenu, TPM_LEFTALIGN, pt.x, pt.y, 0, hWnd, NULL);
    PostMessage(hWnd, WM_NULL, 0, 0);
    if (hSubMenu != NULL)
        DestroyMenu(hSubMenu);
    DestroyMenu(hMenu);
    return TRUE;
}

BOOL ParseSubMenuTitleList()
{
    WCHAR * tmpSubMenuString = _wcsdup(szSubMenuTitle);
    ExpandEnvironmentStrings(tmpSubMenuString, szSubMenuTitle, sizeof(szSubMenuTitle)/sizeof(szSubMenuTitle[0]));
    free(tmpSubMenuString);
    WCHAR *sep = L"\n";
    WCHAR *pos = wcstok(szSubMenuTitle, sep);
    INT i = 0;
    lpSubMenuTitleList[i++] = L"";
    while (pos && i < sizeof(lpSubMenuTitleList)/sizeof(lpSubMenuTitleList[0])){
        lpSubMenuTitleList[i++] = pos;
        pos = wcstok(NULL, sep);
    }
    lpSubMenuTitleList[i] = 0;

    return TRUE;
}

BOOL ParseSubMenuCmdList()
{
    WCHAR * tmpSubMenuString = _wcsdup(szSubMenuCmd);
    ExpandEnvironmentStrings(tmpSubMenuString, szSubMenuCmd, sizeof(szSubMenuCmd)/sizeof(szSubMenuCmd[0]));
    free(tmpSubMenuString);
    WCHAR *sep = L"\n";
    WCHAR *pos = wcstok(szSubMenuCmd, sep);
    INT i = 0;
    lpSubMenuCmdList[i++] = L"";
    while (pos && i < sizeof(lpSubMenuCmdList)/sizeof(lpSubMenuCmdList[0])){
        lpSubMenuCmdList[i++] = pos;
        pos = wcstok(NULL, sep);
    }
    lpSubMenuCmdList[i] = 0;

    return TRUE;
}

BOOL ParseSubMenuPathList()
{
    WCHAR * tmpSubMenuString = _wcsdup(szSubMenuPath);
    ExpandEnvironmentStrings(tmpSubMenuString, szSubMenuPath, sizeof(szSubMenuPath)/sizeof(szSubMenuPath[0]));
    free(tmpSubMenuString);
    WCHAR *sep = L"\n";
    WCHAR *pos = wcstok(szSubMenuPath, sep);
    INT i = 0;
    lpSubMenuPathList[i++] = L"";
    while (pos && i < sizeof(lpSubMenuPathList)/sizeof(lpSubMenuPathList[0])){
        lpSubMenuPathList[i++] = pos;
        pos = wcstok(NULL, sep);
    }
    lpSubMenuPathList[i] = 0;

    return TRUE;
}

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPED|WS_SYSMENU, NULL, NULL, CW_USEDEFAULT, CW_USEDEFAULT, NULL, NULL, hInstance, NULL);

   if (!hWnd){
      return FALSE;
   }

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}


BOOL SetEenvironment()
{
    WCHAR *sep = L"\n";
    WCHAR *pos = NULL;
    WCHAR *token = wcstok(szEnvironment, sep);
    while(token != NULL){
        if (pos = wcschr(token, L'=')){
            *pos = 0;
            SetEnvironmentVariableW(token, pos+1);
            //wprintf(L"[%s] = [%s]\n", token, pos+1);
        }
        token = wcstok(NULL, sep);
    }
    GetEnvironmentVariableW(L"ENV_VISIBLE", szVisible, sizeof(szVisible)/sizeof(szVisible[0])-1);
    GetEnvironmentVariableW(L"ENV_TITLE", szTitle, sizeof(szTitle)/sizeof(szTitle[0])-1);
    GetEnvironmentVariableW(L"ENV_TOOLTIP", szTooltip, sizeof(szTooltip)/sizeof(szTooltip[0])-1);
    GetEnvironmentVariableW(L"ENV_BALLOON", szBalloon, sizeof(szBalloon)/sizeof(szBalloon[0])-1);

    ParseSubMenuTitleList();
    ParseSubMenuCmdList();
    ParseSubMenuPathList();

    GetModuleFileName(NULL, szPath, sizeof(szPath)/sizeof(szPath[0])-1);
    *wcsrchr(szPath, L'\\') = 0;
    SetEnvironmentVariableW(L"ENV_BOOT_PWD", szPath);
    
    return TRUE;
}

BOOL WINAPI ConsoleHandler(DWORD CEvent)
{
    switch(CEvent){
        case CTRL_LOGOFF_EVENT:
        case CTRL_SHUTDOWN_EVENT:
        case CTRL_CLOSE_EVENT:
            SendMessage(hWnd, WM_CLOSE, NULL, NULL);
            break;
    }
    return TRUE;
}

BOOL CreateConsole()
{
    AllocConsole();
    _wfreopen(L"CONIN$",  L"r+t", stdin);
    _wfreopen(L"CONOUT$", L"w+t", stdout);

    hConsole = GetConsoleWindow();

    if (szVisible[0] == L'0'){
        ShowWindow(hConsole, SW_HIDE);
    } else {
        SetForegroundWindow(hConsole);
    }

    if (SetConsoleCtrlHandler((PHANDLER_ROUTINE)ConsoleHandler,TRUE)==FALSE){
        printf("Unable to install handler!\n");
        return FALSE;
    }

    CONSOLE_SCREEN_BUFFER_INFO csbi;
    if (GetConsoleScreenBufferInfo(GetStdHandle(STD_ERROR_HANDLE), &csbi)){
        COORD size = csbi.dwSize;
        if (size.Y < 2048){
            size.Y = 2048;
            if (!SetConsoleScreenBufferSize(GetStdHandle(STD_ERROR_HANDLE), size)){
                printf("Unable to set console screen buffer size!\n");
            }
        }
    }
    return TRUE;
}

BOOL ExecCmdline(WCHAR *path, WCHAR *cmd)
{
    if(NULL == cmd){
        return FALSE;
    }
    
    if(NULL == path){
        SetCurrentDirectory(path);
        lstrcpy(szPathLast, path);
    }

    SetWindowText(hConsole, szTitle);
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = TRUE;
    BOOL bRet = CreateProcess(NULL, cmd, NULL, NULL, FALSE, NULL, NULL, NULL, &si, &pi);
    if(bRet) {
        dwChildrenPid = MyGetProcessId(pi.hProcess);
    } else {
        wprintf(L"ExecCmdline \"%s\" failed!\n", cmd);
        MessageBox(NULL, cmd, L"Error: Cannot execute!", MB_OK);
        ExitProcess(0);
    }
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    
    lstrcpy(szCommandLast, cmd);
    return TRUE;
}

BOOL ReloadCmdline(WCHAR *path, WCHAR *cmd)
{
    ShowWindow(hConsole, SW_SHOW);
    SetForegroundWindow(hConsole);
    wprintf(L"\n\n");
    MyEndTask(dwChildrenPid);
    wprintf(L"\n\n");
    Sleep(200);
    ExecCmdline(path, cmd);
    return TRUE;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    static const UINT WM_TASKBARCREATED = ::RegisterWindowMessage(L"TaskbarCreated");
    int nID;
    switch (message) {
        case WM_TASKBARNOTIFY:
            if (lParam == WM_LBUTTONUP) {
                ShowWindow(hConsole, !IsWindowVisible(hConsole));
                SetForegroundWindow(hConsole);
            } else if (lParam == WM_RBUTTONUP) {
                SetForegroundWindow(hWnd);
                ShowPopupMenu();
            }
            break;
        case WM_COMMAND:
            nID = LOWORD(wParam);
            if (nID == WM_TASKBARNOTIFY_MENUITEM_SHOW) {
                ShowWindow(hConsole, SW_SHOW);
                SetForegroundWindow(hConsole);
            } else if (nID == WM_TASKBARNOTIFY_MENUITEM_HIDE) {
                ShowWindow(hConsole, SW_HIDE);
            }
            if (nID == WM_TASKBARNOTIFY_MENUITEM_RELOAD) {
                ReloadCmdline(szPathLast, szCommandLast);
            } else if (nID == WM_TASKBARNOTIFY_MENUITEM_ABOUT) {
                MessageBoxW(hWnd, szTooltip, szWindowClass, 0);
            } else if (nID == WM_TASKBARNOTIFY_MENUITEM_EXIT) {
                DeleteTrayIcon();
                PostMessage(hConsole, WM_CLOSE, 0, 0);
            } else if (WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE <= nID && nID <= WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE+sizeof(lpSubMenuTitleList)/sizeof(lpSubMenuTitleList[0])) {
                WCHAR *szSubMenu = lpSubMenuTitleList[nID-WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE];
                WCHAR *szSubCmd = lpSubMenuCmdList[nID-WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE];
                WCHAR *szSubPath = lpSubMenuPathList[nID-WM_TASKBARNOTIFY_MENUITEM_SUBMENULIST_BASE];
                ReloadCmdline(szSubPath, szSubCmd);
                ShowTrayIcon(szSubMenu, NIM_MODIFY);
            }
            break;
        case WM_CLOSE:
            DeleteTrayIcon();
            PostQuitMessage(0);
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
        default:
            if (message == WM_TASKBARCREATED) {
                ShowTrayIcon(NULL, NIM_ADD);
                break;
            }
            return DefWindowProc(hWnd, message, wParam, lParam);
   }
   return 0;
}

ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEX wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style            = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = (WNDPROC)WndProc;
    wcex.cbClsExtra        = 0;
    wcex.cbWndExtra        = 0;
    wcex.hInstance        = hInstance;
    wcex.hIcon            = LoadIcon(hInstance, (LPCTSTR)IDI_TASKBAR);
    wcex.hCursor        = LoadCursor(NULL, IDC_ARROW);
    wcex.hbrBackground    = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName    = (LPCTSTR)NULL;
    wcex.lpszClassName    = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, (LPCTSTR)IDI_SMALL);

    return RegisterClassEx(&wcex);
}

int APIENTRY wWinMain(HINSTANCE hInstance, HINSTANCE, LPTSTR lpCmdLine, int nCmdShow)
{
    MSG msg;
    hInst = hInstance;
    SetEenvironment();
    
    MyRegisterClass(hInstance);
    if (!InitInstance (hInstance, SW_HIDE)) {
        return FALSE;
    }
    CreateConsole();
    
    ExecCmdline(szPath, szCommand);
    ShowTrayIcon(szBalloon);
    
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return 0;
}

