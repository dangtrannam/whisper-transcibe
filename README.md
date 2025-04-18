# Whisper Transcription Tool

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Whisper-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A tool to transcribe audio files using OpenAI's Whisper speech recognition model. Available as both a command-line tool and a desktop application.

## Features

- Transcribe audio files (mp3, wav, m4a, etc.) to text
- Support for multiple Whisper model sizes (tiny, base, small, medium, large)
- Option to use FP16 for faster inference on GPU
- Custom output file path option
- Cross-platform compatibility (Windows, macOS, Linux)
- **NEW:** Desktop application with a modern, user-friendly interface
- **NEW:** Real-time system resource monitoring (CPU, Memory, GPU usage)
- **NEW:** Cancel transcription feature

## Desktop Application

The new desktop application provides an intuitive graphical interface for transcribing audio files without using the command line.

### Running the Desktop App

To run the desktop application:

```bash
# First, make sure you have installed the requirements
pip install -r requirements.txt

# Then run the desktop app
python gui_app.py
```

### Desktop App Features

- Simple, modern user interface with easy-to-use controls
- Model selection dropdown to choose between different Whisper models
- File selector to choose audio files for transcription
- Progress bar showing transcription status
- One-click saving of transcription results
- Cancel button to stop long-running transcriptions
- Real-time system resource monitoring (CPU, Memory, GPU usage)

### Building the Desktop App

To build a standalone desktop application:

1. Ensure you have installed all requirements:
```bash
pip install -r requirements.txt
```

2. Run the build script:
```bash
# On Windows
build_app.bat

# On macOS/Linux
./build_app.sh
```

3. The compiled application will be available in the `dist/Whisper Transcribe` directory.

#### Troubleshooting Build Issues

If you encounter PyQt5 conflicts during the build process, you can use one of the alternative build scripts that create a clean virtual environment:

```bash
# On Windows
build_app_venv.bat

# On macOS/Linux
./build_app_venv.sh
```

These scripts create a temporary virtual environment with only the required dependencies, avoiding conflicts with existing packages.

## Command-Line Usage

If you prefer using the command line:

```bash
python cli_app.py your_audio_file.mp3
```

## Requirements

- Python 3.12 or higher
- ffmpeg (for audio processing)
- Appropriate hardware:
  - CPU: Any modern CPU (inference will be slow with larger models)
  - GPU: NVIDIA GPU with CUDA support (recommended for faster inference)

## Virtual Environment Setup

It's recommended to use a virtual environment to avoid conflicts with other Python packages. You can choose either venv or conda:

### Using venv (Python's built-in virtual environment)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Using Conda

```bash
# Create a new conda environment
conda create -n whisper-env python=3.12

# Activate the conda environment
conda activate whisper-env
```

After setting up and activating your virtual environment, proceed with the installation steps below.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/dangtrannam/whisper-transcibe.git
cd whisper-transcibe
```

2. Install the required dependencies:
```bash
make install
```

This will install Python dependencies and ffmpeg. If ffmpeg installation fails, you'll need to install it manually following instructions at [ffmpeg.org](https://ffmpeg.org/download.html).

### Manual Installation

If you don't want to use Make, you can install dependencies manually:

```bash
pip install -r requirements.txt
```

Then install ffmpeg:
- **Ubuntu/Debian**: `sudo apt-get update && sudo apt-get install -y ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your PATH

## Usage

Basic usage:

```bash
python app.py your_audio_file.mp3
```

### Options

- `--model, -m`: Choose Whisper model size (tiny, base, small, medium, large). Default is base.
  ```bash
  python app.py --model medium your_audio_file.mp3
  ```

- `--output, -o`: Specify output file path. Default is input filename with .txt extension.
  ```bash
  python app.py --output transcript.txt your_audio_file.mp3
  ```

- `--fp16/--no-fp16`: Toggle FP16 precision (faster on GPU). Default is enabled.
  ```bash
  python app.py --no-fp16 your_audio_file.mp3
  ```

### Examples

Transcribe an audio file using the tiny model:
```bash
python app.py --model tiny audio.mp3
```

Transcribe with a specific output file:
```bash
python app.py --output transcript.txt audio.mp3
```

Use the example audio file included in the repository:
```bash
make run-example
```

## Development

Run tests:
```bash
make test
```

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Clean up generated files:
```bash
make clean
```

## Model Size Comparison

| Model | Parameters | English-only | Multilingual | Required VRAM | Relative Speed |
|-------|------------|--------------|--------------|---------------|----------------|
| tiny  | 39 M       | tiny.en      | tiny         | ~1 GB         | ~32x           |
| base  | 74 M       | base.en      | base         | ~1 GB         | ~16x           |
| small | 244 M      | small.en     | small        | ~2 GB         | ~6x            |
| medium| 769 M      | medium.en    | medium       | ~5 GB         | ~2x            |
| large | 1550 M     | N/A          | large        | ~10 GB        | 1x             |

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) - The underlying speech recognition model
- [Click](https://click.palletsprojects.com/) - Command-line interface framework 