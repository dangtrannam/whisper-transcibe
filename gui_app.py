"""
Whisper Transcribe - Desktop Application

This is the main entry point for the desktop GUI application.
It provides a user-friendly interface for transcribing audio files using OpenAI's Whisper model.
"""
import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.gui.main_window import MainWindow


def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Whisper Transcribe")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("WhisperTranscribe")
    
    # Set application icon if available
    icon_path = "resources/icons/app_icon.ico"
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 