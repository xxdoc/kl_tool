#ifdef DLL_API
#else
#define extern "C" DLL_API _declspec(dllimport)
#endif

#include <windows.h>

DLL_API bool _stdcall addMD5(LPSTR md5str,LPSTR astr,long sta,long end);
DLL_API bool _stdcall getMD5(LPSTR a);
DLL_API int  _stdcall getStringSize();
DLL_API int  _stdcall MD5Initx (int ix);
DLL_API int  _stdcall MD5Updatex (int ix , LPSTR astr , long len);
DLL_API int  _stdcall MD5Finalx (int ix , LPSTR md5str);
DLL_API int  _stdcall MD5state (int ix);

