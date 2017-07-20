object Form3: TForm3
  Left = 0
  Top = 0
  BorderStyle = bsDialog
  Caption = 'DLL'#27880#20837#20363#31243
  ClientHeight = 500
  ClientWidth = 469
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
  object label_proc_path: TLabel
    Left = 8
    Top = 443
    Width = 60
    Height = 13
    Caption = #30446#26631#36827#31243#65306
    OnClick = label_proc_pathClick
  end
  object label_dll_path: TLabel
    Left = 8
    Top = 416
    Width = 59
    Height = 13
    Caption = '  Dll  '#30446#24405#65306
    OnClick = label_dll_pathClick
  end
  object 注入进程: TButton
    Left = 114
    Top = 467
    Width = 64
    Height = 25
    Caption = #27880#20837#36827#31243
    TabOrder = 0
    OnClick = 注入进程Click
  end
  object 取消注入: TButton
    Left = 200
    Top = 467
    Width = 65
    Height = 25
    Caption = #21462#28040#27880#20837
    TabOrder = 1
    OnClick = 取消注入Click
  end
  object edit_proc_path: TEdit
    Left = 69
    Top = 440
    Width = 340
    Height = 21
    AutoSelect = False
    AutoSize = False
    ReadOnly = True
    TabOrder = 2
  end
  object edit_dll_path: TEdit
    Left = 70
    Top = 413
    Width = 275
    Height = 21
    AutoSelect = False
    AutoSize = False
    Color = clWhite
    ReadOnly = True
    TabOrder = 3
  end
  object edit_proc_pid: TEdit
    Left = 412
    Top = 440
    Width = 49
    Height = 21
    AutoSelect = False
    AutoSize = False
    ReadOnly = True
    TabOrder = 4
  end
  object edit_dll_pid: TEdit
    Left = 412
    Top = 413
    Width = 49
    Height = 21
    AutoSelect = False
    AutoSize = False
    Color = clWhite
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clRed
    Font.Height = -11
    Font.Name = 'Tahoma'
    Font.Style = []
    ParentFont = False
    ReadOnly = True
    TabOrder = 5
    OnChange = edit_dll_pidChange
  end
  object 刷新: TButton
    Left = 47
    Top = 467
    Width = 49
    Height = 25
    Caption = #21047#26032
    TabOrder = 6
    OnClick = 刷新Click
  end
  object ListView1: TListView
    Left = 8
    Top = 8
    Width = 453
    Height = 399
    Columns = <
      item
        Caption = #26144#20687#21517#31216
        Width = 80
      end
      item
        Caption = 'PID'
      end
      item
        Caption = 'CPU'#26102#38388
        Width = 60
      end
      item
        Caption = #20869#23384
        Width = 80
      end
      item
        AutoSize = True
        Caption = #25991#20214#36335#24452
      end>
    ReadOnly = True
    RowSelect = True
    ParentShowHint = False
    ShowHint = False
    TabOrder = 7
    ViewStyle = vsReport
    OnClick = ListView1Click
    OnColumnClick = ListView1ColumnClick
  end
  object 结束进程: TButton
    Left = 287
    Top = 467
    Width = 66
    Height = 25
    Caption = #32467#26463#36827#31243
    TabOrder = 8
    OnClick = 结束进程Click
  end
  object edit_dll_addr: TEdit
    Left = 344
    Top = 413
    Width = 65
    Height = 21
    Color = clWhite
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clBlue
    Font.Height = -11
    Font.Name = 'Tahoma'
    Font.Style = []
    ParentFont = False
    ReadOnly = True
    TabOrder = 9
  end
  object edit_timer_set: TEdit
    Left = 8
    Top = 473
    Width = 33
    Height = 21
    TabOrder = 10
    Text = '10'
    OnChange = edit_timer_setChange
  end
  object OpenDialog1: TOpenDialog
    Left = 416
    Top = 472
  end
  object Timer1: TTimer
    OnTimer = Timer1Timer
    Left = 376
    Top = 472
  end
end
