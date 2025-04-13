#!/bin/bash

echo "Building Whisper Transcribe application..."

# Ensure all dependencies are installed
pip install -r requirements.txt

# Try to uninstall PyQt5 if it's present to avoid conflicts
pip uninstall -y PyQt5 >/dev/null 2>&1
pip uninstall -y PyQt5-sip >/dev/null 2>&1

# Make sure we're using PySide6
pip install PySide6>=6.6.0

# Create the application icon if needed
python create_icon.py

# Clean previous build artifacts
rm -rf build dist

# Build the application with PyInstaller
pyinstaller whisper_transcribe.spec

if [ $? -eq 0 ]; then
    echo "Build completed successfully!"
    echo "You can find the application in the dist/Whisper Transcribe directory."
else
    echo "Build failed with error code $?"
    echo "Please check the output above for errors."
fi 