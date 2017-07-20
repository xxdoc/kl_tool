object Form1: TForm1
  Left = 217
  Top = 128
  Width = 226
  Height = 283
  Caption = 'Form1'
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  OnActivate = FormActivate
  OnDestroy = FormDestroy
  PixelsPerInch = 96
  TextHeight = 13
  object Button1: TButton
    Left = 8
    Top = 56
    Width = 75
    Height = 25
    Caption = 'Button1'
    TabOrder = 0
    OnClick = Button1Click
  end
  object Edit1: TEdit
    Left = 8
    Top = 8
    Width = 185
    Height = 21
    TabOrder = 1
    Text = 'Edit1'
  end
  object Memo1: TMemo
    Left = 8
    Top = 104
    Width = 185
    Height = 129
    Lines.Strings = (
      'Memo1')
    TabOrder = 2
  end
end
