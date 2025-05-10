"""
Application Configuration Settings
This module loads and provides access to application configuration settings.
"""
import os
import json

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default configuration
DEBUG = True
PORT = 5000
HOST = '0.0.0.0'
SECRET_KEY = 'dev_secret_key_change_in_production'
DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'acoustic_player.db')}"
DEFAULT_LIBRARY_PATH = os.path.join(os.path.expanduser("~"), "Music")
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'}
CORS_ORIGINS = ["*"]  # Allow all origins in development

# Load configuration from default_config.json if exists
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'default_config.json')

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
            
        # Override default settings with values from config file
        for key, value in config_data.items():
            if key.isupper():
                globals()[key] = value
    except Exception as e:
        print(f"Error loading configuration from {CONFIG_FILE}: {e}")

# Override settings with environment variables
for key in list(globals().keys()):
    if key.isupper():
        env_value = os.environ.get(key)
        if env_value is not None:
            # Convert environment variable to appropriate type
            current_value = globals()[key]
            if isinstance(current_value, bool):
                globals()[key] = env_value.lower() in ('true', 'yes', '1')
            elif isinstance(current_value, int):
                globals()[key] = int(env_value)
            elif isinstance(current_value, float):
                globals()[key] = float(env_value)
            elif isinstance(current_value, list):
                globals()[key] = [item.strip() for item in env_value.split(',')]
            else:
                globals()[key] = env_value