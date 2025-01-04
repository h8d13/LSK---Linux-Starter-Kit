# ui/components/changes_panel.py
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from data.models import ChangeType

class ChangesPanel(QGroupBox):
    def __init__(self):
        super().__init__("Current Changes")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.changes_list = QListWidget()
        self.changes_list.setAlternatingRowColors(True)
        layout.addWidget(self.changes_list)
        self.setLayout(layout)

    def update_changes(self, changes):
        self.changes_list.clear()
        
        for change_type, file in changes:
            item = QListWidgetItem(f"{change_type.value}: {file}")
            
            if change_type == ChangeType.NEW:
                item.setForeground(Qt.GlobalColor.green)
            elif change_type == ChangeType.MODIFIED:
                item.setForeground(Qt.GlobalColor.blue)
            else:
                item.setForeground(Qt.GlobalColor.red)
                
            self.changes_list.addItem(item)