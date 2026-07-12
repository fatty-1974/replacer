; installer.iss
; Inno Setup Unicode script

[Setup]
AppName=DOCX Замена текста
AppVersion=1.0.3
AppPublisher=Алексей
DefaultDirName={autopf}\DOCX Replacer
DefaultGroupName=DOCX Replacer
OutputBaseFilename=DOCX_Replacer_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
DisableProgramGroupPage=no
UninstallDisplayIcon={app}\main.exe

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
; Основной exe (onefile) — путь к твоему проекту
Source: "C:\Users\Али\Desktop\ПИТОН\replacer\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; Дополнительные ресурсы (опционально)
; Source: "app.ico"; DestDir: "{app}"; Flags: ignoreversion
; Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion

; VC++ Redistributable — положи эти файлы рядом со скриптом или укажи абсолютный путь
Source: "vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "vc_redist.x86.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\DOCX Replacer"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\DOCX Replacer"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительно:"; Flags: unchecked

[Run]
; На 64‑битной системе устанавливаем x64 и x86, на 32‑битной только x86
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "Установка Visual C++ Redistributable x64..."; Flags: runhidden waituntilterminated; Check: Is64BitInstallMode
Filename: "{tmp}\vc_redist.x86.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "Установка Visual C++ Redistributable x86..."; Flags: runhidden waituntilterminated

; Запуск приложения после установки (опционально)
Filename: "{app}\main.exe"; Description: "Запустить DOCX Replacer"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\*"
