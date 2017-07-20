@echo off
MODE con: COLS=120 LINES=15
cls
echo   批处理正在初始化中……
color 1a
echo.
set/p=  ■<nul
for /L %%i in (1 1 36) do set /p a=■<nul&ping /n 1 127.0.0.1>nul
echo                                                              已完成 100%%
echo.

MODE con: COLS=120 LINES=30
title  程序运行器——XXX

:menu
echo.
echo.
echo                  ───────────────——————
echo                  请选择需要运行的程序，然后按回车执行
echo                  ───────────────——————

echo.
echo      【1】.xxx_guild_player_fwq.py      【2】.xxx_guild_sina.py 
echo.  
echo      【3】.xxx_guild_laoyuegou.py       【4】.xxx_guild_list_check.py  
echo. 
echo      【5】.xxx_guild_player_check.py    【6】.json_mysqlexU.py      
echo. 
echo      【7】.down_ah.py	【8】.get_status.py   【9】.关机  【0】.退出  
echo.
echo.
echo.
:opt
set /p run= 请输入您的选择:
IF NOT "%run%"=="" SET run=%run:~0,1%
if /i "%run%"=="1" goto mark_1
if /i "%run%"=="2" goto mark_2
if /i "%run%"=="3" goto mark_3
if /i "%run%"=="4" goto mark_4
if /i "%run%"=="5" goto mark_5
if /i "%run%"=="6" goto mark_6
if /i "%run%"=="7" goto mark_7
if /i "%run%"=="8" goto mark_8
if /i "%run%"=="9" goto mark_9
if /i "%run%"=="0" goto exit

echo 输入无效，请重新输入，是输入数字哦！
echo.
goto menu


:mark_1
@ECHO    xxx_guild_player_fwq.py ，执行！！ 
@ECHO    注意，此任务耗时很久，默认结束后关机 ！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python xxx_guild_player_fwq.py 

@ping -n 3 127.0.0.1 >nul
@ECHO    任务结束，准备关机 ！！
shutdown123.bat

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu



@echo off
:mark_2
@ECHO    xxx_guild_sina.py ，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python xxx_guild_sina.py  

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu



@echo off 
:mark_3
@ECHO    xxx_guild_laoyuegou.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python xxx_guild_laoyuegou.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu

@echo off 
:mark_4
@ECHO    xxx_guild_list_check.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python xxx_guild_list_check.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu

@echo off 
:mark_5
@ECHO    xxx_guild_player_check.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python xxx_guild_player_check.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu

 

@echo off 
:mark_6
@ECHO    json_mysqlexU.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python json_mysqlexU.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu


@echo off 
:mark_7
@ECHO    down_ah.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python down_ah.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu



@echo off 
:mark_8
@ECHO    get_status.py，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........
@ECHO.

python get_status.py 

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu


@echo off
:mark_9
@ECHO    你选择了 关机，执行！！
@ECHO.
@ping -n 2 127.0.0.1 >nul
@ECHO    程序正在执行.........

shutdown123.bat

@ping -n 3 127.0.0.1 >nul

@ECHO    程序已执行完毕，请按任意键返回...
@PAUSE >NUL
goto menu