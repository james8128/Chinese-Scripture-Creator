@echo off
REM %~n0 = batch file name without extension
REM %~dp0 = drive + path of the batch file

set scriptname=%~n0
set scriptpath=%~dp0%scriptname%.py

python "%scriptpath%" %*

PAUSE
