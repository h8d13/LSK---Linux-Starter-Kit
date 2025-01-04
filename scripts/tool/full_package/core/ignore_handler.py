# core/ignore_handler.py
import os
from typing import Set
from utils.config import load_config

class IgnoreHandler:
    def __init__(self):
        config = load_config()
        self.ignore_dirs: Set[str] = set(config.get('ignore_dirs', []))
        self.ignore_extensions: Set[str] = set(config.get('ignore_extensions', []))

    def should_ignore_dir(self, path: str) -> bool:
        return any(part in self.ignore_dirs for part in path.split(os.sep))

    def should_ignore_file(self, filename: str) -> bool:
        return any(filename.endswith(ext) for ext in self.ignore_extensions)