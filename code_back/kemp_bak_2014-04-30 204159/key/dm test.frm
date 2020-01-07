VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Bg KeyPress"
   ClientHeight    =   3840
   ClientLeft      =   168
   ClientTop       =   552
   ClientWidth     =   4308
   Icon            =   "dm test.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   3840
   ScaleWidth      =   4308
   StartUpPosition =   3  '窗口缺省
   Begin VB.TextBox alldelayt 
      Height          =   270
      Left            =   3600
      TabIndex        =   44
      Top             =   600
      Width           =   615
   End
   Begin VB.TextBox playtext 
      Height          =   270
      Left            =   3240
      TabIndex        =   42
      Top             =   3000
      Width           =   492
   End
   Begin VB.TextBox ymt 
      Height          =   270
      Left            =   3240
      TabIndex        =   41
      Top             =   2520
      Width           =   495
   End
   Begin VB.TextBox xmt 
      Height          =   270
      Left            =   2640
      TabIndex        =   40
      Top             =   2520
      Width           =   495
   End
   Begin VB.TextBox htext 
      Height          =   270
      Left            =   2640
      TabIndex        =   39
      Top             =   2160
      Width           =   735
   End
   Begin VB.CommandButton movec 
      Caption         =   "move"
      Height          =   255
      Left            =   3480
      TabIndex        =   38
      Top             =   2160
      Width           =   615
   End
   Begin VB.TextBox mytext 
      Height          =   270
      Left            =   3480
      TabIndex        =   37
      Top             =   1800
      Width           =   615
   End
   Begin VB.TextBox mxtext 
      Height          =   270
      Left            =   2640
      TabIndex        =   36
      Top             =   1800
      Width           =   615
   End
   Begin VB.CheckBox mck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   3120
      TabIndex        =   35
      Top             =   1440
      Width           =   255
   End
   Begin VB.TextBox ntext 
      Enabled         =   0   'False
      Height          =   270
      Left            =   3600
      TabIndex        =   33
      Top             =   3480
      Width           =   615
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   7
      Left            =   2040
      TabIndex        =   32
      Top             =   3000
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   6
      Left            =   2040
      TabIndex        =   31
      Top             =   2640
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   5
      Left            =   2040
      TabIndex        =   30
      Top             =   2280
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   4
      Left            =   2040
      TabIndex        =   29
      Top             =   1920
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   3
      Left            =   2040
      TabIndex        =   28
      Top             =   1560
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   2
      Left            =   2040
      TabIndex        =   27
      Top             =   1200
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   1
      Left            =   2040
      TabIndex        =   26
      Top             =   840
      Width           =   255
   End
   Begin VB.CheckBox isc 
      Caption         =   "Check1"
      Height          =   255
      Index           =   0
      Left            =   2040
      TabIndex        =   25
      Top             =   480
      Width           =   255
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   7
      Left            =   1080
      TabIndex        =   24
      Top             =   3000
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   6
      Left            =   1080
      TabIndex        =   23
      Top             =   2640
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   5
      Left            =   1080
      TabIndex        =   22
      Top             =   2280
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   4
      Left            =   1080
      TabIndex        =   21
      Top             =   1920
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   3
      Left            =   1080
      TabIndex        =   20
      Top             =   1560
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   2
      Left            =   1080
      TabIndex        =   19
      Top             =   1200
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   1
      Left            =   1080
      TabIndex        =   18
      Top             =   840
      Width           =   735
   End
   Begin VB.TextBox delay 
      Height          =   270
      Index           =   0
      Left            =   1080
      TabIndex        =   17
      Top             =   480
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   7
      Left            =   120
      TabIndex        =   15
      Top             =   3000
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   6
      Left            =   120
      TabIndex        =   14
      Top             =   2640
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   5
      Left            =   120
      TabIndex        =   13
      Top             =   2280
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   4
      Left            =   120
      TabIndex        =   12
      Top             =   1920
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   3
      Left            =   120
      TabIndex        =   11
      Top             =   1560
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   2
      Left            =   120
      TabIndex        =   10
      Top             =   1200
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   1
      Left            =   120
      TabIndex        =   9
      Top             =   840
      Width           =   735
   End
   Begin VB.TextBox castk 
      Height          =   270
      Index           =   0
      Left            =   120
      TabIndex        =   7
      Top             =   480
      Width           =   735
   End
   Begin VB.CheckBox logck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   3960
      TabIndex        =   5
      Top             =   1440
      Width           =   255
   End
   Begin VB.ComboBox bindcb 
      Height          =   300
      Left            =   3000
      Style           =   2  'Dropdown List
      TabIndex        =   3
      Top             =   120
      Width           =   1095
   End
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Left            =   3840
      Top             =   2880
   End
   Begin VB.CommandButton stopc 
      Caption         =   "停止"
      Height          =   375
      Left            =   3600
      TabIndex        =   1
      Top             =   960
      Width           =   615
   End
   Begin VB.CommandButton runc 
      Caption         =   "运行"
      Height          =   375
      Left            =   2760
      TabIndex        =   0
      Top             =   960
      Width           =   615
   End
   Begin VB.Label Label1 
      Caption         =   "循环间隔(s):"
      Height          =   270
      Left            =   2400
      TabIndex        =   45
      Top             =   600
      Width           =   1452
   End
   Begin VB.Label Label5 
      Caption         =   "错误次数："
      Height          =   270
      Left            =   2400
      TabIndex        =   43
      Top             =   3000
      Width           =   972
   End
   Begin VB.Label Label4 
      Caption         =   "mouse:"
      Height          =   255
      Left            =   2520
      TabIndex        =   34
      Top             =   1440
      Width           =   495
   End
   Begin VB.Label Label3 
      Caption         =   "延时ms："
      Height          =   255
      Left            =   1080
      TabIndex        =   16
      Top             =   120
      Width           =   735
   End
   Begin VB.Label Label2 
      Caption         =   "绑定方式："
      Height          =   255
      Left            =   2040
      TabIndex        =   8
      Top             =   120
      Width           =   975
   End
   Begin VB.Label Label7 
      Caption         =   "log:"
      Height          =   255
      Left            =   3480
      TabIndex        =   6
      Top             =   1440
      Width           =   375
   End
   Begin VB.Label helpl 
      Caption         =   "按键："
      Height          =   255
      Left            =   120
      TabIndex        =   4
      Top             =   120
      Width           =   615
   End
   Begin VB.Label statel 
      Height          =   255
      Left            =   120
      TabIndex        =   2
      Top             =   3480
      Width           =   3375
   End
   Begin VB.Menu m_syso 
      Caption         =   "托盘"
      Visible         =   0   'False
      Begin VB.Menu m_sys 
         Caption         =   "关于(&O)"
         Index           =   0
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   1
      End
      Begin VB.Menu m_sys 
         Caption         =   "运行(&E)"
         Index           =   2
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   3
      End
      Begin VB.Menu m_sys 
         Caption         =   "停止(&R)"
         Index           =   4
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   5
      End
      Begin VB.Menu m_sys 
         Caption         =   "还原(&T)"
         Index           =   6
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   7
      End
      Begin VB.Menu m_sys 
         Caption         =   "退出(&X)"
         Index           =   8
      End
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Const LOG_FILE = "key_press_kk_log.log"

