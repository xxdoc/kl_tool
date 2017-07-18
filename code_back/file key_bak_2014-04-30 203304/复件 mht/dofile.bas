Attribute VB_Name = "dofile"
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (Destination As Any, Source As Any, ByVal Length As Long)
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

Private Declare Function addMD5 Lib "dll.dll" (ByVal amd5 As String, ByVal astr As String, ByVal sta As Long, ByVal ends As Long) As Boolean
Private Declare Function getMD5 Lib "dll.dll" (ByVal A As String) As Boolean
Private Declare Function getStringSize Lib "dll.dll" () As Long

Public Type keyinfo
    mdbuf(0 To 31) As Byte
    keybuf(0 To 31) As Byte
    obuf(0 To 63) As Byte
    filebuf() As Byte
    chkbuf(0 To 31) As Byte
    
    md As String
    key As String
    file As String
    chk As String
    
    flen As Long
    olen As Long
    fset As Long
    temp As Long
    or1(1 To 64) As Long
    or2(1 To 64) As Long
    
    dtmDateA As Date
End Type

Const BLOCK_SIZE = 8192
Public filex As keyinfo
Public fileProcessing As Long
Public doProcessing As Boolean

Public Function readkeyfile(file As String) As Boolean
If doProcessing = True Then readkeyfile = False:: Exit Function

On Error GoTo NotExist
doProcessing = True

If file = "" Then GoTo NotExist

If Filelong(file) < 1 Then GoTo NotExist

Dim lngFileID As Long, lngFileLen As Long, tmp As Long
Dim startbuf(1 To 32) As Byte
Dim i As Long

lngFileID = FreeFile(0)
Open file For Binary Access Read As lngFileID
lngFileLen = LOF(lngFileID)

Call clearfilex

Get lngFileID, , startbuf

 If startbuf(1) = 75 And startbuf(2) = 76 And startbuf(3) = 68 And startbuf(4) = 1 And _
 startbuf(13) = 102 And startbuf(14) = 109 And startbuf(15) = 116 And startbuf(16) = 32 Then
    
    CopyMemory filex.flen, ByVal VarPtr(startbuf(5)), 4
    CopyMemory filex.temp, ByVal VarPtr(startbuf(9)), 4
    CopyMemory filex.fset, ByVal VarPtr(startbuf(17)), 4
    CopyMemory filex.olen, ByVal VarPtr(startbuf(21)), 4
    CopyMemory filex.dtmDateA, ByVal VarPtr(startbuf(25)), 8
Else
    Close lngFileID
    GoTo NotExist
End If

If lngFileLen <> filex.flen Then
    Close lngFileID
    GoTo NotExist
End If

Get lngFileID, , filex.keybuf

If filex.temp + filex.fset = filex.olen Then filex.fset = filex.olen + filex.temp:: filex.temp = filex.fset

Seek lngFileID, filex.temp - 384 + 1
Get lngFileID, , filex.obuf

Dim orbuf(1 To 64) As Byte

Seek lngFileID, filex.temp - 192 + 1
Get lngFileID, , orbuf
    For i = 1 To 64
    filex.or1(i) = orbuf(i)
    If i > 1 Then:: If orbuf(i - 1) = 32 And orbuf(i) = 0 Then Exit For
    Next i
    
Seek lngFileID, filex.temp - 128 + 1
Get lngFileID, , orbuf
    For i = 1 To 64
    filex.or2(i) = orbuf(i)
    If i > 1 Then:: If orbuf(i - 1) = 32 And orbuf(i) = 0 Then Exit For
    Next i


Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , tmp
If tmp = filex.olen Then
Else
    Close lngFileID
    GoTo NotExist
End If

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , filex.mdbuf

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , startbuf
For i = 1 To 32
If startbuf(i) <> filex.keybuf(i - 1) Then Close lngFileID:: GoTo NotExist
Next i

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , tmp
ReDim filex.filebuf(0 To tmp)
Get lngFileID, , filex.filebuf

Seek lngFileID, filex.flen - 47
Get lngFileID, , filex.chkbuf

Close lngFileID

filex.md = StrConv(filex.mdbuf, vbUnicode)
filex.key = StrConv(filex.keybuf, vbUnicode)
filex.file = StrConv(filex.filebuf, vbUnicode)
filex.chk = StrConv(filex.chkbuf, vbUnicode)

