"""
Main window for the Whisper Transcribe application.
"""
import os
import platform
import psutil
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QTextEdit,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QLabel,
    QFrame,
    QSizePolicy,
    QFormLayout,
    QToolButton,
    QStylePainter,
    QStyleOptionComboBox,
    QStyle,
)
from PySide6.QtCore import Qt, QTimer, QRect, QPoint
from PySide6.QtGui import QFont, QIcon, QPalette, QBrush, QColor, QPainter
from src.core import Transcriber
from .worker import TranscriptionWorker


class CustomComboBox(QComboBox):
    """ComboBox with a custom dropdown arrow."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paintEvent(self, event):
        """Custom paint event to draw a better dropdown arrow."""
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(QPalette.ColorRole.Text))
        
        # Draw the combobox frame, button, etc.
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        painter.drawComplexControl(QStyle.ComplexControl.CC_ComboBox, opt)
        
        # Draw the combobox text
        painter.drawControl(QStyle.ControlElement.CE_ComboBoxLabel, opt)
        
        # Draw custom arrow manually (triangle pointing down)
        if not self.findChild(QToolButton):  # Only if we don't already have a button
            rect = opt.rect.adjusted(opt.rect.width() - 30, 0, -5, 0)  # Arrow area in dropdown
            painter.save()
            painter.setPen(QColor("#555"))
            painter.setBrush(QColor("#555"))
            
            # Draw triangle
            arrow_size = 8
            arrow_x = rect.center().x()
            arrow_y = rect.center().y()
            
            points = [
                QPoint(arrow_x - arrow_size, arrow_y - arrow_size // 2),
                QPoint(arrow_x + arrow_size, arrow_y - arrow_size // 2),
                QPoint(arrow_x, arrow_y + arrow_size // 2)
            ]
            
            painter.drawPolygon(points)
            painter.restore()


class MainWindow(QMainWindow):
    """Main window for the Whisper Transcribe application."""

    def __init__(self):
        super().__init__()
        self.transcriber = Transcriber()  # Initialize transcriber
        self.current_file = None
        self.worker = None
        self.system_monitor_timer = None
        
        self.setWindowTitle("Whisper Transcribe")
        self.setMinimumSize(900, 700)
        
        # Set application icon if available
        icon_path = "resources/icons/app_icon.ico"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create UI elements
        self.setup_ui(layout)
        
        # Setup system monitoring
        self.setup_system_monitoring()
        
    def setup_ui(self, layout):
        """Set up the user interface elements."""
        # Header with app title
        header_label = QLabel("Whisper Transcribe")
        header_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header_label)
        
        # Model selection section
        model_frame = QFrame()
        model_frame.setFrameShape(QFrame.Shape.StyledPanel)
        model_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                padding: 8px 12px;
            }
        """)
        
        # Use form layout for label-field pairing
        model_form_layout = QFormLayout(model_frame)
        model_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        model_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        model_form_layout.setContentsMargins(5, 5, 5, 5)
        model_form_layout.setSpacing(10)  # Reduced spacing
        
        # Model label with enhanced styling
        model_label = QLabel("Model:")
        model_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        # Create the custom combobox
        self.model_combo = CustomComboBox()
        self.model_combo.setFont(QFont("Arial", 12))
        models = ["tiny", "base", "small", "medium", "large"]
        for model in models:
            self.model_combo.addItem(model)
        self.model_combo.setCurrentText("base")
        self.model_combo.setMinimumHeight(40)
        self.model_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Style the combobox
        self.model_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #bbb;
                border-radius: 5px;
                padding: 5px 10px;
                background-color: white;
                min-width: 200px;
                selection-background-color: #4a86e8;
                selection-color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 30px;
                border-left: 1px solid #bbb;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: #f5f5f5;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #bbb;
                background-color: white;
                border-radius: 5px;
                selection-background-color: #4a86e8;
                selection-color: white;
            }
        """)
        
        # Add to form layout - this keeps the label and field closely aligned
        model_form_layout.addRow(model_label, self.model_combo)
        
        # Add the frame to the main layout
        layout.addWidget(model_frame)
        
        # File display section
        file_frame = QFrame()
        file_frame.setFrameShape(QFrame.Shape.StyledPanel)
        file_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f5f5f5;
                padding: 10px;
            }
        """)
        file_layout = QVBoxLayout(file_frame)
        
        file_header = QLabel("Selected File")
        file_header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        file_layout.addWidget(file_header)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setWordWrap(True)
        self.file_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        file_layout.addWidget(self.file_label)
        
        layout.addWidget(file_frame)
        
        # Button section
        button_layout = QHBoxLayout()
        
        # File selection button
        self.select_file_btn = QPushButton("Select Audio File")
        self.select_file_btn.setFont(QFont("Arial", 12))
        self.select_file_btn.setMinimumHeight(50)
        self.select_file_btn.clicked.connect(self.select_file)
        self.select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
        """)
        button_layout.addWidget(self.select_file_btn)
        
        # Transcribe button
        self.transcribe_btn = QPushButton("Transcribe")
        self.transcribe_btn.setFont(QFont("Arial", 12))
        self.transcribe_btn.setMinimumHeight(50)
        self.transcribe_btn.clicked.connect(self.start_transcription)
        self.transcribe_btn.setEnabled(False)  # Disabled until file is selected
        self.transcribe_btn.setStyleSheet("""
            QPushButton {
                background-color: #3cba54;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2caa44;
            }
            QPushButton:pressed {
                background-color: #1c9a34;
            }
            QPushButton:disabled {
                background-color: #8aca9c;
            }
        """)
        button_layout.addWidget(self.transcribe_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(QFont("Arial", 12))
        self.cancel_btn.setMinimumHeight(50)
        self.cancel_btn.clicked.connect(self.cancel_transcription)
        self.cancel_btn.setEnabled(False)  # Disabled until transcription starts
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #db4437;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #cb3427;
            }
            QPushButton:pressed {
                background-color: #bb2417;
            }
            QPushButton:disabled {
                background-color: #e89990;
            }
        """)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Progress section
        progress_layout = QVBoxLayout()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 5px;
                text-align: center;
                background-color: #f5f5f5;
            }
            QProgressBar::chunk {
                background-color: #4a86e8;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setVisible(False)
        progress_layout.addWidget(self.status_label)
        
        layout.addLayout(progress_layout)
        
        # Result text area
        result_label = QLabel("Transcription")
        result_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Arial", 11))
        self.result_text.setMinimumHeight(300)
        self.result_text.setPlaceholderText("Transcription will appear here...")
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bbb;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
            }
        """)
        layout.addWidget(self.result_text)
        
        # System info section
        system_frame = QFrame()
        system_frame.setFrameShape(QFrame.Shape.StyledPanel)
        system_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
                padding: 5px;
            }
        """)
        system_layout = QHBoxLayout(system_frame)
        
        # CPU usage
        self.cpu_label = QLabel("CPU: --")
        system_layout.addWidget(self.cpu_label)
        
        # Memory usage
        self.memory_label = QLabel("Memory: --")
        system_layout.addWidget(self.memory_label)
        
        # GPU info (if available)
        self.gpu_label = QLabel("GPU: --")
        system_layout.addWidget(self.gpu_label)
        
        layout.addWidget(system_frame)
        
        # Save button
        self.save_btn = QPushButton("Save Transcription")
        self.save_btn.setFont(QFont("Arial", 12))
        self.save_btn.setMinimumHeight(50)
        self.save_btn.clicked.connect(self.save_transcription)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #f4b400;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e4a400;
            }
            QPushButton:pressed {
                background-color: #d49400;
            }
            QPushButton:disabled {
                background-color: #f9d980;
            }
        """)
        layout.addWidget(self.save_btn)
        
    def setup_system_monitoring(self):
        """Set up system resource monitoring."""
        self.system_monitor_timer = QTimer()
        self.system_monitor_timer.timeout.connect(self.update_system_info)
        self.system_monitor_timer.start(2000)  # Update every 2 seconds
        
    def update_system_info(self):
        """Update system resource information."""
        # CPU usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU: {cpu_percent}%")
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_used = memory.used / (1024 * 1024 * 1024)  # Convert to GB
        self.memory_label.setText(f"Memory: {memory_usage}% ({memory_used:.1f} GB)")
        
        # GPU info - with usage percentage
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                
                # Get GPU utilization using nvidia-smi through subprocess
                # This only works on NVIDIA GPUs
                import subprocess
                result = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                    encoding='utf-8'
                )
                gpu_usage = float(result.strip())
                
                self.gpu_label.setText(f"GPU: {gpu_usage}% ({gpu_name})")
            else:
                self.gpu_label.setText("GPU: Not available")
        except Exception as e:
            # Fallback if there's an error getting GPU info
            if hasattr(self.transcriber, 'model') and self.transcriber.model:
                self.gpu_label.setText("GPU: Active (usage data unavailable)")
            else:
                self.gpu_label.setText("GPU: Unknown")
    
    def select_file(self):
        """Open file dialog to select an audio file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.ogg);;All Files (*.*)"
        )
        if file_name:
            self.current_file = file_name
            self.file_label.setText(os.path.basename(file_name))
            self.transcribe_btn.setEnabled(True)
            self.result_text.clear()
            self.save_btn.setEnabled(False)
            self.status_label.setText(f"Ready to transcribe: {os.path.basename(file_name)}")
            self.status_label.setVisible(True)
    
    def start_transcription(self):
        """Initialize and start the transcription process."""
        if not self.current_file:
            return
            
        # Disable UI elements during transcription
        self.transcribe_btn.setEnabled(False)
        self.select_file_btn.setEnabled(False)
        self.model_combo.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.result_text.clear()
        
        # Show and reset progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Transcribing: {os.path.basename(self.current_file)}")
        self.status_label.setVisible(True)
        
        # Create and configure worker
        self.worker = TranscriptionWorker(
            self.transcriber,
            self.current_file,
            model_name=self.model_combo.currentText()
        )
        
        # Connect signals
        self.worker.finished.connect(self.on_transcription_complete)
        self.worker.error.connect(self.on_transcription_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        
        # Start transcription
        self.worker.start()
    
    def cancel_transcription(self):
        """Cancel the current transcription process."""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.status_label.setText("Transcription cancelled")
            self.cleanup_after_transcription()
    
    def on_transcription_complete(self, result):
        """Handle completion of transcription."""
        # Update UI with result
        self.result_text.setPlainText(result["text"])
        self.save_btn.setEnabled(True)
        self.status_label.setText("Transcription complete")
        
        # Re-enable UI elements
        self.cleanup_after_transcription()
        
    def on_transcription_error(self, error_msg):
        """Handle transcription errors."""
        QMessageBox.critical(
            self,
            "Transcription Error",
            f"An error occurred during transcription:\n{error_msg}"
        )
        self.status_label.setText("Transcription failed")
        self.cleanup_after_transcription()
    
    def cleanup_after_transcription(self):
        """Re-enable UI elements after transcription (success or failure)."""
        self.transcribe_btn.setEnabled(True)
        self.select_file_btn.setEnabled(True)
        self.model_combo.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.cancel_btn.setEnabled(False)
        
        # Clean up worker
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
    
    def save_transcription(self):
        """Save the transcription to a file."""
        if not self.result_text.toPlainText():
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Transcription",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.result_text.toPlainText())
                QMessageBox.information(
                    self,
                    "Success",
                    f"Transcription saved to: {file_name}"
                )
                self.status_label.setText(f"Saved to: {os.path.basename(file_name)}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save transcription: {str(e)}"
                )
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Stop the timer when the application is closed
        if self.system_monitor_timer:
            self.system_monitor_timer.stop() 