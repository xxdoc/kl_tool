VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Begin VB.Form Form1 
   Caption         =   "Feng"
   ClientHeight    =   3525
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   4785
   LinkTopic       =   "Form1"
   ScaleHeight     =   3525
   ScaleWidth      =   4785
   StartUpPosition =   3  '窗口缺省
   Begin VB.CheckBox Checkc 
      Caption         =   "Check1"
      Height          =   255
      Left            =   720
      TabIndex        =   29
      Top             =   120
      Value           =   1  'Checked
      Width           =   255
   End
   Begin VB.CommandButton addc 
      Caption         =   "Add"
      Height          =   375
      Left            =   2520
      TabIndex        =   3
      Top             =   480
      Width           =   735
   End
   Begin VB.TextBox backt 
      Height          =   270
      Left            =   2520
      TabIndex        =   25
      Top             =   120
      Width           =   615
   End
   Begin VB.TextBox timedelay 
      Height          =   270
      Left            =   3840
      TabIndex        =   24
      Top             =   120
      Width           =   615
   End
   Begin VB.CommandButton QQ 
      Caption         =   "QQ"
      Height          =   255
      Left            =   4080
      TabIndex        =   4
      Top             =   2160
      Width           =   495
   End
   Begin VB.CheckBox alllog 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4320
      TabIndex        =   22
      Top             =   2760
      Width           =   255
   End
   Begin VB.CheckBox restart 
      Caption         =   "Check1"
      Height          =   255
      Left            =   3720
      TabIndex        =   21
      Top             =   2160
      Width           =   255
   End
   Begin VB.TextBox timef 
      Height          =   270
      Left            =   2280
      TabIndex        =   18
      Top             =   2160
      Width           =   375
   End
   Begin VB.Timer stoper 
      Enabled         =   0   'False
      Interval        =   500
      Left            =   1680
      Top             =   2760
   End
   Begin VB.CheckBox autorun 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4320
      TabIndex        =   15
      Top             =   3120
      Width           =   255
   End
   Begin VB.CheckBox Autos 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4320
      TabIndex        =   13
      Top             =   480
      Value           =   1  'Checked
      Width           =   255
   End
   Begin VB.Timer checks 
      Enabled         =   0   'False
      Interval        =   40000
      Left            =   2160
      Top             =   2760
   End
   Begin VB.CommandButton tryStop 
      Caption         =   "Stop"
      Height          =   375
      Left            =   3360
      TabIndex        =   1
      Top             =   1320
      Width           =   855
   End
   Begin VB.TextBox hp 
      Height          =   270
      Left            =   600
      TabIndex        =   12
      Top             =   2160
      Width           =   615
   End
   Begin VB.TextBox keytext 
      Height          =   270
      Left            =   2280
      Locked          =   -1  'True
      TabIndex        =   9
      Top             =   1680
      Width           =   615
   End
   Begin VB.Timer runer 
      Enabled         =   0   'False
      Interval        =   1200
      Left            =   1200
      Top             =   2760
   End
   Begin VB.CommandButton Go 
      Caption         =   "Go"
      Height          =   375
      Left            =   3360
      TabIndex        =   0
      Top             =   840
      Width           =   855
   End
   Begin VB.TextBox ytext 
      Height          =   270
      Left            =   1680
      TabIndex        =   8
      Top             =   465
      Width           =   495
   End
   Begin VB.TextBox xtext 
      Height          =   270
      Left            =   1080
      TabIndex        =   7
      Top             =   465
      Width           =   495
   End
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   600
      Top             =   2760
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.CommandButton Run 
      Caption         =   "运行"
      Height          =   375
      Left            =   3360
      TabIndex        =   2
      Top             =   2640
      Width           =   855
   End
   Begin VB.TextBox xypos 
      Height          =   615
      Left            =   120
      TabIndex        =   17
      Top             =   960
      Width           =   2895
   End
   Begin VB.Label statel 
      Height          =   255
      Left            =   120
      TabIndex        =   30
      Top             =   3240
      Width           =   3255
   End
   Begin VB.Label Label10 
      Caption         =   "cast:"
      Height          =   255
      Left            =   3240
      TabIndex        =   28
      Top             =   120
      Width           =   495
   End
   Begin VB.Label Label9 
      Caption         =   "back:"
      Height          =   255
      Left            =   1920
      TabIndex        =   27
      Top             =   120
      Width           =   495
   End
   Begin VB.Label Label8 
      Caption         =   "Check:"
      Height          =   255
      Left            =   120
      TabIndex        =   26
      Top             =   120
      Width           =   1215
   End
   Begin VB.Label Label7 
      Caption         =   " log"
      Height          =   255
      Left            =   4200
      TabIndex        =   23
      Top             =   2520
      Width           =   375
   End
   Begin VB.Label Label6 
      Caption         =   "重新登录:"
      Height          =   255
      Left            =   2880
      TabIndex        =   20
      Top             =   2160
      Width           =   855
   End
   Begin VB.Label Label5 
      Caption         =   "间隔(s):"
      Height          =   255
      Left            =   1560
      TabIndex        =   19
      Top             =   2160
      Width           =   855
   End
   Begin VB.Label Label4 
      Caption         =   "自动登录:"
      Height          =   375
      Left            =   3480
      TabIndex        =   16
      Top             =   3120
      Width           =   855
   End
   Begin VB.Label Label3 
      Caption         =   "Auto:"
      Height          =   255
      Left            =   3720
      TabIndex        =   14
      Top             =   480
      Width           =   735
   End
   Begin VB.Label Label2 
      Caption         =   "血量:"
      Height          =   375
      Left            =   120
      TabIndex        =   11
      Top             =   2160
      Width           =   615
   End
   Begin VB.Label Label1 
      Caption         =   "按键:"
      Height          =   255
      Left            =   1680
      TabIndex        =   10
      Top             =   1680
      Width           =   615
   End
   Begin VB.Label xycap 
      Caption         =   "挂机坐标:"
      Height          =   255
      Left            =   120
      TabIndex        =   6
      Top             =   480
      Width           =   975
   End
   Begin VB.Label Gamepath 
      Height          =   495
      Left            =   120
      TabIndex        =   5
      Top             =   2640
      Width           =   3135
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim dm As New dmsoft
Public user, pass As String
Dim isbusy, isdone As Boolean
Dim ylh As Long
Dim live, offline, xyn, keyn As Long
Dim xystr() As klpoint

