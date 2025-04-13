@echo off

echo Setting up a clean build environment for Whisper Transcribe...

REM Create a temporary virtual environment for building if it doesn't exist
if not exist build_venv (
    python -m venv build_venv
)

REM Activate the virtual environment
call build_venv\Scripts\activate.bat

echo Installing dependencies in the virtual environment...
pip install -r requirements.txt

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

REM Deactivate the virtual environment
call deactivate

echo You can remove the temporary virtual environment with:
echo rmdir /S /Q build_venv

pause 