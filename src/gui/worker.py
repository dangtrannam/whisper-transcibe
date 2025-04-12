"""
Worker thread for handling transcription in the background.
"""
from PySide6.QtCore import QThread, Signal


class TranscriptionWorker(QThread):
    """Worker thread for running transcription without blocking the GUI."""
    
    # Signals for communication with the main thread
    finished = Signal(dict)  # Emits the transcription result
    error = Signal(str)      # Emits error messages
    progress = Signal(int)   # Emits progress updates (0-100)
    
    def __init__(self, transcriber, audio_file, model_name="base", fp16=True):
        """Initialize the worker with transcription parameters.
        
        Args:
            transcriber: The Transcriber instance to use
            audio_file (str): Path to the audio file
            model_name (str): Name of the Whisper model to use
            fp16 (bool): Whether to use FP16 for faster inference
        """
        super().__init__()
        self.transcriber = transcriber
        self.audio_file = audio_file
        self.model_name = model_name
        self.fp16 = fp16
        
    def run(self):
        """Execute the transcription process in the background thread."""
        try:
            # Load model if not already loaded or if model name changed
            if (self.transcriber.model is None or 
                self.transcriber.model_name != self.model_name):
                self.transcriber.model_name = self.model_name
                self.progress.emit(10)
                self.transcriber.load_model()
            
            # Perform transcription
            self.progress.emit(30)
            result = self.transcriber.transcribe(
                self.audio_file,
                fp16=self.fp16
            )
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e)) 