Private Const REG_SET = "BgPress_kk"

Dim APP_LOG_FILE As String
Dim isplay As Boolean
Dim play_count As Long

Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

Private MinFlag As Boolean
Dim dm As dmsoft
Dim klhnwd As Long, dm_ret As Long, isbusy As Boolean

Dim keyindex As Integer

Private Type NPKEY
    k As String
    d As Long
    nextid As Long
End Type
Dim stime
Dim kcount As Long
Dim keybuff(0 To 7) As NPKEY, alld As Long, numd As Long

Private Sub Form_Load()

    Set dm = CreateObject("dm.dmsoft")
    
    bindcb.AddItem "dx", 0
    bindcb.AddItem "normal", 1
    bindcb.AddItem "gdi", 2
    bindcb.AddItem "gdi2", 3
    bindcb.AddItem "dx2", 4
    bindcb.AddItem "dx3", 5
    bindcb.ListIndex = GetSetting(REG_SET, "Settings", "bind", 0)
    alldelayt.Text = GetSetting(REG_SET, "Settings", "alldelay", "100")
    playtext.Text = GetSetting(REG_SET, "Settings", "play", "100")
    mxtext.Text = GetSetting(REG_SET, "Settings", "mxtext", "896")
    mytext.Text = GetSetting(REG_SET, "Settings", "mytext", "778")
    
    logck.Value = GetSetting(REG_SET, "Settings", "log", 1)
    mck.Value = GetSetting(REG_SET, "Settings", "mck", 1)

    For a = 0 To 7
        castk(a).Text = GetSetting(REG_SET, "Settings", "key" & a, a)
        delay(a).Text = GetSetting(REG_SET, "Settings", "delay" & a, 1000)
        isc(a).Value = GetSetting(REG_SET, "Settings", "isc" & a, 0)
    Next a

    APP_LOG_FILE = App.Path & "\" & LOG_FILE

    isbusy = False
    Timer1.Enabled = False
    klhwnd = 0
    statel.Caption = "程序启动，准备!"
    ntext.Text = 0
    xmt.Text = 0
    ymt.Text = 0
    htext.Text = ""
    
    ' dm_ret = dm.Reg("abcd", "")
    statel.Caption = "dm.Reg ret:" & dm_ret & ", ver:" & dm.Ver()