Private Sub addc_Click()
    If isbusy = False Then
        isbusy = Ture
        addc.Caption = "Adding"
        ylh = dm.FindWindow("", "御龙在天")
        If Autos.Value = 0 Then
            answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
            PauseTime 2000
            ylh = dm.GetMousePointWindow()
        End If
        Filelog "添加字库： " & xtext.Text & ytext.Text & " 句柄： " & CStr(ylh)
        dm_ret = dm.BindWindow(ylh, "dx", "windows", "windows", 0)
        If dm_ret Then
            Filelog "绑定成功，句柄： " & CStr(ylh)
            info = dm.FetchWord(932, 13, 990, 25, "ffffff-000000", xtext.Text & ytext.Text)
            If Len(info) > 0 Then
               dm_ret = dm.AddDict(0, info)
               If dm_ret = 1 Then
                   Filelog "添加字库成功， " & info
                   MsgBox xtext.Text & ytext.Text & "-> 添加字库成功， " & info
                   xypos.Text = xypos.Text & "|" & xtext.Text & "," & ytext.Text
               Else
                   Filelog "添加字库失败！！ " & info
               End If
            End If
            dm_ret = dm.UnBindWindow()
            If dm_ret Then
                Filelog " 解除绑定 "
            Else
                Filelog "解除绑定错误，错误： " & CStr(dm.GetLastError)
                answer = MsgBox("解除绑定错误", vbYesNo)
            End If
        Else
            Filelog "绑定错误，错误： " & CStr(dm.GetLastError)
            answer = MsgBox("绑定错误", vbYesNo)
        End If
        ylh = 0
        addc.Caption = "Add"
        isbusy = False
   Else
   MsgBox "isbusy"
   End If
End Sub

