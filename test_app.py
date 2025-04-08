import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from click.testing import CliRunner
import app


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


@patch("whisper.load_model")
def test_default_output_filename(mock_load_model, mock_whisper_model, runner):
    """Test that default output filename is created correctly when not specified"""
    mock_load_model.return_value = mock_whisper_model

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
        try:
            expected_output = os.path.splitext(audio_file.name)[0] + ".txt"

            # Make sure test file doesn't exist before the test
            if os.path.exists(expected_output):
                os.unlink(expected_output)

            result = runner.invoke(app.transcribe, ["--model", "base", audio_file.name])

            # Check command ran successfully
            assert result.exit_code == 0

            # Check the output file was created with the right name
            assert os.path.exists(expected_output)

            # Check file content
            with open(expected_output, "r", encoding="utf-8") as f:
                content = f.read()
                assert content == "This is a test transcription."

            # Clean up
            os.unlink(expected_output)
        finally:
            # Clean up temporary audio file
            if os.path.exists(audio_file.name):
                os.unlink(audio_file.name)


@patch("whisper.load_model")
def test_fp16_parameter(mock_load_model, mock_whisper_model, runner):
    """Test that fp16 parameter is correctly passed to the model"""
    mock_load_model.return_value = mock_whisper_model

    with tempfile.NamedTemporaryFile(suffix=".mp3") as audio_file:
        # Test with fp16=False
        result = runner.invoke(app.transcribe, ["--no-fp16", audio_file.name])

        # Check command ran successfully
        assert result.exit_code == 0

        # Check the transcribe method was called with fp16=False
        mock_whisper_model.transcribe.assert_called_with(audio_file.name, fp16=False)


def test_missing_audio_file(runner):
    """Test error handling when audio file doesn't exist"""
    result = runner.invoke(app.transcribe, ["nonexistent_file.mp3"])
    assert result.exit_code != 0
    assert "does not exist" in result.output
