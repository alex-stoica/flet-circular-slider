"""Automated build+deploy script for flet-circular-slider demo.

Pipeline:
  flet build apk
    -> patch app.zip (replace .pth editable with real .py files)
    -> regenerate app.zip.hash
    -> flutter build apk --release
    -> adb uninstall + install + launch

Usage:
    python build.py                 # full pipeline
    python build.py --skip-flet     # skip step 1 (reuse existing flet build)
    python build.py --skip-install  # skip step 6 (no adb deploy)
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_FLUTTER = ROOT / "build" / "flutter"
APP_ZIP = BUILD_FLUTTER / "app" / "app.zip"
APP_ZIP_HASH = BUILD_FLUTTER / "app" / "app.zip.hash"
PACKAGE_SRC = ROOT / "flet_circular_slider" / "src" / "flet_circular_slider"
PACKAGE_ID = "com.flet.flet_circular_slider_demo"


def _find_flutter() -> Path:
    """Locate flutter binary from FLUTTER_BIN env var or PATH."""
    env_path = os.environ.get("FLUTTER_BIN")
    if env_path:
        p = Path(env_path)
        if p.is_file():
            return p
    found = shutil.which("flutter")
    if found:
        return Path(found)
    print("ERROR: flutter not found. Set FLUTTER_BIN env var or add flutter to PATH.")
    sys.exit(1)


FLUTTER_BIN = _find_flutter()


def run(cmd, cwd=None, env=None):
    """Run a command, stream output, and raise on failure."""
    print(f"\n>>> {cmd if isinstance(cmd, str) else ' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd, env=env, shell=isinstance(cmd, str))
    if result.returncode != 0:
        print(f"FAILED with exit code {result.returncode}")
        sys.exit(1)


def step_flet_build():
    """Step 1: run flet build apk."""
    print("\n=== Step 1: flet build apk ===")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    run("flet build apk -v", cwd=str(ROOT), env=env)


def _discover_pkg_prefix(zf: zipfile.ZipFile) -> str:
    """Find the site-packages prefix for flet_circular_slider inside the zip."""
    for item in zf.infolist():
        if "flet_circular_slider/" in item.filename and item.filename.endswith(".py"):
            return item.filename.split("flet_circular_slider/")[0] + "flet_circular_slider/"
    return "flet_circular_slider/"


def step_patch_app_zip():
    """Step 2: patch app.zip -- remove .pth editable, add real .py files."""
    print("\n=== Step 2: patch app.zip ===")
    if not APP_ZIP.exists():
        print(f"ERROR: {APP_ZIP} not found. Run flet build first.")
        sys.exit(1)

    tmp_zip = APP_ZIP.with_suffix(".tmp")

    py_files = list(PACKAGE_SRC.rglob("*.py"))
    print(f"  injecting {len(py_files)} .py files from {PACKAGE_SRC}")

    with zipfile.ZipFile(APP_ZIP, "r") as zin, zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        site_pkg_prefix = _discover_pkg_prefix(zin)
        print(f"  discovered prefix: {site_pkg_prefix}")

        for item in zin.infolist():
            # skip .pth redirects and editable finders for our package
            if "__editable__" in item.filename and "flet_circular_slider" in item.filename:
                print(f"  removing: {item.filename}")
                continue
            # skip old dist-info for flet-circular-slider (not the demo)
            if "flet_circular_slider-" in item.filename and "dist-info" in item.filename:
                if "demo" not in item.filename:
                    print(f"  removing: {item.filename}")
                    continue
            # skip existing package .py files (we'll re-add fresh copies)
            if item.filename.startswith(site_pkg_prefix) and item.filename.endswith(".py"):
                print(f"  replacing: {item.filename}")
                continue
            # replace main.py with fresh copy from project root
            if item.filename == "main.py":
                print(f"  replacing: main.py")
                continue
            zout.writestr(item, zin.read(item.filename))

        # add fresh main.py from project root
        main_py = ROOT / "main.py"
        if main_py.exists():
            print(f"  adding: main.py (from project root)")
            zout.write(main_py, "main.py")

        # add fresh .py files
        for py_file in py_files:
            arcname = site_pkg_prefix + py_file.relative_to(PACKAGE_SRC).as_posix()
            print(f"  adding: {arcname}")
            zout.write(py_file, arcname)

    tmp_zip.replace(APP_ZIP)
    print("  app.zip patched successfully")

    # also patch site-packages arch dirs so SERIOUS_PYTHON_SITE_PACKAGES doesn't override with stale copies
    site_packages = ROOT / "build" / "site-packages"
    if site_packages.exists():
        for arch_pkg_dir in site_packages.glob("*/flet_circular_slider"):
            if arch_pkg_dir.is_dir():
                for py_file in py_files:
                    dest = arch_pkg_dir / py_file.name
                    shutil.copy2(py_file, dest)
                print(f"  patched site-packages: {arch_pkg_dir.parent.name}")


def step_update_hash():
    """Step 3: regenerate app.zip.hash."""
    print("\n=== Step 3: regenerate app.zip.hash ===")
    sha256 = hashlib.sha256(APP_ZIP.read_bytes()).hexdigest()
    APP_ZIP_HASH.write_text(sha256)
    print(f"  hash: {sha256}")


def step_flutter_build():
    """Step 4: flutter build apk --release."""
    print("\n=== Step 4: flutter build apk --release ===")
    site_packages = ROOT / "build" / "site-packages"
    if not site_packages.exists():
        print(f"ERROR: {site_packages} not found. Run flet build first.")
        sys.exit(1)

    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    env["SERIOUS_PYTHON_SITE_PACKAGES"] = str(site_packages)
    print(f"  SERIOUS_PYTHON_SITE_PACKAGES={site_packages}")

    run([str(FLUTTER_BIN), "build", "apk", "--release"], cwd=str(BUILD_FLUTTER), env=env)


def step_install():
    """Step 5: adb uninstall + install + launch."""
    print("\n=== Step 5: install on device ===")
    apk = BUILD_FLUTTER / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"
    if not apk.exists():
        print(f"ERROR: APK not found at {apk}")
        sys.exit(1)

    # uninstall (ignore failure if not installed)
    subprocess.run(["adb", "uninstall", PACKAGE_ID], capture_output=True)
    print(f"  uninstalled {PACKAGE_ID} (if present)")

    run(["adb", "install", str(apk)])
    print("  installed successfully")

    # launch
    run(["adb", "shell", "monkey", "-p", PACKAGE_ID, "-c", "android.intent.category.LAUNCHER", "1"])
    print("  launched app")


def main():
    parser = argparse.ArgumentParser(description="Build and deploy flet-circular-slider demo")
    parser.add_argument("--skip-flet", action="store_true", help="skip flet build apk (reuse existing build dir)")
    parser.add_argument("--skip-install", action="store_true", help="skip adb install + launch")
    args = parser.parse_args()

    if not args.skip_flet:
        step_flet_build()

    step_patch_app_zip()
    step_update_hash()
    step_flutter_build()

    if not args.skip_install:
        step_install()

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
