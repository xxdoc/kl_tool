VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "comdlg32.ocx"
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "COMCTL32.OCX"
Begin VB.Form Form1 
   Caption         =   "File key"
   ClientHeight    =   3795
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   7530
   LinkTopic       =   "Form1"
   ScaleHeight     =   3795
   ScaleWidth      =   7530
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton checkcom 
      Caption         =   "Check"
      Height          =   375
      Left            =   6840
      TabIndex        =   17
      Top             =   2640
      Width           =   615
   End
   Begin VB.CommandButton addmd5com 
      Caption         =   "addMD5"
      Height          =   375
      Left            =   6000
      TabIndex        =   16
      Top             =   2640
      Width           =   735
   End
   Begin MSComDlg.CommonDialog CommonDialog2 
      Left            =   4080
      Top             =   1560
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.TextBox gtext 
      Height          =   270
      Left            =   3600
      TabIndex        =   15
      Text            =   "1"
      Top             =   2760
      Width           =   255
   End
   Begin ComctlLib.Slider gsl 
      Height          =   255
      Left            =   3840
      TabIndex        =   13
      Top             =   2760
      Width           =   1215
      _ExtentX        =   2143
      _ExtentY        =   450
      _Version        =   327682
      Min             =   1
      Max             =   9
      SelStart        =   1
      Value           =   1
   End
   Begin VB.CommandButton testcom 
      Caption         =   "TEST"
      Height          =   375
      Left            =   5160
      TabIndex        =   12
      Top             =   2640
      Width           =   735
   End
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   100
      Left            =   4080
      Top             =   600
   End
   Begin VB.TextBox bartext 
      Height          =   270
      Left            =   6840
      TabIndex        =   11
      Top             =   3120
      Width           =   615
   End
   Begin ComctlLib.ProgressBar filebar 
      Height          =   255
      Left            =   120
      TabIndex        =   10
      Top             =   3120
      Width           =   6615
      _ExtentX        =   11668
      _ExtentY        =   450
      _Version        =   327682
      Appearance      =   1
      Max             =   1000
   End
   Begin VB.TextBox md5 
      Height          =   375
      Left            =   120
      TabIndex        =   9
      Top             =   2520
      Width           =   3255
   End
   Begin VB.CommandButton undocom 
      Caption         =   "BACK"
      Height          =   375
      Left            =   6000
      TabIndex        =   8
      Top             =   2160
      Width           =   735
   End
   Begin VB.CommandButton docom 
      Caption         =   "DO"
      Height          =   375
      Left            =   5160
      TabIndex        =   6
      Top             =   2160
      Width           =   735
   End
   Begin VB.TextBox md5text 
      Height          =   2295
      Left            =   120
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   5
      Top             =   120
      Width           =   4095
   End
   Begin VB.TextBox filetext 
      Height          =   375
      Left            =   4440
      TabIndex        =   4
      Top             =   1680
      Width           =   2895
   End
   Begin VB.CommandButton dircom 
      Caption         =   "…"
      Height          =   375
      Left            =   6960
      TabIndex        =   3
      Top             =   2160
      Width           =   375
   End
   Begin VB.CommandButton gocom 
      Caption         =   "GO"
      Height          =   375
      Left            =   4320
      TabIndex        =   2
      Top             =   2160
      Width           =   735
   End
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   3960
      Top             =   1080
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.TextBox dirtext 
      Height          =   975
      Left            =   4440
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   1
      Top             =   600
      Width           =   2895
   End
   Begin VB.TextBox urltext 
      Height          =   375
      Left            =   4440
      TabIndex        =   0
      Top             =   120
      Width           =   2895
   End
   Begin VB.Label Label2 
      Caption         =   "加密等级："
      Height          =   255
      Left            =   3480
      TabIndex        =   14
      Top             =   2520
      Width           =   1095
   End
   Begin VB.Label statelab 
      Height          =   255
      Left            =   120
      TabIndex        =   7
      Top             =   3480
      Width           =   7575
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub gsl_Change()
gtext.Text = ""
gtext.Text = CStr(gsl.Value)
End Sub
Private Sub gtext_Change()
gtext.Text = CStr(gsl.Value)
End Sub

Private Sub gtext_KeyPress(KeyAscii As Integer)
gtext.Text = ""
If KeyAscii > 96 And KeyAscii < 106 Then gsl.Value = KeyAscii - 96
If KeyAscii > 48 And KeyAscii < 58 Then gsl.Value = KeyAscii - 48
gtext.Text = CStr(gsl.Value)
End Sub

