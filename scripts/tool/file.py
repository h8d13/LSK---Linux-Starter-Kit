import os
import shutil
import json
import hashlib
from datetime import datetime

class FileTracker:
    def __init__(self, working_dir=None):
        self.cwd = working_dir or os.getcwd()
        self.saves_dir = os.path.join(self.cwd, '.saves')
        
        self.ignore_dirs = {'.saves', '.git', '__pycache__', '.venv', 'venv', 
                          'env', 'node_modules', '.pytest_cache'}
        self.ignore_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.git'}
        
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
            self.save_state("Initial state")
            
        self.last_state = self.get_files()

    def should_ignore(self, path):
        path_parts = path.split(os.sep)
        return any(part in self.ignore_dirs for part in path_parts) or \
               any(path.endswith(ext) for ext in self.ignore_extensions)

    def get_files(self):
        files = {}
        for root, _, filenames in os.walk(self.cwd):
            if self.should_ignore(root):
                continue
            for name in filenames:
                if self.should_ignore(name):
                    continue
                path = os.path.join(root, name)
                try:
                    with open(path, 'rb') as f:
                        files[os.path.relpath(path, self.cwd)] = hashlib.md5(f.read()).hexdigest()
                except:
                    continue
        return files

    def get_changes(self):
        current_files = self.get_files()
        changes = []
        
        for file, hash in current_files.items():
            if file not in self.last_state:
                changes.append(("New", file))
            elif hash != self.last_state[file]:
                changes.append(("Modified", file))
        
        for file in self.last_state:
            if file not in current_files:
                changes.append(("Deleted", file))
                
        return changes

    def save_state(self, comment):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(self.saves_dir, timestamp)
        os.makedirs(save_path)

        current_files = self.get_files()
        for file in current_files:
            src = os.path.join(self.cwd, file)
            dst = os.path.join(save_path, file)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

        with open(os.path.join(save_path, 'meta.json'), 'w') as f:
            json.dump({
                'comment': comment,
                'timestamp': timestamp,
                'files': current_files
            }, f)
        
        self.last_state = current_files
        return timestamp

    def get_saves(self):
        saves = []
        for save in sorted(os.listdir(self.saves_dir), reverse=True):
            try:
                with open(os.path.join(self.saves_dir, save, 'meta.json')) as f:
                    saves.append(json.load(f))
            except:
                continue
        return saves

    def restore_state(self, timestamp):
        save_path = os.path.join(self.saves_dir, timestamp)
        
        # Load the saved state
        with open(os.path.join(save_path, 'meta.json')) as f:
            saved_state = json.load(f)
        
        # Restore files
        for file in saved_state['files']:
            src = os.path.join(save_path, file)
            dst = os.path.join(self.cwd, file)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
        
        self.last_state = saved_state['files']
        return saved_state