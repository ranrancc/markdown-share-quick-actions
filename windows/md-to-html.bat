@echo off
setlocal
set "ROOT=%~dp0.."
py -3 "%ROOT%\md_share.py" html %*
if errorlevel 1 pause
