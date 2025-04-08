install:
	pip install --upgrade pip && pip install -r requirements.txt
	# Install ffmpeg based on OS
	@if command -v apt-get > /dev/null; then \
		echo "Installing ffmpeg using apt-get..."; \
		sudo apt-get update && sudo apt-get install -y ffmpeg; \
	elif command -v brew > /dev/null; then \
		echo "Installing ffmpeg using brew..."; \
		brew install ffmpeg; \
	else \
		echo "Please install ffmpeg manually: https://ffmpeg.org/download.html"; \
	fi

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

.PHONY: install lint test format run-example clean all