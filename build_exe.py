"""
Removix Desktop Executable Builder
----------------------------------
Builds a standalone, native windowed Removix.exe using PyInstaller.
- No black CMD console window (--windowed)
- Embedded custom Removix logo icon (--icon removix.ico)
- Bundled native WebView2 desktop window (pywebview)
- 3-tier hardware fallback (CUDA -> DirectML -> CPU)
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build():
    print("=" * 65)
    print("  BUILDING REMOVIX NATIVE DESKTOP EXECUTABLE (.EXE)")
    print("  Mode: Windowed (No CMD) | Icon: removix.ico | GPU: DirectML/CUDA/CPU")
    print("=" * 65)
    
    datas = [
        f"{ROOT / 'src'};src",
        f"{ROOT / 'before.webp'};.",
        f"{ROOT / 'after.webp'};.",
        f"{ROOT / 'removix logo.svg'};.",
        f"{ROOT / 'removix.ico'};.",
        f"{ROOT / 'lottie.min.js'};.",
        f"{ROOT / 'lottie_scan.json'};.",
    ]
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "Removix",
        "--icon", str(ROOT / "removix.ico"),
        "--clean",
    ]
    
    for d in datas:
        cmd.extend(["--add-data", d])
        
    cmd.extend([
        "--collect-all", "webview",
        "--collect-all", "pythonnet",
        "--collect-all", "clr_loader",
        "--collect-all", "onnxruntime",
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
        str(ROOT / "app.py"),
    ])
    
    print("\nRunning command:")
    print(" ".join(cmd))
    print("\nCompiling standalone executable... (this takes ~2-3 minutes)")
    
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode == 0:
        exe_path = ROOT / "dist" / "Removix.exe"
        if exe_path.exists():
            mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n" + "=" * 65)
            print("  BUILD SUCCESSFUL!")
            print(f"  Output Executable: {exe_path}")
            print(f"  Total Size:        {mb:.1f} MB")
            print("  Features:")
            print("    [+] Silent Native Window (No Black CMD)")
            print("    [+] Custom Removix Logo Icon Embedded")
            print("    [+] Microsoft Edge WebView2 Modern Chromium GUI")
            print("    [+] Multi-Tier GPU Acceleration (CUDA / DirectML / CPU)")
            print("=" * 65)
            return True
    print("\nBUILD FAILED with exit code:", proc.returncode)
    return False

if __name__ == "__main__":
    build()
