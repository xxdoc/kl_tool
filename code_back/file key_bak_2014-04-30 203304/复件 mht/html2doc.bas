Attribute VB_Name = "html2doc"

Public Function html2docex(opendir As String, savedir As String) As Boolean
On Error Resume Next
 
Dim strTitle As String, strWord
Dim nn As Long, keys As Long, fin As Long
Dim MyName() As String
Dim wrd
Set wrd = CreateObject("Word.Application")
wrd.Visible = False
wrd.application.Activate
Dim fs As Object

Set fs = application.FileSearch

With fs
.LookIn = opendir '设置要查找的起始目录
.FileType = msoFileTypeWebPages  'msoFileTypeExcelWorkbooks 要查找的文件类型
.SearchSubFolders = True '是否查找子目录
.Execute '根据上面的设置执行查找
End With
ReDim MyName(1 To fs.FoundFiles.Count)

For fin = 1 To fs.FoundFiles.Count

If fin > 3 Then Kill (fs.FoundFiles(fin - 2))

 MyName(fin) = fs.FoundFiles(fin)  '遍历打开找到的文件
'MyName(i)  输入
'MyName(i) = "kk (" & CStr(i) & ").doc"
'ChangeFileOpenDirectory (opendir)

Documents.Open FileName:=MyName(fin), _
ConfirmConversions:=False, ReadOnly:=False, AddToRecentFiles:=False, _
PasswordDocument:="", PasswordTemplate:="", Revert:=False, _
WritePasswordDocument:="", WritePasswordTemplate:="", Format:= _
wdOpenFormatAuto, XMLTransform:=""

    strTitle = ""
    strTitle = ""
     If (ActiveDocument.Words.Count > 48) Then
     Dim enter As Long, ii As Long
     enter = 0
         For ii = 48 To ActiveDocument.Words.Count
             strWord = ActiveDocument.Words.Item(ii)
             keys = Asc(strWord)
             If keys = 13 And strTitle <> "" Then
                   Exit For
             End If
          If keys <> 13 And keys <> 63 And keys <> -24159 Then
              If strTitle = "" Then
                  If keys < 0 Or keys > 32 Then strTitle = strTitle + strWord
              Else
                  strTitle = strTitle + strWord
              End If
              If (Len(strTitle) > 100) Then Exit For
          End If
         Next ii
     Else
          strTitle = "kk (" & CStr(fin) & ")"
     End If

'MyName(i) 输出  wdFormatWebArchive  mht格式  wdFormatDocument  doc格式
GetTitle = Replace(strTitle, vbCrLf, "")
MyName(fin) = GetTitle & ".doc"

ChangeFileOpenDirectory (savedir)


'把插入的网页链接形式的图片转为内嵌图片保存在word中
Dim i As InlineShape, j As Shape, N As Long

application.ScreenUpdating = False '关闭屏幕刷新
For Each i In ActiveDocument.InlineShapes '遍历所有插入的InlineShape图形对象
    If i.Type = wdInlineShapeLinkedPicture Then
        i.LinkFormat.SavePictureWithDocument = True
        i.LinkFormat.BreakLink '断开源文件与指定图片之间的链接
        N = N + 1 '计数
    End If
Next i
For Each j In ActiveDocument.Shapes '遍历所有插入的Shape图形对象
    If j.Type = msoLinkedPicture Then
        j.LinkFormat.SavePictureWithDocument = True
        j.LinkFormat.BreakLink '断开源文件与指定图片之间的链接。
        N = N + 1 '计数
    End If
Next j
'MsgBox "共转换了链接图片" & N & "个!"
'Application.ScreenUpdating = True '恢复屏幕刷新

ActiveDocument.SaveAs FileName:=MyName(fin), FileFormat:= _
wdFormatDocument, LockComments:=False, Password:="", AddToRecentFiles:= _
True, WritePassword:="", ReadOnlyRecommended:=False, EmbedTrueTypeFonts:= _
False, SaveNativePictureFormat:=False, SaveFormsData:=False, _
SaveAsAOCELetter:=False

ActiveWindow.Close

Next fin

End Function


'Microsoft.Office.Interop.Word.WdSaveFormat是个枚举，它的定义如下，
'其中没有wdFormatDocumentDefault，你是不是多写了Default：
'wdFormatDocument
'wdFormatDOSText
'wdFormatDOSTextLineBreaks
'wdFormatEncodedText
'wdFormatFilteredHTML
'wdFormatHTML
'wdFormatRTF
'wdFormatTemplate
'wdFormatText
'wdFormatTextLineBreaks
'wdFormatUnicodeText
'wdFormatWebArchive
'wdFormatXML



