program InjectDll;

uses
  Forms,
  Unit1 in 'Unit1.pas' {Form3},
  MemInfo in 'MemInfo.pas',
  unitUseage in 'unitUseage.pas',
  uProcInfo in 'uProcInfo.pas',
  EnumStuff in 'EnumStuff.pas',
  ProcessInfo in 'ProcessInfo.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TForm3, Form3);
  Application.Run;
end.
