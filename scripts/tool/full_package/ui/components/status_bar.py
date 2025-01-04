# ui/components/status_bar.py
from PyQt6.QtWidgets import QStatusBar
from datetime import datetime

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                color: #2c3e50;
            }
        """)
        self.showMessage("Ready")

    def update_status(self, changes_count: int):
        if changes_count > 0:
            self.showMessage(f"Found {changes_count} changes - Last check: {datetime.now().strftime('%H:%M:%S')}")
        else:
            self.showMessage(f"No changes detected - Last check: {datetime.now().strftime('%H:%M:%S')}")

    def show_save_status(self, success: bool):
        if success:
            self.showMessage("State saved successfully")
        else:
            self.showMessage("Failed to save state", 5000)  # Show for 5 seconds

    def show_restore_status(self, success: bool):
        if success:
            self.showMessage("State restored successfully")
        else:
            self.showMessage("Failed to restore state", 5000)