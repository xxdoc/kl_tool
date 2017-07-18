VERSION 5.00
Object = "{F9043C88-F6F2-101A-A3C9-08002B2F49FB}#1.2#0"; "COMDLG32.OCX"
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.1#0"; "MSCOMCTL.OCX"
Begin VB.Form Form1 
   Caption         =   "Pic by KL"
   ClientHeight    =   5490
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   10500
   LinkTopic       =   "Form1"
   ScaleHeight     =   5490
   ScaleWidth      =   10500
   StartUpPosition =   3  '窗口缺省
   Begin VB.CommandButton runc 
      Caption         =   "Run"
      Height          =   375
      Left            =   8280
      TabIndex        =   27
      Top             =   3240
      Width           =   735
   End
   Begin VB.CheckBox autock 
      Height          =   375
      Left            =   9120
      TabIndex        =   26
      Top             =   3240
      Value           =   1  'Checked
      Width           =   255
   End
   Begin VB.CommandButton Picfx 
      Caption         =   "FenXi"
      Height          =   375
      Left            =   9480
      TabIndex        =   25
      Top             =   3240
      Width           =   735
   End
   Begin VB.CommandButton gofishc 
      Caption         =   "GoFish"
      Height          =   375
      Left            =   8280
      TabIndex        =   24
      Top             =   3720
      Width           =   735
   End
   Begin VB.CommandButton Stopc 
      Caption         =   "Stop"
      Enabled         =   0   'False
      Height          =   375
      Left            =   9480
      TabIndex        =   23
      Top             =   3720
      Width           =   735
   End
   Begin VB.CommandButton Command9 
      Caption         =   "RL"
      Height          =   255
      Left            =   8280
      TabIndex        =   20
      Top             =   2520
      Width           =   375
   End
   Begin VB.CommandButton Command7 
      Caption         =   "<-"
      Height          =   255
      Left            =   9240
      TabIndex        =   19
      Top             =   2520
      Width           =   375
   End
   Begin VB.CommandButton Command8 
      Caption         =   "☆"
      Height          =   255
      Left            =   8760
      TabIndex        =   18
      Top             =   2520
      Width           =   375
   End
   Begin VB.TextBox Text3 
      Height          =   270
      Left            =   9720
      TabIndex        =   16
      Text            =   "128"
      Top             =   2160
      Width           =   495
   End
   Begin MSComctlLib.Slider Slider1 
      Height          =   255
      Left            =   8280
      TabIndex        =   15
      Top             =   2160
      Width           =   1455
      _ExtentX        =   2566
      _ExtentY        =   450
      _Version        =   393216
      LargeChange     =   25
      Min             =   1
      Max             =   255
      SelStart        =   128
      TickFrequency   =   16
      Value           =   128
   End
   Begin VB.CommandButton Command6 
      Caption         =   "Split"
      Height          =   375
      Left            =   9360
      TabIndex        =   14
      Top             =   1680
      Width           =   855
   End
   Begin VB.CommandButton Command5 
      Caption         =   "To Gray"
      Height          =   375
      Left            =   8280
      TabIndex        =   13
      Top             =   1680
      Width           =   855
   End
   Begin VB.CheckBox Check1 
      Caption         =   "Check1"
      Height          =   255
      Left            =   8280
      TabIndex        =   12
      Top             =   1200
      Value           =   1  'Checked
      Width           =   255
   End
   Begin VB.CommandButton Command4 
      Caption         =   "□"
      Height          =   255
      Left            =   9960
      MaskColor       =   &H00FFFFFF&
      TabIndex        =   11
      Top             =   840
      Width           =   255
   End
   Begin VB.CommandButton Command3 
      Caption         =   "■"
      Height          =   255
      Left            =   9600
      TabIndex        =   10
      Top             =   840
      Width           =   255
   End
   Begin VB.CommandButton Command2 
      Caption         =   "Save"
      Height          =   375
      Left            =   9360
      TabIndex        =   9
      Top             =   360
      Width           =   735
   End
   Begin VB.TextBox Text2 
      Height          =   270
      Left            =   9600
      TabIndex        =   6
      Text            =   "20"
      Top             =   1200
      Width           =   615
   End
   Begin VB.TextBox Text1 
      Height          =   270
      Left            =   8520
      TabIndex        =   5
      Text            =   "000000"
      Top             =   1200
      Width           =   855
   End
   Begin VB.PictureBox Picture1 
      Height          =   4695
      Left            =   0
      ScaleHeight     =   4635
      ScaleWidth      =   7755
      TabIndex        =   3
      Top             =   0
      Width           =   7815
      Begin VB.PictureBox Picture2 
         AutoRedraw      =   -1  'True
         AutoSize        =   -1  'True
         Height          =   4695
         Left            =   0
         ScaleHeight     =   4635
         ScaleWidth      =   7755
         TabIndex        =   4
         Top             =   0
         Width           =   7815
      End
   End
   Begin VB.CommandButton Command1 
      Caption         =   "Open"
      Height          =   375
      Left            =   8280
      TabIndex        =   2
      Top             =   360
      Width           =   735
   End
   Begin MSComDlg.CommonDialog CommonDialog1 
      Left            =   8400
      Top             =   4800
      _ExtentX        =   847
      _ExtentY        =   847
      _Version        =   393216
   End
   Begin VB.VScrollBar VScroll1 
      Height          =   4695
      Left            =   7800
      TabIndex        =   1
      Top             =   0
      Width           =   255
   End
   Begin VB.HScrollBar HScroll1 
      Height          =   255
      Left            =   0
      TabIndex        =   0
      Top             =   4680
      Width           =   7815
   End
   Begin VB.Frame dof 
      Caption         =   "处理"
      Height          =   2775
      Left            =   8160
      TabIndex        =   21
      Top             =   120
      Width           =   2175
   End
   Begin VB.Frame runf 
      Caption         =   "运行"
      Height          =   2295
      Left            =   8160
      TabIndex        =   22
      Top             =   3000
      Width           =   2175
   End
   Begin VB.Label statel 
      Height          =   375
      Left            =   120
      TabIndex        =   17
      Top             =   5040
      Width           =   7815
   End
   Begin VB.Label Label2 
      Caption         =   "██"
      ForeColor       =   &H00E0E0E0&
      Height          =   255
      Left            =   9360
      TabIndex        =   8
      Top             =   1200
      Width           =   255
   End
   Begin VB.Label Label1 
      Caption         =   "0,0"
      Height          =   375
      Left            =   8280
      TabIndex        =   7
      Top             =   960
      Width           =   1335
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (Destination As Any, Source As Any, ByVal Length As Long)

