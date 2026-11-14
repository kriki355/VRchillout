@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Картинка из Quest 2 на ноутбук (scrcpy)
echo.
echo  Показ картинки из шлема на ноутбуке по кабелю USB, без Meta Link.
echo  1. Подключите Quest 2 кабелем. В шлеме разрешите отладку по USB, если спросит.
echo  2. Нужна программа scrcpy версии 3 или новее: распакуйте её в папку scrcpy рядом с этим файлом.
echo.
set "SC="
if exist "%~dp0scrcpy\scrcpy.exe" set "SC=%~dp0scrcpy\scrcpy.exe"
if not defined SC for /d %%D in ("%~dp0scrcpy-win64-*") do if exist "%%D\scrcpy.exe" set "SC=%%D\scrcpy.exe"
if not defined SC ( where scrcpy >nul 2>nul && set "SC=scrcpy" )
if not defined SC (
  echo  scrcpy не найден. Открываю страницу загрузки: скачайте scrcpy-win64-v3.x.zip,
  echo  распакуйте рядом с этим файлом и запустите его снова.
  start "" https://github.com/Genymobile/scrcpy/releases/latest
  pause
  exit /b 1
)
echo  Запускаю. Окно можно растянуть на весь экран клавишей F11 или Alt+Enter.
"%SC%" --crop 1730:974:1934:450 --max-fps 60 --video-bit-rate 16M --no-audio --window-title "Quest 2 — VR-шоурум"
if errorlevel 1 (
  echo.
  echo  Не получилось. Проверьте кабель и разрешение отладки в шлеме.
  echo  Если видно обе линзы сразу — обновите scrcpy до версии 3.
  pause
)
