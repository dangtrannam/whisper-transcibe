"""
Whisper Transcription Tool - Transcribe audio files using OpenAI's Whisper model.

This script provides a command-line interface for transcribing audio files
using Whisper, with options for model selection, output path and precision.
"""
import click
from src.transcriber import Transcriber


@click.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option(
    "--model",
    "-m",
    type=click.Choice(["tiny", "base", "small", "medium", "large"]),
    default="base",
    help="Whisper model to use for transcription. Default is base.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: same as input with .txt extension)",
)
@click.option(
    "--fp16/--no-fp16",
    default=True,
    help="Use FP16 for faster inference on GPU. Default is True.",
)
def transcribe(audio_file, model, output, fp16):
    """Transcribe audio file using OpenAI's Whisper model."""
    click.echo(f"Loading {model} model...")
    transcriber = Transcriber(model_name=model)
    transcriber.load_model()

    click.echo("Transcribing audio...")
    result = transcriber.transcribe(audio_file, fp16=fp16)

    # Save transcription
    output_path = transcriber.save_transcription(result["text"], output)

    click.echo(f"\nTranscription saved to: {output_path}")
    click.echo("\nTranscription text:")
    click.echo(result["text"])


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    transcribe()
