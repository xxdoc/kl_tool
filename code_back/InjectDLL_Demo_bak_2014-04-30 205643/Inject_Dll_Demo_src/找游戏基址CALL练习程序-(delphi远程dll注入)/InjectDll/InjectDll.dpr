program InjectDll;

uses
  Forms,
  Unit1 in 'Unit1.pas' {Form3},
  EnumStuff in 'EnumStuff.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TForm3, Form3);
  Application.Run;
end.