readkeyfile = True
NotExist:
doProcessing = False
End Function

Public Function keyfile(file As String, outf As String, md5 As String, key As String) As Boolean
If doProcessing = True Then keyfile = False:: Exit Function

On Error GoTo NotExist
doProcessing = True

If file = "" Or outf = "" Or key = "" Or md5 = "" Then keyfile = False:: GoTo NotExist

Dim byteBuff() As Byte, lngBlockCount As Long
Dim lngFileID As Long, lngFileLen As Long
Dim lngOutFileID As Long
Dim i As Long, j As Long
Dim or1 As Long, or2 As Long, tmp As Long

Dim fptr As Long
Dim startbuf(1 To 64) As Byte

Dim passkey As String
passkey = String(32, 0)
If addMD5(passkey, key, 1, 0) = False Then keyfile = False::

Dim mdbuf() As Byte, keybuf() As Byte, filebuf() As Byte
ReDim mdbuf(LenB(StrConv(md5, vbFromUnicode)))
ReDim keybuf(LenB(StrConv(passkey, vbFromUnicode)))
ReDim filebuf(LenB(StrConv(file, vbFromUnicode)))
mdbuf = StrConv(md5, vbFromUnicode)
keybuf = StrConv(passkey, vbFromUnicode)
filebuf = StrConv(file, vbFromUnicode)

Dim P As Date
P = Now()

If Filelong(file) < 1 Then keyfile = False:: GoTo NotExist

Do Until or1 <> or2
    Randomize
    or1 = (Int(27 * Rnd) + 5) Mod 27 + 5
    Randomize
    or2 = (Int(21 * Rnd) + 11) Mod 21 + 11
Loop
    
    lngFileID = FreeFile(0)
    Open file For Binary Access Read As lngFileID
    lngOutFileID = FreeFile(1)
    Open outf For Binary As lngOutFileID
    lngFileLen = LOF(lngFileID)
    
    lngBlockCount = lngFileLen \ BLOCK_SIZE
    If (lngFileLen Mod BLOCK_SIZE) <> 0 Then lngBlockCount = lngBlockCount + 1
    
Dim tmpbuf(0 To 31) As Byte, tmpb As Long
    For i = 0 To 31
    tmpb = mdbuf(i) + keybuf(i)
    If tmpb > 255 Then tmpb = tmpb - 234
    tmpbuf(i) = tmpb
'    If passbuf(i) <> filex.keybuf(i) Then Close lngFileID:: GoTo NotExist
    Next i
    
For i = 1 To lngBlockCount - 1
    ReDim byteBuff(1 To BLOCK_SIZE) As Byte
    Get lngFileID, , byteBuff
    
    tmp = UBound(byteBuff) - or1
    For j = or1 To tmp Step or1
    byteBuff(j - 3) = byteBuff(j - 3) Xor mdbuf(j Mod 23)
    byteBuff(j - 1) = byteBuff(j - 1) Xor mdbuf(j Mod 29)
    byteBuff(j) = byteBuff(j) Xor mdbuf(j Mod 32)
    Next j
    tmp = UBound(byteBuff) - or2
    For j = or2 To tmp Step or2
    byteBuff(j - 9) = byteBuff(j - 9) Xor tmpbuf(j Mod 11)
    byteBuff(j - 7) = byteBuff(j - 7) Xor tmpbuf(j Mod 17)
    byteBuff(j - 4) = byteBuff(j - 4) Xor tmpbuf(j Mod 25)
    byteBuff(j) = byteBuff(j) Xor tmpbuf(j Mod 32)
    Next j
    
    
    Put lngOutFileID, , byteBuff
    fileProcessing = (1000 * i) \ lngBlockCount
    DoEvents
