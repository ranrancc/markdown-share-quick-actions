@echo off
setlocal
set "ROOT=%~dp0.."
echo Choose an HTML theme:
echo   1. Classic
echo   2. Article
echo   3. Report
echo   4. Reading
echo   5. Interactive
choice /C 12345 /N /M "Theme [1-5]: "
if errorlevel 5 set "THEME=interactive"
if errorlevel 4 if not defined THEME set "THEME=reading"
if errorlevel 3 if not defined THEME set "THEME=report"
if errorlevel 2 if not defined THEME set "THEME=article"
if errorlevel 1 if not defined THEME set "THEME=classic"
py -3 "%ROOT%\md_share.py" html --theme "%THEME%" %*
if errorlevel 1 pause
