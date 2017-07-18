unit Unit1;

interface
uses
  uProcInfo,
  //ProcessInfo,
  StrUtils,
  ShellAPI,
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, EnumStuff, Grids, ValEdit, ComCtrls, ExtCtrls;

type
  TForm3 = class(TForm)
    注入进程: TButton;
    取消注入: TButton;
    edit_proc_path: TEdit;
    label_proc_path: TLabel;
    label_dll_path: TLabel;
    edit_dll_path: TEdit;
    OpenDialog1: TOpenDialog;
    edit_proc_pid: TEdit;
    edit_dll_pid: TEdit;
    刷新: TButton;
    ListView1: TListView;
    结束进程: TButton;
    Timer1: TTimer;
    edit_dll_addr: TEdit;
    edit_timer_set: TEdit;
    procedure 注入进程Click(Sender: TObject);
    procedure 取消注入Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure label_dll_pathClick(Sender: TObject);
    procedure ListView1Click(Sender: TObject);
    procedure 刷新Click(Sender: TObject);
    procedure 结束进程Click(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure ListView1ColumnClick(Sender: TObject; Column: TListColumn);
    procedure edit_dll_pidChange(Sender: TObject);
    procedure edit_timer_setChange(Sender: TObject);
    procedure label_proc_pathClick(Sender: TObject);
  private
    { Private declarations }
    //InjectID : Cardinal;

  public
    { Public declarations }


  end;

function CustomSortProc(Item1, Item2: TListItem; ParamSort: Integer): Integer;stdcall;



var
  Form3: TForm3;
  m_bSort: Boolean = TRUE;

implementation

{$R *.dfm}
function LeftStrEx(in_str: string; in_len: Integer) : String;
begin
  if (in_len > 0) then
    begin
      Result := LeftStr(in_str, in_len);
    end
  else
    begin
      Result := LeftStr(in_str, Length(in_str) + in_len);
  end;
end;

function StrIndexOfList(in_list: TStringList; in_str: String) : Integer;
begin
  try
    begin
      Result := in_list.IndexOf(in_str);
    end;
  except
      Result := -2;
  end;
end;

function EnableDebugPriv : Boolean;
var
  hToken : THANDLE;
  tp : TTokenPrivileges;
  rl : Cardinal;
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

function InjectDll(const DllFullPath : string;
  const dwRemoteProcessId : Cardinal): Integer;
var
  hRemoteProcess, hRemoteThread,dwHandle: THANDLE;
  pszLibFileRemote : Pointer;
  pszLibAFilename: PwideChar;
  pfnStartAddr : TFNThreadStartRoutine;
  memSize, WriteSize, lpThreadId : Cardinal;
begin
  result := 0;
  // 调整权限，使程序可以访问其他进程的内存空间
  if EnableDebugPriv then
  begin
    //打开远程线程 PROCESS_ALL_ACCESS 参数表示打开所有的权限
    hRemoteProcess := OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwRemoteProcessId );

    try

      // 为注入的dll文件路径分配内存大小,由于为WideChar,故要乘2
      GetMem(pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 之所以要转换成 WideChar, 是因为当DLL位于有中文字符的路径下时不会出错
      StringToWideChar(DllFullPath, pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 计算 pszLibAFilename 的长度，注意，是以字节为单元的长度
      memSize := (1 + lstrlenW(pszLibAFilename)) * sizeof(WCHAR);

      //使用VirtualAllocEx函数在远程进程的内存地址空间分配DLL文件名空间
      pszLibFileRemote := VirtualAllocEx( hRemoteProcess, nil, memSize,
        MEM_COMMIT, PAGE_READWRITE);

      if Assigned(pszLibFileRemote) then
      begin

        //使用WriteProcessMemory函数将DLL的路径名写入到远程进程的内存空间
        if WriteProcessMemory(hRemoteProcess, pszLibFileRemote,
          pszLibAFilename, memSize, WriteSize) and (WriteSize = memSize) then
        begin

          lpThreadId := 0;
          dwHandle := 0;
          // 计算LoadLibraryW的入口地址
          pfnStartAddr := GetProcAddress(LoadLibrary('Kernel32.dll'), 'LoadLibraryW');
          // 启动远程线程LoadLbraryW,通过远程线程调用创建新的线程
          hRemoteThread := CreateRemoteThread(hRemoteProcess, nil, 0,
            pfnStartAddr, pszLibFileRemote, 0, lpThreadId);

          // 等待LoadLibraryW 加载完毕
          WaitForSingleObject( hRemoteThread, INFINITE );
          // 获得LoadLibraryW的返回值,存在dwHandle变量中
          GetExitCodeThread(hRemoteThread, dwHandle);

          // 如果执行成功返回　True;
          if (dwHandle <> 0) then
            result := dwHandle;

          // 释放目标进程中申请的空间
          VirtualFreeEx(hRemoteProcess, pszLibFileRemote, Length(DllFullPath)+1, MEM_DECOMMIT);
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

function UnInjectDll(const DllFullPath : string;
  const dwRemoteProcessId : Cardinal) : Integer;
// 进程注入和取消注入其实都差不多，只是运行的函数不同而已
var
  hRemoteProcess, hRemoteThread : THANDLE;
  pszLibFileRemote : pchar;
  pszLibAFilename: PwideChar;
  pfnStartAddr : TFNThreadStartRoutine;
  memSize, WriteSize, lpThreadId, dwHandle, dwFreeHandle : Cardinal;
begin
  result := 0;

  // 调整权限，使程序可以访问其他进程的内存空间
  if EnableDebugPriv then
  begin
    //打开远程线程 PROCESS_ALL_ACCESS 参数表示打开所有的权限
    hRemoteProcess := OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwRemoteProcessId );

    try

      // 为注入的dll文件路径分配内存大小,由于为WideChar,故要乘2
      GetMem(pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 之所以要转换成 WideChar, 是因为当DLL位于有中文字符的路径下时不会出错
      StringToWideChar(DllFullPath, pszLibAFilename, Length(DllFullPath) * 2 + 1);
      // 计算 pszLibAFilename 的长度，注意，是以字节为单元的长度
      memSize := (1 + lstrlenW(pszLibAFilename)) * sizeof(WCHAR);

      //使用VirtualAllocEx函数在远程进程的内存地址空间分配DLL文件名空间
      pszLibFileRemote := VirtualAllocEx( hRemoteProcess, nil, memSize,
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
          WaitForSingleObject(hRemoteThread,INFINITE);
          // 获得GetModuleHandle的返回值,存在dwHandle变量中
          GetExitCodeThread(hRemoteThread, dwHandle);

          // 计算FreeLibrary的入口地址
          pfnStartAddr := GetProcAddress(LoadLibrary('Kernel32.dll'), 'FreeLibrary');
          // 使目标进程调用FreeLibrary，卸载DLL
          hRemoteThread := CreateRemoteThread(hRemoteProcess, nil, 0,
            pfnStartAddr, Pointer(dwHandle), 0, lpThreadId);
          // 等待FreeLibrary卸载完毕
          WaitForSingleObject( hRemoteThread, INFINITE );

          // 获得FreeLibrary 的返回值,存在dwFreeHandle变量中
          GetExitCodeThread(hRemoteThread, dwFreeHandle);

          // 如果执行成功返回　True;
          if (dwFreeHandle <> 0) then
            result := dwHandle;

          // 释放目标进程中申请的空间
          VirtualFreeEx(hRemoteProcess, pszLibFileRemote, Length(DllFullPath)+1, MEM_DECOMMIT);
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

procedure GetProcInfo(list_view: TListView; dll_pid: TEdit);
var
  List:TStringList;
  I,J,Index:Integer;
  AItem:TListItem;
  AInfo:TProcInfo;
begin
  J := 0;
  List := TStringList.Create;
  try
  RunningProcessesList(List);

  if (dll_pid.Text <> '') and (StrIndexOfList(List, dll_pid.Text)=-1) then
    begin
      dll_pid.Text := '';
    end;

  list_view.Items.BeginUpdate;
  //list_view.Items.Clear();

  For I := 0 To list_view.Items.Count-1 do
  begin
     AItem := list_view.Items.Item[J];
     Index := StrIndexOfList(List, AItem.SubItems.Strings[0]);
     If Index<>-1 then  //已存在,修改数据
     begin
       AInfo := TProcInfo(List.Objects[Index]);
       AItem.Caption := AInfo.ProcName;
       If AItem.SubItems.Count>3 then
       begin
         AItem.SubItems.Strings[0] := IntToStr(AInfo.PID);
         AItem.SubItems.Strings[1] := FormatDateTime('hh:nn:ss',AInfo.CPUTime);
         AItem.SubItems.Strings[2] := IntToStr(AInfo.MemSize)+' K';
         AItem.SubItems.Strings[3] := AInfo.FullName;
       end;
       AInfo.Free;
       List.Delete(Index); //删除
       INC(J);
     end else    //进程已不存在,删除
         begin
           list_view.Items.Delete(J);
           DEC(J);
         end;
  end;

  For I := 0 To List.Count-1 do
    begin
      AInfo := TProcInfo(List.Objects[I]);
      AItem := list_view.Items.Add;
      AItem.Caption := AInfo.FileName;
      AItem.SubItems.Add(IntToStr(AInfo.PID));
      AItem.SubItems.Add(FormatDateTime('hh:nn:ss',AInfo.CPUTime));
      AItem.SubItems.Add(IntToStr(AInfo.MemSize)+' K');
      AItem.SubItems.Add(AInfo.FullName);
      AInfo.Free;
    end;

  finally
    list_view.Items.EndUpdate;
    List.Free;
  end;

end;

procedure TForm3.注入进程Click(Sender: TObject);
var
  Process : TProcessList;
  i,dll_addr : integer;
begin
  //来自于 EnumStuff单元的一个函数，可以得到当前进程列表．
  Process := GetProcessList;
  for i := Low(Process) to High(Process) do
    if ((Integer(Process[i].pid) = StrToInt(edit_proc_pid.Text)) and (edit_dll_pid.Text = '') and  FileExists(edit_dll_path.Text)) then
      begin
        dll_addr := InjectDll(edit_dll_path.Text, Process[i].pid);
        if ( dll_addr > 0) then
          begin
            edit_dll_pid.Text := IntToStr(Process[i].pid);
            edit_dll_addr.Text := Format('$%x',[dll_addr])
          end
        else
          begin
            ShowMessage('注入  失败！！');
          end;
      end;
end;

procedure TForm3.取消注入Click(Sender: TObject);
begin
  if ((edit_dll_pid.Text <> '' ) and (StrToInt(edit_dll_pid.Text) > 0 ) and FileExists(edit_dll_path.Text)) then
    begin
      if (UnInjectDll(edit_dll_path.Text, StrToInt(edit_dll_pid.Text)) > 0) then
        begin
          edit_dll_pid.Text := '';
        end
      else
        begin
          ShowMessage('取消注入失败！！');
        end;
    end;
end;

procedure TForm3.刷新Click(Sender: TObject);
begin
  GetProcInfo(ListView1, edit_dll_pid);
end;


procedure TForm3.结束进程Click(Sender: TObject);
Const
  WarnMsg= '警告: 终止进程会导致不希望发生的结果，'+#10#13
          +'包括数据丢失和系统不稳定。在被终止前，'+#10#13
          +'进程将没有机会保存其状态和数据。确实'+#10#13
          +'想终止该进程吗?';
var
  Process : TProcessList;
  i : integer;
begin
  //来自于 EnumStuff单元的一个函数，可以得到当前进程列表．
  Process := GetProcessList;
  for i := Low(Process) to High(Process) do
    if (edit_proc_pid.Text <> '') and (Integer(Process[i].pid) = StrToInt(edit_proc_pid.Text)) and
       (Application.MessageBox(WarnMsg,'任务管理器警告',MB_YESNO+MB_ICONWARNING)=IDYES ) then
      begin
          KillProcess(Process[i].pid);
          edit_proc_path.Text := '';
          edit_proc_pid.Text := '';
      end;
end;


procedure TForm3.edit_dll_pidChange(Sender: TObject);
begin
  if (edit_dll_pid.Text = '') then edit_dll_addr.Text := '';
end;

procedure TForm3.edit_timer_setChange(Sender: TObject);
begin
  if (edit_timer_set.Text <> '') and (StrToInt(edit_timer_set.Text) > 0) then Timer1.Interval := StrToInt(edit_timer_set.Text)*100;
end;

procedure TForm3.FormCreate(Sender: TObject);

begin
  GetProcInfo(ListView1, edit_dll_pid);
  edit_dll_path.Text := ExtractFilePath(ParamStr(0))+'DLL.dll';
  edit_dll_pid.Text := '';
  m_bSort := TRUE;
end;

procedure TForm3.label_dll_pathClick(Sender: TObject);
begin
  if OpenDialog1.InitialDir = '' then  OpenDialog1.InitialDir := ExtractFilePath(ParamStr(0));
  OpenDialog1.Filter := 'dll文件(*.dll)|*.dll|所有文件(*.*)|*.*';
  if opendialog1.execute and FileExists(OpenDialog1.FileName) then edit_dll_path.Text := OpenDialog1.FileName;
end;


procedure TForm3.label_proc_pathClick(Sender: TObject);
begin
  if (FileExists(edit_proc_path.Text)) then
    ShellExecute(0,'open','Explorer.exe',PChar('/n,/select,'+edit_proc_path.Text ),0,SW_NORMAL);

end;

procedure TForm3.ListView1Click(Sender: TObject);
begin
  if ListView1.Selected <> nil then
    begin
      edit_proc_path.Text := ListView1.Selected.SubItems.Strings[3];
      edit_proc_pid.Text := ListView1.Selected.SubItems.Strings[0];
    end;
end;

procedure TForm3.Timer1Timer(Sender: TObject);
begin
    GetProcInfo(ListView1, edit_dll_pid);
end;



procedure TForm3.ListView1ColumnClick(Sender: TObject;
    Column: TListColumn);
begin
  ListView1.CustomSort(@CustomSortProc, Column.Index);
  m_bSort := not m_bSort;
end;

function CustomSortProc(Item1, Item2: TListItem;
    ParamSort: Integer): Integer; stdcall;
var
    stxt1, stxt2: string;
    txt1, txt2: Integer;
begin
  if (ParamSort <> 0) then
    begin
      try
        txt1 := 0; txt2 := 0;
        stxt1 := (Item1.SubItems.Strings[ParamSort - 1]);
        stxt2 := (Item2.SubItems.Strings[ParamSort - 1]);
        if (ParamSort = 3) then stxt1 := LeftStrEx(stxt1, -2);
        if (ParamSort = 3) then stxt2 := LeftStrEx(stxt2, -2);
        if (ParamSort = 1) or (ParamSort = 3) then txt1 := StrToInt(stxt1);
        if (ParamSort = 1) or (ParamSort = 3) then txt2 := StrToInt(stxt2);
        if m_bSort then
          begin
            Result := CompareText(stxt1, stxt2);
            if (ParamSort = 1) or (ParamSort = 3) then Result := txt1 - txt2;
          end
        else
          begin
            Result := -CompareText(stxt1, stxt2);
            if (ParamSort = 1) or (ParamSort = 3) then Result := -(txt1 - txt2);
        end;
      except
         Result := -1;
      end;
    end
  else
    begin
      if m_bSort then
        begin
          Result := CompareText(Item1.Caption, Item2.Caption);
        end
      else
        begin
        Result := -CompareText(Item1.Caption, Item2.Caption);
      end;
  end;
end;


{function GetProcIndexByStrPID(list:TStringList;str_pid: String): Integer;
var
  i_loop: integer;
begin
  Result := -1;
  For i_loop := 0 To list.Count-1 do
    begin
      if (i_loop = StrToInt(str_pid) ) then
        begin
          Result := i_loop;
        end;
    end;
end;}


end.
