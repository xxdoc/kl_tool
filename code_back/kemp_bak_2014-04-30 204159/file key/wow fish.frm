VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "WOW Auto Fish"
   ClientHeight    =   3090
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   ScaleHeight     =   3090
   ScaleWidth      =   4680
   StartUpPosition =   3  '窗口缺省
   Begin VB.PictureBox Picture1 
      Height          =   2415
      Left            =   120
      ScaleHeight     =   2355
      ScaleWidth      =   3195
      TabIndex        =   1
      Top             =   120
      Width           =   3255
   End
   Begin VB.CommandButton runc 
      Caption         =   "Run"
      Height          =   375
      Left            =   3480
      TabIndex        =   0
      Top             =   240
      Width           =   735
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim dm As dmsoft
Dim hwow As Long
Dim isbusy As Boolean


Private Sub Form_Load()
    isbusy = False
    base_path = dm.GetBasePath()
    dm_ret = dm.SetShowErrorMsg(0)
    dm_ret = dm.SetPath(base_path)
    dm_ret = dm.SetDict(0, "dm_soft.txt")
End Sub

Private Sub runc_Click()
    If isbusy = True Then Exit Sub
    answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
    If answer = vbNo Then Exit Sub
    PauseTime 2000
    hwow = dm.GetMousePointWindow()
    If hwow = 0 Then Exit Sub Else dm_ret = dm.BindWindow(hwow, "dx", "windows", "windows", 0)
    If dm_ret = 1 Then Else MsgBox "绑定错误，错误： " & CStr(dm.GetLastError):: Exit Sub
    dm_ret = dm.GetClientSize(hwow, w, h)
    dm_ret = dm.Capture(w \ 4, h \ 12, w * 3 \ 4, h * 5 \ 12, "screen.bmp")

      
End Sub
