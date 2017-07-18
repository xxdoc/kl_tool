VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "cJSONScript"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Dim dictVars As New Dictionary

Public Function Eval(sJSON As String) As String
   Dim cJ As New cVBJSON
   Dim SB As New cStringBuilder
   Dim o As Object
   Dim c As Object
   Dim i As Long
   
   Set o = cJ.parse(sJSON)
   If (cJ.GetParserErrors = "") And Not (o Is Nothing) Then
      For i = 1 To o.Count
         Select Case VarType(o.Item(i))
         Case vbNull
            SB.Append "null"
         Case vbDate
            SB.Append CStr(o.Item(i))
         Case vbString
            SB.Append CStr(o.Item(i))
         Case Else
            Set c = o.Item(i)
            SB.Append ExecCommand(c)
         End Select
      Next
   Else
      MsgBox cJ.GetParserErrors, vbExclamation, "Parser Error"
   End If
   Eval = SB.toString
End Function

Public Function ExecCommand(ByRef obj As Variant) As String
   Dim SB As New cStringBuilder
   Select Case VarType(obj)
      Case vbNull
         SB.Append "null"
      Case vbDate
         SB.Append CStr(obj)
      Case vbString
         SB.Append CStr(obj)
      Case vbObject
         
         Dim i As Long
         Dim j As Long
         Dim this As Object
                  
         If TypeName(obj) = "Dictionary" Then
            Dim sOut As String
            Dim sRet As String

            Dim keys
            keys = obj.keys
            For i = 0 To obj.Count - 1
               Dim key
               key = keys(i)
               Set this = obj.Item(key)
               
               ' command implementation
               Select Case LCase(key)
               Case "alert":
                  MsgBox ExecCommand(this.Item("message")), vbInformation, ExecCommand(this.Item("title"))
                  
               Case "input":
                  SB.Append InputBox(ExecCommand(this.Item("prompt")), ExecCommand(this.Item("title")), ExecCommand(this.Item("default")))
                  
               Case "switch"
                  sOut = ExecCommand(this.Item("default"))
                  sRet = LCase(ExecCommand(this.Item("case")))
                  For j = 0 To this.Item("items").Count - 1
                     If LCase(this.Item("items").Item(j + 1).Item("case")) = sRet Then
                        sOut = ExecCommand(this.Item("items").Item(j + 1).Item("return"))
                        Exit For
                     End If
                  Next
                  SB.Append sOut
               
               Case "set":
                  If dictVars.Exists(this.Item("name")) Then
                     dictVars.Item(this.Item("name")) = ExecCommand(this.Item("value"))
                  Else
                     dictVars.Add this.Item("name"), ExecCommand(this.Item("value"))
                  End If
                  
               Case "get":
                  sRet = ExecCommand(dictVars(CStr(this.Item("name"))))
                  If sRet = "" Then
                     sRet = ExecCommand(this.Item("default"))
                  End If
                  
                  SB.Append sRet
                  
               Case "if"
                  Dim val1 As String
                  Dim val2 As String
                  Dim bRes As Boolean
                  val1 = ExecCommand(this.Item("value1"))
                  val2 = ExecCommand(this.Item("value2"))
                  
                  bRes = False
                  Select Case LCase(this.Item("type"))
                  Case "eq" ' =
                     If LCase(val1) = LCase(val2) Then
                        bRes = True
                     End If
                     
                  Case "gt" ' >
                     If val1 > val2 Then
                        bRes = True
                     End If
                  
                  Case "lt" ' <
                     If val1 < val2 Then
                        bRes = True
                     End If
                  
                  Case "gte" ' >=
                     If val1 >= val2 Then
                        bRes = True
                     End If
                  
                  Case "lte" ' <=
                     If val1 <= val2 Then
                        bRes = True
                     End If
                  
                  End Select
                  
                  If bRes Then
                     SB.Append ExecCommand(this.Item("true"))
                  Else
                     SB.Append ExecCommand(this.Item("false"))
                  End If
                  
               Case "return"
                  SB.Append obj.Item(key)
               
                  
               Case Else
                  SB.Append obj.Item(key)
                  
               End Select
               'SB.Append """" & key & """:" & toString(obj.Item(key))
            Next i
            
         ElseIf TypeName(obj) = "Collection" Then

            Dim Value
            For Each Value In obj
               SB.Append ExecCommand(Value)
            Next Value
            
         End If
         Set this = Nothing

      Case vbBoolean
         If obj Then SB.Append "true" Else SB.Append "false"
      
      Case vbVariant, vbArray, vbArray + vbVariant
       '  Dim sEB
       '  SB.Append multiArray(obj, 1, "", sEB)
      
      Case Else
         SB.Append Replace(obj, ",", ".")
   End Select

   ExecCommand = SB.toString
   Set SB = Nothing
   
End Function















' please ignore this for now
               
'               Case "function"
'               '   // defines a function
'               '   'function': {
'               '      'name': 'showMessage',
'               '      'code': [{
'               '         'alert': {
'               'title:             'Function Call',
'               'message:             'No params implemented yet.'
'               '         }
'               '      }]
'               '
'               '   },
'                  If dictVars.Exists(this.Item("name")) Then
'                     dictVars.Item(this.Item("name")) = this.Item("code")
'                  Else
'                     dictVars.Add this.Item("name"), this.Item("code")
'                  End If
'
'               Case "call"
'                  SB.Append ExecCommand(dictVars(CStr(this.Item("name"))))
