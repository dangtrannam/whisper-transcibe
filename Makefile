install:
	pip install --upgrade pip && pip install -r requirements.txt
	@echo "Please install ffmpeg manually if not already installed:"
	@echo "Windows: https://ffmpeg.org/download.html or 'choco install ffmpeg'"
	@echo "Linux: sudo apt-get install ffmpeg"
	@echo "macOS: brew install ffmpeg"

install-linux:
	pip install --upgrade pip && pip install -r requirements.txt
	sudo apt-get update && sudo apt-get install -y ffmpeg

install-mac:
	pip install --upgrade pip && pip install -r requirements.txt
	brew install ffmpeg

lint:
	python -m pylint app.py

test:
	python -m pytest -vv test_app.py --cov=.

format:
	black *.py

run-example:
	# Run with sample audio file using base model
	python app.py --model base ikigai.m4a

clean:
	rm -f *.txt  # Remove generated transcription files
	find . -type f -name "*.pyc" -delete  # Remove Python cache files
	find . -type d -name "__pycache__" -delete

all: install format test

.PHONY: install install-linux install-mac lint test format run-example clean all