Private Sub addc_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
If isbusy = False And Shift = 1 Then
dm_ret = dm.SaveDict(0, "dm_soft.txt")
If dm_ret = 1 Then MsgBox "保存当前字库到文件！"
End If
End Sub

Private Sub checks_Timer()
    ret = isback()
    If alllog.Value = 1 Then Filelog xtext.Text & "," & ytext.Text & " 检查 isback()  返回值：" & CStr(ret)
If Checkc.Value = 1 Then
    If ret = -1 Then offline = offline + 1
    If ret = 1 Then offline = 0
    If offline > 3 Then
       Call tryStop_Click
       dm_ret = dm.UnBindWindow()
       ylh = 0
       ylh = dm.FindWindow("SysListView32", "FolderView")
       dm_ret = dm.BindWindow(ylh, "normal", "normal", "normal", 0)
       dm_ret = dm.Capture(0, 0, 1440, 870, "screen.bmp")
       dm_ret = dm.UnBindWindow()
       If restart.Value = 1 Then
        Filelog "连续 三次异常 重新登陆 "
         autorun.Value = 1
'        Call EndAll
'        Call Run_Click
       Else
        Filelog "连续 三次异常 触发 关机 "
        Shell "autoshutdown.bat"
       End If
    End If
    If alllog.Value = 1 Then Call OtherError(1)
End If
 Call OtherError(0)
End Sub
Private Sub Form_Load()
base_path = dm.GetBasePath()
dm_ret = dm.SetShowErrorMsg(0)
dm_ret = dm.SetPath(base_path)
dm_ret = dm.SetDict(0, "dm_soft.txt")

Gamepath.Caption = GetSetting("Feng set", "Settings", "path", "F:\游戏\御龙在天\TCLS\Client.exe")
xtext.Text = GetSetting("Feng set", "Settings", "pox", 621)
ytext.Text = GetSetting("Feng set", "Settings", "poy", 462)
keytext.Text = GetSetting("Feng set", "Settings", "key", "0")
xypos.Text = GetSetting("Feng set", "Settings", "xypos", "621,462|612,449|622,449")
timef.Text = GetSetting("Feng set", "Settings", "timef", "40")
user = GetSetting("Feng set", "Settings", "user", "1192200720")
pass = GetSetting("Feng set", "Settings", "pass", "")
timedelay.Text = GetSetting("Feng set", "Settings", "timedelay", "1200")
backt.Text = GetSetting("Feng set", "Settings", "timeback", "5000")
isbusy = False
isdone = False
stoper.Enabled = False
Checkc.Value = 1
autorun.Value = 0: restart.Value = 0
If pass = "" Then autorun.Value = 2: restart.Value = 2
End Sub
Private Sub Form_Unload(Cancel As Integer)
SaveSetting "Feng set", "Settings", "path", Gamepath.Caption
SaveSetting "Feng set", "Settings", "pox", xtext.Text
SaveSetting "Feng set", "Settings", "poy", ytext.Text
SaveSetting "Feng set", "Settings", "key", keytext.Text
SaveSetting "Feng set", "Settings", "xypos", xypos.Text
SaveSetting "Feng set", "Settings", "timef", timef.Text
SaveSetting "Feng set", "Settings", "user", user
SaveSetting "Feng set", "Settings", "pass", pass
SaveSetting "Feng set", "Settings", "timedelay", timedelay.Text
SaveSetting "Feng set", "Settings", "timeback", backt.Text
dm_ret = dm.UnBindWindow()
End
End Sub
Private Sub Gamepath_DblClick()
Gamepath.Caption = ""
End Sub
Private Sub Go_Click()
offline = 0
live = 0

    If isbusy = False Then
        ylh = dm.FindWindow("", "御龙在天")
        If Autos.Value = 0 Then
            answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
            PauseTime 2000
            ylh = dm.GetMousePointWindow()
        End If
        Filelog "开始运行 ！句柄： " & CStr(ylh)
        Dim sp() As String
        sp = Split(xypos.Text, "|")
        xyn = UBound(sp)
        ReDim xystr(xyn)
        For strn = 0 To xyn
           xystr(strn).x = Val(Split(sp(strn), ",")(0))
           xystr(strn).y = Val(Split(sp(strn), ",")(1))
           If strn = xyn Then
             xystr(strn).nextx = Val(Split(sp(0), ",")(0))
             xystr(strn).nexty = Val(Split(sp(0), ",")(1))
           Else
             xystr(strn).nextx = Val(Split(sp(strn + 1), ",")(0))
             xystr(strn).nexty = Val(Split(sp(strn + 1), ",")(1))
           End If
        Next strn
        
        xtext.Text = xystr(0).x:: ytext.Text = xystr(0).y
        'dm_ret = dm.GetClientRect(ylh, X1, Y1, X2, Y2)
        dm_ret = dm.BindWindow(ylh, "dx", "windows", "windows", 0)
        If dm_ret Then
            addc.Enabled = False
            Go.Caption = "Doing"
            xypos.Enabled = False
            runer.Enabled = True
            runer.Interval = Val(timedelay.Text)
            checks.Interval = Val(timef.Text) * 1000
            checks.Enabled = True
            isbusy = True
            Filelog "绑定成功，句柄： " & CStr(ylh)
        Else
            Filelog "绑定错误，错误： " & CStr(dm.GetLastError)
            answer = MsgBox("绑定错误", vbYesNo)
        End If
    Else
       MsgBox "isbusy"
    End If
