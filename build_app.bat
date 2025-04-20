@echo off
title Building Volume Labeler...

echo (1/4) Deleting temporary files...
echo.

rmdir /q /s "build"
rmdir /q /s "dist"
del /f /q "volume_labeler.spec"

echo.
echo (2/4) Installing dependencies...
echo.

python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo (3/4) Building with PyInstaller...
echo.

python -m PyInstaller main.pyw --onedir --icon "icons/icon.ico" --version-file "version.txt" --name "volume_labeler" --add-data "icons;./icons/" --add-data "OPEN_SOURCE_LICENSES.txt;." --add-data "LICENSE;." --exclude-module "numpy" --exclude-module "setuptools" --exclude-module "wheel" --exclude-module "importlib_metadata" --exclude-module "markupsafe" --exclude-module "ssl" --exclude-module "_ssl"
del /f /q dist\volume_labeler\_internal\libcrypto-3.dll
del /f /q dist\volume_labeler\_internal\libcrypto-3-arm64.dll
del /f /q dist\volume_labeler\_internal\api-ms-win-*.dll
rmdir /s /q dist\volume_labeler\_internal\_tcl_data\msgs
rmdir /s /q dist\volume_labeler\_internal\_tcl_data\tzdata
rmdir /s /q dist\volume_labeler\_internal\tkinter_tooltip-*

echo.
echo (4/4) Deleting temporary files...
echo.

rmdir /q /s "build"
del /f /q "volume_labeler.spec"
ren "dist" "build"

echo.
echo Volume Labeler has been successfully built.