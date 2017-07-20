unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, EnumStuff;

type
  TForm3 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Label1: TLabel;
    ComboBox1: TComboBox;
    Button3: TButton;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
  private
    { Private declarations }
    InjectID: Cardinal;
  public
    { Public declarations }
  end;

var
  Form3: TForm3;

implementation

{$R *.dfm}

function EnableDebugPriv: Boolean;
var
  hToken: THANDLE;
  tp: TTokenPrivileges;
  rl: Cardinal;
begin
  result := false;

  //打开进程令牌环
  OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES or TOKEN_QUERY, hToken);

  //获得进程本地唯一ID
  if LookupPrivilegeValue(nil, 'SeDebugPrivilege', tp.Privileges[0].Luid) then
  begin
    tp.PrivilegeCount := 1;
    tp.Privileges[0].Attributes := SE_PRIVILEGE_ENABLED;
    //调整权限
    result := AdjustTokenPrivileges(hToken, False, tp, sizeof(tp), nil, rl);
  end;
end;

function InjectDll(const DllFullPath: string;
  const dwRemoteProcessId: Cardinal): boolean;
var
  hRemoteProcess, hRemoteThread: THANDLE;
  pszLibFileRemote: Pointer;
  pszLibAFilename: PwideChar;
  pfnStartAddr: TFNThreadStartRoutine;
  memSize, WriteSize, lpThreadId: Cardinal;
