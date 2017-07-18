#ifdef DLL_API
#else
#define extern "C" DLL_API _declspec(dllimport)
#endif

#include <windows.h>

DLL_API int _stdcall add(int a,int b);
DLL_API BOOL  _stdcall addString(LPSTR a);
DLL_API BOOL  _stdcall getString(LPSTR a);
DLL_API int  _stdcall getStringSize();