End Sub
Private Sub Form_Unload(Cancel As Integer)
    dm_ret = 1
    If klhnwd > 0 And dm.IsBind(klhnwd) = 1 Then dm_ret = dm.UnBindWindow()
    If dm_ret = 0 Then
        statel.Caption = "解除绑定失败!"
        MsgBox "解除绑定失败!"
    End If

    SaveSetting REG_SET, "Settings", "bind", bindcb.ListIndex
    SaveSetting REG_SET, "Settings", "alldelay", alldelayt.Text
    SaveSetting REG_SET, "Settings", "play", playtext.Text
    SaveSetting REG_SET, "Settings", "mxtext", mxtext.Text
    SaveSetting REG_SET, "Settings", "mytext", mytext.Text
    
    SaveSetting REG_SET, "Settings", "log", logck.Value
    SaveSetting REG_SET, "Settings", "mck", mck.Value

    For a = 0 To 7
        SaveSetting REG_SET, "Settings", "key" & a, castk(a).Text
        SaveSetting REG_SET, "Settings", "delay" & a, delay(a).Text
        SaveSetting REG_SET, "Settings", "isc" & a, isc(a).Value
    Next a

    statel.Caption = "退出程序!"
End Sub


Private Sub movec_Click()
    Dim mx As Long, my As Long

    mx = CLng(xmt.Text)
    my = CLng(ymt.Text)
    dm.MoveWindow CLng(htext.Text), mx, my

End Sub

