VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "kVBJSON"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' kVBJSON is a VB6 adaptation of the VBA JSON project
' Some bugs fixed, speed improvements
' BSD Licensed
Private Declare Function MultiByteToWideChar Lib "kernel32" (ByVal CodePage As Long, ByVal dwFlags As Long, ByRef lpMultiByteStr As Any, ByVal cchMultiByte As Long, ByVal lpWideCharStr As Long, ByVal cchWideChar As Long) As Long
Private Const CP_UTF8 = 65001

Option Explicit

Const MAX_FILE_BUFF     As Long = 8 * 1024

Private r_t() As String
Private r_kv() As String

Public r_tstr As String
Public r_tl As Long
Public r_rl As Long
Public r_ck As Long

Public can_next As Boolean
Public can_index As Long
Public can_str As String

Private psErrors As String
Private paErrors As String
Private pnErrors As String

Public Function GetParserErrors() As String
    GetParserErrors = psErrors & "--" & paErrors & "--" & pnErrors
End Function

Public Function ClearParserErrors() As String
    psErrors = ""
    paErrors = ""
    pnErrors = ""
End Function
Public Function Getkv(i As Long) As String
    If r_tl > 0 And r_rl > 0 And UBound(r_kv) - LBound(r_kv) + 1 > 0 Then
        If i >= 0 And i < UBound(r_kv) - LBound(r_kv) + 1 Then
            Getkv = r_kv(i)
            Exit Function
        End If
    End If
    Getkv = ""
End Function
Public Function parse_UTF(str As String, tstr As String, offset As Long, ck As Long) As Long
    On Error GoTo CuoWu
    parse_UTF = parse_str(UTF8_Decode(str, offset), tstr, ck)

    Exit Function
CuoWu:
    psErrors = "Invalid JSON UTF"
    parse_UTF = 0
End Function
Public Function parse_file(str As String, tstr As String, offset As Long, ck As Long) As Long
    On Error GoTo CuoWu
    parse_file = parse_str(ReadTextFile(str, offset), tstr, ck)

    Exit Function
CuoWu:
    psErrors = "Invalid JSON txt"
    parse_file = 0
End Function
Public Function parse_str(str As String, tstr As String, ck As Long) As Long
    On Error GoTo CuoWu

    Dim Index As Long, tl As Long, parse As Long
    Dim t() As String
    t = Split(tstr, "|")
    tl = UBound(t) - LBound(t) + 1
    r_rl = 0
    r_t = t
    r_tl = tl
    r_tstr = tstr
    r_ck = ck
    ReDim r_kv(tl - 1)
    parse = 0
    Index = 1
    On Error Resume Next

    Select Case Mid$(str, Index, 1)
        Case "{"
        r_rl = 1
        parse = parseObject(str, Index, t, tl, ck)
        Case "["
        parse = parseArray(str, Index, t, tl, ck)
        Case Else
        psErrors = "Invalid JSON"
        GoTo CuoWu

    End Select
    parse_str = parse
    Exit Function
CuoWu:
    parse_str = -1
End Function
Public Function nextchar(str As String, Index As Long) As String
    On Error GoTo CuoWu
    nextchar = ""
    nextchar = Mid$(str, Index + 1, 1)
    Do While nextchar = Chr$(9) Or nextchar = Chr$(10) Or nextchar = Chr$(13) Or nextchar = " "
        Index = Index + 1
        nextchar = Mid$(str, Index + 1, 1)
    Loop

    Exit Function
CuoWu:
    nextchar = ""
