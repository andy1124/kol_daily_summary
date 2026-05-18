@echo off
setlocal enabledelayedexpansion

cd /d C:\code\kol_daily_summary

:: Create logs directory if needed
if not exist logs mkdir logs

:: Get today's date via PowerShell (avoids locale-dependent %%date%% parsing)
powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'" > "%TEMP%\kol_today.tmp"
set /p TODAY=< "%TEMP%\kol_today.tmp"
del "%TEMP%\kol_today.tmp" 2>nul

set LOGFILE=logs\phase1_%TODAY%.log

:: Log start
echo ============================================================ >> "%LOGFILE%"
echo [START] %TODAY% %time% >> "%LOGFILE%"
echo ============================================================ >> "%LOGFILE%"

:: Force Python stdout/stderr to UTF-8 regardless of system codepage
set PYTHONUTF8=1

:: Activate venv
call venv\Scripts\activate.bat >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] venv activation failed >> "%LOGFILE%"
    echo [RESULT] FAILED - venv activation failed >> "%LOGFILE%"
    echo [END] %time% >> "%LOGFILE%"
    echo. >> "%LOGFILE%"
    echo Failed. See %LOGFILE%
    pause
    exit /b 1
)

:: Step 1: RSS check + Whisper transcription
echo. >> "%LOGFILE%"
echo [STEP 1] run_all.py --max-episodes 2  (%time%) >> "%LOGFILE%"
echo ------------------------------------------------------------ >> "%LOGFILE%"
python scripts\run_all.py --max-episodes 2 >> "%LOGFILE%" 2>&1
set STEP1_ERR=%errorlevel%
if %STEP1_ERR% neq 0 (
    echo [ERROR] run_all.py exit code %STEP1_ERR% >> "%LOGFILE%"
) else (
    echo [OK] run_all.py done >> "%LOGFILE%"
)

:: Step 2: Apply dictionary preprocessing
echo. >> "%LOGFILE%"
echo [STEP 2] preprocess.py  (%time%) >> "%LOGFILE%"
echo ------------------------------------------------------------ >> "%LOGFILE%"
python scripts\preprocess.py >> "%LOGFILE%" 2>&1
set STEP2_ERR=%errorlevel%
if %STEP2_ERR% neq 0 (
    echo [ERROR] preprocess.py exit code %STEP2_ERR% >> "%LOGFILE%"
) else (
    echo [OK] preprocess.py done >> "%LOGFILE%"
)

:: Overall result
echo. >> "%LOGFILE%"
if %STEP1_ERR% neq 0 (
    echo [RESULT] FAILED  ^(run_all.py=%STEP1_ERR%, preprocess.py=%STEP2_ERR%^) >> "%LOGFILE%"
    set EXIT_CODE=1
) else if %STEP2_ERR% neq 0 (
    echo [RESULT] PARTIAL ^(run_all.py=OK, preprocess.py=%STEP2_ERR%^) >> "%LOGFILE%"
    set EXIT_CODE=2
) else (
    echo [RESULT] SUCCESS >> "%LOGFILE%"
    set EXIT_CODE=0
)
echo [END] %time% >> "%LOGFILE%"
echo. >> "%LOGFILE%"

echo.
echo Done. Log: %LOGFILE%
echo.
pause

exit /b %EXIT_CODE%