Next i
    
    ReDim byteBuff(1 To lngFileLen - (lngBlockCount - 1) * BLOCK_SIZE) As Byte
    Get lngFileID, , byteBuff
    
    tmp = UBound(byteBuff) - or1
    For j = or1 To tmp Step or1
    byteBuff(j - 3) = byteBuff(j - 3) Xor mdbuf(j Mod 23)
    byteBuff(j - 1) = byteBuff(j - 1) Xor mdbuf(j Mod 29)
    byteBuff(j) = byteBuff(j) Xor mdbuf(j Mod 32)
    Next j
    tmp = UBound(byteBuff) - or2
    For j = or2 To tmp Step or2
    byteBuff(j - 9) = byteBuff(j - 9) Xor tmpbuf(j Mod 11)
    byteBuff(j - 7) = byteBuff(j - 7) Xor tmpbuf(j Mod 17)
    byteBuff(j - 4) = byteBuff(j - 4) Xor tmpbuf(j Mod 25)
    byteBuff(j) = byteBuff(j) Xor tmpbuf(j Mod 32)
    Next j

    Put lngOutFileID, , byteBuff
    
    ReDim byteBuff(1 To (2 * BLOCK_SIZE - UBound(byteBuff))) As Byte
    
    For j = 1 To UBound(byteBuff)
        byteBuff(j) = Int(256 * Rnd)
    Next j
    
    Seek lngFileID, 1
    Get lngFileID, , startbuf
    
    i = or1:: j = or2
    Randomize
    or1 = Int(512 * Rnd) + 512
    
    CopyMemory ByVal VarPtr(byteBuff(or1 - 384 + 1)), ByVal VarPtr(startbuf(1)), 64
    
    tmp = or1 - 192 + 1:: byteBuff(tmp) = i:: byteBuff(tmp + 1) = 5
    tmp = tmp + 2:: byteBuff(tmp) = 23:: byteBuff(tmp + 1) = 3
    tmp = tmp + 2:: byteBuff(tmp) = 29:: byteBuff(tmp + 1) = 1
    tmp = tmp + 2:: byteBuff(tmp) = 32:: byteBuff(tmp + 1) = 0
    
    tmp = or1 - 128 + 1:: byteBuff(tmp) = j:: byteBuff(tmp + 1) = 11
    tmp = tmp + 2:: byteBuff(tmp) = 11:: byteBuff(tmp + 1) = 9
    tmp = tmp + 2:: byteBuff(tmp) = 17:: byteBuff(tmp + 1) = 7
    tmp = tmp + 2:: byteBuff(tmp) = 25:: byteBuff(tmp + 1) = 4
    tmp = tmp + 2:: byteBuff(tmp) = 32:: byteBuff(tmp + 1) = 0
    
    fptr = lngFileLen + or1:: tmp = or1
    CopyMemory ByVal VarPtr(byteBuff(tmp - 4)), fptr, 4
    CopyMemory ByVal VarPtr(byteBuff(tmp + 4)), lngFileLen, 4
    or2 = Int(256 * Rnd) + 256
    CopyMemory byteBuff(tmp), fptr + or2, 4
    
    fptr = fptr + or2:: tmp = tmp + or2
    CopyMemory ByVal VarPtr(byteBuff(tmp - 4)), fptr, 4
    CopyMemory ByVal VarPtr(byteBuff(tmp + 4)), ByVal VarPtr(mdbuf(0)), 32
    or2 = Int(256 * Rnd) + 256
    CopyMemory ByVal VarPtr(byteBuff(tmp)), fptr + or2, 4
    
    fptr = fptr + or2:: tmp = tmp + or2
    CopyMemory ByVal VarPtr(byteBuff(tmp - 4)), fptr, 4
    CopyMemory ByVal VarPtr(byteBuff(tmp + 4)), ByVal VarPtr(keybuf(0)), 32
    or2 = Int(256 * Rnd) + 256
    CopyMemory ByVal VarPtr(byteBuff(tmp)), fptr + or2, 4
    
    fptr = fptr + or2:: tmp = tmp + or2
    CopyMemory ByVal VarPtr(byteBuff(tmp - 4)), fptr, 4
    CopyMemory ByVal VarPtr(byteBuff(tmp + 4)), UBound(filebuf), 4
    CopyMemory ByVal VarPtr(byteBuff(tmp + 8)), ByVal VarPtr(filebuf(0)), UBound(filebuf) + 1
    or2 = Int(256 * Rnd) + 256
    CopyMemory ByVal VarPtr(byteBuff(tmp)), fptr + or2, 4
    
    tmp = UBound(byteBuff) - 15:: byteBuff(tmp) = 255:: byteBuff(tmp + 1) = 255
    tmp = tmp + 2:: byteBuff(tmp) = 3:: byteBuff(tmp + 1) = 5
    tmp = tmp + 2:: byteBuff(tmp) = 7:: byteBuff(tmp + 1) = 11
    tmp = tmp + 2:: byteBuff(tmp) = 13:: byteBuff(tmp + 1) = 17
    tmp = tmp + 2:: byteBuff(tmp) = 0:: byteBuff(tmp + 1) = 0
    tmp = tmp + 2:: byteBuff(tmp) = 0:: byteBuff(tmp + 1) = 0
    tmp = tmp + 2:: byteBuff(tmp) = 75:: byteBuff(tmp + 1) = 76
    tmp = tmp + 2:: byteBuff(tmp) = 69:: byteBuff(tmp + 1) = 68
    
    Put lngOutFileID, , byteBuff
    
    tmp = (lngBlockCount + 1) * BLOCK_SIZE
    
    startbuf(1) = 75:: startbuf(2) = 76:: startbuf(3) = 68:: startbuf(4) = 1
    CopyMemory ByVal VarPtr(startbuf(5)), tmp, 4
    CopyMemory ByVal VarPtr(startbuf(9)), or1, 4
    startbuf(13) = 102:: startbuf(14) = 109:: startbuf(15) = 116:: startbuf(16) = 32
    CopyMemory ByVal VarPtr(startbuf(17)), lngFileLen - or1, 4
    CopyMemory ByVal VarPtr(startbuf(21)), lngFileLen, 4
    CopyMemory ByVal VarPtr(startbuf(25)), P, 8
    CopyMemory ByVal VarPtr(startbuf(33)), ByVal VarPtr(keybuf(0)), 32
    
    Seek lngOutFileID, 1
    Put lngOutFileID, , startbuf
    
    Close lngFileID, lngOutFileID
    Erase byteBuff
    Erase startbuf

