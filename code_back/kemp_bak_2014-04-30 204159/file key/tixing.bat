@echo off
echo 你好，你设置的提醒时间到了：
echo 提醒开始于2011-5-22 19:41:48----延时为4380秒
set /p word=按任意键退出，当然别按f和s，切忌别按f：
if /i %word%==f  %systemroot%\system32\shutdown -f -s -t 10
if /i %word%==s  %systemroot%\system32\shutdown -f -s -t 150
cls
:yn
set /p word=输入Y取消关机，输入N退出：
if /i %word%==y %systemroot%\system32\shutdown -a&&goto :eof
if /i %word%==m %systemroot%\system32\shutdown -a&&goto :min
if /i %word%==r goto :start
if /i %word%==n (goto :eof) else (cls&&echo 输入有误,输入R重新关机!&&%systemroot%\system32\shutdown -a&&goto :yn)
:min
set /p word=输入等待关机时间（单位：分钟），F强制关机，R重启：
if /i %word%==0 (%systemroot%\system32\shutdown -f -s -t 30)&&goto :yn
if /i %word%==1 (%systemroot%\system32\shutdown -f -s -t 60)&&goto :yn
if /i %word%==2 (%systemroot%\system32\shutdown -f -s -t 120)&&goto :yn
if /i %word%==3 (%systemroot%\system32\shutdown -f -s -t 180)&&goto :yn
if /i %word%==4 (%systemroot%\system32\shutdown -f -s -t 240)&&goto :yn
if /i %word%==5 (%systemroot%\system32\shutdown -f -s -t 300)&&goto :yn
if /i %word%==f (%systemroot%\system32\shutdown -f -s -t 0)&&goto :yn
if /i %word%==r (%systemroot%\system32\shutdown -f -r -t 10&&goto :yn) else (cls&&echo 输入有误,重新关机!&&goto :start)