begin
  result := FALSE;
  // 调整权限，使程序可以访问其他进程的内存空间
  if EnableDebugPriv then
  begin
    //打开远程线程 PROCESS_ALL_ACCESS 参数表示打开所有的权限
    hRemoteProcess := OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwRemoteProcessId);

    try

      // 为注入的dll文件路径分配内存大小,由于为WideChar,故要乘2
      GetMem(pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 之所以要转换成 WideChar, 是因为当DLL位于有中文字符的路径下时不会出错
      StringToWideChar(DllFullPath, pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 计算 pszLibAFilename 的长度，注意，是以字节为单元的长度
      memSize := (1 + lstrlenW(pszLibAFilename)) * sizeof(WCHAR);

      //使用VirtualAllocEx函数在远程进程的内存地址空间分配DLL文件名空间
      pszLibFileRemote := VirtualAllocEx(hRemoteProcess, nil, memSize,
        MEM_COMMIT, PAGE_READWRITE);

      if Assigned(pszLibFileRemote) then
      begin

        //使用WriteProcessMemory函数将DLL的路径名写入到远程进程的内存空间
        if WriteProcessMemory(hRemoteProcess, pszLibFileRemote,
          pszLibAFilename, memSize, WriteSize) and (WriteSize = memSize) then
        begin

          lpThreadId := 0;
          // 计算LoadLibraryW的入口地址
          pfnStartAddr := GetProcAddress(LoadLibrary('Kernel32.dll'), 'LoadLibraryW');
          // 启动远程线程LoadLbraryW,通过远程线程调用创建新的线程
          hRemoteThread := CreateRemoteThread(hRemoteProcess, nil, 0,
            pfnStartAddr, pszLibFileRemote, 0, lpThreadId);

          // 如果执行成功返回　True;
          if (hRemoteThread <> 0) then
            result := TRUE;

          // 释放句柄
          CloseHandle(hRemoteThread);
        end;
      end;
    finally
      // 释放句柄
      CloseHandle(hRemoteProcess);
    end;
  end;
end;

function UnInjectDll(const DllFullPath: string;
  const dwRemoteProcessId: Cardinal): Boolean;
// 进程注入和取消注入其实都差不多，只是运行的函数不同而已
var
  hRemoteProcess, hRemoteThread: THANDLE;
  pszLibFileRemote: pchar;
  pszLibAFilename: PwideChar;
  pfnStartAddr: TFNThreadStartRoutine;
  memSize, WriteSize, lpThreadId, dwHandle: Cardinal;
begin
  result := FALSE;

  // 调整权限，使程序可以访问其他进程的内存空间
  if EnableDebugPriv then
  begin
    //打开远程线程 PROCESS_ALL_ACCESS 参数表示打开所有的权限
    hRemoteProcess := OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwRemoteProcessId);

    try

      // 为注入的dll文件路径分配内存大小,由于为WideChar,故要乘2
      GetMem(pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 之所以要转换成 WideChar, 是因为当DLL位于有中文字符的路径下时不会出错
      StringToWideChar(DllFullPath, pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 计算 pszLibAFilename 的长度，注意，是以字节为单元的长度
      memSize := (1 + lstrlenW(pszLibAFilename)) * sizeof(WCHAR);

      //使用VirtualAllocEx函数在远程进程的内存地址空间分配DLL文件名空间
      pszLibFileRemote := VirtualAllocEx(hRemoteProcess, nil, memSize,
        MEM_COMMIT, PAGE_READWRITE);

      if Assigned(pszLibFileRemote) then
      begin

        //使用WriteProcessMemory函数将DLL的路径名写入到远程进程的内存空间
        if WriteProcessMemory(hRemoteProcess, pszLibFileRemote,
          pszLibAFilename, memSize, WriteSize) and (WriteSize = memSize) then
        begin

          // 计算GetModuleHandleW的入口地址
          pfnStartAddr := GetProcAddress(LoadLibrary('Kernel32.dll'), 'GetModuleHandleW');
          //使目标进程调用GetModuleHandleW，获得DLL在目标进程中的句柄
          hRemoteThread := CreateRemoteThread(hRemoteProcess, nil, 0,
            pfnStartAddr, pszLibFileRemote, 0, lpThreadId);
          // 等待GetModuleHandle运行完毕
          WaitForSingleObject(hRemoteThread, INFINITE);
          // 获得GetModuleHandle的返回值,存在dwHandle变量中
          GetExitCodeThread(hRemoteThread, dwHandle);

          // 计算FreeLibrary的入口地址
          pfnStartAddr := GetProcAddress(LoadLibrary('Kernel32.dll'), 'FreeLibrary');
          // 使目标进程调用FreeLibrary，卸载DLL
          hRemoteThread := CreateRemoteThread(hRemoteProcess, nil, 0,
            pfnStartAddr, Pointer(dwHandle), 0, lpThreadId);
          // 等待FreeLibrary卸载完毕
          WaitForSingleObject(hRemoteThread, INFINITE);

          // 如果执行成功返回　True;
          if hRemoteProcess <> 0 then
            result := TRUE;

          // 释放目标进程中申请的空间
          VirtualFreeEx(hRemoteProcess, pszLibFileRemote, Length(DllFullPath) + 1, MEM_DECOMMIT);
          // 释放句柄
          CloseHandle(hRemoteThread);
        end;
      end;
    finally
      // 释放句柄
      CloseHandle(hRemoteProcess);
    end;
  end;
end;

procedure TForm3.Button1Click(Sender: TObject);
var
  Process : TProcessList;
  i : integer;
begin
  //来自于 EnumStuff单元的一个函数，可以得到当前进程列表．
  Process := GetProcessList;
  for I := Low(Process) to High(Process) do
  begin
    if LowerCase(Process[i].name) = LowerCase(ComboBox1.Text) then
    begin
      InjectDll(ExtractFilePath(ParamStr(0))+'DLL.dll', Process[i].pid);
      InjectID := Process[i].pid;
      exit;
    end;
  end;
end;

procedure TForm3.Button2Click(Sender: TObject);
begin
  UnInjectDll(ExtractFilePath(ParamStr(0)) + 'DLL.dll', InjectID);
end;

procedure TForm3.Button3Click(Sender: TObject);
var
  Process : TProcessList;
  i : integer;
begin
  //来自于 EnumStuff单元的一个函数，可以得到当前进程列表．
  Process := GetProcessList;
  for I := Low(Process) to High(Process) do
    if LowerCase(Process[i].name) = LowerCase(ComboBox1.Text) then
    begin
      InjectDll(ExtractFilePath(ParamStr(0))+'DLL.dll', Process[i].pid);
      InjectID := Process[i].pid;
      exit;
    end;
end;

procedure TForm3.FormCreate(Sender: TObject);
var
  Process : TProcessList;
  i : integer;
begin
  //来自于 EnumStuff单元的一个函数，可以得到当前进程列表．
  Process := GetProcessList;
  for I := Low(Process) to High(Process) do
    ComboBox1.Items.Add(Process[i].name);
  ComboBox1.ItemIndex:= 0;
end;

end.

