@echo off
echo Очистка временных файлов...
rmdir /s /q __pycache__ 2>nul
rmdir /s /q src\__pycache__ 2>nul
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul
echo Очистка завершена!
pause