Private Sub runc_Click()

    statel.Caption = "    "

    If isbusy = False Then
        keyindex = 0
        For a = 0 To 7
            If isc(a).Value = 1 Then
                keybuff(keyindex).k = castk(a).Text
                If CLng(delay(a).Text) < 100 Then
                    keybuff(keyindex).d = 100
                ElseIf CLng(delay(a).Text) > 60000 Then
                    keybuff(keyindex).d = 60000
                Else
                    keybuff(keyindex).d = CLng(delay(a).Text)
                End If
                If keyindex > 0 Then
                    keybuff(keyindex - 1).nextid = keyindex
                End If
                keyindex = keyindex + 1
            End If
        Next a

        If keyindex > 0 Then
            keybuff(keyindex - 1).nextid = 0
        Else
            MsgBox "没有选择按键，注意!"
            statel.Caption = "没有选择按键，注意!"
            Exit Sub
        End If

        alld = 0
        alld = CLng(alldelayt.Text)
        If alld < 0 Then
            alld = 0
        ElseIf alld > 60 Then
            alld = 60
        End If

        answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
        If answer = vbNo Then Exit Sub
        Bydelay 2000
        klhwnd = dm.GetMousePointWindow()

        If mck.Value = 1 Then
        
            dm.GetCursorPos x, y
            dm_ret = dm.ScreenToClient(klhwnd, x, y)

            If mxtext.Text = "" Then mxtext.Text = x
            If mytext.Text = "" Then mytext.Text = y

        End If

        If mck.Value = 1 Then
            dm_ret = dm.BindWindow(klhwnd, bindcb.Text, "normal", "windows", 0)
        Else
            dm_ret = dm.BindWindow(klhwnd, bindcb.Text, "windows", "windows", 0)
        End If

        If dm_ret = 0 Then
            MsgBox "绑定失败 句柄：" & klhwnd
            statel.Caption = "绑定失败 句柄：" & klhwnd
            Exit Sub
        End If

        kcount = 0
        keyindex = 0
        statel.Caption = "绑定成功  开始运行 句柄：" & klhwnd
        ntext.Text = 0
        htext.Text = klhwnd

        isplay = False
        play_count = 0
        isbusy = True
        stime = Timer
        
        keyindex = 0
        
        Timer1.Interval = keybuff(keyindex).d
        Timer1.Enabled = True

        For a = 0 To 7
            castk(a).Enabled = False
            delay(a).Enabled = False
            isc(a).Enabled = False
        Next a
        alldelayt.Enabled = False
        bindcb.Enabled = False
        mck.Enabled = False
    Else
        statel.Caption = "正在运行中，注意!"
    End If

End Sub

Private Sub stopc_Click()

    If isbusy = True Then
        dm_ret = 1
        If klhnwd > 0 And dm.IsBind(klhnwd) = 1 Then dm_ret = dm.UnBindWindow()
        If dm_ret = 0 Then
            MsgBox "停止运行  解绑失败 "
            statel.Caption = "停止运行  解绑失败 "

            Exit Sub
        End If
        statel.Caption = "停止运行"
        isbusy = False

        isplay = False

        Timer1.Enabled = False

        For a = 0 To 7
            castk(a).Enabled = True
            delay(a).Enabled = True
            isc(a).Enabled = True
        Next a
        alldelayt.Enabled = True
        bindcb.Enabled = True
        mck.Enabled = True
        
        dm_ret = dm.UnBindWindow()
        Set dm = CreateObject("dm.dmsoft")
    Else
        statel.Caption = "无法停止，没有运行!"
    End If

End Sub

