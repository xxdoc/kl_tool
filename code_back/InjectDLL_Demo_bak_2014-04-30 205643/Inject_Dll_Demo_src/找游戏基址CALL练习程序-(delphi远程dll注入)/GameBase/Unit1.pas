unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls;

type
  TForm1 = class(TForm)
    Button1: TButton;
    Button3: TButton;
    Memo1: TMemo;
    procedure Button1Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;
type
  //游戏测试对象
  GameObj = class
    Blood: integer; //血值
    Magic: integer; //魔力值
    BloodMax: integer; //血值上限
    MagicMax: integer; //魔力值上限
    x: single; //X坐标 float;
    h: single; //h坐标
    y: single; //Y坐标
    grade: integer; //等级
  end;

  //仓库结构
  TStor = record
    item:array[0..3] of integer;   //仓库物品数组
  end;

  //角色对象
  Roleobj = class
  public
    N1: integer;
    N2: integer;
    roleA: GameObj;  //对象中的对象 测试找 N 级基址
    Stor:TStor;      //对象中的结构 测试找 N 级基址 （这里包括了数组）
  public
    constructor Create;
    destructor Destroy;
    function addvalues(val:Integer):byte; stdcall;   //用于测试找的CALL   这里以C/C++ 参数传值方式调用
  end;
var
  Form1: TForm1;

  Role: Roleobj;   //用于找基址的角色对象

implementation

{$R *.dfm}

constructor Roleobj.Create;
var i:integer;
begin
  inherited Create;
  for i:= 0 to 3 do
  begin
    Stor.item[i]:= i+$100;
  end;
  roleA:= GameObj.Create;
end;

destructor Roleobj.Destroy;
begin
  roleA.Free;
  inherited Destroy;
end;

function Roleobj.addvalues(val:Integer):byte; stdcall;
begin
    roleA.Blood := roleA.Blood - val;
    roleA.Magic := roleA.Magic - val;
    roleA.BloodMax := roleA.BloodMax + val;
    roleA.MagicMax := roleA.MagicMax + val;
    MessageBox(0,PChar('执行角色动作 roleA.Blood = '+IntToStr(roleA.Blood)), 'OK了', 0);
    Result:= 100;
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  if Role = nil then
  begin
    role := Roleobj.Create; //动态分配一块内存给role
    role.roleA.Blood := $272;
    role.roleA.Magic := $271;
    role.roleA.BloodMax := $300;
    role.roleA.MagicMax := $300;
    role.roleA.x := 100.1;
    role.roleA.h := 10.2;
    role.roleA.y := 200.3;
    Memo1.Lines.Add('role.roleA.Blood = $272');
    Memo1.Lines.Add('role.roleA.Magic = $271');
    Memo1.Lines.Add('role.roleA.BloodMax = $300');
    Memo1.Lines.Add('role.roleA.MagicMax = $300;');
  end;

end;

procedure TForm1.Button3Click(Sender: TObject);
begin
  if role <> nil then
  begin
    Role.addvalues($4);  //调用CALl
    Memo1.Lines.Add('-----------------------------------');
    Memo1.Lines.Add('role.roleA.Magic = ' + IntToStr(role.roleA.Magic));
  end;
end;

procedure TForm1.FormDestroy(Sender: TObject);
begin
  if  Role<> nil then
    role.Free;
end;

end.

 