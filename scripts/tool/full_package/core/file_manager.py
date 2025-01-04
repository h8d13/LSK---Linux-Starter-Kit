# core/file_manager.py
import os
import shutil
import hashlib
from typing import Dict, Optional
from data.models import FileState

class FileManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def get_file_hash(self, filepath: str) -> Optional[str]:
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def copy_file(self, src: str, dst: str) -> bool:
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            return True
        except:
            return False

    def get_files_state(self, ignore_handler) -> Dict[str, FileState]:
        files = {}
        for root, _, filenames in os.walk(self.base_dir):
            if ignore_handler.should_ignore_dir(root):
                continue
            
            for name in filenames:
                if ignore_handler.should_ignore_file(name):
                    continue
                    
                abs_path = os.path.join(root, name)
                rel_path = os.path.relpath(abs_path, self.base_dir)
                file_hash = self.get_file_hash(abs_path)
                
                if file_hash:
                    files[rel_path] = FileState(
                        path=rel_path,
                        hash=file_hash,
                        last_modified=os.path.getmtime(abs_path)
                    )
        return files