Private Sub Timer1_Timer()
    If isbusy = False Then Timer1.Enabled = False:: Exit Sub
    If mck.Value = 1 And mxtext.Text <> "" And mytext.Text <> "" Then
        dm_ret = dm.MoveTo(Val(mxtext.Text), Val(mytext.Text))
        If dm_ret = 0 Then statel.Caption = "移动鼠标，发生错误！"
        dm_ret = dm.LeftClick()
        If dm_ret = 0 Then
            statel.Caption = "点击鼠标，发生错误！"
        Else
            statel.Caption = "点击 x：" & mxtext.Text & ", y:" & mytext.Text
        End If
    End If
    
    dm.GetCursorPos x, y
    dm_ret = dm.ScreenToClient(klhwnd, x, y)
    statel.Caption = "当前坐标 x：" & x & ", y:" & y

    If kcount > 2100000000 Then kcount = 0
    kcount = kcount + 1
    
    isPress = True
    keyChar = keybuff(keyindex).k
    statel.Caption = "[" & keyindex & "] 进入 预按键：" & keyChar
    tmp = keyindex
    
    If keyChar = "2" Then
        keyindex = False
        dm_ret = dm.FindPic(25, 175, 430, 500, "1.bmp|2.bmp", "000000", 0.9, 0, intX, intY)
        If intX > 0 And intY > 0 Then
            statel.Caption = "[" & tmp & "] 找到 坐标 x：" & intX & ", y:" & intY
        Else
            statel.Caption = "[" & tmp & "] 没找到，跳过按键：" & keyChar
            isPress = False
        End If
    End If
    keyindex = tmp
    
    If isPress Then
        dm_ret = dm.KeyPressChar(keyChar)
        If dm_ret = 0 Then
            statel.Caption = "[" & keyindex & "] 按键，发生错误！"
        Else
            statel.Caption = "[" & keyindex & "] 按键：" & keyChar
        End If
    End If

            
    If keyindex = 0 And alld > 0 Then
        Bydelay alld * 1000
    End If
    If Timer - stime > 0 Then
        stime = Timer
        statel.Caption = "[" & keyindex & "] 按键计数：" & kcount & "，正在运行!"
    End If
    
    keyindex = keybuff(keyindex).nextid
    
    statel.Caption = "[" & keyindex & "] 按键完成 delay：" & keybuff(keyindex).d
    
    Timer1.Interval = keybuff(keyindex).d
    ntext.Text = kcount

    If playtext.Text <> "" Then
        If kcount > Val(playtext.Text) Then
            isplay = True
        Else
            isplay = False
        End If
    End If
    
    If isplay = True Then
        dm_ret = dm.FindPic(110, 40, 250, 67, "3.bmp", "000000", 0.9, 0, intX, intY)
        If intX > 0 And intY > 0 Then
            statel.Caption = "[" & keyindex & "] 存活检查 找到 坐标 x：" & intX & ", y:" & intY
            play_count = 0
        Else
            statel.Caption = "[" & keyindex & "] 存活检查 错误次数：" & play_count
            play_count = play_count + 1
        End If
        
        If play_count > 0 Then
            If play_count < Val(playtext.Text) Then
                If play_count > 5 Then dm.Beep 800, 200
                statel.Caption = "BEEP：" & play_count & " max:(" & playtext.Text & ")!"
            Else
                statel.Caption = "ExitOs：" & play_count & " max:(" & playtext.Text & ")!"
                Bydelay 30 * 1000
                dm.ExitOs (1)
            End If
        End If
    End If
End Sub
Private Sub Label3_DblClick()
    For a = 0 To 7
        castk(a).Text = a
        delay(a).Text = "1000"
        isc(a).Value = 0
    Next a
End Sub
Private Sub helpl_DblClick()
    Help.Show
End Sub
Private Sub Label2_DblClick()
    bindcb.ListIndex = 0
End Sub

Private Sub Label1_DblClick()
    alldelayt.Text = "0"
End Sub
Private Sub Label7_DblClick()
    If FileExist(APP_LOG_FILE) Then
        Shell "notepad " & APP_LOG_FILE, vbNormalFocus
    End If
End Sub
Private Sub Label4_Click()
    xmt.Text = 0
    ymt.Text = 0
