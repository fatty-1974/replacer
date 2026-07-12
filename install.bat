@echo off
echo Обновление pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Ошибка обновления pip. Продолжаем установку...
)
echo Установка зависимостей...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Ошибка установки зависимостей!
    pause
    exit /b 1
)
echo Установка завершена!
pause
