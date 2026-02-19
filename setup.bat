@echo off
REM Initializing script location and activate.bat file path
set "SCRIPT_DIR=%~dp0"
set "FILE_PATH=%SCRIPT_DIR%venv\Scripts\activate.bat"

REM Remove trailing backslash if needed
REM if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Show the resolved paths
REM echo Script directory: %SCRIPT_DIR%
REM echo File path: %FILE_PATH%

REM run the bat script
call %FILE_PATH%
REM navigate to the sources folder
cd src