End Sub
Private Sub QQ_Click()
Form2.Show
Form1.Hide
End Sub
Private Sub Run_Click()
If isbusy = False Then
    isbusy = True
    isdone = False
    If FileExist(Gamepath.Caption) Then
        If FileIsR(Gamepath.Caption) = False Then Shell Gamepath.Caption
    Else
        CommonDialog1.Filename = ""
        CommonDialog1.Filter = "程序(*.exe)|*.exe"
        CommonDialog1.ShowOpen
        If CommonDialog1.Filename <> "" Then
            Gamepath.Caption = CommonDialog1.Filename
            If FileIsR(Gamepath.Caption) = False Then Shell Gamepath.Caption
        End If
    End If
    If autorun.Value = 1 Then
'        Dim logh As Long
'        PauseTime 10000
'        logh = dm.FindWindow("", "御龙在天登录程序")
'        Call login(logh, 500, 5000)
    End If
End If
isbusy = False
isdone = True
End Sub
Private Sub stoper_Timer()
Call tryStop_Click
End Sub
Private Sub tryStop_Click()
If isbusy Then
    runer.Enabled = False
    checks.Enabled = False
    tryStop.Caption = "Stoping"
    stoper.Enabled = True
        If isdone Then
            stoper.Enabled = False
            runer.Enabled = False
            checks.Enabled = False
            isbusy = False
            isdone = False
            ylh = 0
            live = 0
            Filelog " 停止运行！ "
            dm_ret = dm.UnBindWindow()
            If dm_ret Then
                Filelog " 解除绑定 "
            Else
                Filelog "解除绑定错误，错误： " & CStr(dm.GetLastError)
                answer = MsgBox("解除绑定错误", vbYesNo)
            End If
        xypos.Enabled = True
        addc.Enabled = True
        Go.Caption = "Go"
        tryStop.Caption = "Stop"
    End If
End If
End Sub
Private Sub runer_Timer()
    isdone = False
    ny = 50
    Scolor = "ff6000"
    For nx = 102 To 222 Step 5
        Color = dm.GetColor(nx, ny)
        If Color <> Scolor Then Color = dm.GetColor(nx + 4, ny)
        If Color <> Scolor Then Color = dm.GetColor(nx + 8, ny)
        If Color <> Scolor Then Exit For
    Next nx
    hp.Text = (nx - 102) / 126 * 100
    hp.Text = hp.Text + "%"
    If nx < 110 Then live = live + 1
    If live > 7 Then
        Filelog " 死亡！！！ "
        live = 0
        Call relive(ylh, 400, 8000)
        Call runback(ylh, 400, 12000)
    End If
    If live = 0 And nx > 120 Then Call runback(ylh, 400, Val(backt.Text))
    If isback() = 1 Then dm.KeyPressChar keytext.Text
    
    If keyn > Val(timef.Text) Then
          For strn = 0 To xyn
           If xtext.Text = xystr(strn).x Then
               xtext.Text = xystr(strn).nextx
               ytext.Text = xystr(strn).nexty
               Exit For
           End If
         Next strn
    keyn = 0
    End If
    keyn = keyn + 1
    statel.Caption = "keyn:" & keyn & "  live:" & live & "  offline:" & offline
    isdone = True