Private Sub gsl_LostFocus()
If gtext.Text = "" Then gtext.Text = "1"
If CLng(gtext.Text) > 9 Or CLng(gtext.Text) < 1 Then gtext.Text = "1"
gsl.Value = CLng(gtext.Text)
End Sub
Private Sub md5_DblClick()
md5.Text = ""
End Sub
Private Sub statelab_DblClick()
statelab.Caption = ""
End Sub
Private Sub Timer1_Timer()
filebar.Value = dofile.fileProcessing
bartext.Text = Format(filebar.Value / 10, "0.0") & "%"
If filebar.Value > 990 Then Timer1.Enabled = False
End Sub
Private Sub urltext_DblClick()
urltext.Text = ""
End Sub
Private Sub Form_Load()
urltext.Text = GetSetting("Html do", "Settings", "lastUrl", "123456")
dirtext.Text = GetSetting("Html do", "Settings", "lastDir", "c:\test")
filetext.Text = GetSetting("Html do", "Settings", "lastfile", "test.rar")
urltext.Text = "123456"
CommonDialog1.InitDir = dirtext.Text
End Sub
Private Sub Form_Unload(Cancel As Integer)
SaveSetting "Html do", "Settings", "lastUrl", urltext.Text
SaveSetting "Html do", "Settings", "lastDir", dirtext.Text
SaveSetting "Html do", "Settings", "lastfile", filetext.Text
End Sub
Private Sub dircom_Click()

statelab.Caption = "open"
md5text.Text = ""
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

