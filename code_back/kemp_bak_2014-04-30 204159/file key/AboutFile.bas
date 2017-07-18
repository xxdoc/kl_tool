Attribute VB_Name = "AboutFile"
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)

Public Type klpoint
    x As Long
    y As Long
    nextx As Long
    nexty As Long
End Type

Public Function FileExist(Filename As String) As Boolean
On Error GoTo NotExist
Call FileLen(Filename)
FileExist = True
Exit Function
NotExist:
End Function
Public Function FileIsR(Filename As String) As Boolean
Dim objWMIService, colProcessList, objProcess
If InStrRev(Filename, "\", -1, vbTextCompare) Then Filename = Mid$(Filename, InStrRev(Filename, "\", -1, vbTextCompare) + 1)
FileIsR = False
Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
Set colProcessList = objWMIService.ExecQuery _
("Select * from Win32_Process Where Name='" & Filename & "'")
For Each objProcess In colProcessList
FileIsR = True
Exit For
Next
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
Public Function Filelog(strlog As String) As Boolean
    Open "fish_log.log" For Append As #1
    Print #1, Format$(Now, "c") & "  : " & strlog
    Close #1
End Function
