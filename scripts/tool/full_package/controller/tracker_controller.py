# controller/tracker_controller.py
import os
from typing import List, Optional, Tuple
from data.models import SaveState, ChangeType
from core.file_manager import FileManager
from core.state_manager import StateManager
from core.ignore_controller import IgnoreController
from utils.logger import logger

class TrackerController:
    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = working_dir or os.getcwd()
        self.saves_dir = os.path.join(self.working_dir, '.saves')
        
        # Initialize components
        self.ignore_controller = IgnoreController()
        self.file_manager = FileManager(self.working_dir)
        self.state_manager = StateManager(self.file_manager)
        
        if not os.path.exists(self.saves_dir):
            os.makedirs(self.saves_dir)
            self.save_state("Initial state")
        
        self.refresh_state()

    def get_changes(self) -> List[Tuple[ChangeType, str]]:
        """Get list of changes in the current directory"""
        try:
            self.refresh_state()
            return self.state_manager.get_changes()
        except Exception as e:
            logger.error(f"Error getting changes: {e}")
            return []

    def refresh_state(self) -> None:
        try:
            self.state_manager.update_current_state(self.ignore_controller)
        except Exception as e:
            logger.error(f"Error refreshing state: {e}")

    def save_state(self, comment: str) -> bool:
        try:
            self.refresh_state()
            current_files = self.file_manager.get_files_state(self.ignore_controller)
            save_state = SaveState.create(comment, current_files)
            # Create save directory
            save_path = os.path.join(self.saves_dir, save_state.timestamp)
            os.makedirs(save_path)
            
            # Save files
            for file_path, file_state in current_files.items():
                src = os.path.join(self.working_dir, file_path)
                dst = os.path.join(save_path, file_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                self.file_manager.copy_file(src, dst)
            
            # Update state
            self.state_manager.set_last_save(save_state)
            return True
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            return False

    def get_saves(self) -> List[SaveState]:
        try:
            saves = []
            for save in sorted(os.listdir(self.saves_dir)):
                save_path = os.path.join(self.saves_dir, save)
                if os.path.isdir(save_path):
                    saves.append(SaveState(
                        timestamp=save,
                        comment=f"Save point {save}",
                        files=self.file_manager.get_files_state(self.ignore_controller)
                    ))
            return saves
        except Exception as e:
            logger.error(f"Error getting saves: {e}")
            return []

    def restore_state(self, timestamp: str) -> bool:
        try:
            save_path = os.path.join(self.saves_dir, timestamp)
            if not os.path.exists(save_path):
                return False
            
            # Clear current directory (except ignored)
            for root, _, files in os.walk(self.working_dir):
                if self.ignore_controller.should_ignore_dir(root):
                    continue
                for file in files:
                    if not self.ignore_controller.should_ignore_file(file):
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            continue
            
            # Restore files
            for root, _, files in os.walk(save_path):
                rel_root = os.path.relpath(root, save_path)
                for file in files:
                    src = os.path.join(root, file)
                    dst = os.path.join(self.working_dir, rel_root, file)
                    self.file_manager.copy_file(src, dst)
            
            self.refresh_state()
            return True
        except Exception as e:
            logger.error(f"Error restoring state: {e}")
            return False