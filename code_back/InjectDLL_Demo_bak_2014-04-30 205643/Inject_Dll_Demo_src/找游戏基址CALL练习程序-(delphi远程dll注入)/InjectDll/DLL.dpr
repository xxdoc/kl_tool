library DLL;

{ Important note about DLL memory management: ShareMem must be the
  first unit in your library's USES clause AND your project's (select
  Project-View Source) USES clause if your DLL exports any procedures or
  functions that pass strings as parameters or function results. This
  applies to all strings passed to and from your DLL--even those that
  are nested in records and classes. ShareMem is the interface unit to
  the BORLNDMM.DLL shared memory manager, which must be deployed along
  with your DLL. To avoid using BORLNDMM.DLL, pass string information
  using PChar or ShortString parameters. }

uses
  SysUtils,
  Dialogs,
  Classes,
  Windows,
  Forms, 
  Unit2 in 'Unit2.pas' {Form1};

{$R *.res}
var
  s: string;

type
  Thookdll = class(TThread) // 
  private
    { Private declarations }
    Form1: Tform1;
  protected
    procedure Execute; override;
  public
    constructor Create(CreateSuspended:Boolean); overload;
    destructor Destroy; overload;
  end;

constructor Thookdll.Create(CreateSuspended:Boolean);  
begin
  inherited Create(CreateSuspended);
end;

destructor Thookdll.Destroy;
begin
  Form1.Free;
  inherited Destroy;
end;

procedure Thookdll.Execute; //
begin
//  s := '这是一个Delphi的DLL注入例程';
//  ShowMessage(s);
  //Application.Initialize;

  Form1:= Tform1.Create(nil);
  Form1.ShowModal;
  Self.Terminate;
end;

var
  hookdlla: Thookdll;
 
begin
//  Form1:= Tform1.Create(nil);
//  Form1.ShowModal;
  hookdlla:=Thookdll.Create(true);
  hookdlla.FreeOnTerminate:= True;
  hookdlla.Resume;
end.

