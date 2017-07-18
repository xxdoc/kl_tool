unit uProcInfo;

interface
uses StrUtils,Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, Menus, ExtCtrls, ComCtrls,DateUtils,PsAPI,Tlhelp32;
Type
  TProcessorTimeInfo = record
    IdleTime: int64;
    KernelTime: int64;
    UserTime: int64;
    DpcTime: int64;
    InterruptTime:int64;
    InterruptCount:cardinal;
  end;
  TThreadInfo = record
    ftCreationTime: TFileTime;
    dwUnknown1: DWORD;
    dwStartAddress: DWORD;
    dwOwningPID: DWORD;
    dwThreadID: DWORD;
    dwCurrentPriority: DWORD;
    dwBasePriority: DWORD;
    dwContextSwitches: DWORD;
    dwThreadState: DWORD;
    dwUnknown2: DWORD;
    dwUnknown3: DWORD;
    dwUnknown4: DWORD;
    dwUnknown5: DWORD;
    dwUnknown6: DWORD;
    dwUnknown7: DWORD;
  end;
  TProcessInfo = record
    dwOffset: DWORD;
    dwThreadCount: DWORD;
    dwUnknown1: array[0..5] of DWORD;
    ftCreationTime: TFileTime;
    ftUserTime: int64;
    ftKernelTime: int64;
  //      dwUnknown4: DWORD;
  //      dwUnknown5: DWORD;
    dwUnknown6: DWORD;
    pszProcessName: pwideChar;
    dwBasePriority: DWORD;
    dwProcessID: DWORD;
    dwParentProcessID: DWORD;
    dwHandleCount: DWORD;
    dwUnknown7: DWORD;
    dwUnknown8: DWORD;
    dwVirtualBytesPeak: DWORD;
    dwVirtualBytes: DWORD;
    dwPageFaults: DWORD;
    dwWorkingSetPeak: DWORD;
    dwWorkingSet: DWORD;
    dwUnknown9: DWORD;
    dwPagedPool: DWORD;
    dwUnknown10: DWORD;
    dwNonPagedPool: DWORD;
    dwPageFileBytesPeak: DWORD;
    dwPageFileBytes: DWORD;
    dwPrivateBytes: DWORD;
    dwUnknown11: DWORD;
    dwUnknown12: DWORD;
    dwUnknown13: DWORD;
    dwUnknown14: DWORD;
    ati: array[0..0] of TThreadInfo;
  end;
  TProcInfo=Class
  private
    FProcName:String;
    FPID:Integer;
    FMemSize:DWord;
    FCPUTime:TDateTime;
    FFullName:String;
  public
    property PID:Integer Read FPID Write FPID;
    property ProcName:String Read FProcName Write FProcName;
    property FileName:String Read FProcName Write FProcName;
    property FullName:String Read FFullName Write FFullName;
    property MemSize:DWord Read FMemSize Write FMemSize;
    property CPUTime:TDateTime Read FCPUTime Write FCPUTime;
  end;
  TWinInfo=class
    FIcon:HICON;
    FCaption:String;
    FClsName:String;
    FHandle:THandle;
  end;
  function NtQuerySystemInformation(si_class: cardinal; si: pointer; si_length: cardinal; ret_length:cardinal):cardinal; stdcall; external 'ntdll.dll';
  function RunningProcessesList(const List: TStrings): Boolean;
  function GetProcessNameFromWnd(Wnd: HWND): String;
  function GetProcessFullNameByPID(PID: DWORD; FullPath : Boolean): string;
  procedure GetAllWindow(List:TStrings);
  procedure KillProcess(hprocessID: HWND);
implementation

procedure KillProcess(hprocessID: HWND);
var
  processHandle:HWND;
begin
    if hprocessID <> 0 then
    begin
      { Get the process handle }
      processHandle := OpenProcess(PROCESS_TERMINATE or PROCESS_QUERY_INFORMATION,
        False, hprocessID);
      if processHandle <> 0 then
      begin
        { Terminate the process }
        TerminateProcess(processHandle, 0);
        CloseHandle(ProcessHandle);
      end;
    end;
end;



//Get MemSize by PID
function GetProcessMemorySizeByPID(l_nProcID:HWND; var _nMemSize: Cardinal): Boolean;
var
  l_nTmpHandle: HWND;
  l_pPMC: PPROCESS_MEMORY_COUNTERS;
  l_pPMCSize: Cardinal;
begin

  l_pPMCSize := SizeOf(PROCESS_MEMORY_COUNTERS);

  GetMem(l_pPMC, l_pPMCSize);
  l_pPMC^.cb := l_pPMCSize;
  l_nTmpHandle := OpenProcess(PROCESS_ALL_ACCESS, False, l_nProcID);

  if (GetProcessMemoryInfo(l_nTmpHandle, l_pPMC, l_pPMCSize)) then
    _nMemSize := l_pPMC^.WorkingSetSize
  else
    _nMemSize := 0;
  FreeMem(l_pPMC);
  Result := True;
end;

