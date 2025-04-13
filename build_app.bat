@echo off

echo Building Whisper Transcribe application...

REM Ensure all dependencies are installed
pip install -r requirements.txt

REM Try to uninstall PyQt5 if it's present to avoid conflicts
pip uninstall -y PyQt5 2>NUL
pip uninstall -y PyQt5-sip 2>NUL

REM Make sure we're using PySide6
pip install PySide6>=6.6.0

REM Create the application icon if needed
python create_icon.py

REM Clean previous build artifacts
rmdir /S /Q build dist 2>NUL

REM Build the application with PyInstaller
pyinstaller whisper_transcribe.spec

if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully!
    echo You can find the application in the dist/Whisper Transcribe directory.
) else (
    echo Build failed with error code %ERRORLEVEL%
    echo Please check the output above for errors.
)

pause 