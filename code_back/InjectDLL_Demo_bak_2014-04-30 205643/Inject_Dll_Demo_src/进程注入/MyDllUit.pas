unit MyDllUit;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls;

type
  TForm1 = class(TForm)
    Button1: TButton;
    Edit1: TEdit;
    Memo1: TMemo;
    procedure Button1Click(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure FormDestroy(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;
  function HookProc(nCode:Integer;WParam: WPARAM;LParam:LPARAM):LRESULT;stdcall;
  function HookOn(lpHwnd:HWND;lpType:Longint):Longint;stdcall;export;
  function HookOff:Boolean;stdcall;export;


implementation

{$R *.dfm}

var
  hHk: HHOOK=0;
  hMOUSEHk: HHOOK=0;
  mhwnd:HWND=0;
  bShow:Boolean=False;
  myKey:Byte=VK_F7;
  kbArray:TKeyboardState;
  hThread: Cardinal;
  hmod: Pointer; //Hinstance
  hProcessId: Cardinal;

  // KeyHookStruct:^THardwareHookStruct;
  mMode:Integer;

function HookProc(nCode:Integer;WParam: WPARAM;LParam:LPARAM):LRESULT;stdcall;
begin
  Result :=0;

  if nCode<0 then
    Result := CallNextHookEx(hHk,nCode,WParam,LParam)
  else
  begin
    GetKeyboardState(kbArray);

//    if (bShow=False) And (kbArray[myKey]=1) then
    if bShow = False Then
    begin
      bShow:=True;
      Form1:=TForm1.Create(Application);
      ShowCursor(True);
    end;
    // Form1.Caption :=’我的DLL中的窗体！’;
    // LockWindowUpdate(mhwnd);
    /// SetParent(Form1.Handle,mhwnd);
    // MoveWindow(Form1.Handle,1,1,2,2,True);
    // UpdateWindow(Form1.Handle);
    // UpdateWindow(mhwnd);
    SetWindowPos(Form1.Handle, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE);
    // UpdateWindow(mhwnd);
    // mMode:=GetMapMode(GetDC(mhwnd));
    // SetMapMode(GetDC(Form1.Handle),mMode);
    // UpdateWindow(Form1.Handle);
    // SetWindowLong(Form1.Handle,GWL_STYLE,GetWindowLong(mhwnd, GWL_STYLE));


    Result :=1;
    SuspendThread(hThread);
    Form1.Show;
    Form1.Memo1.Lines.Add(IntToStr(WParam));
    ShowCursor(True);
    ResumeThread(hThread);
    //kbArray[myKey] := 0;
    //SetKeyboardState(kbArray);
    CallNextHookEx(hHk,nCode,WParam,LParam);
  end;
end;

function HookOn(lpHwnd:HWND;lpType:Longint): Longint;stdcall; export;
begin
  mhwnd:=lpHwnd;
  if hHk<>0 then UnHookWindowsHookEx(hHk);
    hThread :=GetWindowThreadProcessId(mhwnd,hmod);
  //其实，这个地方可以判断一下你的键盘是什么，再决定要不要执行下面的
  hHk :=SetWindowsHookEx(lpType,@HookProc,hInstance,hThread); // WH_KEYBOARD
  Result :=hHk
end;

function HookOff:Boolean;stdcall; export;
begin
  if hHk<>0 then
  begin
    UnHookWindowsHookEx(hHk);
    hHk :=0;
    Result :=true;
  end
  else
    Result :=false;
end;

procedure TForm1.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  bShow:=False;
  Action := caFree;
end;

procedure TForm1.FormDestroy(Sender: TObject);
begin
  bShow:=False;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  Form1.close;
end;

procedure TForm1.FormActivate(Sender: TObject);
begin
  ShowCursor(true);
end;

end.

