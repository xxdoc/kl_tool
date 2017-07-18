VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Begin VB.Form setform 
   Caption         =   "Set"
   ClientHeight    =   3435
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   5445
   LinkTopic       =   "Form1"
   ScaleHeight     =   3435
   ScaleWidth      =   5445
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton delset 
      Caption         =   "DEL"
      Height          =   375
      Left            =   360
      TabIndex        =   20
      Top             =   3000
      Width           =   735
   End
   Begin VB.CommandButton exitset 
      Caption         =   "EXIT"
      Height          =   375
      Left            =   3480
      TabIndex        =   19
      Top             =   3000
      Width           =   735
   End
   Begin VB.CommandButton okset 
      Caption         =   "OK"
      Height          =   375
      Left            =   2400
      TabIndex        =   18
      Top             =   3000
      Width           =   735
   End
   Begin MSComDlg.CommonDialog cdset 
      Left            =   4920
      Top             =   2400
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   5
      Left            =   4200
      TabIndex        =   11
      Top             =   2520
      Width           =   495
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   4
      Left            =   4200
      TabIndex        =   10
      Top             =   2040
      Width           =   495
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   3
      Left            =   4200
      TabIndex        =   9
      Top             =   1560
      Width           =   495
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   2
      Left            =   4200
      TabIndex        =   8
      Top             =   1080
      Width           =   495
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   1
      Left            =   4200
      TabIndex        =   7
      Top             =   600
      Width           =   495
   End
   Begin VB.CommandButton cset 
      Caption         =   ">>>"
      Height          =   375
      Index           =   0
      Left            =   4200
      TabIndex        =   6
      Top             =   120
      Width           =   495
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   5
      Left            =   960
      TabIndex        =   5
      Top             =   2520
      Width           =   3135
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   4
      Left            =   960
      TabIndex        =   4
      Top             =   2040
      Width           =   3135
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   3
      Left            =   960
      TabIndex        =   3
      Top             =   1560
      Width           =   3135
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   2
      Left            =   960
      TabIndex        =   2
      Top             =   1080
      Width           =   3135
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   1
      Left            =   960
      TabIndex        =   1
      Top             =   600
      Width           =   3135
   End
   Begin VB.TextBox tset 
      Height          =   375
      Index           =   0
      Left            =   960
      TabIndex        =   0
      Top             =   120
      Width           =   3135
   End
   Begin VB.Label lset 
      Caption         =   "JSON.py："
      Height          =   375
      Index           =   5
      Left            =   120
      TabIndex        =   17
      Top             =   2640
      Width           =   735
   End
   Begin VB.Label lset 
      Caption         =   "迅雷："
      Height          =   375
      Index           =   4
      Left            =   120
      TabIndex        =   16
      Top             =   2160
      Width           =   735
   End
   Begin VB.Label lset 
      Caption         =   "MySQL："
      Height          =   375
      Index           =   3
      Left            =   120
      TabIndex        =   15
      Top             =   1680
      Width           =   735
   End
   Begin VB.Label lset 
      Caption         =   "Python："
      Height          =   375
      Index           =   2
      Left            =   120
      TabIndex        =   14
      Top             =   1200
      Width           =   735
   End
   Begin VB.Label lset 
      Caption         =   "HTTP："
      Height          =   375
      Index           =   1
      Left            =   120
      TabIndex        =   13
      Top             =   720
      Width           =   735
   End
   Begin VB.Label lset 
      Caption         =   "目录："
      Height          =   375
      Index           =   0
      Left            =   120
      TabIndex        =   12
      Top             =   240
      Width           =   735
   End
End
Attribute VB_Name = "setform"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub cset_Click(Index As Integer)
    If Index = 0 Then
        cdset.Filter = "配置文件(*.cfg)|*.cfg|所有文件(*.*)|*.*"
    ElseIf Index = 5 Then
        cdset.Filter = "Python脚本(*.py,*.pyc,*.so)|*.py;*.pyc;*.so|所有文件(*.*)|*.*"
    Else
        cdset.Filter = "程序(*.exe)|*.exe|所有文件(*.*)|*.*"
    End If
    
    cdset.FileName = ""
    If tset(Index).Text <> "" Then cdset.FileName = tset(Index).Text
    cdset.ShowOpen
    If Not cdset.FileName = "" Then tset(Index).Text = cdset.FileName
    
End Sub

Private Sub delset_Click()
    For n = 0 To 5
        tset(n).Text = ""
        'AHscan.SaveAry n, ""
    Next n
End Sub


Private Sub lset_Click(Index As Integer)
    If tset(Index).Text = "" Then
        tset(Index).Text = AHscan.GetAry(Index)
    Else
        tset(Index).Text = ""
    End If
End Sub

Private Sub okset_Click()
    For n = 0 To 5
        AHscan.SaveAry n, tset(n).Text
    Next n
    Me.Hide
End Sub
Private Sub exitset_Click()
    Unload Me
End Sub

Private Sub Form_Load()
    For n = 0 To 5
        tset(n).Text = AHscan.GetAry(n)
    Next n
End Sub

Private Sub tset_DblClick(Index As Integer)
    tset(Index).SetFocus
    tset(Index).SelStart = 0
    tset(Index).SelLength = Len(tset(Index).Text)
End Sub
