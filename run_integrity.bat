@echo off
REM ------------------------------------------------------------
REM Portable File Integrity Checker Batch Script
REM Features:
REM - Activates the virtual environment
REM - Asks user for folder path to scan (no hardcoding)
REM - Works even if project folder is moved
REM - Automatically opens latest HTML report
REM -------------------------------------------------------------

REM Get the current directory ( where this .bat file is located)
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM Activate the virtual environment
call venv\Scripts\Activate

REM Prompt user to enter the folder path to scan
set /p FOLDER_PATH="Enter the folder path to scan: "

REM Run the main integrity checker with the user-provided folder path
python main.py "%FOLDER_PATH%"

REM Find and open the most recent HTML report
set "REPORTS_DIR=%PROJECT_DIR%reports"
set "LATEST_REPORT="

for /f "delims=" %%f in ('dir /b /a:-d /o:-d "%REPORTS_DIR%\report_*.html"') do (
    set "LATEST_REPORT=%%f"
    goto :open_report
)

:open_report
if defined LATEST_REPORT (
    echo.
    echo Opening latest report: %LATEST_REPORT%
    start "" "%REPORTS_DIR%\%LATEST_REPORT%"
) else (
    echo No report found to open.
)

echo.
pause