function RunningProcessesList(const List: TStrings): Boolean;
var
  AI:TProcInfo;
  buf:array[0..299999] of char;
  pi: ^TProcessInfo;
  //ti: ^TProcessorTimeInfo;
  aMemSize:DWord;
begin
  NtQuerySystemInformation(5, @buf, 300000, 0);
  pi:=@buf;
  repeat
    try
      AI := TProcInfo.Create;
      AI.FPID := pi^.dwProcessID;
      AI.FProcName :=WideCharToString(pi^.pszProcessName);
      AI.FCPUTime :=  ((pi^.ftUserTime+pi^.ftKernelTime) div 10000000)/86400;
      GetProcessMemorySizeByPID(AI.PID,aMemSize);
      AI.MemSize := Round(aMemSize /1024);
      if AI.ProcName='' then
        begin
          AI.ProcName := 'System Idle';
          AI.MemSize := 0;
        end;
      AI.FFullName := GetProcessFullNameByPID(AI.FPID, TRUE);
      if (AI.FProcName='winlogon.exe') and (AI.FFullName<>'') then AI.FFullName := RightStr(AI.FFullName,Length(AI.FFullName)-4);
      if AI.FFullName='' then  AI.FFullName := AI.FProcName;
      List.AddObject(IntToStr(AI.PID),AI);
    except
    end;
    pi:=pointer(cardinal(pi)+pi^.dwOffset);
  until pi^.dwOffset=0;
    //获得为0时的情况
    AI := TProcInfo.Create;
    AI.PID := pi^.dwProcessID;
    AI.ProcName :=WideCharToString(pi^.pszProcessName);
    AI.FCPUTime :=  ((pi^.ftUserTime+pi^.ftKernelTime) div 10000000)/86400;
    GetProcessMemorySizeByPID(AI.PID,aMemSize);
    AI.MemSize := Round(aMemSize /1024);
    if AI.ProcName='' then
      begin
        AI.ProcName := 'System Idle';
        AI.MemSize := 0;
      end;
    AI.FFullName := GetProcessFullNameByPID(AI.PID, TRUE);
    if (AI.FProcName='winlogon.exe') and (AI.FFullName<>'') then AI.FFullName := RightStr(AI.FFullName,Length(AI.FFullName)-4);
    if (AI.FFullName='') then  AI.FFullName := AI.FProcName;
    List.AddObject(IntToStr(AI.PID),AI);
    Result := true;
end;

function EnumWindowsProc(Handle: HWND; List: TStrings):boolean;stdcall;
var
  WinStyles : DWord;
  WinText:Array[0..100] of Char;
  WinClsName:Array[0..100] of Char;
  strTmp:string;
  //aIcon:HICON;
  AI:TWinInfo;
begin
  Result := true;
  WinStyles := GetWindowLong(Handle, GWL_STYLE);
  If ((WinStyles and WS_VISIBLE) > 0) then 
  begin
  GetClassName(Handle,WinClsName,100);
  GetWindowText(Handle,WinText,100);
  strTmp := WinText;
  If Trim(strTmp)<>'' then
  begin
    AI := TWinInfo.Create;
    AI.FIcon := GetClassLong(Handle,GCL_HICON);
    AI.FCaption := strTmp;
    AI.FClsName := WinClsName;
    AI.FHandle := Handle;
    List.AddObject(IntToStr(Handle),AI);
  end;
  end;
end;

procedure GetAllWindow(List:TStrings);
begin
  EnumWindows(@EnumWindowsProc,Integer(List));
end;

function GetProcessNameFromWnd(Wnd: HWND): string;
var
  List: TStringList;
  PID: DWORD;
  I: Integer;
begin

  Result := '';
  if IsWindow(Wnd) then
  begin
    PID := INVALID_HANDLE_VALUE;
    GetWindowThreadProcessId(Wnd, @PID);
    List := TStringList.Create;
    try
      if RunningProcessesList(List) then
      begin
        I := List.IndexOfObject(Pointer(PID));
        if I > -1 then
          Result := List[I];
      end;
    finally
      List.Free;
    end;
  end;
end;




{ TProcInfo }

function GetFileNameByPath(FFullName :String ): String;
begin
  Result := ExtractFileName(FFullName);
end;


function GetProcessFullNameByPID(PID: DWORD; FullPath : Boolean): string;
var
  Handle: THandle;
begin
  Result := '';
  Handle := OpenProcess(PROCESS_QUERY_INFORMATION or PROCESS_VM_READ, False, PID);
  if Handle <> 0 then
    try
      SetLength(Result, MAX_PATH);
      if FullPath then
        begin
          if GetModuleFileNameEx(Handle, 0, PChar(Result), MAX_PATH) > 0 then
            SetLength(Result, StrLen(PChar(Result)))
          else
            Result := '';
        end
      else
        begin
          if GetModuleBaseNameA(Handle, 0, PAnsiChar(AnsiString(Result)), MAX_PATH) > 0 then
            SetLength(Result, StrLen(PChar(Result)))
          else
            Result := '';
        end;
    finally
      CloseHandle(Handle);
    end;
end;


end.
