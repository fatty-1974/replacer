import os
import sys
from datetime import datetime

APP_NAME = "DOCX Замена текста"
APP_VERSION = "1.0.3"
APP_AUTHOR = "Алексей Зотов"
APP_DESCRIPTION = (
    "Программа предназначена для массовой замены текста "
    "в документах .docx с сохранением структуры."
)

def get_compile_date():
    # Если запущено как EXE
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
        timestamp = os.path.getmtime(exe_path)
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")

    # Если запущено как обычный .py (отладка)
    script_path = __file__
    timestamp = os.path.getmtime(script_path)
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")

