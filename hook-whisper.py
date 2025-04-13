"""
PyInstaller hook for OpenAI Whisper
This ensures that all necessary assets and models are included in the package
"""
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all submodules of whisper
hiddenimports = collect_submodules('whisper')

# Collect all data files of whisper, particularly the assets directory
datas = collect_data_files('whisper', includes=['assets/*.*'])

# Print information about what's being collected
print("Whisper hook: Collecting the following data files:")
for src, dest in datas:
    print(f"  {src} -> {dest}")

print("Whisper hook: Collecting the following hidden imports:")
for imp in hiddenimports:
    print(f"  {imp}") 