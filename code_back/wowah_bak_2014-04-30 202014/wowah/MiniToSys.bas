Attribute VB_Name = "MiniToSys"
Public Const DefaultIconIndex = 1 '图标缺省索引
Public Const WM_LBUTTONDOWN = &H201 '按鼠标左键
Public Const WM_RBUTTONDOWN = &H204 '按鼠标右键
Public Const NIM_ADD = 0 '添加图标
Public Const NIM_MODIFY = 1 '修改图标
Public Const NIM_DELETE = 2 '删除图标
Public Const NIF_MESSAGE = 1 'message 有效
Public Const NIF_ICON = 2 '图标操作（添加、修改、删除）有效
Public Const NIF_TIP = 4 'ToolTip(提示）有效

Declare Function Shell_NotifyIcon Lib "shell32.dll" Alias "Shell_NotifyIconA" (ByVal dwMessage As Long, lpData As NOTIFYICONDATA) As Long
Declare Function IsIconic Lib "user32" (ByVal hWnd As Long) As Long
Declare Function SetWindowPos Lib "user32" (ByVal hWnd As Long, ByVal hWndInsertAfter As Long, ByVal x As Long, ByVal y As Long, ByVal cx As Long, ByVal cy As Long, ByVal wFlags As Long) As Long

Private Declare Function DeleteUrlCacheEntry Lib "wininet" Alias "DeleteUrlCacheEntryA" (ByVal lpszUrlName As String) As Long
Private Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long
Private Declare Function GetTickCount Lib "kernel32" () As Long
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (Destination As Any, Source As Any, ByVal Length As Long)
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Private Declare Function MultiByteToWideChar Lib "kernel32" (ByVal CodePage As Long, ByVal dwFlags As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long) As Long

Public Declare Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" (ByVal hWnd As Long, ByVal lpOperation As String, ByVal lpFile As String, ByVal lpParameters As String, ByVal lpDirectory As String, ByVal nShowCmd As Long) As Long

Public Const SW_SHOWNORMAL As Long = 1
Public Const SW_HIDE As Long = 0

Private Const CP_UTF8 = 65001
Private Const MAX_FILE_BUFF = 1024 * 8

Public Type NOTIFYICONDATA
    cbSize As Long
    hWnd As Long
    uID As Long
    uFlags As Long
    uCallbackMessage As Long
    hIcon As Long
    szTip As String * 64
End Type

'other function
Public Function Filelog(islog As Long, strlog As String, log_file As String) As Boolean
    On Error GoTo Notlog
    If islog = 1 Then
        If log_file = "" Then log_file = "common_kl_log.log"
        
        Dim lngFileID As Long
        lngFileID = FreeFile(0)
        Open App.Path & "\" & log_file For Append As lngFileID
        Print #lngFileID, Format$(Now, "c") & ":  " & strlog
        Close lngFileID
        Filelog = True
    End If
    Exit Function
Notlog:
End Function

Public Function FileExists(file As String) As Boolean
    On Error Resume Next
    If (GetAttr(file) And vbDirectory) = False Then FileExists = True
    If Err Then FileExists = False: Err.Clear
End Function

Public Function FolderExists(Folder As String) As Boolean
    On Error Resume Next
    If GetAttr(Folder) And vbDirectory Then FolderExists = True
    If Err Then FolderExists = False: Err.Clear
End Function

Public Function DownloadFile(url As String, LocalFilename As String, ReWrite As Long) As Boolean
    If url = "" Or LocalFilename = "" Then DownloadFile = False:: Exit Function
    If Filelong(LocalFilename) > 10 And ReWrite = 0 Then DownloadFile = True:: Exit Function

    Dim lngRetVal As Long
    lngRetVal = URLDownloadToFile(0, url, LocalFilename, 0, 0)
    If lngRetVal = 0 Then
        DownloadFile = True
        DeleteUrlCacheEntry url
    End If
End Function