Private Type BmpHeaderType
    fill As Integer
    FileTag1 As Byte
    FileTag2 As Byte '0000-0001：文件标识，为字母ASCII码“BM”。
    FileCapacity As Long     '0002-0005：文件大小。
    Reserved As Long '0006-0009：保留，每字节以“00”填写。
    reserved2 As Long '000A-000D：记录图像数据区的起始位置。各字节的信息依次含义为：文件头信息块大小，图像描述信息块的大小，图像颜色表的大小，保留（为01）。
End Type
Private Type BmpBlockDescription
    BmpDescription As Long '000E-0011：图像描述信息块的大小，常为28H。
    BmpWidth As Long     '0012-0015：图像宽度。
    BmpHeight As Long    '0016-0019：图像高度。
    BmpPlane As Integer '01A-001B：图像的plane总数（恒为1）。
    BmpBits As Integer   '001C-001D：记录像素的位数，很重要的数值，图像的颜色数由该值决定。
    DataCompress As Long     '001E-0021：数据压缩方式（数值位0：不压缩；1：8位压缩；2：4位压缩）。
    BmpData As Long      '0022-0025：图像区数据的大小。
    HResolution As Long      '0026-0029：水平每米有多少像素，在设备无关位图（.DIB）中，每字节以00H填写。
    VResolution As Long      '002A-002D：垂直每米有多少像素，在设备无关位图（.DIB）中，每字节以00H填写。
    BmpColors As Long    '002E-0031：此图像所用的颜色数，如值为0，表示所有颜色一样重要。
    Reserved3 As Long    '0032-0035：保留字
