"""
Tests for the GUI application components.
"""
import sys
import pytest
from PySide6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


@pytest.fixture
def app():
    """Create a Qt Application."""
    return QApplication(sys.argv)


@pytest.fixture
def main_window(app):
    """Create the main window."""
    window = MainWindow()
    return window


def test_initial_state(main_window):
    """Test the initial state of the main window."""
    # Check window properties
    assert main_window.windowTitle() == "Whisper Transcribe"
    
    # Check initial button states
    assert not main_window.transcribe_btn.isEnabled()
    assert main_window.select_file_btn.isEnabled()
    assert not main_window.save_btn.isEnabled()
    
    # Check model combo box
    assert main_window.model_combo.currentText() == "base"
    assert set(main_window.model_combo.items()) == {"tiny", "base", "small", "medium", "large"}
    
    # Check progress bar
    assert not main_window.progress_bar.isVisible()


def test_file_selection(main_window, monkeypatch):
    """Test file selection behavior."""
    # Mock QFileDialog.getOpenFileName to return a test file
    def mock_get_file(*args, **kwargs):
        return "test.mp3", "Audio Files"
    
    monkeypatch.setattr(
        "PySide6.QtWidgets.QFileDialog.getOpenFileName",
        mock_get_file
    )
    
    # Simulate file selection
    main_window.select_file()
    
    # Check state changes
    assert main_window.current_file == "test.mp3"
    assert main_window.transcribe_btn.isEnabled()
    assert not main_window.save_btn.isEnabled()


def test_transcription_ui_state(main_window):
    """Test UI state changes during transcription."""
    # Set up initial state
    main_window.current_file = "test.mp3"
    main_window.transcribe_btn.setEnabled(True)
    
    # Start transcription
    main_window.start_transcription()
    
    # Check UI state during transcription
    assert not main_window.transcribe_btn.isEnabled()
    assert not main_window.select_file_btn.isEnabled()
    assert not main_window.model_combo.isEnabled()
    assert not main_window.save_btn.isEnabled()
    assert main_window.progress_bar.isVisible()


def test_cleanup_after_transcription(main_window):
    """Test cleanup of UI state after transcription."""
    # Set up transcription state
    main_window.transcribe_btn.setEnabled(False)
    main_window.select_file_btn.setEnabled(False)
    main_window.model_combo.setEnabled(False)
    main_window.progress_bar.setVisible(True)
    
    # Simulate cleanup
    main_window.cleanup_after_transcription()
    
    # Check final state
    assert main_window.transcribe_btn.isEnabled()
    assert main_window.select_file_btn.isEnabled()
    assert main_window.model_combo.isEnabled()
    assert not main_window.progress_bar.isVisible()
    assert main_window.worker is None 