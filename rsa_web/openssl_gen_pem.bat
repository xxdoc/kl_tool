@echo off
set path==%path%;"F:\Program Files\Git\usr\bin\"
openssl genrsa -out .\pem\www_priv.pem 1024
openssl rsa -pubout -in .\pem\www_priv.pem -out .\pem\www_pub.pem

@echo off
for /l %%i in (1,1,100) do @openssl genrsa -out .\pem\%%i_priv.pem 1024
for /l %%i in (1,1,100) do @openssl rsa -pubout -in .\pem\%%i_priv.pem -out .\pem\%%i_pub.pem
pause