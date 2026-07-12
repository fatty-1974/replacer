echo Обновление pip...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка установки PyInstaller!
    pause
    exit /b 1
)
echo Компиляция в исполняемый файл...
pyinstaller --noconsole --onefile --add-data "src\logo.png;." --icon=src\logo.ico src/main.py
if %errorlevel% neq 0 (
    echo Ошибка компиляции!
    pause
    exit /b 1
)
echo Компиляция завершена! Исполняемый файл находится в папке dist
pause
