@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set PYDIR=%~dp0python-embed
set PYEXE=%PYDIR%\python.exe
set PYVER=3.11.9
set PYZIP=python-%PYVER%-embed-amd64.zip

if not exist "%PYEXE%" (
    echo ===============================================
    echo  Первый запуск - настройка окружения.
    echo  Это займёт пару минут, нужен интернет.
    echo ===============================================

    echo Скачиваю портативный Python %PYVER%...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/%PYVER%/%PYZIP% -OutFile '%~dp0%PYZIP%'"
    if not exist "%~dp0%PYZIP%" (
        echo Не удалось скачать Python. Проверьте интернет-соединение.
        pause
        exit /b 1
    )

    echo Распаковываю...
    powershell -Command "Expand-Archive -Path '%~dp0%PYZIP%' -DestinationPath '%PYDIR%' -Force"
    del "%~dp0%PYZIP%"

    echo Включаю site-packages...
    powershell -Command "(Get-Content '%PYDIR%\python311._pth') -replace '#import site', 'import site' | Set-Content '%PYDIR%\python311._pth'"

    echo Устанавливаю pip...
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile '%~dp0get-pip.py'"
    "%PYEXE%" "%~dp0get-pip.py"
    del "%~dp0get-pip.py"

    echo Устанавливаю зависимости проекта...
    "%PYEXE%" -m pip install -r requirements.txt
)

echo Запускаю приложение...
"%PYEXE%" -m streamlit run app.py

pause