End Sub
Private Sub Label7_MouseUp(Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 2 And Shift = 1 Then
        If FileExist(APP_LOG_FILE) Then
            Kill APP_LOG_FILE
        End If
    End If
End Sub

Private Sub statel_Change()
    If logck.Value = 1 Then
        Filelog logck.Value, statel.Caption, LOG_FILE
    End If
End Sub


Public Function FileExist(Filename As String) As Boolean
    FileExist = False
    On Error GoTo NotExist
    If Filename = "" Then Exit Function
    Call FileLen(Filename)
    FileExist = True
    Exit Function
NotExist:
End Function

Public Function FileIsR(Filename As String) As Boolean
    Dim objWMIService, colProcessList, objProcess
    If InStrRev(Filename, "\", -1, vbTextCompare) Then Filename = Mid$(Filename, InStrRev(Filename, "\", -1, vbTextCompare) + 1)
    FileIsR = False
    Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
    Set colProcessList = objWMIService.ExecQuery _
        ("Select * from Win32_Process Where Name='" & Filename & "'")

    For Each objProcess In colProcessList
        FileIsR = True
        Exit For
    Next
End Function

Public Function Bydelay(Millisecond As Long)
    Dim Start, Endtime As Single
    Start = Timer
    Endtime = Start + Millisecond / 1000
    Do While Timer < Endtime
        DoEvents
        Sleep 10
    Loop
End Function

Public Function Filelog(islog As Long, strlog As String, file As String) As Boolean
    On Error GoTo Notlog
    If islog = 1 Then
        Dim lngFileID As Long
        lngFileID = FreeFile(0)
        Open file For Append As lngFileID
        Print #lngFileID, Format$(Now, "c") & ":  " & strlog
        Close lngFileID
        Filelog = True
    End If
Notlog:
End Function

'窗体代码:

' 机能      : 窗口大小改变时
' 机能说明  : 窗口大小改变。
' 备注      :
Private Sub Form_Resize()
    '判断窗口是否最小化状态，并且是按最小化按纽后第一次发生Resize事件
    If IsIconic(Me.hWnd) <> 0 And MinFlag = False Then
        MinFlag = True
        Me.Visible = False '隐藏窗口
        '将窗口图标加入通知栏
        Call Icon_Add(Me.hWnd, Me.Caption, Me.Icon, 0)
    End If
End Sub

' 机能      : 点击托盘图标
' 机能说明  : 点击托盘图标。
' 备注      :
Private Sub Form_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    Dim l
    l = x \ Screen.TwipsPerPixelX
    '    Form1.Caption = Button & "  " & Shift & "  " & x & "  " & y & "   " & l

    '点击通知栏图标，用鼠标右键时调出弹出菜单

    Select Case l
        Case WM_LBUTTONDOWN
        showfrm
        Case WM_RBUTTONDOWN
        Me.PopupMenu m_syso
    End Select

    '点击通知栏图标，用鼠标左键时，将通知栏图标改为另外的图标
    '
End Sub

Private Sub m_sys_Click(Index As Integer)
    Select Case Index
        Case 0

        MsgBox "大漠插件实现，业余按键。"
        Case 2

        Call runc_Click
        Case 4

        Call stopc_Click
        Case 6
        '当单击"还原"菜单时
        If MinFlag = True Then
            showfrm
        End If
        Case 8
        '当单击"退出"菜单时
        Dim ret As Integer
        ret = MsgBox("您确定要退出系统吗？", vbYesNo)
        If ret = vbYes Then
            Call Icon_Del(Form1.hWnd, 0) '删除通知栏图标
            Unload Me
            End '退出程序
        End If
    End Select
End Sub

Private Sub showfrm()
    If MinFlag = False Then
        Exit Sub
    End If
    Form1.Show '调出窗口
    Form1.WindowState = 0
    Call Icon_Del(Form1.hWnd, 0) '删除通知栏图标
    Form1.SetFocus
    MinFlag = False
End Sub

Private Sub play_music()
    playsnd 440, 100
    playsnd 494, 100
    playsnd 554, 100
    playsnd 622, 100
    playsnd 698, 100
    playsnd 784, 100
    playsnd 880, 100

    playsnd 0, 0
End Sub

Private Function playsnd(ByVal x As Long, y As Long)
    If x = 0 And y = 0 Then
        isplay = False
        Exit Function
    End If
    
    If isplay = True Then
        DoEvents
        dm.Beep x, y * 3
        DoEvents
    End If
End Function

Private Sub delay_KeyPress(Index As Integer, KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub

Private Sub xmt_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub ymt_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub mxtext_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub mytext_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub htext_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub alldelayt_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
Private Sub playtext_KeyPress(KeyAscii As Integer)
    'If KeyAscii = 46 And Not CBool(InStr(txbNumber, ".")) Then Exit Sub
    If KeyAscii = 8 Then Exit Sub
    If KeyAscii < 48 Or KeyAscii > 57 Then KeyAscii = 0
End Sub