keyfile = True
NotExist:
doProcessing = False
End Function

Public Function unkeyfile(file As String, outf As String, key As String) As Boolean
If doProcessing = True Then unkeyfile = False:: Exit Function

On Error GoTo NotExist
doProcessing = True

If file = "" Or outf = "" Or key = "" Then unkeyfile = False:: GoTo NotExist

Dim passkey As String

If Mid(key, 1, 11) = "kloffset000" Then
    key = Replace(key, "kloffset000", "", , , vbTextCompare)
End If

passkey = String(32, 0)
If addMD5(passkey, key, 1, 0) = False Then unkeyfile = False:: GoTo NotExist

If Filelong(file) < 1 Then unkeyfile = False:: GoTo NotExist

Dim byteBuff() As Byte
Dim passbuf() As Byte
ReDim passbuf(LenB(StrConv(passkey, vbFromUnicode)))
passbuf = StrConv(passkey, vbFromUnicode)
ReDim Preserve passbuf(0 To 31)

Dim lngFileID As Long, lngFileLen As Long, lngBlockCount As Long, tmp As Long
Dim startbuf(1 To 32) As Byte
Dim i As Long, j As Long, or1 As Long, or2 As Long

lngFileID = FreeFile(0)
Open file For Binary Access Read As lngFileID
lngFileLen = LOF(lngFileID)

Call clearfilex

Get lngFileID, , startbuf

 If startbuf(1) = 75 And startbuf(2) = 76 And startbuf(3) = 68 And startbuf(4) = 1 And _
 startbuf(13) = 102 And startbuf(14) = 109 And startbuf(15) = 116 And startbuf(16) = 32 Then
    
    CopyMemory filex.flen, ByVal VarPtr(startbuf(5)), 4
    CopyMemory filex.temp, ByVal VarPtr(startbuf(9)), 4
    CopyMemory filex.fset, ByVal VarPtr(startbuf(17)), 4
    CopyMemory filex.olen, ByVal VarPtr(startbuf(21)), 4
    CopyMemory filex.dtmDateA, ByVal VarPtr(startbuf(25)), 8
Else
    Close lngFileID
    GoTo NotExist
End If

If lngFileLen <> filex.flen Then
    Close lngFileID
    GoTo NotExist
End If

Get lngFileID, , filex.keybuf

