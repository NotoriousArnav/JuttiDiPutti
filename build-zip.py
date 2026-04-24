#!/usr/bin/env python3
"""
Build script to create portable ZIP packages for distribution.
Includes the executable and all necessary assets.
"""

import os
import shutil
import zipfile
import argparse
from pathlib import Path


def create_portable_zip(platform: str, exe_name: str):
    dist_dir = Path("dist")
    release_dir = Path("releases")
    platform_dir = release_dir / platform

    release_dir.mkdir(parents=True, exist_ok=True)

    if platform_dir.exists():
        shutil.rmtree(platform_dir)
    platform_dir.mkdir(parents=True)

    exe_path = dist_dir / exe_name
    if exe_path.exists():
        shutil.copy(exe_path, platform_dir / exe_name)
        print(f"Copied executable: {exe_name}")
    else:
        print(f"WARNING: Executable not found at {exe_path}")
        return False

    for folder in ["assets", "faces"]:
        if Path(folder).exists():
            dest = platform_dir / folder
            shutil.copytree(folder, dest, dirs_exist_ok=True)
            print(f"Copied folder: {folder}")

    zip_path = release_dir / f"{platform}.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(platform_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(platform_dir)
                zf.write(file_path, arc_name)
                print(f"Added to zip: {arc_name}")

    print(f"\nCreated: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")

    return True


def main():
    parser = argparse.ArgumentParser(description="Create portable ZIP packages")
    parser.add_argument(
        "--platform",
        required=True,
        help="Platform name (e.g., JuttiDiPutti-Windows-x64)",
    )
    parser.add_argument(
        "--exe-name", required=True, help="Executable name (e.g., main.exe or main)"
    )
    args = parser.parse_args()

    success = create_portable_zip(args.platform, args.exe_name)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
