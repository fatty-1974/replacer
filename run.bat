@echo off
echo Обновление pip...
python -m pip install --upgrade pip >nul 2>&1
python src/main.py
if %errorlevel% neq 0 (
    echo Ошибка запуска приложения!
    pause
    exit /b 1
)
