# utils/config.py
import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    'ignore_dirs': {
        '.saves', '.git', '__pycache__', 
        '.venv', 'venv', 'env', 
        'node_modules', '.pytest_cache'
    },
    'ignore_extensions': {
        '.pyc', '.pyo', '.pyd', '.so', 
        '.git', '.env'
    },
    'save_interval': 2000,  # ms
    'max_saves': 100
}

def load_config() -> Dict[str, Any]:
    config_path = 'config.json'
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
    except Exception as e:
        print(f"Error loading config: {e}")
    return DEFAULT_CONFIG

def save_config(config: Dict[str, Any]) -> bool:
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False