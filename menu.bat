@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "VENV_PATH=venv"
set "MENU_SCRIPT=statementOfTheSuccess\menu\menu.py"

set "PYTHON_EXECUTABLE=python"
set "ACTIVATE_SCRIPT=%VENV_PATH%\Scripts\activate"

set IS_CREATE_VENV=0

"%PYTHON_EXECUTABLE%" --version >nul 2>&1
if !errorlevel! equ 1 (
    echo Python не знайдено у системі.
    echo Скачайте та встановіть його: https://www.python.org/downloads/release/python-3810/
    pause
    exit
)

echo Перевірка наявності віртуального середовища...
if not exist "%VENV_PATH%" (
    :CREATED_VENV
    echo Створення віртуального середовища...
    "%PYTHON_EXECUTABLE%" -m venv "%VENV_PATH%"
    set IS_CREATE_VENV=1
    if !errorlevel! equ 1 (
        echo Виникла помилка при створенні віртуального середовища.
        goto end
    )
    echo Віртуальне середовище створено у %VENV_PATH%.
)

echo Активація віртуального середовища
call "%ACTIVATE_SCRIPT%"
if !errorlevel! equ 1 (
    echo Віртуальне середовище пошкоджено. Зачекайте будь ласка...
    goto CREATED_VENV
)

REM Після створення віртуально середовищя, перевіряє оновлення для pip
if %IS_CREATE_VENV%==1 (
    echo Перевірка оновлень для pip...
    "%PYTHON_EXECUTABLE%" -m pip install --upgrade pip
	echo install requirements...
	"%PYTHON_EXECUTABLE%" -m pip install -r requirements.txt
    echo Запуск скрипта "menu.py"
    "%PYTHON_EXECUTABLE%" "%MENU_SCRIPT%" "--CREATE_VENV"
) else (
    echo Запуск скрипта "menu.py"
    "%PYTHON_EXECUTABLE%" "%MENU_SCRIPT%"
)

if !errorlevel! equ 1 (
    echo Помилка при виконанні скрипта 'menu.py'.
)

echo Деактивація віртуального середовища...
call "%VENV_PATH%\Scripts\deactivate.bat"

:end
pause
