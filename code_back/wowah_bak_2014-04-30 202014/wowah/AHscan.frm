VERSION 5.00
Object = "{48E59290-9880-11CF-9754-00AA00C00908}#1.0#0"; "MSINET.OCX"
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "MSCOMCTL.OCX"
Begin VB.Form AHscan 
   Caption         =   "AHscan"
   ClientHeight    =   3840
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4950
   LinkTopic       =   "Form1"
   ScaleHeight     =   3840
   ScaleWidth      =   4950
   StartUpPosition =   3  '窗口缺省
   Begin MSComctlLib.ProgressBar dpb 
      Height          =   255
      Left            =   240
      TabIndex        =   27
      Top             =   2640
      Width           =   3615
      _ExtentX        =   6376
      _ExtentY        =   450
      _Version        =   393216
      Appearance      =   1
   End
   Begin InetCtlsObjects.Inet Inet1 
      Left            =   480
      Top             =   1320
      _ExtentX        =   1005
      _ExtentY        =   1005
      _Version        =   393216
   End
   Begin VB.TextBox timetext 
      Height          =   270
      Left            =   3960
      TabIndex        =   25
      Top             =   3000
      Width           =   855
   End
   Begin VB.CheckBox selfck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4560
      TabIndex        =   24
      Top             =   2640
      Width           =   255
   End
   Begin VB.TextBox proctext 
      Height          =   270
      Left            =   3960
      TabIndex        =   23
      Top             =   2640
      Width           =   495
   End
   Begin VB.TextBox tt 
      Height          =   270
      Left            =   3960
      TabIndex        =   18
      Top             =   1920
      Width           =   855
   End
   Begin VB.TextBox nt 
      Height          =   270
      Left            =   3960
      TabIndex        =   17
      Text            =   "00:00:00"
      Top             =   2280
      Width           =   855
   End
   Begin VB.TextBox aft2 
      Height          =   270
      Left            =   3960
      TabIndex        =   16
      Top             =   1560
      Width           =   855
   End
   Begin VB.TextBox aft1 
      Height          =   270
      Left            =   3960
      TabIndex        =   15
      Top             =   1320
      Width           =   855
   End
   Begin VB.Timer tm 
      Interval        =   1000
      Left            =   0
      Top             =   1680
   End
   Begin VB.CheckBox upck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4680
      TabIndex        =   12
      Top             =   960
      Width           =   255
   End
   Begin VB.CheckBox autock 
      Caption         =   "Check1"
      Height          =   255
      Left            =   3720
      TabIndex        =   11
      Top             =   960
      Width           =   255
   End
   Begin VB.CheckBox logck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   3720
      TabIndex        =   9
      Top             =   600
      Width           =   255
   End
   Begin VB.CheckBox deck 
      Caption         =   "Check1"
      Height          =   255
      Left            =   4680
      TabIndex        =   7
      Top             =   600
      Width           =   255
   End
   Begin VB.CommandButton cmdRUN 
      Caption         =   "RUN"
      Height          =   375
      Left            =   3120
      TabIndex        =   6
      Top             =   120
      Width           =   495
   End
   Begin VB.CommandButton cmdSET 
      Caption         =   "SET"
      Height          =   375
      Left            =   3720
      TabIndex        =   5
      Top             =   120
      Width           =   495
   End
   Begin VB.TextBox filetext 
      Height          =   375
      Left            =   240
      TabIndex        =   4
      Top             =   2160
      Width           =   2415
   End
   Begin VB.CommandButton cmdEXIT 
      Caption         =   "EXIT"
      Height          =   375
      Left            =   4320
      TabIndex        =   2
      Top             =   120
      Width           =   495
   End
   Begin VB.TextBox savefile 
      Height          =   975
      Left            =   240
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   1
      Top             =   1080
      Width           =   2655
   End
   Begin VB.TextBox txtURL 
      Height          =   855
      Left            =   240
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   0
      Top             =   120
      Width           =   2655
   End
   Begin VB.Label self_l 
      Height          =   255
      Left            =   120
      TabIndex        =   26
      Top             =   3480
      Width           =   4695
   End
   Begin VB.Label Label8 
      Caption         =   "Run Time:"
      Height          =   255
      Left            =   3000
      TabIndex        =   22
      Top             =   2280
      Width           =   855
   End
   Begin VB.Label Label7 
      Caption         =   "Timer T:"
      Height          =   255
      Left            =   3120
      TabIndex        =   21
      Top             =   1920
      Width           =   735
   End
   Begin VB.Label Label6 
      Caption         =   "MySQL T:"
      Height          =   255
      Left            =   3120
      TabIndex        =   20
      Top             =   1560
      Width           =   735
   End
   Begin VB.Label Label3 
      Caption         =   "Check T:"
      Height          =   255
      Left            =   3120
      TabIndex        =   19
      Top             =   1320
      Width           =   735
   End
   Begin VB.Label Label5 
      Caption         =   "asMin:"
      Height          =   255
      Left            =   4080
      TabIndex        =   14
      Top             =   960
      Width           =   495
   End
   Begin VB.Label Label4 
      Caption         =   "Auto:"
      Height          =   255
      Left            =   3120
      TabIndex        =   13
      Top             =   960
      Width           =   615
   End
   Begin VB.Label Label2 
      Caption         =   "iLog:"
      Height          =   255
      Left            =   3120
      TabIndex        =   10
      Top             =   600
      Width           =   615
   End
   Begin VB.Label Label1 
      Caption         =   "Debug:"
      Height          =   255
      Left            =   4080
      TabIndex        =   8
      Top             =   600
      Width           =   615
   End
   Begin VB.Label state 
      Height          =   375
      Left            =   120
      TabIndex        =   3
      Top             =   3000
      Width           =   3735
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
Attribute VB_Name = "AHscan"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim b_s(10) As String, l_s(10) As String, d_s(10) As String
Dim set_str(0 To 5) As String