End Function
Public Function parseObject(str As String, Index As Long, t() As String, tl As Long, ck As Long) As Long
    'On Error GoTo CuoWu
    If nextchar(str, Index - 1) <> "{" Then psErrors = "first is not {":: GoTo CuoWu

    Dim a As Long, b As Long, c As Long, d As Long, e As Long, i As Long
    Dim n_c As String, n_d As String
    e = 0
    For i = 0 To tl - 1
        d = 0
        a = InStr(Index, str, Chr$(34) & t(i) & Chr$(34), vbBinaryCompare)
        If a > 0 Then
            e = e + 1
            b = InStr(a + Len(Chr$(34) & t(i) & Chr$(34)), str, ":", vbBinaryCompare)
            n_c = nextchar(str, b)
            n_d = ""
            If b > 0 And n_c = "{" Then
                c = InStr(b + 2, str, "[", vbBinaryCompare)
                d = InStr(b + 2, str, "}", vbBinaryCompare)
                If d > 0 Then
                    If c > 0 And c < d Then
                        c = InStr(c + 1, str, "]", vbTextCompare)
                        If c <= 0 Then psErrors = ": [ then no ] ":: GoTo CuoWu
                        d = InStr(c + 1, str, "}", vbBinaryCompare)
                        Do While d > 0
                            n_d = nextchar(str, d)
                            If n_d = "," Or n_d = "}" Then Exit Do
                            d = InStr(d + 1, str, "{", vbBinaryCompare)
                            d = InStr(d + 1, str, "}", vbBinaryCompare)
                        Loop
                        If d <= 0 Then psErrors = ":{...[ then no]}":: GoTo CuoWu
                        r_kv(i) = Mid$(str, b + 1, d - b + 1)
                    Else
                        Do While d > 0
                            n_d = nextchar(str, d)
                            If n_d = "," Or n_d = "}" Then Exit Do
                            d = InStr(d + 1, str, "{", vbBinaryCompare)
                            d = InStr(d + 1, str, "}", vbBinaryCompare)
                        Loop
                        If d <= 0 Then psErrors = ": { then no } ":: GoTo CuoWu
                        r_kv(i) = Mid$(str, b + 1, d - b)
                    End If
                Else
                    psErrors = ":{ then no}"
                    GoTo CuoWu
                End If
            ElseIf b > 0 And n_c = "[" Then
                d = InStr(b + 2, str, "]", vbBinaryCompare)
                Do While d > 0
                    n_d = nextchar(str, d)
                    If n_d = "," Or n_d = "}" Then Exit Do
                    d = InStr(d + 1, str, "[", vbBinaryCompare)
                    d = InStr(d + 1, str, "]", vbBinaryCompare)
                Loop
                If d <= 0 Then psErrors = ": [ then no ] ":: GoTo CuoWu
                r_kv(i) = Mid$(str, b + 1, d - b)
            ElseIf b > 0 And n_c = Chr$(34) Then
                d = InStr(b + 2, str, Chr$(34), vbBinaryCompare)
                Do While d > 0
                    n_d = nextchar(str, d)
                    If n_d = "," Or n_d = "}" Then Exit Do
                    d = InStr(d + 1, str, Chr$(34), vbBinaryCompare)
                    d = InStr(d + 1, str, Chr$(34), vbBinaryCompare)
                Loop
                If d <= 0 Then psErrors = ":" & Chr$(34) & "then no" & Chr$(34):: GoTo CuoWu
                r_kv(i) = Mid$(str, b + 2, d - b - 2)
            ElseIf b > 0 Then
                c = InStr(b + 1, str, "}", vbBinaryCompare)
                If c <= 0 Then psErrors = ": then no }":: GoTo CuoWu
                d = InStr(b + 1, str, ",", vbBinaryCompare)
                If d <= 0 Or d > c Then d = c
                r_kv(i) = Mid$(str, b + 1, d - b - 1)
            Else
                If b <= 0 Then psErrors = "key then no :":: GoTo CuoWu
            End If
        Else
            If a <= 0 Then psErrors = "then no key":: r_kv(i) = ""
        End If
        If d > 0 And ck = 1 Then
            Index = d
        End If
    Next i
    parseObject = e

    Exit Function
CuoWu:
    parseObject = -1
End Function
Public Function nextArray() As Long
    On Error GoTo CuoWu
    If can_next = False Or Len(can_str) <= 0 Then pnErrors = "can not next":: GoTo CuoWu
    If nextchar(can_str, can_index - 1) <> "{" Then pnErrors = "after [ is not {":: GoTo CuoWu

    can_index = InStr(can_index, can_str, "{", vbBinaryCompare)
    Dim n_c As String
    Dim d As Long, ra As Long
    can_next = False
    n_c = ""
    d = InStr(can_index + 1, can_str, "}", vbBinaryCompare)
    Do While d > 0
        n_c = nextchar(can_str, d)
        If n_c = "," Or n_c = "]" Then Exit Do
        d = InStr(d + 1, can_str, "{", vbBinaryCompare)
        d = InStr(d + 1, can_str, "}", vbBinaryCompare)
    Loop
    If d <= 0 Then pnErrors = "[{ then no } ":: GoTo CuoWu
    ra = parseObject(Mid$(can_str, can_index, d - can_index + 1), 1, r_t, r_tl, r_ck)

    If n_c = "," Then
        can_next = True
        can_index = d + 2
    Else
        can_next = False
    End If

    r_rl = r_rl + 1
    nextArray = ra
    Exit Function
CuoWu:
    nextArray = -11
End Function

