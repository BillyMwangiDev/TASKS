#!/usr/bin/env python3
"""
TASKY Build Script — Cross-Platform (Windows & macOS)
Creates a standalone executable/bundle for distribution.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

APP_NAME = "TASKY"
VERSION = "2.0.0"
IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"


def check_dependencies():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  npm not found — skipping frontend build (web/dist must already exist)")

    return True


def build_frontend():
    web_dir = Path("web")
    if not web_dir.exists():
        print("⚠️  'web' directory not found — skipping frontend build")
        return False

    try:
        if not (web_dir / "node_modules").exists():
            subprocess.run(["npm", "install"], cwd=web_dir, check=True)
        subprocess.run(["npm", "run", "build"], cwd=web_dir, check=True)
        print("✅ Frontend built")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend build failed: {e}")
        return False


def prepare_icons():
    """Create platform-appropriate icons from icon.png / icon.iconset."""
    icon_png = Path("icon.png")
    if not icon_png.exists():
        print("⚠️  icon.png not found — no icon will be embedded")
        return None

    if IS_MAC:
        # Prefer iconutil (uses the pre-built iconset if present)
        iconset = Path("icon.iconset")
        if iconset.exists():
            try:
                subprocess.run(
                    ["iconutil", "-c", "icns", str(iconset), "-o", "icon.icns"],
                    check=True,
                )
                print("✅ Created icon.icns via iconutil")
                return "icon.icns"
            except subprocess.CalledProcessError:
                pass  # fall through to Pillow

        # Pillow fallback
        try:
            from PIL import Image  # type: ignore[import]
            img = Image.open(icon_png).convert("RGBA")
            img.save("icon.icns")
            print("✅ Created icon.icns via Pillow")
            return "icon.icns"
        except Exception as e:
            print(f"⚠️  Could not create icon.icns: {e}")
            return str(icon_png)

    elif IS_WINDOWS:
        # Create a proper multi-resolution .ico from the iconset PNGs
        ico_path = Path("icon.ico")
        try:
            from PIL import Image  # type: ignore[import]
            sizes = [16, 32, 48, 64, 128, 256]
            images = []
            iconset = Path("icon.iconset")
            for size in sizes:
                candidate = iconset / f"icon_{size}x{size}.png" if iconset.exists() else None
                if candidate and candidate.exists():
                    images.append(Image.open(candidate).convert("RGBA"))
                else:
                    img = Image.open(icon_png).convert("RGBA").resize((size, size), Image.LANCZOS)
                    images.append(img)
            images[0].save(str(ico_path), format="ICO", sizes=[(i.width, i.height) for i in images], append_images=images[1:])
            print("✅ Created icon.ico")
            return str(ico_path)
        except Exception as e:
            print(f"⚠️  Could not create icon.ico: {e} — using icon.png")
            return str(icon_png)

    return str(icon_png)


def clean_build():
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")


def build_executable():
    print(f"🔨 Building {APP_NAME} via TASKY.spec ...")
    try:
        subprocess.run(["pyinstaller", "--noconfirm", "TASKY.spec"], check=True)
        print(f"✅ PyInstaller build succeeded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_dmg(app_path: Path) -> str | None:
    """Create a macOS .dmg from the .app bundle."""
    if not IS_MAC:
        return None

    dmg_name = f"{APP_NAME}-v{VERSION}.dmg"
    if os.path.exists(dmg_name):
        os.remove(dmg_name)

    tmp = Path("tmp_dmg")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    shutil.copytree(app_path, tmp / app_path.name)
    (tmp / "Applications").symlink_to("/Applications")

    try:
        subprocess.run(
            ["hdiutil", "create", "-volname", APP_NAME,
             "-srcfolder", str(tmp), "-ov", "-format", "UDZO", dmg_name],
            check=True, capture_output=True,
        )
        print(f"✅ Created {dmg_name}")
        return dmg_name
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG creation failed: {e.stderr.decode()}")
        return None
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


def create_windows_installer() -> str | None:
    """Create a Windows NSIS installer if makensis is available."""
    if not IS_WINDOWS:
        return None

    nsi_script = Path("tasky.nsi")
    if not nsi_script.exists():
        print("⚠️  tasky.nsi not found — skipping NSIS installer")
        return None

    try:
        subprocess.run(["makensis", str(nsi_script)], check=True)
        installer = f"TASKY-Setup-v{VERSION}.exe"
        if Path(installer).exists():
            print(f"✅ Created {installer}")
            return installer
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  makensis not available — skipping installer creation")
    return None


def create_distribution():
    os_label = "Windows" if IS_WINDOWS else "Mac"

    if IS_MAC:
        app_path = Path("dist") / "TASKY.app"
        if not app_path.exists():
            print("❌ TASKY.app not found in dist/")
            return False
        dmg = create_dmg(app_path)
        if not dmg:
            # Fall back to ZIP of the .app
            zip_name = f"{APP_NAME}-v{VERSION}-{os_label}.zip"
            shutil.make_archive(zip_name.replace(".zip", ""), "zip", "dist", "TASKY.app")
            print(f"✅ Created {zip_name} (DMG fallback)")
        return True

    elif IS_WINDOWS:
        dist_dir = Path("dist") / "TASKY"
        if not dist_dir.exists():
            print("❌ dist/TASKY directory not found")
            return False

        # Try NSIS installer first (produces TASKY-Setup-vX.Y.Z.exe if makensis available)
        create_windows_installer()

        # Always create a ZIP as well
        zip_name = f"{APP_NAME}-v{VERSION}-{os_label}.zip"
        shutil.make_archive(zip_name.replace(".zip", ""), "zip", dist_dir)
        print(f"✅ Created {zip_name}")
        return True


def main():
    print(f"🚀 {APP_NAME} v{VERSION} — Building for {platform.system()}")
    print("=" * 50)

    check_dependencies()
    clean_build()

    if not build_frontend():
        print("⚠️  Proceeding without frontend rebuild (web/dist must exist)")

    prepare_icons()

    if build_executable():
        create_distribution()
        print(f"\n🎉 Build complete!")
    else:
        print("\n❌ Build failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