CommonDialog1.Filter = "所有文件(*.*)|*.*|压缩包(*.rar,*.zip,*.7z)|*.rar;*.zip;*.7z|视频(*.avi,*.rmvb,*.flv,*.mkv)|*.avi;*.rmvb;*.flv;*.mkv|KL加密文档(*.kld)|*.kld"
CommonDialog1.FileName = ""
CommonDialog1.ShowOpen
If CommonDialog1.FileName = "" Then Exit Sub
If InStrRev(CommonDialog1.FileName, "\", -1, vbTextCompare) Then
    filetext.Text = Mid$(CommonDialog1.FileName, InStrRev(CommonDialog1.FileName, "\", -1, vbTextCompare) + 1)
End If
'dirtext.Text = Mid$(CommonDialog1.FileName, 1, InStrRev(CommonDialog1.FileName, "\", -1, vbTextCompare) - 1)
dirtext.Text = CommonDialog1.FileName
End Sub
Private Sub addmd5com_Click()
If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

statelab.Caption = "MD5 doing"
md5text.Text = ""
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

Form1.Refresh

If readkeyfile(dirtext.Text) = False Then
    statelab.Caption = "readkeyfile 出错！"
    md5text.Text = md5text.Text & "文件不是KL加密文档！"
    Exit Sub
End If

If dirtext.Text = "" Then Exit Sub
md5.Text = klMD5(dirtext.Text, 1, Filelong(dirtext.Text) - 64)
If LenB(md5.Text) <> 64 Then statelab.Caption = "MD5 file错误！":: Exit Sub

If dirtext.Text = "" Then Exit Sub
If addfilemd5(dirtext.Text, md5.Text) Then
statelab.Caption = "addMD5 完成！"
Else
statelab.Caption = "addMD5 出错！"
Exit Sub
End If

If dirtext.Text = "" Then Exit Sub
If readkeyfile(dirtext.Text) = False Then
    statelab.Caption = "readkeyfile 出错！"
    md5text.Text = md5text.Text & "文件不是KL加密文档！"
    Exit Sub
Else
    statelab.Caption = "readkeyfile 完成！"
    md5text.Text = md5text.Text & "filMD5: " & dofile.filex.md & vbNewLine
    md5text.Text = md5text.Text & "keyMD5: " & dofile.filex.key & vbNewLine
    md5text.Text = md5text.Text & "加密时间: " & dofile.filex.dtmDateA & vbNewLine
    md5text.Text = md5text.Text & "长度: " & dofile.filex.flen & vbNewLine
    md5text.Text = md5text.Text & "原长度: " & dofile.filex.olen & vbNewLine
    md5text.Text = md5text.Text & "偏移: " & dofile.filex.fset & vbNewLine
    md5text.Text = md5text.Text & "路径: " & dofile.filex.file & vbNewLine
    md5text.Text = md5text.Text & "校验MD5: " & dofile.filex.chk & vbNewLine
End If


md5text.Text = md5text.Text & "部分MD5: " & md5.Text & vbNewLine

statelab.Caption = "addMD5 完成！"
md5.Text = ""
End Sub
Private Sub gocom_Click()
If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

statelab.Caption = "MD5 doing"
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

Form1.Refresh
If dirtext.Text = "" Then Exit Sub
md5.Text = klMD5(dirtext.Text, 1, 1)
If LenB(md5.Text) <> 64 Then statelab.Caption = "MD5 file错误！":: Exit Sub

statelab.Caption = "MD5 完成！   MD5: " & md5.Text & "    len: " & Filelong(dirtext.Text)

End Sub
Private Sub checkcom_Click()

If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

statelab.Caption = "MD5 doing"
md5text.Text = ""
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

Form1.Refresh

If dirtext.Text = "" Then Exit Sub
If readkeyfile(dirtext.Text) = False Then
    statelab.Caption = "readkeyfile 出错！"
    md5text.Text = md5text.Text & "文件不是KL加密文档！"
    Exit Sub
Else
    statelab.Caption = "readkeyfile 完成！"
    md5text.Text = md5text.Text & "filMD5: " & dofile.filex.md & vbNewLine
    md5text.Text = md5text.Text & "keyMD5: " & dofile.filex.key & vbNewLine
    md5text.Text = md5text.Text & "加密时间: " & dofile.filex.dtmDateA & vbNewLine
    md5text.Text = md5text.Text & "长度: " & dofile.filex.flen & vbNewLine
    md5text.Text = md5text.Text & "原长度: " & dofile.filex.olen & vbNewLine
    md5text.Text = md5text.Text & "偏移: " & dofile.filex.fset & vbNewLine
    md5text.Text = md5text.Text & "路径: " & dofile.filex.file & vbNewLine
    md5text.Text = md5text.Text & "校验MD5: " & dofile.filex.chk & vbNewLine
End If

If dirtext.Text = "" Then Exit Sub
md5.Text = klMD5(dirtext.Text, 1, Filelong(dirtext.Text) - 64)
If LenB(md5.Text) <> 64 Then statelab.Caption = "MD5 file错误！":: Exit Sub

md5text.Text = md5text.Text & "部分MD5: " & md5.Text & vbNewLine

statelab.Caption = "MD5校验 完成！"
md5.Text = ""
End Sub

Private Sub docom_Click()
If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

md5text.Text = ""
bartext.Text = ""
filebar.Value = 0

statelab.Caption = "keyfile doing"
filebar.Value = 0
bartext.Text = "MD5ing"
If dirtext.Text = "" Then Exit Sub
If md5.Text = "" Then md5.Text = klMD5(dirtext.Text, 1, 1)
If LenB(md5.Text) <> 64 Then statelab.Caption = "MD5 file错误！":: Exit Sub
Form1.Refresh
Dim odir As String
odir = dirtext.Text

Dim ofile As String
ofile = filetext.Text & ".kld"

CommonDialog2.FileName = ofile
CommonDialog2.Flags = cdlOFNOverwritePrompt
CommonDialog2.Filter = "KL加密文档(*.kld)|*.kld|压缩包(*.rar,*.zip,*.7z)|*.rar;*.zip;*.7z|视频(*.avi,*.rmvb,*.flv,*.mkv)|*.avi;*.rmvb;*.flv;*.mkv|所有文件(*.*)|*.*"
CommonDialog2.ShowSave
If CommonDialog2.FileName = "" Or CommonDialog2.FileName = ofile Then statelab.Caption = "esc":: Exit Sub

If InStrRev(CommonDialog2.FileName, "\", -1, vbTextCompare) Then
    filetext.Text = Mid$(CommonDialog2.FileName, InStrRev(CommonDialog2.FileName, "\", -1, vbTextCompare) + 1)
End If
dirtext.Text = CommonDialog2.FileName

Timer1.Enabled = True
If keyfile(odir, CommonDialog2.FileName, md5.Text, urltext.Text) = False Then
    statelab.Caption = statelab.Caption & "  keyfile 出错！"
Else
    statelab.Caption = "keyfile 完成！"
    filebar.Value = 1000
    bartext.Text = "完成"
End If
Timer1.Enabled = False

md5.Text = ""

End Sub
Private Sub undocom_Click()

On Error Resume Next

If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

md5text.Text = ""
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

statelab.Caption = "unkeyfile doing"
Form1.Refresh

Dim odir As String
odir = dirtext.Text
md5text.Text = "len: " & Filelong(dirtext.Text) & vbNewLine

If readkeyfile(dirtext.Text) = False Then
    statelab.Caption = "readkeyfile 出错！"
    md5text.Text = md5text.Text & "文件不是KL加密文档！"
    Exit Sub
Else
    statelab.Caption = "readkeyfile 完成！"
    md5text.Text = md5text.Text & "filMD5: " & dofile.filex.md & vbNewLine
    md5text.Text = md5text.Text & "keyMD5: " & dofile.filex.key & vbNewLine
    md5text.Text = md5text.Text & "加密时间: " & dofile.filex.dtmDateA & vbNewLine
    md5text.Text = md5text.Text & "长度: " & dofile.filex.flen & vbNewLine
    md5text.Text = md5text.Text & "原长度: " & dofile.filex.olen & vbNewLine
    md5text.Text = md5text.Text & "偏移: " & dofile.filex.fset & vbNewLine
    md5text.Text = md5text.Text & "路径: " & dofile.filex.file & vbNewLine
    md5text.Text = md5text.Text & "校验MD5: " & dofile.filex.chk & vbNewLine
End If

Dim ofile As String
If InStrRev(dofile.filex.file, "\", -1, vbTextCompare) Then
ofile = Mid$(dofile.filex.file, InStrRev(dofile.filex.file, "\", -1, vbTextCompare) + 1)
End If

CommonDialog2.FileName = ofile
CommonDialog2.Flags = cdlOFNOverwritePrompt
CommonDialog2.Filter = "所有文件(*.*)|*.*|压缩包(*.rar,*.zip,*.7z)|*.rar;*.zip;*.7z|视频(*.avi,*.rmvb,*.flv,*.mkv)|*.avi;*.rmvb;*.flv;*.mkv|KL加密文档(*.kld)|*.kld"
CommonDialog2.ShowSave
If CommonDialog2.FileName = "" Or CommonDialog2.FileName = ofile Then statelab.Caption = "esc":: Exit Sub

If InStrRev(CommonDialog2.FileName, "\", -1, vbTextCompare) Then
    filetext.Text = Mid$(CommonDialog2.FileName, InStrRev(CommonDialog2.FileName, "\", -1, vbTextCompare) + 1)
End If
dirtext.Text = CommonDialog2.FileName


Timer1.Enabled = True

If unkeyfile(odir, CommonDialog2.FileName, urltext.Text) = False Then
    statelab.Caption = statelab.Caption & "  unkeyfile 出错！"
Else
    statelab.Caption = "unkeyfile 完成！"
    filebar.Value = 1000
    bartext.Text = "完成"
    Name dirtext.Text & ".kld" As dirtext.Text
End If
Timer1.Enabled = False

End Sub

Private Sub testcom_Click()

If dofile.doProcessing = True Then statelab.Caption = "dofille is doing":: Exit Sub

md5text.Text = ""
md5.Text = ""
bartext.Text = ""
filebar.Value = 0

statelab.Caption = "readfile doing"
filebar.Value = 0
bartext.Text = "read"
Form1.Refresh

md5text.Text = "len: " & Filelong(dirtext.Text) & vbNewLine

If dirtext.Text = "" Then Exit Sub

If readkeyfile(dirtext.Text) = False Then
    statelab.Caption = "readkeyfile 出错！"
    md5text.Text = md5text.Text & "文件不是KL加密文档！"
    Exit Sub
Else
    statelab.Caption = "readkeyfile 完成！"
    md5text.Text = md5text.Text & "filMD5: " & dofile.filex.md & vbNewLine
    md5text.Text = md5text.Text & "keyMD5: " & dofile.filex.key & vbNewLine
    md5text.Text = md5text.Text & "加密时间: " & dofile.filex.dtmDateA & vbNewLine
    md5text.Text = md5text.Text & "长度: " & dofile.filex.flen & vbNewLine
    md5text.Text = md5text.Text & "原长度: " & dofile.filex.olen & vbNewLine
    md5text.Text = md5text.Text & "偏移: " & dofile.filex.fset & vbNewLine
    md5text.Text = md5text.Text & "路径: " & dofile.filex.file & vbNewLine
    md5text.Text = md5text.Text & "校验MD5: " & dofile.filex.chk & vbNewLine
End If

End Sub
