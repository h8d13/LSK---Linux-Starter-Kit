# data/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from enum import Enum

class ChangeType(Enum):
    NEW = "New"
    MODIFIED = "Modified"
    DELETED = "Deleted"

@dataclass
class FileState:
    path: str
    hash: str
    last_modified: float

@dataclass
class SaveState:
    timestamp: str
    comment: str
    files: Dict[str, FileState]

    @staticmethod
    def create(comment: str, files: Dict[str, FileState]) -> 'SaveState':
        return SaveState(
            timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"),
            comment=comment,
            files=files
        )