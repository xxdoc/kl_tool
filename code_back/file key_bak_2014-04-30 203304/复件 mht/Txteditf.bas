Attribute VB_Name = "Txteditf"
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

Private Declare Function DeleteUrlCacheEntry Lib "wininet" Alias "DeleteUrlCacheEntryA" (ByVal lpszUrlName As String) As Long
Private Declare Function PathFileExists Lib "shlwapi.dll" Alias "PathFileExistsA" (ByVal pszPath As String) As Long
Private Declare Function SetWindowPos Lib "user32" (ByVal hWnd As Long, ByVal hWndInstrtAfter As Long, ByVal X As Long, ByVal Y As Long, ByVal cx As Long, ByVal cy As Long, ByVal wFlags As Long) As Long
Private Declare Function SendMessage Lib "user32" Alias "SendMessageA" (ByVal hWnd As Long, ByVal wMsg As Long, ByVal wParam As Long, lParam As Any) As Long
Private Declare Function ReleaseCapture Lib "user32" () As Long
Private Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long

Public Function DownloadFile(Url As String, LocalFilename As String, ReWrite As Long) As Boolean
If Url = "" Or LocalFilename = "" Then DownloadFile = False:: Exit Function
If PathFileExists(LocalFilename) And ReWrite = 1 Then DownloadFile = True:: Exit Function

strDir = Mid$(LocalFilename, 1, InStrRev(LocalFilename, "\", -1, vbTextCompare) - 1)
strSaveDir = Mid$(LocalFilename, 1, InStr(4, LocalFilename, "\", vbTextCompare) - 1)
If PathFileExists(strSaveDir) = 0 Then
While strDir <> strSaveDir
    If PathFileExists(strSaveDir) = 0 Then MkDir (strSaveDir)
    If InStr(Len(strSaveDir) + 2, LocalFilename, "\", vbTextCompare) Then strSaveDir = Mid$(LocalFilename, 1, InStr(Len(strSaveDir) + 2, LocalFilename, "\", vbTextCompare) - 1)
Wend
If PathFileExists(strSaveDir) = 0 Then MkDir (strSaveDir)
End If

Dim lngRetVal As Long
lngRetVal = URLDownloadToFile(0, Url, LocalFilename, 0, 0)
If lngRetVal = 0 Then
    DownloadFile = True
    DeleteUrlCacheEntry Url 'Çå³ý»º´æ
End If
End Function


Public Function UrltoDir(Url As String, Dir As String) As String
If Url = "" Or Dir = "" Then Exit Function

If Right$(Dir, 1) = "\" Then Dir = Mid$(Dir, 1, Len(Text3.Text) - 1)

strDir = Url
If InStr(1, LCase(strDir), "http:", vbTextCompare) Then
    strDir = Mid$(strDir, 8)
Else
    UrltoDir = "error!"
    Exit Function
End If

If InStr(1, strDir, "@", vbTextCompare) Then strDir = Mid$(strDir, InStr(1, strDir, "@", vbTextCompare) + 1)
If Right$(strDir, 1) = "/" Then strDir = Mid$(strDir, 1, Len(strDir) - 1)
If Right$(strDir, 1) = "." Then strDir = Mid$(strDir, 1, Len(strDir) - 1)

If InStrRev(strDir, "/", -1, vbTextCompare) Then
    FileName = Mid$(strDir, InStrRev(strDir, "/", -1, vbTextCompare) + 1)
Else
    FileName = "index.html"
End If


If InStr(1, strDir, "/", vbTextCompare) Then strDir = Replace(Mid$(strDir, 1, InStrRev(strDir, "/", -1, vbTextCompare) - 1), "/", "\")
strSaveDir = Dir & "\" & strDir
If InStrRev(FileName, ".", -1, vbTextCompare) Then
strDir = Mid$(FileName, InStrRev(FileName, ".", -1, vbTextCompare) + 1)
Else
FileName = FileName & ".html"
strDir = "html"
End If

'If StrComp(strDir, "html", vbTextCompare) <> 0 And StrComp(strDir, "htm", vbTextCompare) <> 0 Then
' Svar = MsgBox(strDir & "--The file is other type ,Download or Rename as html ?", vbYesNo + vbQuestion, "Net Downter 1.0")
' If Svar = vbYes Then
'  ElseIf Svar = vbNo Then
'  fileName = Mid$(fileName, 1, InStrRev(fileName, ".", -1, vbTextCompare) - 1) & ".html"
'  Else
'   Exit Function
' End If
' End If
UrltoDir = strSaveDir & "\" & FileName
End Function


Function opentxt(FileName As String) As String
    On Error GoTo NotExist
    Dim i As Integer, s As String, BB() As Byte
    If Dir(FileName) = "" Then Exit Function
    i = FreeFile
    ReDim BB(FileLen(FileName) - 1)
    Open FileName For Binary As #i
    Get #i, , BB
    Close #i
    s = StrConv(BB, vbUnicode)
    opentxt = s
NotExist:
End Function

Public Function savetxt(strtxt As String, FileName As String) As Boolean
    On Error GoTo NotExist
    Open FileName For Output As #1
    Print #1, strtxt
    Close #1
    savetxt = True
NotExist:
End Function

Public Function Filelog(strlog As String) As Boolean
    On Error GoTo NotExist
    Open "fish_log.log" For Append As #1
    Print #1, Format$(Now, "c") & "  : " & strlog
    Close #1
    Filelog = True
NotExist:
End Function

Public Function Filelong(FileName As String) As Long
    Filelong = -1
    On Error GoTo NotExist
    Filelong = FileLen(FileName)
    Exit Function
NotExist:
End Function

Function FileExist(FileName As String) As Boolean
    Dim Fso As New FileSystemObject
    If Fso.FileExists(FileName) = True Then FileExist = True Else FileExist = False
    Set Fso = Nothing
End Function

Function FolderExist(foldername As String) As Boolean
    Dim Fso As New FileSystemObject
    If Fso.FolderExists(foldername) = True Then FolderExist = True Else FolderExist = False
    Set Fso = Nothing
End Function

Public Function FileIsR(FileName As String) As Boolean
    Dim objWMIService, colProcessList, objProcess
    If InStrRev(FileName, "\", -1, vbTextCompare) Then FileName = Mid$(FileName, InStrRev(FileName, "\", -1, vbTextCompare) + 1)
    FileIsR = False
    Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
    Set colProcessList = objWMIService.ExecQuery _
    ("Select * from Win32_Process Where Name='" & FileName & "'")
    For Each objProcess In colProcessList
        FileIsR = True
    Exit For
    Next
End Function

Function GetWindir()
    Dim Fso As New FileSystemObject
    GetWindir = Fso.GetSpecialFolder(WindowsFolder)
    Set Fso = Nothing
End Function

Function GetWinSysdir()
    Dim Fso As New FileSystemObject
    GetWinSysdir = Fso.GetSpecialFolder(SystemFolder)
    Set Fso = Nothing
End Function


Public Function PauseTime(Millisecond As Long)
    Dim Start, Endtime As Single
    Start = Timer
    Endtime = Start + Millisecond / 1000
    Do While Timer < Endtime
    DoEvents
    Sleep 10
    Loop
End Function


