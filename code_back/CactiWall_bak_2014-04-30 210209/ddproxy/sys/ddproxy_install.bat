@echo off

echo run...
echo .

del /F /Q C:\Windows\System32\drivers\ddproxy.sys
echo del C:\Windows\System32\drivers\ddproxy.sys
echo .

INSTDRV.EXE /i /s ddproxy.sys
echo install of ddproxy.sys
echo .

pause