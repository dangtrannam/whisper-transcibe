# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import PyInstaller.config
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

# Configuration
block_cipher = None
app_name = "Whisper Transcribe"
app_icon = None  # Will be updated when we add the icon

# Check if resources/icons/app_icon.ico exists and use it
if os.path.exists("resources/icons/app_icon.ico"):
    app_icon = "resources/icons/app_icon.ico"

# Define additional data files to include
# This includes Whisper model files, if they're found in the user's cache
whisper_data = []
home_dir = os.path.expanduser("~")
whisper_cache = os.path.join(home_dir, ".cache", "whisper")

if os.path.exists(whisper_cache):
    for model_file in os.listdir(whisper_cache):
        model_path = os.path.join(whisper_cache, model_file)
        if os.path.isfile(model_path):
            # Include model file in the package
            whisper_data.append((model_path, os.path.join("whisper", model_file)))

# Add Whisper assets directory to fix the missing assets error
try:
    import whisper
    whisper_package_dir = os.path.dirname(whisper.__file__)
    whisper_assets_dir = os.path.join(whisper_package_dir, 'assets')
    
    if os.path.exists(whisper_assets_dir):
        print(f"Found Whisper assets directory: {whisper_assets_dir}")
        for asset_file in os.listdir(whisper_assets_dir):
            asset_path = os.path.join(whisper_assets_dir, asset_file)
            if os.path.isfile(asset_path):
                # Include asset file in the package with the correct structure
                whisper_data.append((asset_path, os.path.join('whisper', 'assets')))
                print(f"  Adding asset: {asset_file}")
    else:
        print(f"WARNING: Could not find Whisper assets directory at {whisper_assets_dir}")
        
except ImportError:
    print("WARNING: Could not import whisper module. Make sure it's installed.")
except Exception as e:
    print(f"WARNING: Error processing Whisper assets: {e}")

# Create a directory for the hook if it doesn't exist
if not os.path.exists('hooks'):
    os.makedirs('hooks')
    print("Created hooks directory")

# Include package metadata to prevent "No package metadata found" errors
extra_datas = []
# Add recursive metadata copies for critical packages
extra_datas += copy_metadata('transformers', recursive=True)
extra_datas += copy_metadata('tqdm', recursive=True)
extra_datas += copy_metadata('regex', recursive=True)
extra_datas += copy_metadata('numpy', recursive=True)
extra_datas += copy_metadata('tokenizers', recursive=True)
extra_datas += copy_metadata('openai-whisper', recursive=True)
extra_datas += copy_metadata('filelock', recursive=True)
extra_datas += copy_metadata('packaging', recursive=True)

# Set up the analysis
a = Analysis(
    ['gui_app.py'],  # Main script
    pathex=[],
    binaries=[],
    datas=whisper_data + extra_datas,  # Add the metadata
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'torch',
        'tqdm',
        'numpy',
        'psutil',
        'whisper.assets',  # Explicitly include the assets module
        'sklearn.utils._cython_blas',  # These may be needed by whisper's dependencies
        'sklearn.neighbors.typedefs',
        'sklearn.neighbors.quad_tree',
        'sklearn.tree',
        'sklearn.tree._utils',
    ] + collect_submodules('whisper'),
    hookspath=['.', 'hooks'],  # Look for hooks in current directory and hooks directory
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',  # Exclude PyQt5 to avoid conflicts with PySide6
        'PyQt6',
        'PyQt',
        'tkinter',  # Exclude unnecessary GUI packages
        'wx',
        'wxPython',
        'matplotlib',  # Not used in our app
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create the PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True for debugging - shows console output
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=app_icon,
)

# Create the directory structure
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)

# Additional packaging information for specific platforms
if sys.platform == 'darwin':
    # macOS application bundle
    app = BUNDLE(
        coll,
        name=f"{app_name}.app",
        icon=app_icon,
        bundle_identifier=None,
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
        },
    ) 