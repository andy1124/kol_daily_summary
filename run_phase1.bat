@echo off
cd /d C:\code\kol_daily_summary
call venv\Scripts\activate.bat
python scripts\run_all.py --max-episodes 2
python scripts\preprocess.py