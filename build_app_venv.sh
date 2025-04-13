#!/bin/bash

echo "Setting up a clean build environment for Whisper Transcribe..."

# Create a temporary virtual environment for building
python -m venv build_venv

# Activate the virtual environment
source build_venv/bin/activate

echo "Installing dependencies in the virtual environment..."
pip install -r requirements.txt

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

# Deactivate the virtual environment
deactivate

echo "You can remove the temporary virtual environment with:"
echo "rm -rf build_venv" 