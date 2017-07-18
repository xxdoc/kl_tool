VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   3090
   ClientLeft      =   165
   ClientTop       =   855
   ClientWidth     =   4680
   LinkTopic       =   "Form1"
   ScaleHeight     =   3090
   ScaleWidth      =   4680
   StartUpPosition =   3  '窗口缺省
   Begin VB.Menu m_syso 
      Caption         =   "托盘"
      WindowList      =   -1  'True
      Begin VB.Menu m_sys 
         Caption         =   "关于(&O)"
         Index           =   0
         Shortcut        =   ^O
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   1
      End
      Begin VB.Menu m_sys 
         Caption         =   "最小(&E)"
         Index           =   2
         Shortcut        =   ^E
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   3
      End
      Begin VB.Menu m_sys 
         Caption         =   "还原(&R)"
         Index           =   4
         Shortcut        =   ^D
      End
      Begin VB.Menu m_sys 
         Caption         =   "-"
         Index           =   5
      End
      Begin VB.Menu m_sys 
         Caption         =   "退出(&T)"
         Index           =   6
         Shortcut        =   ^T
      End
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
'窗体代码:
Private MinFlag As Boolean

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
    l = x \ 15
'    Form1.Caption = Button & "  " & Shift & "  " & x & "  " & y & "   " & l

    '点击通知栏图标，用鼠标右键时调出弹出菜单

    Select Case l
        Case WM_LBUTTONDOWN:    showfrm
        Case WM_RBUTTONDOWN:    Me.PopupMenu m_syso
    End Select
         
    '点击通知栏图标，用鼠标左键时，将通知栏图标改为另外的图标
'
End Sub

Private Sub m_sys_Click(Index As Integer)
    Select Case Index
        Case 0:
            MsgBox "大漠插件实现，业余按键。"
        Case 2:
            If MinFlag = False Then
                MinFlag = True
                Me.Visible = False '隐藏窗口
                '将窗口图标加入通知栏
                Call Icon_Add(Me.hWnd, Me.Caption, Me.Icon, 0)
            End If
        Case 4: '当单击"还原"菜单时
            If MinFlag = True Then
                showfrm
            End If
        Case 6: '当单击"退出"菜单时
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