Dim is_runing As Boolean, DE As Long, info_s As String
Dim dm As New dmsoft, ThunderAgent As Object, ch As New kVBJSON
Private MinFlag As Boolean

Dim self_is_downing As Boolean
Dim self_save_dir As String
Dim self_s_time As Date

Dim stime, ltime1, ltime2
Private Const LOG_FILE_SET = "AHscan_log.log"
Private Const R_URL = "http://www.battlenet.com.cn/api/wow/auction/data/"

Private Declare Function DeleteUrlCacheEntry Lib "wininet" Alias "DeleteUrlCacheEntryA" (ByVal lpszUrlName As String) As Long
Private Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long

Private Declare Function GetTickCount Lib "kernel32" () As Long
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (Destination As Any, Source As Any, ByVal Length As Long)
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Private Declare Function MultiByteToWideChar Lib "kernel32" (ByVal CodePage As Long, ByVal dwFlags As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long) As Long
Private Const CP_UTF8 = 65001

Private Sub cmdRUN_Click()
    On Error GoTo CuoWu
    If is_runing = True Then
        state.Caption = "Error in running cannot run."

        Exit Sub
    End If

    Dim rc As Long, k As Long, n As Long

    For n = 0 To 5
        If dir(set_str(n)) = "" Then
            setform.Show 1, Me
            Exit Sub
        End If
    Next

    is_runing = True
    For n = 1 To 4
        If Not FileIsR(set_str(n)) And n <> 2 Then
            Shell set_str(n), vbMinimizedNoFocus
            state.Caption = "Shell Run : " & set_str(n)
        End If
    Next

    Me.Refresh
    k = dm.SetWindowState(Me.hWnd, 1)

    proctext.Text = "0.0%"
    timetext.Text = "00:00:00"
    self_l.Caption = ""

    state.Caption = "Read cfg : " & set_str(0)

    is_runing = False
    If is_runing = False Then info_s = read_cfg(set_str(0), 4, 1)

    If Len(info_s) > 8 Then
        is_runing = False
        rc = -1
        If is_runing = False Then rc = do_task(info_s)
        If rc > 0 Then
            If DE = 1 Then state.Caption = "Do Task done."
        Else
            state.Caption = "Error In Do Task."

            GoTo CuoWu
        End If
    Else
        state.Caption = "Error Task Info."

        GoTo CuoWu
    End If
    state.Caption = "Run and Check, Over!! "
    k = dm.SetWindowState(Me.hWnd, 1)
    stime = Now
    ltime1 = stime
    ltime2 = stime
    is_runing = False

    Exit Sub
CuoWu:
    is_runing = False
    state.Caption = "Try Run error!!!"

