#!/usr/bin/env python3
"""
TASKY Build Script
Creates a standalone executable for distribution
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

try:
    import PyInstaller
    PYINSTALLER_AVAILABLE = True
except ImportError:
    PYINSTALLER_AVAILABLE = False

def check_dependencies():
    """Check if required build tools are installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            print("Please install manually: pip install pyinstaller")
            return False
    return True

def clean_build():
    """Clean previous build artifacts."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}")

def build_executable():
    """Build the TASKY executable."""
    print("🔨 Building TASKY executable...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=TASKY",
        "--icon=icon.ico",
        "--add-data=ui;ui",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui", 
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=win10toast",
        "--hidden-import=sqlite3",
        "--hidden-import=asyncio",
        "--hidden-import=threading",
        "--hidden-import=winsound",
        "main.py"
    ]
    
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_distribution():
    """Create the distribution package."""
    print("📦 Creating distribution package...")
    
    dist_dir = "TASKY-Distribution"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    if os.path.exists("dist/TASKY.exe"):
        shutil.copy2("dist/TASKY.exe", f"{dist_dir}/TASKY.exe")
        print("✅ Copied TASKY.exe")
    else:
        print("❌ TASKY.exe not found in dist folder")
        return False
    
    docs = ["README.md", "USER_MANUAL.md", "LICENSE"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, f"{dist_dir}/{doc}")
            print(f"✅ Copied {doc}")
    
    install_txt = """TASKY - Installation Instructions
=====================================

1. Extract this ZIP file to any folder
2. Double-click TASKY.exe to run
3. No Python installation required!
4. No additional dependencies needed!

Note: Windows Defender may show a warning because this is a custom application.
Click "More info" and then "Run anyway" to use TASKY.

For help, read USER_MANUAL.md

Enjoy TASKY! 🎉
"""
    
    with open(f"{dist_dir}/INSTALL.txt", "w", encoding="utf-8") as f:
        f.write(install_txt)
    print("✅ Created INSTALL.txt")
    
    version_info = """TASKY v1.0.0
============

Features:
- Task Management (Create, Edit, Delete, Complete)
- Time Tracking
- Smart Notifications
- Dark/Light Themes
- Real-time Search
- Live Statistics
- Keyboard Shortcuts

System Requirements:
- Windows 10/11
- 100MB RAM
- 50MB disk space

Made with ❤️ by the TASKY Team
"""
    
    with open(f"{dist_dir}/VERSION.txt", "w", encoding="utf-8") as f:
        f.write(version_info)
    print("✅ Created VERSION.txt")
    
    return True

def create_zip():
    """Create a ZIP file for easy distribution."""
    print("📦 Creating ZIP archive...")
    
    try:
        import zipfile
        
        with zipfile.ZipFile("TASKY-v1.0.0-Windows.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("TASKY-Distribution"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, "TASKY-Distribution")
                    zipf.write(file_path, arcname)
        
        print("✅ Created TASKY-v1.0.0-Windows.zip")
        return True
    except Exception as e:
        print(f"❌ Failed to create ZIP: {e}")
        return False

def main():
    """Main build process."""
    print("🚀 TASKY Build Process Started")
    print("=" * 40)
    
    if not check_dependencies():
        print("❌ Dependency check failed. Exiting.")
        return
    
    clean_build()
    
    if not build_executable():
        print("❌ Build failed. Exiting.")
        return
    
    if not create_distribution():
        print("❌ Distribution creation failed. Exiting.")
        return
    
    if not create_zip():
        print("❌ ZIP creation failed.")
    
    print("\n🎉 TASKY Build Process Completed!")
    print("=" * 40)
    print("📁 Distribution folder: TASKY-Distribution/")
    print("📦 ZIP file: TASKY-v1.0.0-Windows.zip")
    print("\n📤 Share the ZIP file with your friends!")
    print("💡 They can extract and run TASKY.exe directly")

if __name__ == "__main__":
    main()
