; Inno Setup Script for PDF OCR Desktop Application
; This creates a professional Windows installer with wizard interface

#define MyAppName "PDF OCR Text Extractor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PDF Tools"
#define MyAppURL "https://github.com/yourusername/pdf-tools"
#define MyAppExeName "PDF_OCR.exe"
#define MyAppId "{{PDF-OCR-TEXT-EXTRACTOR}"

[Setup]
; Application information
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output configuration
OutputDir=Output
OutputBaseFilename=PDF_OCR_Setup_{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes

; Installer interface
WizardStyle=modern
SetupIconFile=app_icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; License and info files
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main application files (from PyInstaller output)
Source: "dist\PDF_OCR\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Tesseract installer
Source: "installer_files\tesseract-installer.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

; Documentation
Source: "README.md"; DestDir: "{app}"; DestName: "README.txt"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop shortcut (if selected)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Install Tesseract OCR
Filename: "{tmp}\tesseract-installer.exe"; Parameters: "/VERYSILENT /NORESTART /DIR=""{autopf}\Tesseract-OCR"""; StatusMsg: "Installing Tesseract OCR..."; Flags: waituntilterminated

; Run the application after installation (optional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Add Tesseract to PATH for the application
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{autopf}\Tesseract-OCR"; \
    Check: NeedsAddPath('{autopf}\Tesseract-OCR')

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Notify user about Tesseract installation
    MsgBox('Tesseract OCR has been installed. The application is now ready to use.', 
           mbInformation, MB_OK);
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