End Sub

Private Function read_cfg(st As String, offset As Long, ck As Long) As String
    On Error GoTo CuoWu

    If is_runing = True Then
        state.Caption = "Error in running cannot read cfg."

        read_cfg = ""
        Exit Function
    End If

    is_runing = True
    Dim rc As Long, ts As String, i As Long, k As Long, n As Long

    info_s = ""
    rc = ch.Class_Clear()
    rc = ch.parse_UTF(st, "base_set|MySQL_set|log_set|task", offset, ck)
    If rc = 4 Then
        ts = ch.Getkv(3)

        Dim bh As New kVBJSON
        rc = bh.parse_str(ch.Getkv(0), "base_path|cfg_file|JSON_path|DATA_TEMP_path|DATA_BAK_path|bak_size_limt|help", 1)
        For i = 0 To rc
            b_s(i) = bh.Getkv(i)
        Next
        If b_s(0) = "" Then b_s(0) = Left$(set_str(0), InStrRev(set_str(0), "\") - 1)
        If b_s(2) = "" Then b_s(2) = "JSON"
        If b_s(3) = "" Then b_s(3) = "DATA_TEMP"
        If b_s(4) = "" Then b_s(4) = "DATA_BAK"

        rc = bh.Class_Clear()
        rc = bh.parse_str(ch.Getkv(1), "host|user|passwd|db|charset|ah_tmp|fwq_tmp|help", 1)
        For i = 0 To rc
            d_s(i) = bh.Getkv(i)
        Next

        rc = bh.Class_Clear()
        rc = bh.parse_str(ch.Getkv(2), "filename|level|filemode|format|help", 1)
        For i = 0 To rc
            l_s(i) = bh.Getkv(i)
        Next
    Else
        state.Caption = "error cfg : " & set_str(0)

        GoTo CuoWu
    End If

    rc = ch.Class_Clear()
    rc = ch.parse_str(ts, "info", 1)
    If rc = 1 Then
        read_cfg = ch.Getkv(0)
    Else
        read_cfg = ""
    End If
    is_runing = False
    Exit Function
CuoWu:
    state.Caption = "read cfg error!!!"

    read_cfg = ""
    is_runing = False
End Function
Private Function do_task(st As String) As Long
    On Error GoTo CuoWu
    If is_runing = True Then
        state.Caption = "Error in running cannot do task."

        do_task = -11
        Exit Function
    End If

    is_runing = True
    Dim fp As String, fo As String, url_str As String, file_str As String, dir_str As String
    Dim rs As Long, k As Long
    rc = ch.Class_Clear()
    rc = ch.parse_str(st, "is|name", 1)

    dir_str = b_s(0) & "\temp"

    If Not FolderExists(dir_str) Then MkDir (dir_str)
    If Not FolderExists(b_s(0) & "\" & b_s(2)) Then MkDir (b_s(0) & "\" & b_s(2))
    If Not FolderExists(b_s(0) & "\" & b_s(2) & "\" & b_s(3)) Then MkDir (b_s(0) & "\" & b_s(2) & "\" & b_s(3))

    Do
        If rc = 2 And ch.Getkv(0) = "1" Then
            file_str = ch.Getkv(1) & ".json"
            url_str = R_URL & GBtoUTF8(ch.Getkv(1))
            
            txtURL.Text = R_URL & ch.Getkv(1)
            filetext.Text = file_str
            savefile.Text = dir_str & "\" & file_str
            
            k = 0
            fp = dir_str & "\" & file_str
            fo = b_s(0) & "\" & b_s(2) & "\" & file_str
            state.Caption = "Download file : " & file_str
            Me.Refresh
            DoEvents
            

            Do While Not DownloadFile(url_str, fp, 1)
                k = k + 1
                If k > 10 Then
                    state.Caption = "Download to file error!"
                    MsgBox state.Caption
                    GoTo CuoWu
                    Exit Do
                End If
                DoEvents
            Loop
            k = check_file(fp, fo)
            If k <= 0 Then
                state.Caption = "check file error : " & filetext.Text
            End If
        ElseIf rc = 2 Then
            state.Caption = "Not Download file : " & ch.Getkv(1) & ".json"
        Else
            state.Caption = "Error Task Info No.: " & ch.r_tl

        End If
        If ch.can_next Then
            rc = ch.nextArray()
        Else
            state.Caption = "All Task Count : " & ch.r_rl
            Exit Do
        End If
    Loop

    state.Caption = "Do Task, Over!! "
    do_task = 1
    is_runing = False
    Exit Function

CuoWu:
    is_runing = False
    state.Caption = "Do Task error!!!"

    do_task = -1
End Function

Private Function check_file(fp As String, fo As String) As Long
    On Error GoTo CuoWu
    If Not FileExists(fp) Then
        state.Caption = ch.Getkv(1) & " >> no fp!"

        GoTo CuoWu
    End If

    Dim ph As New kVBJSON, oh As New kVBJSON, rc As Long, i As Long, ts As String
    rc = ph.parse_file(fp, "files", 0, 1)
    If rc = 1 Then
        rc = ph.parse_str(ph.Getkv(0), "url|lastModified", 1)
    Else
        state.Caption = "fp no key files!"

        GoTo CuoWu
    End If
    If rc <> 2 Then
        state.Caption = "fp no key url|lastModified!"

        GoTo CuoWu
    End If

    If Not FileExists(fo) Then
        state.Caption = ch.Getkv(1) & " >> no fo,do it!"
        Name fp As fo
        ts = b_s(0) & "\" & b_s(2) & "\" & b_s(3) & "\" & ch.Getkv(1) & "_" & ph.Getkv(1) & ".json"

        self_l.Caption = state.Caption
        rc = try_down(ph.Getkv(0), ts)
        'download ah json file by thender

        If rc <= 0 Then
            state.Caption = "no fo,thd file error : " & ch.Getkv(1)

            check_file = -12
        Else
            state.Caption = "no fo,thd file done : " & ch.Getkv(1)

            check_file = 2
        End If
        Exit Function
    End If

    rc = oh.parse_file(fo, "files", 0, 1)
    If rc = 1 Then
        rc = oh.parse_str(oh.Getkv(0), "url|lastModified", 1)
    Else
        state.Caption = "fo no key files!"

        GoTo CuoWu
    End If
    If rc <> 2 Then
        state.Caption = "fo no key url|lastModified!"

        GoTo CuoWu
    End If

    If StrComp(ph.Getkv(1), oh.Getkv(1), vbTextCompare) > 0 Then
        state.Caption = ch.Getkv(1) & " >> new fp,do it!"

        Kill fo
        Name fp As fo
        ts = b_s(0) & "\" & b_s(2) & "\" & b_s(3) & "\" & ch.Getkv(1) & "_" & ph.Getkv(1) & ".json"

        self_l.Caption = state.Caption
        
        rc = 1
        'rc = try_down(ph.Getkv(0), ts)
        
        'download ah json file by thender

        If rc <= 0 Then
            state.Caption = "new fp,thd file error : " & ch.Getkv(1)

            check_file = -11
        Else
            state.Caption = "new fp,thd file done : " & ch.Getkv(1)

            check_file = 1
        End If
        Exit Function
    End If

    state.Caption = ch.Getkv(1) & " >> is new,do nothing!"
    self_l.Caption = state.Caption
    check_file = 3
    Me.Refresh
    Exit Function
CuoWu:
    check_file = -1
    state.Caption = "Try check_file error!!!"

End Function
Private Function try_down(url As String, dir As String) As Long
    txtURL.Text = url
    savefile.Text = dir
    filetext.Text = Right$(dir, Len(dir) - InStrRev(dir, "\"))
    
    

    If selfck.Value = 0 Then
        try_down = thd(url, dir)
    Else
        try_down = self_down(url, dir)
    End If
End Function

Private Function self_down(url As String, dir As String) As Long
    On Error GoTo CuoWu

    If FileExists(dir) Or FileExists(dir & ".td") Or FileExists(Left$(dir, InStrRev(dir, "\") - Len(b_s(3)) - 1) & Replace$(dir, b_s(3) & "\", b_s(3) & "\" & b_s(4) & "\", InStrRev(dir, "\") - Len(b_s(3)), 1, vbTextCompare)) Then
        If DE = 1 Then state.Caption = "have dir ah file!"
        self_down = 2
        Exit Function
    End If

    pt = Left$(dir, InStrRev(dir, "\") - 1)
    na = Right$(dir, Len(dir) - InStrRev(dir, "\"))

    proctext.Text = "0.0%"
    timetext.Text = "00:00:00"
    self_l.Caption = ""

    StartDownLoad url, url

    self_down = 1
    Exit Function
CuoWu:
    self_down = -1
    state.Caption = "Try self_down down file error!!!"

End Function
Private Sub StartDownLoad(url As String, dir As String)
    self_is_downing = True
    self_save_dir = dir
    self_s_time = Now
    Inet1.Execute url, "get"
End Sub

Private Sub Inet1_StateChanged(ByVal state As Integer)

    On Error GoTo CuoWu
    'State = 12 时，用 GetChunk 方法检索服务器的响应。
    Dim k As Long, n As Long, s As Long, o As Long

    Dim vtData() As Byte
    Select Case state
        Case icError '11
        '出现错误时，返回 ResponseCode 和 ResponseInfo。
        vtData = Inet1.ResponseCode & ":" & Inet1.ResponseInfo
        MsgBox "return 11,net error: " & Inet1.ResponseCode & ":" & Inet1.ResponseInfo
        Case icResponseCompleted ' 12
        Dim bDone As Boolean
        bDone = False
        '取得第一个块。
        vtData() = Inet1.GetChunk(1024, 1)
        DoEvents
        Open self_save_dir For Binary Access Write As #1     '设置保存路径文件后

        ' 开始保存
        '获取下载文件长度
        'MsgBox Len(Inet1.GetHeader("Content-Length"))
        If Len(Inet1.GetHeader("Content-Length")) > 0 Then ProgressBar1.Max = CLng(Inet1.GetHeader("Content-Length"))

        '循环分块下载
        k = GetTickCount()
        n = 0
        s = 0
        o = 0
        Do While Not bDone
            n = n + 1
            Put #1, Loc(1) + 1, vtData()
            vtData() = Inet1.GetChunk(1024, 1)
            DoEvents
            ProgressBar1.Value = Loc(1)   '设置进度条长度
            proctext.Text = CStr(Format$(ProgressBar1.Value / (ProgressBar1.Max + 1) * 100, "0.0")) & "%"
            self_l.Caption = "Downloading now: " & ByteToString(ProgressBar1.Value) & " /" & ByteToString(ProgressBar1.Max)
            timetext.Text = SecondToString(DateDiff("s", self_s_time, Now)) & " >> " & ByteToString(s) & "/s"
            If Loc(1) >= ProgressBar1.Max Then bDone = True
            If n = 70 Then
                s = (ProgressBar1.Value - o) * 1000 \ (GetTickCount() - k)
                k = GetTickCount()
                o = ProgressBar1.Value
                n = 0
            End If
        Loop

        Close #1
        self_l.Caption = "Download Finished,Total: " & ByteToString(ProgressBar1.Max)
        proctext.Text = "100%"
        k = DateDiff("s", self_s_time, Now)
        timetext.Text = SecondToString(k) & " ++ " & ByteToString(ProgressBar1.Max \ k) & "/s"
        self_is_downing = False
        self_save_dir = ""
    End Select

    Exit Sub
CuoWu:
    self_l.Caption = "Downloading error!!!"
End Sub

Private Function thd(url As String, dir As String) As Long
    On Error GoTo CuoWu

    If FileExists(dir) Or FileExists(dir & ".td") Or FileExists(Left$(dir, InStrRev(dir, "\") - Len(b_s(3)) - 1) & Replace$(dir, b_s(3) & "\", b_s(3) & "\" & b_s(4) & "\", InStrRev(dir, "\") - Len(b_s(3)), 1, vbTextCompare)) Then
        If DE = 1 Then state.Caption = "have dir ah file!"
        thd = 2
        Exit Function
    End If

    Dim na As String, pt As String, k As Long, c As Long

    pt = Left$(dir, InStrRev(dir, "\") - 1)
    na = Right$(dir, Len(dir) - InStrRev(dir, "\"))
    Call ThunderAgent.AddTask(url, na, pt, "", "", 1, 0, 5)
    Call ThunderAgent.CommitTasks2(1)
    Bydelay 300
    k = 0
    c = 0
    Do While k = 0
        DoEvents
        k = dm.FindWindow("XLUEModalHostWnd", "新建")
        DoEvents
        c = c + 1
        If k > 0 Or c > 10 Then Exit Do
        Bydelay 100
    Loop
    If k > 0 Then
        Bydelay 100
        k = dm.KeyPressChar("enter")
    End If
    k = 0
    c = 0
    Do While k = 0
        DoEvents
        k = dm.FindWindow("XLUEModalHostWnd", "重复任务提示")
        DoEvents
        c = c + 1
        If k > 0 Or c > 3 Then Exit Do
        Bydelay 100
    Loop
    If k > 0 Then
        Bydelay 100
        k = dm.KeyPressChar("enter")
    End If
    k = 0
    c = 0
    Do While k = 0
        DoEvents
        k = dm.FindWindow("XLUEModalHostWnd", "重复任务提示")
        DoEvents
        c = c + 1
        If k > 0 Or c > 1 Then Exit Do
        Bydelay 100
    Loop
    If k > 0 Then
        Bydelay 100
        k = dm.KeyPressChar("esc")
    End If
    k = 0
    c = 0
    Do While k = 0
        DoEvents
        k = dm.FindWindow("XLUEModalHostWnd", "重新下载")
        DoEvents
        c = c + 1
        If k > 0 Or c > 3 Then Exit Do
        Bydelay 100
    Loop
    If k > 0 Then
        Bydelay 100
        k = dm.KeyPressChar("enter")
    End If
    thd = 1
    Exit Function
CuoWu:
    thd = -1
    state.Caption = "Try thd down file error!!!"

End Function

Private Sub cmdSET_Click()
    setform.Show 1, Me
End Sub

Private Sub state_Change()
    Me.Refresh
    If logck.Value > 0 Then Filelog logck.Value, state.Caption, LOG_FILE_SET
    If DE = 1 Then MsgBox state.Caption
End Sub

Private Sub deck_Click()
    If deck.Value > 0 Then
        DE = 1
        state.Caption = "start debug ..."
    Else
        DE = 0
        state.Caption = "start debug ..."
    End If
End Sub

Private Sub upck_Click()
    If upck.Value > 0 Then
        autock.Value = 2
        state.Caption = "start setup ..."
    Else
        autock.Value = 0
        state.Caption = "stop setup ..."
    End If
End Sub

Private Sub autock_Click()
    If autock.Value > 0 Then
        state.Caption = "start auto ..."
    Else
        state.Caption = "stop auto ..."
    End If
End Sub

Private Sub logck_Click()
    If logck.Value > 0 Then
        state.Caption = "start logging ..."
    Else
        state.Caption = "stop logging ..."
    End If
End Sub
Private Sub selfck_Click()
    If selfck.Value > 0 Then
        state.Caption = "start selfck ..."
    Else
        state.Caption = "stop selfck ..."
    End If
End Sub

Private Sub aft1_Change()
    If CLng(aft1.Text) < 60 Then
        aft1.Text = 60
    End If
End Sub

Private Sub aft2_Change()
    If CLng(aft2.Text) < 60 Then
        aft2.Text = 60
    End If
End Sub
Private Sub tt_Change()
    If CLng(tt.Text) < 1000 Then
        tt.Text = 1000
    End If
    If CLng(tt.Text) > 60000 Then
        tt2.Text = 60000
    End If
End Sub

Private Sub Label2_DblClick()
    Shell "notepad.exe " + App.Path + "\" + LOG_FILE_SET, vbNormalFocus
End Sub

Public Function GetAry(ByVal Index As Long) As String
    GetAry = set_str(Index)
End Function

Public Function SaveAry(ByVal Index As Long, strin As String) As Long
    set_str(Index) = strin
    SaveAry = Index
    state.Caption = "set patch: " & setform.lset(Index).Caption & "->" & strin
End Function

Private Sub Form_Resize()
    If IsIconic(Me.hWnd) <> 0 And MinFlag = False Then
        MinFlag = True
        Me.Visible = False
        Call Icon_Add(Me.hWnd, Me.Caption, Me.Icon, 0)
    End If
End Sub

Private Sub Form_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    Dim l
    l = x \ 15
    Select Case l
        Case WM_LBUTTONDOWN
        showfrm
        Case WM_RBUTTONDOWN
        Me.PopupMenu m_syso
    End Select
End Sub

Private Sub m_sys_Click(Index As Integer)
    Select Case Index
        Case 0

        MsgBox "运行时间：" & nt.Text
        Case 2

        autock.Value = 1
        Case 4

        autock.Value = 0
        Case 6

        If MinFlag = True Then
            showfrm
        End If
        Case 8
        '当单击"退出"菜单时
        Call cmdEXIT_Click
    End Select
End Sub

Private Sub showfrm()
    If MinFlag = False Then
        Exit Sub
    End If
    Me.Show
    Me.WindowState = 0
    Call Icon_Del(Me.hWnd, 0)
    Me.SetFocus
    MinFlag = False
End Sub

Private Sub cmdEXIT_Click()
    Dim msgRes As VbMsgBoxResult
    If is_runing = True Then
        msgRes = MsgBox("正在运行，是否退出?", vbQuestion + vbYesNo + vbDefaultButton2, "退出")
        If msgRes = vbNo Then Exit Sub
    End If
    Unload Me
    End
End Sub

Private Sub Form_Load()
    For n = 0 To 5
        set_str(n) = GetSetting("AHscan", "Settings", "set_" & n, "")
    Next n

    logck.Value = GetSetting("AHscan", "Settings", "logck", 0)
    deck.Value = GetSetting("AHscan", "Settings", "deck", 0)
    autock.Value = GetSetting("AHscan", "Settings", "autock", 0)
    upck.Value = GetSetting("AHscan", "Settings", "upck", 0)
    selfck.Value = GetSetting("AHscan", "Settings", "selfck", 0)

    aft1.Text = GetSetting("AHscan", "Settings", "aft1", "1200")
    aft2.Text = GetSetting("AHscan", "Settings", "aft2", "2400")
    tt.Text = GetSetting("AHscan", "Settings", "tt", "1000")

    'txtURL.Text = GetSetting("AHscan", "Settings", "url", "")
    'savefile.Text = GetSetting("AHscan", "Settings", "save_dir", "")

    self_is_downing = False
    is_runing = False
    Set ThunderAgent = CreateObject("ThunderAgent.Agent.1")

    dpb.Value = 0

    proctext.Text = "0.0%"
    timetext.Text = "00:00:00"
    self_l.Caption = ""

    DE = deck.Value
    state.Caption = "Form_Load..."

    If CLng(aft1.Text) < 60 Then
        aft1.Text = 60
    End If
    If CLng(aft2.Text) < 60 Then
        aft2.Text = 60
    End If
    If CLng(tt.Text) < 1000 Then
        tt.Text = 1000
    End If
    If CLng(tt.Text) > 60000 Then
        tt.Text = 60000
    End If
    tm.Enabled = True
    tm.Interval = CLng(tt.Text)
    If upck.Value = 1 Then
        MinFlag = True
        Me.Visible = False
        Call Icon_Add(Me.hWnd, Me.Caption, Me.Icon, 0)
        Call cmdRUN_Click
        autock.Value = 2
    End If

    state.Caption = "Ready..."
End Sub

Private Sub Form_Unload(Cancel As Integer)
    Unload setform
    For n = 0 To 5
        If set_str(n) <> "" Then SaveSetting "AHscan", "Settings", "set_" & n, set_str(n)
    Next n

    SaveSetting "AHscan", "Settings", "logck", logck.Value
    SaveSetting "AHscan", "Settings", "deck", deck.Value
    SaveSetting "AHscan", "Settings", "autock", autock.Value
    SaveSetting "AHscan", "Settings", "upck", upck.Value
    SaveSetting "AHscan", "Settings", "selfck", selfck.Value

    SaveSetting "AHscan", "Settings", "aft1", aft1.Text
    SaveSetting "AHscan", "Settings", "aft2", aft2.Text
    SaveSetting "AHscan", "Settings", "tt", tt.Text

    SaveSetting "AHscan", "Settings", "url", txtURL.Text
    SaveSetting "AHscan", "Settings", "save_dir", savefile.Text

    state.Caption = "Form_Unload..."
End Sub

Private Sub tm_Timer()
    If is_runing = True Then Exit Sub
    Dim rc As Long
    If autock.Value > 0 And info_s <> "" Then
        If stime > 0 Then nt.Text = SecondToString(DateDiff("s", stime, Now))

        For n = 1 To 4
            If Not FileIsR(set_str(n)) And n <> 2 Then
                Shell set_str(n), vbMinimizedNoFocus
                state.Caption = "Shell Run : " & set_str(n)
            End If
        Next

        If DateDiff("s", ltime1, Now) > CLng(aft1.Text) Then
            If Len(info_s) > 8 Then
                If is_runing = False Then rc = do_task(info_s)
            End If
            state.Caption = "Check, Over!! "
            ltime1 = Now
        End If

        If DateDiff("s", ltime2, Now) > CLng(aft2.Text) Then
            Shell "cmd " & set_str(5) & " " & set_str(0), vbMinimizedNoFocus
            state.Caption = "Run Python Script!! "
            ltime2 = Now
        End If
        If stime > 0 Then nt.Text = SecondToString(DateDiff("s", stime, Now))
    End If
End Sub

Public Function URLEncoding(ByVal vstrIn As String) As String

    strReturn = ""

    Dim i
    Dim thisChr

    For i = 1 To Len(vstrIn)

        thisChr = Mid$(vstrIn, i, 1)

        If Abs(Asc(thisChr)) < &HFF Then
            If thisChr = " " Then
                strReturn = strReturn & "+"
            ElseIf InStr(1, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.", thisChr) > 0 Then
                strReturn = strReturn & thisChr
            Else
                strReturn = strReturn & "%" & IIf(Asc(thisChr) > 16, "", "0") & Hex$(Asc(thisChr))
            End If
        Else
            innerCode = Asc(thisChr)
            If innerCode < 0 Then
                innerCode = innerCode + &H10000
            End If
            Hight8 = (innerCode And &HFF00) \ &HFF
            Low8 = innerCode And &HFF
            strReturn = strReturn & "%" & Hex$(Hight8) & "%" & Hex$(Low8)
        End If
    Next

    URLEncoding = strReturn

End Function

Public Function GBtoUTF8(szInput As String) As String
    Dim wch, uch, szRet
    Dim x
    Dim nAsc, nAsc2, nAsc3

    '如果输入参数为空，则退出函数
    If szInput = "" Then
        GBtoUTF8 = szInput
        Exit Function
    End If

    '开始转换
    For x = 1 To Len(szInput)
        wch = Mid$(szInput, x, 1)
        nAsc = AscW(wch)

        If nAsc < 0 Then nAsc = nAsc + 65536

        If (nAsc And &HFF80) = 0 Then
            szRet = szRet & wch
        Else
            If (nAsc And &HF000) = 0 Then
                uch = "%" & Hex$(((nAsc \ 2 ^ 6)) Or &HC0) & Hex$(nAsc And &H3F Or &H80)
                szRet = szRet & uch
            Else
                uch = "%" & Hex$((nAsc \ 2 ^ 12) Or &HE0) & "%" & _
                      Hex$((nAsc \ 2 ^ 6) And &H3F Or &H80) & "%" & _
                      Hex$(nAsc And &H3F Or &H80)
                szRet = szRet & uch
            End If
        End If
    Next

    GBtoUTF8 = szRet
End Function

Private Function ByteToString(ByVal iSize As Long) As String
    '//Byte ->Byte KB or MB
    Dim c       As Double
    If iSize < 1024 Then
        ByteToString = CStr(iSize) & " Byte"
    Else
        c = iSize / 1024& / 1024&
        If c > 1 Then
            ByteToString = CStr(Format$(c, "###,###,##0.0")) & " MB"
        Else
            c = iSize / 1024&
            ByteToString = CStr(Format$(c, "###,###,##0.0")) & " KB"
        End If
    End If
    If iSize <= 0 Then
        ByteToString = "NaN Byte"
    End If
End Function

Private Function SecondToString(ByVal secn As Long) As String
    '//Second ->00::00::00
    If secn > 3600 Then
        SecondToString = Format$(secn \ 3600, "00")
        secn = secn Mod 3600
    Else
        SecondToString = "00"
    End If
    If secn > 60 Then
        SecondToString = SecondToString & ":" & Format$(secn \ 60, "00")
        secn = secn Mod 60
    Else
        SecondToString = SecondToString & ":" & "00"
    End If
    SecondToString = SecondToString & ":" & Format$(secn, "00")
End Function
