@echo off
setlocal enabledelayedexpansion

cd /d C:\code\kol_daily_summary

:: ── 設定 log 路徑 ──────────────────────────────────────────────
if not exist logs mkdir logs
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set YY=%%a
    set MM=%%b
    set DD=%%c
)
set TODAY=%YY%-%MM%-%DD%
set LOGFILE=logs\phase1_%TODAY%.log
set TMPOUT=logs\_tmp_phase1.txt

:: ── 紀錄開始 ────────────────────────────────────────────────────
for /f "tokens=1-2 delims=." %%a in ("%time: =0%") do set HHMM=%%a:%%b
echo ============================================================ >> "%LOGFILE%"
echo [START] %TODAY% %time% >> "%LOGFILE%"
echo ============================================================ >> "%LOGFILE%"

:: ── 啟動虛擬環境 ─────────────────────────────────────────────────
call venv\Scripts\activate.bat >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo [ERROR] venv 啟動失敗 >> "%LOGFILE%"
    echo [RESULT] FAILED - venv 啟動失敗 >> "%LOGFILE%"
    echo [END] %time% >> "%LOGFILE%"
    echo. >> "%LOGFILE%"
    exit /b 1
)

:: ── Step 1：RSS 檢查 + Whisper 轉錄 ─────────────────────────────
echo. >> "%LOGFILE%"
echo [STEP 1] run_all.py --max-episodes 2  (%time%) >> "%LOGFILE%"
echo ------------------------------------------------------------ >> "%LOGFILE%"
python scripts\run_all.py --max-episodes 2 >> "%LOGFILE%" 2>&1
set STEP1_ERR=%errorlevel%
if %STEP1_ERR% neq 0 (
    echo [ERROR] run_all.py 結束碼 %STEP1_ERR% >> "%LOGFILE%"
) else (
    echo [OK] run_all.py 完成 >> "%LOGFILE%"
)

:: ── Step 2：套用 dictionary 前處理 ──────────────────────────────
echo. >> "%LOGFILE%"
echo [STEP 2] preprocess.py  (%time%) >> "%LOGFILE%"
echo ------------------------------------------------------------ >> "%LOGFILE%"
python scripts\preprocess.py >> "%LOGFILE%" 2>&1
set STEP2_ERR=%errorlevel%
if %STEP2_ERR% neq 0 (
    echo [ERROR] preprocess.py 結束碼 %STEP2_ERR% >> "%LOGFILE%"
) else (
    echo [OK] preprocess.py 完成 >> "%LOGFILE%"
)

:: ── 整體結果 ─────────────────────────────────────────────────────
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

exit /b %EXIT_CODE%
