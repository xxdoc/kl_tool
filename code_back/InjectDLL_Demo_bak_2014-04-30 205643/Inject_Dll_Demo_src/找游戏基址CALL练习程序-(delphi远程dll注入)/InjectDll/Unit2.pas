unit Unit2;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls;

type
  TForm1 = class(TForm)
    Button1: TButton;
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}
procedure testCall(); stdcall;
begin
  asm
    pushad
    push 4
    mov ecx, $00453bd4
    mov eax,[ecx]
    push eax
    mov ebx,$00450508
    call ebx
    popad
  end;

end;
procedure TForm1.Button1Click(Sender: TObject);
begin
  testCall();
end;

end.
