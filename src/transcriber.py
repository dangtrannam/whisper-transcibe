"""
Whisper Transcription Tool - Core transcription functionality.

This module provides the Transcriber class that handles audio transcription
using OpenAI's Whisper model.
"""
import os
from typing import Optional, Dict, Any

import whisper
import torch


class Transcriber:
    """Handles audio transcription using OpenAI's Whisper model."""

    def __init__(self, model_name: str = "base"):
        """Initialize the transcriber with specified model.

        Args:
            model_name (str): Name of the Whisper model to use.
                             Options: "tiny", "base", "small", "medium", "large"
        """
        self.model_name = model_name
        self.model = None
        self.current_audio_file = None
        # Print GPU availability
        print(f"Using GPU: {torch.cuda.is_available()}")

    def load_model(self) -> None:
        """Load the Whisper model."""
        if self.model is None:
            self.model = whisper.load_model(self.model_name)

    def transcribe(
        self, 
        audio_file: str, 
        fp16: bool = True,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Transcribe an audio file using the loaded Whisper model.

        Args:
            audio_file (str): Path to the audio file to transcribe
            fp16 (bool): Whether to use FP16 for faster inference on GPU
            progress_callback (callable, optional): Callback function for progress updates

        Returns:
            Dict[str, Any]: Transcription result containing the text and other metadata
        """
        if self.model is None:
            self.load_model()

        self.current_audio_file = audio_file
        # TODO: Implement progress callback when Whisper API supports it
        result = self.model.transcribe(audio_file, fp16=fp16)
        return result

    def save_transcription(self, text: str, output_path: Optional[str] = None) -> str:
        """Save the transcription text to a file.

        Args:
            text (str): The transcription text to save
            output_path (str, optional): Path to save the transcription.
                                       If None, uses input filename with .txt extension

        Returns:
            str: Path where the transcription was saved
        """
        if not output_path and self.current_audio_file:
            output_path = os.path.splitext(self.current_audio_file)[0] + ".txt"
        elif not output_path:
            raise ValueError("No output path specified and no current audio file set")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return output_path 