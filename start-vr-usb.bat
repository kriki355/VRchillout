@echo off
chcp 65001 >nul
cd /d "%~dp0"
title VR-шоурум: запуск в шлеме по кабелю
echo.
echo  1. Подключите Quest 2 к компьютеру кабелем USB.
echo  2. В шлеме разрешите отладку по USB, если спросит.
echo.
set "ADB="
if exist "%LOCALAPPDATA%\Programs\SideQuest\resources\app.asar.unpacked\build\platform-tools\adb.exe" set "ADB=%LOCALAPPDATA%\Programs\SideQuest\resources\app.asar.unpacked\build\platform-tools\adb.exe"
if not defined ADB (
  where adb >nul 2>nul && set "ADB=adb"
)
if not defined ADB if exist "C:\platform-tools\adb.exe" set "ADB=C:\platform-tools\adb.exe"
if not defined ADB (
  echo  Не нашёл adb. Установите SideQuest или Android Platform-Tools в C:\platform-tools
  pause
  exit /b 1
)
start "VR-шоурум: сервер" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"
timeout /t 2 >nul
"%ADB%" devices
"%ADB%" reverse tcp:8080 tcp:8080
if errorlevel 1 (
  echo.
  echo  Шлем не найден. Проверьте кабель и разрешение отладки в шлеме, потом запустите этот файл ещё раз.
  pause
  exit /b 1
)
"%ADB%" shell am start -a android.intent.action.VIEW -d http://localhost:8080/ com.oculus.browser >nul 2>nul
echo.
echo  Готово. В шлеме откроется страница http://localhost:8080 — нажмите «Войти в VR».
echo  Если не открылась — откройте браузер в шлеме и введите этот адрес вручную.
echo.
pause
