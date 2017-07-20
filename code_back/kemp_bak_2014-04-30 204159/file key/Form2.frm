VERSION 5.00
Begin VB.Form Form2 
   Caption         =   "帐号设置"
   ClientHeight    =   1965
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   4230
   LinkTopic       =   "Form2"
   ScaleHeight     =   1965
   ScaleWidth      =   4230
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton esc 
      Caption         =   "取消"
      Height          =   375
      Left            =   3360
      TabIndex        =   4
      Top             =   840
      Width           =   735
   End
   Begin VB.CommandButton ok 
      Caption         =   "确认"
      Height          =   375
      Left            =   3360
      TabIndex        =   3
      Top             =   240
      Width           =   735
   End
   Begin VB.TextBox pass2 
      Height          =   375
      IMEMode         =   3  'DISABLE
      Left            =   720
      PasswordChar    =   "*"
      TabIndex        =   2
      Top             =   1200
      Width           =   2415
   End
   Begin VB.TextBox pass1 
      Height          =   375
      IMEMode         =   3  'DISABLE
      Left            =   720
      PasswordChar    =   "*"
      TabIndex        =   1
      Top             =   720
      Width           =   2415
   End
   Begin VB.TextBox user 
      Height          =   375
      Left            =   720
      TabIndex        =   0
      Top             =   240
      Width           =   2415
   End
   Begin VB.Label Label4 
      Caption         =   "注意：使用此功能可能会导致丢失账号！"
      Height          =   255
      Left            =   120
      TabIndex        =   9
      Top             =   1680
      Width           =   3375
   End
   Begin VB.Label state 
      Height          =   255
      Left            =   3240
      TabIndex        =   8
      Top             =   1320
      Width           =   1095
   End
   Begin VB.Label Label3 
      Caption         =   "确认："
      Height          =   255
      Left            =   120
      TabIndex        =   7
      Top             =   1320
      Width           =   615
   End
   Begin VB.Label Label2 
      Caption         =   "密码："
      Height          =   255
      Left            =   120
      TabIndex        =   6
      Top             =   840
      Width           =   735
   End
   Begin VB.Label Label1 
      Caption         =   "帐号："
      Height          =   375
      Left            =   120
      TabIndex        =   5
      Top             =   360
      Width           =   615
   End
End
Attribute VB_Name = "Form2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub esc_Click()
Unload Me
End Sub
Private Sub Form_Load()
user.Text = Form1.user
pass1.Text = Form1.pass
pass2.Text = Form1.pass
End Sub
Private Sub Form_Unload(Cancel As Integer)
Form1.Show
End Sub

Private Sub ok_Click()
state.Caption = ""
If pass1.Text = pass2.Text And user.Text <> "" And pass1.Text <> "" Then
Form1.user = user.Text
Form1.pass = pass1.Text
Form1.autorun.Value = 1
Form1.restart.Value = 1
Unload Me
Else
pass1.Text = ""
pass2.Text = ""
state.Caption = "密码不一致"
End If
End Sub
