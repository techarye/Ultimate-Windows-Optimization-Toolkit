::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFAlVXA2GAE+1BaAR7ebv/NayrlkUWeMrfbjS1LCBN/Mn/UDlfoUR0ntOmfcAAxxXMBuoYW8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFAlVXA2GAE+1BaAR7ebv/NayrlkUWeMrfbjS1LCBN/Mn/UDlfoUR23tTlvQYAxRUdRu/IAosrA4=
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:CHECK_PYTHON
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Running install_python.ps1 to install Python...
    powershell -ExecutionPolicy Bypass -File data\install_python.ps1
    if errorlevel 1 (
        echo Failed to install Python. Please install it manually and rerun this script.
        pause
        exit /b 1
    )
) else (
    echo Python is installed.
)

:MENU
title Ultimate Windows Optimization Toolkit by github.com/techarye
cls
echo ============================================
echo   Ultimate Windows Optimization Toolkit
echo   By github.com/techarye
echo ============================================
echo.
echo Select category to apply tweaks:
echo.
echo 1. General System Tweaks
echo 2. Gamer Tweaks
echo 3. Business Tweaks
echo 4. Work Tweaks
echo 5. Storage Tweaks
echo 6. CPU/Network/Security Tweaks
echo 7. Programmer Tweaks
echo 8. Remove Bloatware
echo.
echo 9. Open GitHub Repository
echo.
echo 0. Exit
echo.
set /p choice=Enter your choice [0-9]:

if "%choice%"=="1" python data\categories\general_tweaks.py & pause & goto MENU
if "%choice%"=="2" python data\categories\gamer_tweaks.py & pause & goto MENU
if "%choice%"=="3" python data\categories\business_tweaks.py & pause & goto MENU
if "%choice%"=="4" python data\categories\work_tweaks.py & pause & goto MENU
if "%choice%"=="5" python data\categories\storage_tweaks.py & pause & goto MENU
if "%choice%"=="6" python data\categories\cpu_network_security_tweaks.py & pause & goto MENU
if "%choice%"=="7" python data\categories\programmer_tweaks.py & pause & goto MENU
if "%choice%"=="8" python data\categories\remove_bloatware.py & pause & goto MENU
if "%choice%"=="9" start https://github.com/techarye/Ultimate-Windows-Optimization-Toolkit & pause & goto MENU
if "%choice%"=="0" exit /b

echo Invalid option. Try again.
pause
goto MENU
