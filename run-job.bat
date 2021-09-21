@echo off
set LOGFILE=batch.log
echo starting todoist-to-notion at %date% %time%
call :LOG >> %LOGFILE%
exit /B

call conda init
call conda activate productivity-2
call python todoist-to-notion.py
call conda deactivate