If filex.temp + filex.fset = filex.olen Then filex.fset = filex.olen + filex.temp:: filex.temp = filex.fset

Seek lngFileID, filex.temp - 384 + 1
Get lngFileID, , filex.obuf

Dim orbuf(1 To 64) As Byte

Seek lngFileID, filex.temp - 192 + 1
Get lngFileID, , orbuf
    For i = 1 To 64
    filex.or1(i) = orbuf(i)
    If i > 1 Then:: If orbuf(i - 1) = 32 And orbuf(i) = 0 Then Exit For
    Next i
    
Seek lngFileID, filex.temp - 128 + 1
Get lngFileID, , orbuf
    For i = 1 To 64
    filex.or2(i) = orbuf(i)
    If i > 1 Then:: If orbuf(i - 1) = 32 And orbuf(i) = 0 Then Exit For
    Next i


Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , tmp
If tmp = filex.olen Then
Else
    Close lngFileID
    GoTo NotExist
End If

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , filex.mdbuf

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , startbuf
For i = 1 To 32
If startbuf(i) <> filex.keybuf(i - 1) Then Close lngFileID:: GoTo NotExist
Next i

Seek lngFileID, filex.temp - 4
Get lngFileID, , tmp
If tmp = filex.temp Then
    Get lngFileID, , filex.temp
Else
    Close lngFileID
    GoTo NotExist
End If
Get lngFileID, , tmp
ReDim filex.filebuf(1 To tmp + 1)
Get lngFileID, , filex.filebuf

Seek lngFileID, filex.flen - 47
Get lngFileID, , filex.chkbuf

    filex.md = StrConv(filex.mdbuf, vbUnicode)
    filex.key = StrConv(filex.keybuf, vbUnicode)
    filex.file = StrConv(filex.filebuf, vbUnicode)
    filex.chk = StrConv(filex.chkbuf, vbUnicode)
       
       
Dim tmpbuf(0 To 31) As Byte, mdbuf(0 To 31) As Byte, tmpb As Long
    For i = 0 To 31
    If key = CStr(filex.fset - filex.olen) Then passbuf(i) = filex.keybuf(i)
    mdbuf(i) = filex.mdbuf(i)
    tmpb = filex.mdbuf(i) + passbuf(i)
    If tmpb > 255 Then tmpb = tmpb - 234
    tmpbuf(i) = tmpb
'    If passbuf(i) <> filex.keybuf(i) Then Close lngFileID:: GoTo NotExist
    Next i

or1 = filex.or1(1):: or2 = filex.or2(1)
Seek lngFileID, 1

lngOutFileID = FreeFile(1)
Open outf For Binary As lngOutFileID
lngFileLen = filex.olen

lngBlockCount = lngFileLen \ BLOCK_SIZE
If (lngFileLen Mod BLOCK_SIZE) <> 0 Then lngBlockCount = lngBlockCount + 1
    
For i = 1 To lngBlockCount - 1
    ReDim byteBuff(1 To BLOCK_SIZE) As Byte
    Get lngFileID, , byteBuff
    
    tmp = UBound(byteBuff) - or2
    For j = or2 To tmp Step or2
    byteBuff(j - 9) = byteBuff(j - 9) Xor tmpbuf(j Mod 11)
    byteBuff(j - 7) = byteBuff(j - 7) Xor tmpbuf(j Mod 17)
    byteBuff(j - 4) = byteBuff(j - 4) Xor tmpbuf(j Mod 25)
    byteBuff(j) = byteBuff(j) Xor tmpbuf(j Mod 32)
    Next j
    tmp = UBound(byteBuff) - or1
    For j = or1 To tmp Step or1
    byteBuff(j - 3) = byteBuff(j - 3) Xor mdbuf(j Mod 23)
    byteBuff(j - 1) = byteBuff(j - 1) Xor mdbuf(j Mod 29)
    byteBuff(j) = byteBuff(j) Xor mdbuf(j Mod 32)
    Next j
    
    Put lngOutFileID, , byteBuff
    fileProcessing = (1000 * i) \ lngBlockCount
    DoEvents
