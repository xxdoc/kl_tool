#ifndef DLL_H
#define DLL_H

#include <windows.h>

#define DLL_API extern "C" _declspec(dllexport)
#define _C_ _stdcall

//#define DLL_MIN_SIZE
#ifdef DLL_MIN_SIZE
 // default lib setting.
 #pragma comment(linker, "/defaultlib:kernel32.lib") 
 #pragma comment(linker, "/defaultlib:LIBCTINY.LIB")
 #pragma comment(linker, "/nodefaultlib:libc.lib")
 #pragma comment(linker, "/nodefaultlib:libcmt.lib")

 // section size
 #pragma comment(linker, "/FILEALIGN:16")
 #pragma comment(linker, "/ALIGN:16") 
 #pragma comment(linker, "/OPT:NOWIN98")

 // ºÏ²¢¶Î
/****
 #pragma comment(linker, "/MERGE:.rdata=.data")
 #pragma comment(linker, "/MERGE:.text=.data")
 #pragma comment(linker, "/MERGE:.reloc=.data")
****/
#endif
//end  #ifdef DLL_MIN_SIZE


DLL_API long _C_ TEST_DLL(long s1, long s2);
DLL_API long _C_ GET_DLL_VER_CODE();
DLL_API long _C_ GET_DLL_OK_CODE();
DLL_API long _C_ GET_DLL_ERROR_CODE();
DLL_API long _C_ GET_DLL_MAX_BUFFER_SIZE();

DLL_API long _C_ setStr(LPSTR str);
DLL_API long _C_ getStr(LPSTR a);
DLL_API long _C_ getLen();



#endif
//end  #ifndef DLL_H