Public Function FileIsR(FileName As String) As Boolean
    On Error GoTo NotExist
    Dim objWMIService, colProcessList, objProcess
    Dim file As String
    If InStrRev(FileName, "\", -1, vbTextCompare) Then file = Mid$(FileName, InStrRev(FileName, "\", -1, vbTextCompare) + 1)
    If Len(file) < 4 Or Filelong(FileName) < 10 Then GoTo NotExist
    Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
    Set colProcessList = objWMIService.ExecQuery _
        ("Select * from Win32_Process Where Name='" & file & "'")
    For Each objProcess In colProcessList
        FileIsR = True
        Exit For
    Next
    Exit Function
NotExist:
    FileIsR = False
End Function

Public Function Filelong(FileName As String) As Long
    Filelong = -1
    On Error GoTo NotExist
    Filelong = FileLen(FileName)
    Exit Function
NotExist:
End Function

Private Function ByteToString(ByVal iSize As Long) As String
    '//Byte ->Byte KB or MB
    Dim c       As Double
    If iSize < 1024 Then
        ByteToString = CStr(iSize) & " Byte"
    Else
        c = iSize / 1024& / 1024&
        If c > 1 Then
            ByteToString = CStr(Format$(c, "###,###,##0.0")) & " MB"
        Else
            c = iSize / 1024&
            ByteToString = CStr(Format$(c, "###,###,##0.0")) & " KB"
        End If
    End If
    If iSize <= 0 Then
        ByteToString = "NaN Byte"
    End If
End Function
Public Function SecondToString(ByVal secn As Long) As String
    '//Second ->00::00::00
    If secn > 3600 Then
        SecondToString = Format$(secn \ 3600, "00")
        secn = secn Mod 3600
    Else
        SecondToString = "00"
    End If
    If secn > 60 Then
        SecondToString = SecondToString & ":" & Format$(secn \ 60, "00")
        secn = secn Mod 60
    Else
        SecondToString = SecondToString & ":" & "00"
    End If
    SecondToString = SecondToString & ":" & Format$(secn, "00")
End Function
Public Function Bydelay(Millisecond As Long)
    Dim Start, Endtime As Single
    Start = Timer
    Endtime = Start + Millisecond / 1000
    Do While Timer < Endtime
        DoEvents
        Sleep 10
    Loop
End Function

'函数定义
'添加图标至通知栏
Public Function Icon_Add(iHwnd As Long, sTips As String, hIcon As Long, IconID As Long) As Long
    '参数说明：iHwnd：窗口句柄，sTips：当鼠标移到通知栏图标上时显示的提示内容
    'hIcon：图标句柄，IconID：图标Id号
    Dim IconVa As NOTIFYICONDATA
    With IconVa
        .hWnd = iHwnd
        .szTip = sTips + Chr$(0)
        .hIcon = hIcon
        .uID = IconID
        .uCallbackMessage = WM_LBUTTONDOWN
        .cbSize = Len(IconVa)
        .uFlags = NIF_MESSAGE Or NIF_ICON Or NIF_TIP
        Icon_Add = Shell_NotifyIcon(NIM_ADD, IconVa)
    End With
End Function
'删除通知栏图标(参数说明同Icon_Add)
Function Icon_Del(iHwnd As Long, lIndex As Long) As Long
    Dim IconVa As NOTIFYICONDATA
    Dim l As Long
    With IconVa
        .hWnd = iHwnd
        .uID = lIndex
        .cbSize = Len(IconVa)
    End With
    Icon_Del = Shell_NotifyIcon(NIM_DELETE, IconVa)
End Function
'修改通知栏图标(参数说明同Icon_Add)
Public Function Icon_Modify(iHwnd As Long, sTips As String, hIcon As Long, IconID As Long) As Long
    Dim IconVa As NOTIFYICONDATA
    With IconVa
        .hWnd = iHwnd
        .szTip = sTips + Chr$(0)
        .hIcon = hIcon
        .uID = IconID
        .uCallbackMessage = WM_LBUTTONDOWN
        .cbSize = Len(IconVa)
        .uFlags = NIF_MESSAGE Or NIF_ICON Or NIF_TIP
        Icon_Modify = Shell_NotifyIcon(NIM_MODIFY, IconVa)
    End With
End Function