Next i
    
    ReDim byteBuff(1 To lngFileLen - (lngBlockCount - 1) * BLOCK_SIZE) As Byte
    Get lngFileID, , byteBuff
    
    tmp = UBound(byteBuff) - or2
    For j = or2 To tmp Step or2
    byteBuff(j - 9) = byteBuff(j - 9) Xor tmpbuf(j Mod 11)
    byteBuff(j - 7) = byteBuff(j - 7) Xor tmpbuf(j Mod 17)
    byteBuff(j - 4) = byteBuff(j - 4) Xor tmpbuf(j Mod 25)
    byteBuff(j) = byteBuff(j) Xor tmpbuf(j Mod 32)
    Next j
    tmp = UBound(byteBuff) - or1
    For j = or1 To tmp Step or1
    byteBuff(j - 3) = byteBuff(j - 3) Xor mdbuf(j Mod 23)
    byteBuff(j - 1) = byteBuff(j - 1) Xor mdbuf(j Mod 29)
    byteBuff(j) = byteBuff(j) Xor mdbuf(j Mod 32)
    Next j
    
    Put lngOutFileID, , byteBuff
    Seek lngOutFileID, 1
    Put lngOutFileID, , filex.obuf
    
    Erase byteBuff

Close lngOutFileID
Close lngFileID

unkeyfile = True
NotExist:
doProcessing = False
End Function
Public Function addfilemd5(file As String, key As String) As Boolean
If doProcessing = True Then Exit Function

On Error GoTo NotExist
doProcessing = True

If file = "" Or key = "" Then GoTo NotExist

If Filelong(file) < 1 Then GoTo NotExist

Dim lngFileID As Long, lngFileLen As Long
Dim passbuf() As Byte
ReDim passbuf(LenB(StrConv(key, vbFromUnicode)))
passbuf = StrConv(key, vbFromUnicode)
ReDim Preserve passbuf(0 To 31)

lngFileID = FreeFile(0)
Open file For Binary As lngFileID
lngFileLen = LOF(lngFileID)

Seek lngFileID, lngFileLen - 47
Put lngFileID, , passbuf

Close lngFileID

addfilemd5 = True
NotExist:
doProcessing = False

End Function

Public Function Filelong(FileName As String) As Long
    Filelong = -1
    If FileName = "" Then GoTo NotExist
    On Error GoTo NotExist
    Filelong = FileLen(FileName)
    Exit Function
NotExist:
End Function

Public Function klMD5(str As String, md1 As Long, md2 As Long) As String
If doProcessing = True Then klMD5 = "is busy":: Exit Function

On Error GoTo NotExist
doProcessing = True
If str = "" Or md1 < 0 Or md2 < 0 Then klMD5 = "NULL":: GoTo NotExist
If md2 > 0 And Filelong(str) < 1 Then klMD5 = "FILE NOT FOUND":: GoTo NotExist
klMD5 = String(32, 0)
If addMD5(klMD5, str, md1, md2) = False Then klMD5 = "DLL ERROR"
If Asc(klMD5) = 0 Then klMD5 = "DLL ERROR"
NotExist:
doProcessing = False
End Function

Public Function clearfilex() As Boolean
On Error GoTo NotExist
Erase filex.filebuf
Erase filex.keybuf
Erase filex.mdbuf
Erase filex.obuf
Erase filex.or1
Erase filex.or2

filex.dtmDateA = Now()
filex.file = ""
filex.key = ""
filex.md = ""
filex.flen = 0
filex.fset = 0
filex.olen = 0
filex.temp = 0

clearfilex = True
NotExist:

End Function


' 关闭文件
'  Close #FileNumber
'  获得文件的长度
'  LOF (FileNumber)
'  文件读写指针到结尾
'  EOF (FileNumber)
'  获得文件读写指针当前位置
'  Loc (FileNumber)
'  设置文件读写指针为Start指明的位置
'  Seek FileNumber, Start
'Dim startbuf(0 To 3) As Byte '要被转化的Byte()
'Dim l_long As Long '要保存转化的Long
'startbuf(0) = Buffer(3)
'startbuf(1) = Buffer(2)
'startbuf(2) = Buffer(1)
'startbuf(3) = Buffer(0)
'l_long = "&H" & (CStr(Hex(startbuf(0))) & CStr(Hex(startbuf(1)))) & CStr(Hex(startbuf(2))) & CStr(Hex(startbuf(3)))
' CopyMemory Buffer(0), a, 4
