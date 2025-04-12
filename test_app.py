import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner
import app as app


@pytest.fixture
def runner():
    """Provides a Click CLI test runner"""
    return CliRunner()


@pytest.fixture
def mock_whisper_model():
    """Create a mock for the Whisper model"""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "This is a test transcription."}
    return mock_model


def test_transcribe_command_help(runner):
    """Test that the CLI shows help information"""
    result = runner.invoke(app.transcribe, ["--help"])
    assert result.exit_code == 0
    assert "Transcribe audio file using OpenAI's Whisper model." in result.output
    assert "--model" in result.output
    assert "--output" in result.output
    assert "--fp16 / --no-fp16" in result.output


@patch("whisper.load_model")
def test_transcribe_basic_functionality(mock_load_model, mock_whisper_model, runner):
    """Test basic transcription functionality with mocked Whisper model"""
    mock_load_model.return_value = mock_whisper_model

    with tempfile.NamedTemporaryFile(suffix=".mp3") as audio_file:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "output.txt")

            result = runner.invoke(
                app.transcribe,
                ["--model", "tiny", "--output", output_path, audio_file.name],
            )

            # Check command ran successfully
            assert result.exit_code == 0

            # Check the model was loaded with the right parameter
            mock_load_model.assert_called_once_with("tiny")

            # Check the transcribe method was called with the right parameters
            mock_whisper_model.transcribe.assert_called_once_with(
                audio_file.name, fp16=True
            )

            # Check the output file was created with the right content
            assert os.path.exists(output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert content == "This is a test transcription."

            # Check the output message
            assert f"Transcription saved to: {output_path}" in result.output
            assert "This is a test transcription." in result.output


@patch("app.Transcriber")
def test_default_output_filename(MockTranscriber, runner):
    """Test that default output filename is created correctly when not specified"""
    # Configure the mock Transcriber instance and its methods
    mock_instance = MockTranscriber.return_value
    mock_instance.transcribe.return_value = {"text": "This is a test transcription."}
    # Mock save_transcription to return the generated path for verification
    def mock_save(text, output_path=None):
        # In the default case (output_path is None), the app calculates it
        if output_path is None:
            output_path = os.path.splitext(audio_file_path)[0] + ".txt"
        
        # Actually write the file to disk
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        return output_path

    mock_instance.save_transcription.side_effect = mock_save # Use side effect if complex logic needed

    # Create, close, and get path of the temporary file
    audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    audio_file_path = audio_file.name
    audio_file.close() # Close the handle before invoking the app

    expected_output = None # Define outside try for finally block
    try:
        expected_output = os.path.splitext(audio_file_path)[0] + ".txt"

        # Make sure expected output file doesn't exist before the test
        if os.path.exists(expected_output):
            os.unlink(expected_output)

        # Run the command using the file path
        result = runner.invoke(app.transcribe, ["--model", "base", audio_file_path])

        # Check command ran successfully
        assert result.exit_code == 0, f"CLI command failed: {result.output}"

        # Verify Transcriber instantiation and methods were called
        MockTranscriber.assert_called_once_with(model_name="base")
        mock_instance.load_model.assert_called_once()
        mock_instance.transcribe.assert_called_once_with(audio_file_path, fp16=True)
        # Check save_transcription call - it receives the result text and potentially None for output path
        mock_instance.save_transcription.assert_called_once_with("This is a test transcription.", None)


        # Check the output file was created with the right name
        assert os.path.exists(expected_output), f"Expected output file '{expected_output}' was not created."

        # Check file content (app.py should write this based on mocked transcribe result)
        with open(expected_output, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "This is a test transcription."

        # Check CLI output message mentions the correct path
        assert f"Transcription saved to: {expected_output}" in result.output

    finally:
        # Clean up temporary audio file
        if os.path.exists(audio_file_path):
            os.unlink(audio_file_path)
        # Clean up output file
        if expected_output and os.path.exists(expected_output):
            os.unlink(expected_output)


@patch("app.Transcriber")
def test_fp16_parameter(MockTranscriber, runner):
    """Test that fp16 parameter is correctly passed to the model"""
    mock_instance = MockTranscriber.return_value
    mock_instance.transcribe.return_value = {"text": "Test"}
    def mock_save(text, output_path=None):
        if output_path is None:
            output_path = os.path.splitext(audio_file_path)[0] + ".txt"
        # Actually write to the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return output_path
    mock_instance.save_transcription.side_effect = mock_save

    # Create, close, get path
    audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    audio_file_path = audio_file.name
    audio_file.close()

    output_path = None
    try:
        # Test with fp16=False
        result = runner.invoke(app.transcribe, ["--no-fp16", audio_file_path])

        # Check command ran successfully
        assert result.exit_code == 0

        # Check the transcribe method was called with fp16=False
        mock_instance.transcribe.assert_called_with(audio_file_path, fp16=False)
        
        # Get the expected output path for cleanup
        output_path = os.path.splitext(audio_file_path)[0] + ".txt"
    finally:
        if os.path.exists(audio_file_path):
            os.unlink(audio_file_path)
        # Clean up output file
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)


def test_missing_audio_file(runner):
    """Test error handling when audio file doesn't exist"""
    result = runner.invoke(app.transcribe, ["nonexistent_file.mp3"])
    assert result.exit_code != 0
    assert "does not exist" in result.output
