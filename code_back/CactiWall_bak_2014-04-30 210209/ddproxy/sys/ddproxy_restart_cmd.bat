@echo off

echo run...

net stop ddproxy

ping -n 3 127.0.0.1>nul

echo stop ddproxy
echo .
pause


net start ddproxy
echo start ddproxy
echo .
pause