End Sub
Private Sub relive(hwnd As Long, delay1 As Long, delay2 As Long)
    runer.Enabled = False
    dm.MoveTo 385, 380
    PauseTime delay1
    dm.LeftClick
    PauseTime delay1
    dm.MoveTo 390, 348
    PauseTime delay1
    dm.LeftClick
    PauseTime delay2
    dm.KeyPressChar "t"
    PauseTime delay1
    live = 0
    runer.Enabled = True
End Sub
Private Sub runback(hwnd As Long, delay1 As Long, delay2 As Long)
    ret = isback()
    If ret = 1 Then Exit Sub
    runer.Enabled = False
    If ret = -1 Then
        Filelog "不在王城，企图使用 回城卷轴 按键9 "
        dm.KeyPressChar "9"
        PauseTime 10000
    End If
    dm.KeyPressChar "m"
    PauseTime delay1
    dm.MoveTo 693, 106
    PauseTime delay1
    dm.LeftClick
    PauseTime delay1
    dm.SendString hwnd, xtext.Text
    PauseTime delay1
    dm.MoveTo 747, 106
    PauseTime delay1
    dm.LeftClick
    PauseTime delay1
    dm.SendString hwnd, ytext.Text
    PauseTime delay1
    dm.MoveTo 787, 95
    PauseTime delay1
    dm.LeftClick
    PauseTime delay1
    dm.KeyPressChar "m"
    PauseTime delay2
    runer.Enabled = True
End Sub
Private Sub OtherError(count As Long)
dm_ret = dm.FindStr(664, 310, 676, 323, "cha", "ebbf88-222222|eb9b4b-222222|eb9642-222222", 1#, intX, intY) '军需
If intX >= 0 Or count > 0 Then
    dm.MoveTo 505, 435
    PauseTime 300
    dm.LeftClick
    dm.MoveTo 575, 435
    PauseTime 300
    dm.LeftClick
    dm.MoveTo 561, 450
    PauseTime 300
    dm.LeftClick
End If
End Sub
Private Function isback() As Long
    isback = 0
    dm_ret = dm.FindStr(901, 13, 924, 26, "wang", "ffffff-000000", 1#, intX, intY) '王城
    If intX >= 0 And intY >= 0 Then
        dm_ret = dm.FindStr(932, 13, 990, 25, xtext.Text & ytext.Text, "ffffff-000000", 1#, intX, intY)
        If intX >= 0 And intY >= 0 Then isback = 1
    Else
        isback = -1
    End If
End Function

Private Sub login(hwnd As Long, delay1 As Long, delay2 As Long)
  dm_ret = dm.SetWindowState(hwnd, 1)
  colors = "fff4a6"
  For timei = 1 To 40
  PauseTime delay1
  color1 = logindm.GetColor(196, 476)
  color2 = logindm.GetColor(208, 482)
  color3 = logindm.GetColor(232, 485)
  If colors = color1 And colors = color2 And colors = color3 >= 0 Then Exit For
  Next timei
  PauseTime delay1
  logindm.MoveTo 570, 420
  logindm.LeftClick
  For timei = 1 To 15
  PauseTime delay1 / 3
  logindm.KeyPressChar "back"
  Next timei
  logindm.SendString hwnd, user
  PauseTime delay1 * 2
  logindm.MoveTo 570, 450
  logindm.LeftClick
  logindm.SendString hwnd, pass
  PauseTime delay1 * 2
  logindm.KeyPressChar "enter"


    runer.Enabled = False
End Sub
Private Sub EndAll()

End Sub

Private Sub xypos_DblClick()
xypos.Text = "621,462|612,449|622,449"
End Sub