End Type

Private Type BmpPalette
    Blue As Byte
    Green As Byte
    Red As Byte
    fill As Byte
End Type

Private Type FromSizeInfo
    from_width As Long
    from_height As Long
    pic_width As Long
    pic_height As Long
    v_left As Long
    h_top As Long
    statel_top As Long
    
    is_fist_load As Boolean
End Type

Dim old_from_size As FromSizeInfo
Dim picw As Long
Dim Bpic() As Byte
Dim ORG() As Byte
Dim BmpHeader As BmpHeaderType, BmpDescription As BmpBlockDescription
Dim pic_file_name As String

Dim colors() As Byte
Dim pix As Byte
Dim b As Byte, g As Byte, r As Byte
Dim dm As New dmsoft
Dim hwow As Long, dm_ret As Long
Dim isbusy As Boolean
Dim base_path As String

Private Sub Check1_Click()
    If Check1.Value = 1 Then
        Text1.Text = Hex$(Text1.Text)
    ElseIf Check1.Value = 0 Then
        Text1.Text = Val("&H" & Text1.Text)
    End If
End Sub

Private Sub Command2_Click()
    On Error GoTo ErrExit
    CommonDialog1.Filter = "BMP (*.bmp)|*.bmp|JPG (*.jpg)|*.jpg|PNG (*.png)|*.png|All File(*.*)|*.*"
    CommonDialog1.FilterIndex = 1
    CommonDialog1.ShowSave
    Picture2.AutoRedraw = True
    SavePicture Picture2.Picture, CommonDialog1.Filename
    Picture2.AutoRedraw = False
ErrExit:
End Sub

Private Sub Command3_Click()
    Call Tobuff(colors, Bpic)

    Dim comp(1, 2) As Long
    Dim vclor As Long
    If Check1.Value = 0 Then
        vclor = Val(Text1.Text)
    ElseIf Check1.Value = 1 Then
        vclor = Val("&H" & Text1.Text)
    End If
    Const ByN As Integer = 256
    Const ByN2 As Long = 65536
    Dim A(2) As Long
    A(0) = (vclor \ ByN2)
    A(1) = ((vclor Mod ByN2) \ ByN)
    A(2) = (vclor Mod ByN)
    For I = 0 To 2
        comp(0, I) = A(I) - Val(Text2.Text)
        If comp(0, I) < 0 Then comp(0, I) = 0
        If comp(0, I) > 255 Then comp(0, I) = 255
        comp(1, I) = A(I) + Val(Text2.Text)
        If comp(1, I) < 0 Then comp(1, I) = 0
        If comp(1, I) > 255 Then comp(1, I) = 255
    Next I

    Dim indexp As Long
    indexp = 0
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            If colors(indexp) >= comp(0, 0) And colors(indexp) <= comp(1, 0) _
               And colors(indexp + 1) >= comp(0, 1) And colors(indexp + 1) <= comp(1, 1) _
               And colors(indexp + 2) >= comp(0, 2) And colors(indexp) <= comp(1, 2) Then
                colors(indexp) = 0
                colors(indexp + 1) = 0
                colors(indexp + 2) = 0
            End If
        Next j
    Next I

    Call Frombuff(colors, Bpic)

End Sub