Public Function parseArray(str As String, Index As Long, t() As String, tl As Long, ck As Long) As Long
    On Error GoTo CuoWu

    If nextchar(str, Index - 1) <> "[" Then paErrors = "first is not [":: GoTo CuoWu
    If nextchar(str, Index) <> "{" Then paErrors = "after [ is not {":: GoTo CuoWu
    Dim d As Long, ra As Long
    Dim n_c As String
    can_next = False
    n_c = ""

    d = InStr(Index + 1, str, "}", vbBinaryCompare)
    Do While d > 0
        n_c = nextchar(str, d)
        If n_c = "," Or n_c = "]" Then Exit Do
        d = InStr(d + 1, str, "{", vbBinaryCompare)
        d = InStr(d + 1, str, "}", vbBinaryCompare)
    Loop
    If d <= 0 Then paErrors = "[{ then no } ":: GoTo CuoWu
    ra = parseObject(Mid$(str, Index + 1, d - Index), 1, t, tl, ck)

    If n_c = "," Then
        can_next = True
        can_index = d + 2
        can_str = str
    Else
        can_next = False
    End If

    r_rl = 1
    parseArray = ra
    Exit Function
CuoWu:
    parseArray = -11
End Function
Public Function Class_Clear() As Long
    r_tstr = ""
    r_tl = 0
    r_rl = 0
    r_ck = 0
    can_next = False
    can_index = 0
    can_str = ""
    psErrors = ""
    paErrors = ""
    pnErrors = ""
    Class_Clear = 0
End Function

Private Sub Class_Initialize()
    r_tstr = ""
    r_tl = 0
    r_rl = 0
    r_ck = 0
    can_next = False
    can_index = 0
    can_str = ""
    psErrors = ""
    paErrors = ""
    pnErrors = ""
End Sub

'功能: 把Utf8字符转化成ANSI字符
Public Function UTF8_Decode(FileName As String, offset As Long) As String
    On Error Resume Next
    Dim sUTF8 As String
    Dim lngUtf8Size As Long
    Dim strBuffer As String
    Dim lngBufferSize As Long
    Dim lngResult As Long
    Dim bytUtf8() As Byte
    Dim n As Long
    sUTF8 = GetFile(FileName, offset)
    If LenB(sUTF8) = 0 Then Exit Function
    On Error GoTo EndFunction
    bytUtf8 = sUTF8
    lngUtf8Size = UBound(bytUtf8) + 1
    lngBufferSize = lngUtf8Size * 2
    strBuffer = String$(lngBufferSize, vbNullChar)
    lngResult = MultiByteToWideChar(CP_UTF8, 0, bytUtf8(0), _
                lngUtf8Size, StrPtr(strBuffer), lngBufferSize)
    If lngResult Then
        UTF8_Decode = Left$(strBuffer, lngResult)
    End If
EndFunction:

End Function
'读文件至变量
Public Function GetFile(FileName As String, offset As Long) As String
    On Error Resume Next
    Dim i As Integer, BB() As Byte
    If Not FileExists(FileName) Then Exit Function
    i = FreeFile
    Open FileName For Binary As #i
    If offset >= FileLen(FileName) Then Close #i:: Exit Function
    If offset <= 0 Then
        ReDim BB(FileLen(FileName) - 1)
    Else
        Seek #i, offset
        If (LOF(i) - offset) > MAX_FILE_BUFF Then
            ReDim BB(FileLen(FileName) - offset)
        Else
            ReDim BB(MAX_FILE_BUFF)
        End If
    End If
    Get #i, , BB
    Close #i
    GetFile = BB
End Function
Public Function ReadTextFile(sFilePath As String, offset As Long) As String
    On Error Resume Next
    Dim handle As Integer
    If Not FileExists(sFilePath) Then Exit Function
    handle = FreeFile
    Open sFilePath For Binary As #handle
    If offset >= LOF(handle) Then Close #handle:: Exit Function
    If offset <= 0 Then
        ReadTextFile = Space$(LOF(handle))
    Else
        Seek #handle, offset
        If (LOF(handle) - offset) > MAX_FILE_BUFF Then
            ReadTextFile = Space$(LOF(handle) - offset)
        Else
            ReadTextFile = Space$(MAX_FILE_BUFF)
        End If
    End If
    Get #handle, , ReadTextFile
    Close #handle
End Function
Private Function FileExists(file As String) As Boolean
    On Error Resume Next
    If (GetAttr(file) And vbDirectory) = False Then FileExists = True
    If Err Then FileExists = False: Err.Clear
End Function
Private Function FolderExists(Folder As String) As Boolean
    On Error Resume Next
    If GetAttr(Folder) And vbDirectory Then FolderExists = True
    If Err Then FolderExists = False: Err.Clear
End Function
Private Function Filelong(FileName As String) As Long
    Filelong = -1
    On Error GoTo NotExist
    Filelong = FileLen(FileName)
    Exit Function
NotExist:
    If dir(FileName) <> "" Then Filelong = -2
End Function
