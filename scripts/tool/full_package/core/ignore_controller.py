# core/ignore_controller.py
from typing import Set
from utils.config import load_config, save_config
from utils.logger import logger

class IgnoreController:
    def __init__(self):
        self._config = load_config()
        self._ignore_dirs: Set[str] = set(self._config['ignore_dirs'])
        self._ignore_extensions: Set[str] = set(self._config['ignore_extensions'])
        self._custom_ignores: Set[str] = set()

    def should_ignore_dir(self, path: str) -> bool:
        """Check if directory should be ignored"""
        path_parts = path.split('/')
        return any(part in self._ignore_dirs for part in path_parts)

    def should_ignore_file(self, path: str) -> bool:
        """Check if file should be ignored"""
        return any(path.endswith(ext) for ext in self._ignore_extensions)

    def should_ignore(self, path: str) -> bool:
        """General ignore check"""
        # Check custom ignores
        if any(pattern in path for pattern in self._custom_ignores):
            return True
        
        # Check if it's a directory ignore
        if self.should_ignore_dir(path):
            return True
            
        # Check if it's a file ignore
        if self.should_ignore_file(path):
            return True
            
        return False

    def add_ignore_pattern(self, pattern: str) -> bool:
        try:
            if pattern.endswith('/'):
                self._ignore_dirs.add(pattern.rstrip('/'))
            elif pattern.startswith('.'):
                self._ignore_extensions.add(pattern)
            else:
                self._custom_ignores.add(pattern)
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Error adding ignore pattern: {e}")
            return False

    def remove_ignore_pattern(self, pattern: str) -> bool:
        try:
            if pattern in self._ignore_dirs:
                self._ignore_dirs.remove(pattern)
            elif pattern in self._ignore_extensions:
                self._ignore_extensions.remove(pattern)
            elif pattern in self._custom_ignores:
                self._custom_ignores.remove(pattern)
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Error removing ignore pattern: {e}")
            return False

    def _save_config(self) -> None:
        self._config.update({
            'ignore_dirs': list(self._ignore_dirs),
            'ignore_extensions': list(self._ignore_extensions),
            'custom_ignores': list(self._custom_ignores)
        })
        save_config(self._config)