Private Sub Command4_Click()
    Call Tobuff(colors, Bpic)

    Dim comp(1, 2) As Long
    Dim vclor As Long
    If Check1.Value = 0 Then
        vclor = Val(Text1.Text)
    ElseIf Check1.Value = 1 Then
        vclor = Val("&H" & Text1.Text)
    End If
    Const ByN As Integer = 256
    Const ByN2 As Long = 65536
    Dim A(2) As Long
    A(0) = (vclor \ ByN2)
    A(1) = ((vclor Mod ByN2) \ ByN)
    A(2) = (vclor Mod ByN)
    For I = 0 To 2
        comp(0, I) = A(I) - Val(Text2.Text)
        If comp(0, I) < 0 Then comp(0, I) = 0
        If comp(0, I) > 255 Then comp(0, I) = 255
        comp(1, I) = A(I) + Val(Text2.Text)
        If comp(1, I) < 0 Then comp(1, I) = 0
        If comp(1, I) > 255 Then comp(1, I) = 255
    Next I

    Dim indexp As Long

    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            If colors(indexp) >= comp(0, 0) And colors(indexp) <= comp(1, 0) _
               And colors(indexp + 1) >= comp(0, 1) And colors(indexp + 1) <= comp(1, 1) _
               And colors(indexp + 2) >= comp(0, 2) And colors(indexp) <= comp(1, 2) Then
                colors(indexp) = 255
                colors(indexp + 1) = 255
                colors(indexp + 2) = 255
            End If
        Next j
    Next I

    Call Frombuff(colors, Bpic)

End Sub

Private Sub Command5_Click()
    Call Tobuff(colors, Bpic)
    'ReDim Preserve colors(BmpDescription.BmpHeight, BmpDescription.BmpWidth, 3)
    Dim temp As Integer
    Dim indexp As Long
    temp = 0
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            temp = colors(indexp) \ 3 + colors(indexp + 1) \ 3 + colors(indexp + 2) \ 3

            colors(indexp) = temp
            colors(indexp + 1) = temp
            colors(indexp + 2) = temp

        Next j
    Next I

    Call Frombuff(colors, Bpic)

End Sub

Private Sub Command6_Click()
    Call Tobuff(colors, Bpic)

    Dim temp As Byte
    Dim sv As Byte
    Dim indexp As Long
    sv = Slider1.Value
    temp = 0
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3

            If colors(indexp) < sv Then
                temp = 0
            Else
                temp = 255
            End If

            colors(indexp) = temp
            colors(indexp + 1) = temp
            colors(indexp + 2) = temp

        Next j
    Next I

    Call Frombuff(colors, Bpic)
End Sub

Private Sub Command7_Click()
    Call Frombuff(ORG, Bpic)
End Sub

Private Sub Command8_Click()
    Call Tobuff(colors, Bpic)
    ReDim ORG(BmpDescription.BmpData) As Byte
    CopyMemory ByVal VarPtr(ORG(0)), ByVal VarPtr(Bpic(112)), BmpDescription.BmpData
End Sub

Private Sub Command9_Click()
    Picture2.Picture = LoadPicture(pic_file_name)
End Sub

Public Sub ResizeInit(FormName As Form)
    Dim Obj As Control
    FormOldWidth = FormName.ScaleWidth
    FormOldHeight = FormName.ScaleHeight
    On Error Resume Next
    '保存
    For Each Obj In FormName
        Obj.Tag = Obj.Left
    Next Obj

    old_from_size.from_width = FormName.Width:: old_from_size.from_height = FormName.Height
    
    old_from_size.pic_width = Picture1.Width:: old_from_size.pic_height = Picture1.Height
    
    old_from_size.v_left = VScroll1.Left
    old_from_size.h_top = HScroll1.Top
    old_from_size.statel_top = statel.Top
    
    old_from_size.is_fist_load = False
 End Sub
 
Private Sub Form_Load()
    isbusy = False
    base_path = dm.GetBasePath()
    dm_ret = dm.SetShowErrorMsg(0)
    dm_ret = dm.SetPath(base_path)
    dm_ret = dm.SetDict(0, "dm_soft.txt")
    Picture2.Left = 0
    Picture2.Top = 0
    Picture2.Width = Picture1.Width
    Picture2.Height = Picture1.Height
    VScroll1.min = 0
    HScroll1.min = 0
    HScroll1.min = 0
    VScroll1.max = Picture2.Height - Picture1.Height
    HScroll1.max = Picture2.Width - Picture1.Width

    If HScroll1.max < 0 Then HScroll1.Enabled = False
    If VScroll1.max < 0 Then VScroll1.Enabled = False
    Command1.TabIndex = 0

    Command2.Enabled = False
    Command3.Enabled = False
    Command4.Enabled = False
    Command5.Enabled = False
    Command6.Enabled = False
    Command7.Enabled = False
    Command8.Enabled = False
    Command9.Enabled = False
    
    ResizeInit Me
    
    statel.Caption = "ready!"
