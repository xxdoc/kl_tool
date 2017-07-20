Attribute VB_Name = "Module1"

Declare Function TEST_DLL Lib "dll.dll" (ByVal a As Long, ByVal b As Long) As Long

Declare Function GET_DLL_VER_CODE Lib "dll.dll" () As Long
Declare Function GET_DLL_OK_CODE Lib "dll.dll" () As Long
Declare Function GET_DLL_ERROR_CODE Lib "dll.dll" () As Long
Declare Function GET_DLL_MAX_BUFFER_SIZE Lib "dll.dll" () As Long

Declare Function setStr Lib "dll.dll" (ByVal a As String) As Long
Declare Function getStr Lib "dll.dll" (ByVal a As String) As Long

Declare Function getLen Lib "dll.dll" () As Long

