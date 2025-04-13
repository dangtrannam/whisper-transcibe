# Desktop App To-Do List

## Phase 1: Setup & Basic Structure

- [x] Create project directory structure (`src/gui`, `src/core`, `docs`, etc.)
- [x] Move existing `transcriber.py` to `src/core/`
- [x] Rename existing `app.py` to `cli_app.py` and update its import
- [x] Create `gui_app.py` entry point
- [x] Create `requirements.txt` with initial dependencies (`PySide6`, `openai-whisper`, `click`)
- [x] Create `docs/desktop-todo.md` (this file!)

## Phase 2: Basic GUI Implementation

- [x] Create basic `MainWindow` class in `src/gui/main_window.py`
- [x] Add UI elements to `MainWindow` (File selection button, model dropdown, transcribe button, result area, progress bar)
- [x] Implement file selection logic (using `QFileDialog`)
- [x] Populate model selection dropdown

## Phase 3: Core Logic Integration

- [x] Create `Worker` thread class in `src/gui/worker.py` for transcription
- [x] Instantiate `Transcriber` from `src.core` in the GUI logic
- [x] Implement logic to start transcription in the worker thread when "Transcribe" is clicked
- [x] Use signals/slots to update GUI (progress bar, result text area) from the worker thread
- [x] Implement basic error handling (e.g., show message box on error)
- [x] Implement "Save Transcription" functionality (using `QFileDialog`)

## Phase 4: Packaging & Refinements

- [x] Refine UI/UX (styling, layout adjustments)
  - [x] Add bigger, colorful buttons
  - [x] Display the current file being transcribed
  - [x] Add cancel button
  - [x] Show system resource usage (CPU, Memory, GPU)
  - [x] Improve model selection dropdown with custom styling and dropdown arrow
- [x] Set up `PyInstaller` configuration
  - [x] Create PyInstaller spec file
  - [x] Set up build scripts for Windows/macOS/Linux
- [ ] Test packaging for Windows (or target platforms)
- [x] Create a simple application icon (`resources/icons/app_icon.ico`)
- [x] Add icon to the application window and packaged executable
- [x] Update README instructions for running/building

## Phase 5: Enhancements
- [ ] Add drag-and-drop support for audio files (optional)
- [ ] Save/load user preferences (last model used, etc.) (optional)