End Sub
Private Sub Command1_Click()
    On Error GoTo ErrExit
    CommonDialog1.Filter = "所有图片文件(*.jpg;*.bmp;*.png) |*.jpg;*.bmp;*.png|BMP (*.bmp)|*.bmp|JPG (*.jpg)|*.jpg|PNG (*.png)|*.png|All File(*.*)|*.*"
    CommonDialog1.FilterIndex = 1
    CommonDialog1.ShowOpen
    If CommonDialog1.Filename = "" Then Exit Sub
    
    pic_file_name = CommonDialog1.Filename
    Picture2.Picture = LoadPicture(pic_file_name)
    
    VScroll1.min = 0
    HScroll1.min = 0
    VScroll1.max = Picture2.Height - Picture1.Height
    HScroll1.max = Picture2.Width - Picture1.Width
    HScroll1.Enabled = True
    VScroll1.Enabled = True
    If HScroll1.max <= 0 Then HScroll1.Enabled = False
    If VScroll1.max <= 0 Then VScroll1.Enabled = False
    If HScroll1.Enabled Then HScroll1.SmallChange = Int(HScroll1.max / 10 + 0.5) + 1
    If VScroll1.Enabled Then VScroll1.SmallChange = Int(VScroll1.max / 10 + 0.5) + 1

    Call Tobuff(colors, Bpic)
    
    ReDim ORG(BmpDescription.BmpData) As Byte
    CopyMemory ByVal VarPtr(ORG(0)), ByVal VarPtr(Bpic(112)), BmpDescription.BmpData

    Command2.Enabled = True
    Command3.Enabled = True
    Command4.Enabled = True
    Command5.Enabled = True
    Command6.Enabled = True
    Command7.Enabled = True
    Command8.Enabled = True
    Command9.Enabled = True
    
    statel.Caption = "open:" & pic_file_name & " (" & BmpDescription.BmpWidth & "," & BmpDescription.BmpHeight & ")"
    
ErrExit:
End Sub

Private Sub Form_Resize()

    Dim pic_w As Long, pic_h As Long
    
    If old_from_size.is_fist_load = True Then Exit Sub
    
    pic_w = old_from_size.pic_width + Me.Width - old_from_size.from_width
    pic_h = old_from_size.pic_height + Me.Height - old_from_size.from_height
    If pic_w < 1000 Then
        Me.Width = old_from_size.from_width + 1000 - old_from_size.pic_width
        pic_w = 1000
    End If
    If pic_h < 2000 Then
        Me.Height = old_from_size.from_height + 2000 - old_from_size.pic_height
        pic_h = 2000
    End If
    
    For Each Obj In Me
        On Error GoTo NextObj
            If Obj.Tag > 0 Then Obj.Left = Obj.Tag - old_from_size.pic_width + pic_w
NextObj:
    Next Obj
     
    Picture1.Width = pic_w:: Picture1.Height = pic_h
    If pic_file_name = "" Then Picture2.Width = pic_w::  Picture2.Height = pic_h
    VScroll1.Left = old_from_size.v_left - old_from_size.pic_width + pic_w::    VScroll1.Height = pic_h
    HScroll1.Top = old_from_size.h_top - old_from_size.pic_height + pic_h::    HScroll1.Width = pic_w
    statel.Top = old_from_size.statel_top - old_from_size.pic_height + pic_h::    statel.Width = pic_w
    
    
    VScroll1.min = 0
    HScroll1.min = 0
    VScroll1.max = Picture2.Height - Picture1.Height
    HScroll1.max = Picture2.Width - Picture1.Width
    HScroll1.Enabled = True
    VScroll1.Enabled = True
    If HScroll1.max <= 0 Then HScroll1.Enabled = False
    If VScroll1.max <= 0 Then VScroll1.Enabled = False
    If HScroll1.Enabled Then HScroll1.SmallChange = Int(HScroll1.max / 10 + 0.5) + 1
    If VScroll1.Enabled Then VScroll1.SmallChange = Int(VScroll1.max / 10 + 0.5) + 1
    
    ResizeInit Me
     
