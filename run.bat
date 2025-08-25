@echo off
setlocal
cd /D D:\Python\LevelUp_bot

rem
set "HTTP_PROXY="
set "http_proxy="
set "https_proxy="
set "HTTPS_PROXY="
set "ALL_PROXY="
set "all_proxy="
set "NO_PROXY=127.0.0.1,localhost,::1="
set "no_proxy=127.0.0.1,localhost,::1="

@REM echo Установка кодировки UTF-8. Для отображения эмоджи
@REM chcp 65001 > nul

D:\Python\LevelUp_bot\venv\Scripts\python.exe main.py 1>LogCMD.txt 2>&1

endlocal