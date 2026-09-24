"""
Removix Professional Windows Installer Builder
----------------------------------------------
1. Compiles a high-speed directory-based app using PyInstaller (--onedir)
   - Eliminates startup extraction delay: launches in < 1 second!
2. Packages the build with Inno Setup into a professional 'Removix-Setup-v1.0.exe'
   - Clean Windows setup wizard (Next -> Next -> Install)
   - Desktop icon shortcut
   - Start Menu shortcut
   - Clean Windows Uninstaller in Settings / Control Panel
   - Auto-launch option after setup finishes
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ISCC_PATHS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe",
    Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
    Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
]


def find_iscc() -> Path | None:
    for p in ISCC_PATHS:
        if p.exists():
            return p
    which = shutil.which("iscc")
    return Path(which) if which else None


def build():
    print("=" * 70)
    print("  BUILDING REMOVIX PROFESSIONAL WINDOWS INSTALLER (SETUP.EXE)")
    print("  Engine: PyInstaller (--onedir) + Inno Setup (LZMA2 Solid)")
    print("=" * 70)

    iscc_exe = find_iscc()
    if not iscc_exe:
        print("\n[ERROR] Inno Setup compiler (ISCC.exe) not found!")
        print("Please install Inno Setup 6 or run: winget install JRSoftware.InnoSetup")
        return False

    print(f"\n[1/3] Found Inno Setup Compiler: {iscc_exe}")

    # Clean old builds
    shutil.rmtree(ROOT / "build", ignore_errors=True)
    onedir_out = ROOT / "dist" / "Removix"
    if onedir_out.exists():
        shutil.rmtree(onedir_out, ignore_errors=True)

    # 1. Locate LaMa AI Model
    hf_cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--Carve--LaMa-ONNX"
    lama_model = None
    if hf_cache.exists():
        for f in hf_cache.rglob("lama_fp32.onnx"):
            lama_model = f
            break

    datas = [
        f"{ROOT / 'src'};src",
        f"{ROOT / 'before.webp'};.",
        f"{ROOT / 'after.webp'};.",
        f"{ROOT / 'removix.png'};.",
        f"{ROOT / 'removix.ico'};.",
        f"{ROOT / 'removix.svg'};.",
        f"{ROOT / 'lottie.min.js'};.",
        f"{ROOT / 'lottie_scan.json'};.",
    ]

    if lama_model:
        datas.append(f"{lama_model};models")
        print(f"  [+] Bundling LaMa AI Model: {lama_model.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("  [!] WARNING: LaMa model not found in cache! Will download on first run.")

    # 2. Build onedir application with PyInstaller
    print("\n[2/3] Compiling high-speed application directory (--onedir)...")
    cmd_pyi = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name",
        "Removix",
        "--icon",
        str(ROOT / "removix.ico"),
        "--clean",
    ]

    for d in datas:
        cmd_pyi.extend(["--add-data", d])

    cmd_pyi.extend([
        "--collect-all", "webview",
        "--collect-all", "pythonnet",
        "--collect-all", "clr_loader",
        "--collect-all", "onnxruntime",
        "--collect-all", "piexif",
        "--collect-all", "pillow_heif",
        "--collect-all", "pywt",
        "--collect-all", "c2pa",
        "--collect-all", "av",
        "--collect-all", "imageio_ffmpeg",
        "--hidden-import", "clr",
        "--hidden-import", "pythonnet",
        "--hidden-import", "webview",
        "--hidden-import", "webview.platforms.winforms",
        "--hidden-import", "webview.platforms.edgechromium",
        "--hidden-import", "cv2",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "flask",
        "--hidden-import", "jinja2",
        "--hidden-import", "werkzeug",
        "--hidden-import", "huggingface_hub",
        "--hidden-import", "onnxruntime",
        "--hidden-import", "piexif",
        "--hidden-import", "pillow_heif",
        "--hidden-import", "pywt",
        "--hidden-import", "click",
        "--hidden-import", "c2pa",
        "--hidden-import", "av",
        "--hidden-import", "dotenv",
        "--hidden-import", "imageio_ffmpeg",
        "--hidden-import", "cryptography",
        "--hidden-import", "toml",
        "--hidden-import", "requests",
        str(ROOT / "app.py"),
    ])

    proc = subprocess.run(cmd_pyi, cwd=str(ROOT))
    if proc.returncode != 0:
        print("\n[ERROR] PyInstaller compilation failed!")
        return False

    removix_exe = onedir_out / "Removix.exe"
    if not removix_exe.exists():
        print("\n[ERROR] Removix.exe was not created in output directory!")
        return False

    print(f"  [+] Directory build ready at: {onedir_out}")

    # 3. Create Inno Setup Script
    print("\n[3/3] Compiling Windows Installer with Inno Setup...")
    iss_content = f"""[Setup]
AppId={{{{D37F8E32-47C1-4D9A-82B5-1E8548987AC1}}
AppName=Removix
AppVersion=1.0.0
AppVerName=Removix 1.0.0
AppPublisher=Removix AI
AppPublisherURL=https://github.com/shivankthakurr/Removix
AppSupportURL=https://github.com/shivankthakurr/Removix
AppUpdatesURL=https://github.com/shivankthakurr/Removix
DefaultDirName={{autopf}}\\Removix
DisableProgramGroupPage=yes
OutputDir={ROOT / 'dist'}
OutputBaseFilename=Removix-Setup-v1.0
SetupIconFile={ROOT / 'removix.ico'}
UninstallDisplayIcon={{app}}\\Removix.exe
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{onedir_out}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{autoprograms}}\\Removix"; Filename: "{{app}}\\Removix.exe"; IconFilename: "{{app}}\\removix.ico"
Name: "{{autodesktop}}\\Removix"; Filename: "{{app}}\\Removix.exe"; IconFilename: "{{app}}\\removix.ico"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\Removix.exe"; Description: "{{cm:LaunchProgram,Removix}}"; Flags: nowait postinstall skipifsilent
"""

    iss_file = ROOT / "installer.iss"
    iss_file.write_text(iss_content, encoding="utf-8")

    cmd_iscc = [str(iscc_exe), str(iss_file)]
    proc_iscc = subprocess.run(cmd_iscc, cwd=str(ROOT))
    if proc_iscc.returncode != 0:
        print("\n[ERROR] Inno Setup compilation failed!")
        return False

    installer_exe = ROOT / "dist" / "Removix-Setup-v1.0.exe"
    if installer_exe.exists():
        mb = installer_exe.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 70)
        print("  [SUCCESS] INSTALLER BUILD SUCCESSFUL!")
        print(f"  Setup Installer: {installer_exe}")
        print(f"  Installer Size:  {mb:.1f} MB (Solid LZMA2 Compressed)")
        print("  Features:")
        print("    [+] Standard Windows Setup Wizard (Next -> Next -> Install)")
        print("    [+] Automatic Desktop Shortcut with Removix Logo Icon")
        print("    [+] Start Menu Shortcut Added")
        print("    [+] Installed App Launches INSTANTLY in < 1 second!")
        print("    [+] Clean Windows Uninstaller included")
        print("=" * 70)
        return True

    return False


if __name__ == "__main__":
    build()
