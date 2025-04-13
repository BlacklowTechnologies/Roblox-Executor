@echo off
title Python & pip Setup + Launch bootstrapper.py
color 0A

echo Checking for Python...

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
    echo Downloading Python installer...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -UseShellExecute $true"
    echo Please install Python, then re-run this script.
    pause
    exit
)

echo Python is installed.

echo ------------------------------
echo Checking pip...

pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip not found. Installing pip...
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
) ELSE (
    echo pip is installed.
)

echo ------------------------------
echo Installing required packages...

REM Ajoute ici tous les modules Python nécessaires
python -m pip install cloudyapi

echo ------------------------------
echo Launching bootstrapper.py...

REM Lancer ton fichier bootstrapper.py
python bootstrapper.py

echo ------------------------------
echo Done.
pause
