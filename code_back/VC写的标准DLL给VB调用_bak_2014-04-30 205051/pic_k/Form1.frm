VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   2400
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   3990
   LinkTopic       =   "Form1"
   ScaleHeight     =   2400
   ScaleWidth      =   3990
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton Command6 
      Caption         =   "Command6"
      Height          =   495
      Left            =   360
      TabIndex        =   5
      Top             =   1560
      Width           =   1215
   End
   Begin VB.CommandButton Command5 
      Caption         =   "Command5"
      Height          =   495
      Left            =   360
      TabIndex        =   4
      Top             =   960
      Width           =   1215
   End
   Begin VB.CommandButton Command4 
      Caption         =   "Command4"
      Height          =   495
      Left            =   360
      TabIndex        =   3
      Top             =   360
      Width           =   1215
   End
   Begin VB.CommandButton Command1 
      Caption         =   "Command1"
      Height          =   495
      Left            =   2040
      TabIndex        =   2
      Top             =   360
      Width           =   1215
   End
   Begin VB.CommandButton Command3 
      Caption         =   "getString"
      Height          =   495
      Left            =   2040
      TabIndex        =   1
      Top             =   1560
      Width           =   1215
   End
   Begin VB.CommandButton Command2 
      Caption         =   "addString"
      Height          =   495
      Left            =   2040
      TabIndex        =   0
      Top             =   960
      Width           =   1215
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub Command1_Click()
    Dim a As String
    a = "11111111111111111111111111111111111"
    setStr (a)
End Sub

Private Sub Command2_Click()
    setStr ("这样就不会发生名字改编")
End Sub

Private Sub Command3_Click()
    Dim a As String
    a = "22222222222222222222222222222222222222222222222222222222222222"
    getStr (a)
    MsgBox a
    MsgBox getLen()
End Sub

Private Sub Command4_Click()
    MsgBox GET_DLL_VER_CODE()
    MsgBox GET_DLL_OK_CODE()
    MsgBox GET_DLL_ERROR_CODE()
    MsgBox GET_DLL_MAX_BUFFER_SIZE()
End Sub

Private Sub Command5_Click()
    MsgBox TEST_DLL(12, 34)
End Sub

Private Sub Command6_Click()
    setStr 123
    Dim a As String
    a = "22222222222222222222222222222222222222222222222222222222222222"
    getStr (a)
    MsgBox a
        MsgBox getLen()
End Sub
