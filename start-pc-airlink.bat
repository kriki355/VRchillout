@echo off
chcp 65001 >nul
cd /d "%~dp0"
title VR-шоурум: запуск через Air Link
start "VR-шоурум: сервер" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"
timeout /t 2 >nul
where chrome >nul 2>nul && (start "" chrome http://localhost:8080/ & goto opened)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" http://localhost:8080/ & goto opened)
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (start "" "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" http://localhost:8080/ & goto opened)
start "" msedge http://localhost:8080/
:opened
echo.
echo  Страница открыта в браузере на компьютере: http://localhost:8080
echo  1. В шлеме включите Air Link и подключитесь к компьютеру.
echo  2. На странице нажмите «Войти в VR» — картинка уйдёт в шлем.
echo  Держите открытой только одну вкладку с шоурумом.
echo.
pause