End Sub

Private Sub gofishc_Click()
    If isbusy = True Then Exit Sub
    If autock.Value = 0 Then
        answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
        If answer = vbNo Then Exit Sub
        PauseTime 2000
        hwow = dm.GetMousePointWindow()
    Else
        hwow = dm.FindWindow("GxWindowClass", "魔兽世界")
    End If
    If hwow = 0 Then Exit Sub Else dm_ret = dm.BindWindow(hwow, "dx", "windows", "windows", 0)
    If dm_ret = 1 Then Else MsgBox "绑定错误，错误： " & CStr(dm.GetLastError):: Exit Sub
    isbusy = True
    Me.Enabled = False
    Stopc.Enabled = True
    dm_ret = dm.GetClientSize(hwow, w, h)

End Sub
Private Sub starfish()
    dm.KeyPressChar "1"
    PauseTime 2000
    dm_ret = dm.Capture(w \ 4, h * 2 \ 12, w * 3 \ 4, h * 5 \ 12, "wowfish.bmp")
    PauseTime 500
    Picture2.Picture = LoadPicture(base_path & "\" & "wowfish.bmp")
    VScroll1.min = 0
    HScroll1.min = 0
    VScroll1.max = Picture2.Height - Picture1.Height
    HScroll1.max = Picture2.Width - Picture1.Width
    If HScroll1.max < 0 Then HScroll1.Enabled = False
    If VScroll1.max < 0 Then VScroll1.Enabled = False
    Call Tobuff(colors, Bpic)
    Dim temp As Integer, max As Integer, min As Integer
    Dim indexp As Long, minx As Long, miny As Long
    max = 0

    min = 255
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            temp = colors(indexp) \ 3 + colors(indexp + 1) \ 3 + colors(indexp + 2) \ 3
            If temp > max Then max = temp
            If temp < min Then min = temp:: minx = j:: miny = I
        Next j
    Next I

End Sub
Private Sub HScroll1_Change()
    Picture2.Left = -HScroll1.Value
End Sub

Private Sub Slider1_Change()
    Text3.Text = Slider1.Value
End Sub

Private Sub Text3_Change()
    Dim snum As Long
    snum = Int(Val(Text3.Text))
    If snum > 0 Or snum < 256 Then
        Slider1.Value = snum
    End If
End Sub

Private Sub VScroll1_Change()
    Picture2.Top = -VScroll1.Value
End Sub
Private Sub Picture2_MouseDown(Button As Integer, Shift As Integer, x As Single, y As Single)
    If Button = 1 And Shift = 1 Then
        Label1.Caption = x / 15 & "," & y / 15
        picColor = Picture2.Point(x, y)
        Label2.ForeColor = picColor
        Text1.Text = picColor
        If Check1.Value = 1 Then
            Text1.Text = Hex$(Text1.Text)
        End If

    End If
End Sub
Private Sub runc_Click()
    If isbusy = True Then Exit Sub
    If autock.Value = 0 Then
        answer = MsgBox("2秒后绑定至指向窗口", vbYesNo)
        If answer = vbNo Then Exit Sub
        PauseTime 2000
        hwow = dm.GetMousePointWindow()
    Else
        hwow = dm.FindWindow("GxWindowClass", "魔兽世界")
    End If
    If hwow = 0 Then Exit Sub Else dm_ret = dm.BindWindow(hwow, "dx", "windows", "windows", 0)
    If dm_ret = 1 Then Else MsgBox "绑定错误，错误： " & CStr(dm.GetLastError):: Exit Sub
    dm_ret = dm.GetClientSize(hwow, w, h)
    dm_ret = dm.Capture(w \ 4, h \ 12, w * 3 \ 4, h * 5 \ 12, "wowfish.bmp")
    
    Picture2.Picture = LoadPicture(base_path & "\" & "wowfish.bmp")
    VScroll1.min = 0
    HScroll1.min = 0
    VScroll1.max = Picture2.Height - Picture1.Height
    HScroll1.max = Picture2.Width - Picture1.Width
    If HScroll1.max < 0 Then HScroll1.Enabled = False
    If VScroll1.max < 0 Then VScroll1.Enabled = False

    Call Tobuff(colors, Bpic)
    ReDim ORG(BmpDescription.BmpHeight * BmpDescription.BmpWidth * 3) As Byte
    CopyMemory ByVal VarPtr(ORG(0)), ByVal VarPtr(Bpic(112)), BmpDescription.BmpHeight * BmpDescription.BmpWidth * 3


    dm_ret = dm.UnBindWindow()
    If dm_ret Then
    Else
        Filelog "解除绑定错误，错误： " & CStr(dm.GetLastError)
        answer = MsgBox("解除绑定错误", vbYesNo)
    End If
End Sub
Private Sub Picfx_Click()
    Call Tobuff(colors, Bpic)
    'ReDim Preserve colors(BmpDescription.BmpHeight, BmpDescription.BmpWidth, 3)
    Dim temp As Integer, max As Integer, min As Integer
    Dim indexp As Long, countc As Long, counts As Long, minx As Long, miny As Long
    counts = 0

    countc = 0
    temp = 0
    max = 0

    min = 255
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            temp = colors(indexp) \ 3 + colors(indexp + 1) \ 3 + colors(indexp + 2) \ 3
            If temp > max Then max = temp
            If temp < min Then min = temp:: minx = j:: miny = I
            countc = countc + temp
        Next j
        counts = counts + Round(countc / BmpDescription.BmpWidth)
        countc = 0
    Next I
    counts = Round(counts / BmpDescription.BmpHeight)
    statel.Caption = "AVG:" & CStr(counts) & "  Max:" & CStr(max) & "  MIN:" & CStr(min) & "  xy " & minx & "-" & BmpDescription.BmpHeight - miny
    erzhi min + 30
End Sub
Function erzhi(split As Long) As Boolean
    Call Tobuff(colors, Bpic)
    Dim temp As Byte
    Dim sv As Byte
    Dim indexp As Long
    sv = split
    temp = 0
    For I = 0 To BmpDescription.BmpHeight - 1
        For j = 0 To BmpDescription.BmpWidth - 1
            indexp = I * picw + j * 3
            If colors(indexp) < sv Then
                temp = 0
            Else
                temp = 255
            End If
            colors(indexp) = temp
            colors(indexp + 1) = temp
            colors(indexp + 2) = temp
        Next j
    Next I
    Call Frombuff(colors, Bpic)
End Function

Function Tobuff(col() As Byte, abc() As Byte) '图片保存到数组
    Dim PBag As New PropertyBag
    PBag.WriteProperty "Picture", Picture2.Picture, vbNullString
    '读取Picture1.Picture 图片并写到 Pbag 容器中
    abc = PBag.Contents '获取容器Byte 到 数组中
    '这时 数组B 就时我们想要获得的图像字节数组
    CopyMemory ByVal VarPtr(BmpHeader), ByVal VarPtr(abc(56)), 16
    CopyMemory ByVal VarPtr(BmpDescription), ByVal VarPtr(abc(72)), Len(BmpDescription)
    'BmpDescription.BmpWidth = Round(BmpDescription.BmpWidth / 4) * 4
    
    picw = BmpDescription.BmpData / BmpDescription.BmpHeight
    ReDim col(BmpDescription.BmpData) As Byte

    CopyMemory ByVal VarPtr(col(0)), ByVal VarPtr(abc(112)), BmpDescription.BmpData

End Function

Function Frombuff(col() As Byte, abc() As Byte)  '从数组读取图片

    CopyMemory ByVal VarPtr(abc(112)), ByVal VarPtr(col(0)), BmpDescription.BmpData
    Dim PBag As New PropertyBag
    PBag.Contents = abc  '数组内容返回Pbag 容器
    Set Picture2.Picture = PBag.ReadProperty("Picture")  '从容器恢复图片
End Function
