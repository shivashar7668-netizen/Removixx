[Setup]
AppId={{D37F8E32-47C1-4D9A-82B5-1E8548987AC1}
AppName=Removix
AppVersion=1.0.0
AppVerName=Removix 1.0.0
AppPublisher=Shivank Thakur
AppPublisherURL=https://github.com/shivankthakurr/Removix
AppSupportURL=https://github.com/shivankthakurr/Removix
AppUpdatesURL=https://github.com/shivankthakurr/Removix
DefaultDirName={autopf}\Removix
DisableProgramGroupPage=yes
OutputDir=C:\Users\Production\Documents\Removix\Removix\dist
OutputBaseFilename=Removix-Setup-v1.0
SetupIconFile=C:\Users\Production\Documents\Removix\Removix\removix.ico
UninstallDisplayIcon={app}\removix.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "C:\Users\Production\Documents\Removix\Removix\dist\Removix\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Production\Documents\Removix\Removix\removix.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Removix"; Filename: "{app}\Removix.exe"; IconFilename: "{app}\removix.ico"; IconIndex: 0
Name: "{autodesktop}\Removix"; Filename: "{app}\Removix.exe"; IconFilename: "{app}\removix.ico"; IconIndex: 0; Tasks: desktopicon

[Run]
Filename: "{app}\Removix.exe"; Description: "{cm:LaunchProgram,Removix}"; Flags: nowait postinstall skipifsilent
