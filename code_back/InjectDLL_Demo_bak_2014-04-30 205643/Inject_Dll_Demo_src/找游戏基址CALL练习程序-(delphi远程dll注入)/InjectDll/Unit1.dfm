object Form3: TForm3
  Left = 534
  Top = 418
  BorderStyle = bsDialog
  Caption = 'DLL'#27880#20837#20363#31243
  ClientHeight = 80
  ClientWidth = 493
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  Position = poDesktopCenter
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 8
    Top = 11
    Width = 60
    Height = 13
    Caption = #30446#26631#36827#31243#65306
  end
  object Button1: TButton
    Left = 9
    Top = 43
    Width = 120
    Height = 25
    Caption = #27880#20837'DLL'#27979#35797
    TabOrder = 0
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 312
    Top = 43
    Width = 169
    Height = 25
    Caption = #21462#28040#27880#20837
    TabOrder = 1
    OnClick = Button2Click
  end
  object ComboBox1: TComboBox
    Left = 72
    Top = 8
    Width = 409
    Height = 21
    ItemHeight = 13
    TabOrder = 2
  end
  object Button3: TButton
    Left = 144
    Top = 43
    Width = 153
    Height = 25
    Caption = #27880#20837'DLL'#21040#36827#31243#20013
    TabOrder = 3
    OnClick = Button3Click
  end
end
