# core/state_manager.py
from typing import List, Dict, Tuple
from data.models import FileState, SaveState, ChangeType

class StateManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.current_state: Dict[str, FileState] = {}
        self.last_save: SaveState = None

    def update_current_state(self, ignore_handler) -> None:
        self.current_state = self.file_manager.get_files_state(ignore_handler)

    def get_changes(self) -> List[Tuple[ChangeType, str]]:
        changes = []
        current_files = set(self.current_state.keys())
        saved_files = set(self.last_save.files.keys()) if self.last_save else set()

        # Check for new and modified files
        for file in current_files:
            if file not in saved_files:
                changes.append((ChangeType.NEW, file))
            elif (self.last_save and 
                  self.current_state[file].hash != self.last_save.files[file].hash):
                changes.append((ChangeType.MODIFIED, file))

        # Check for deleted files
        for file in saved_files - current_files:
            changes.append((ChangeType.DELETED, file))

        return changes

    def set_last_save(self, save_state: SaveState) -> None:
        self.last_save = save_state