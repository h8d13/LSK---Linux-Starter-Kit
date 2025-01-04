# Internal
import os
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, Qt
# External
from file import FileTracker

class TrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File State Tracker")
        self.setGeometry(100, 100, 800, 500)
        
        # Initialize the core tracker
        self.tracker = FileTracker()
        
        self.init_ui()
        
        # Setup timer for changes
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_changes)
        self.timer.start(2000)

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        main_layout = QVBoxLayout()

        # Info header
        info_layout = QHBoxLayout()
        self.watching_label = QLabel(f"Watching: {os.path.basename(self.tracker.cwd)}")
        self.watching_label.setStyleSheet("font-weight: bold")
        self.save_count_label = QLabel("Saves: 0")
        info_layout.addWidget(self.watching_label)
        info_layout.addWidget(self.save_count_label)
        info_layout.addStretch()
        main_layout.addLayout(info_layout)

        # Split view
        content_layout = QHBoxLayout()

        # Left side - Changes
        changes_group = QGroupBox("Current Changes")
        changes_layout = QVBoxLayout()
        self.changes_list = QListWidget()
        self.changes_list.setAlternatingRowColors(True)
        changes_layout.addWidget(self.changes_list)
        changes_group.setLayout(changes_layout)
        content_layout.addWidget(changes_group)

        # Right side - Save History
        history_group = QGroupBox("Save History")
        history_layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        history_layout.addWidget(self.history_list)
        history_group.setLayout(history_layout)
        content_layout.addWidget(history_group)

        main_layout.addLayout(content_layout)

        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Current State")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        
        restore_btn = QPushButton("Restore Previous State")
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        save_btn.clicked.connect(self.prompt_save)
        restore_btn.clicked.connect(self.prompt_restore)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(restore_btn)
        main_layout.addLayout(button_layout)

        self.statusBar().showMessage("Monitoring changes...")
        
        widget.setLayout(main_layout)
        self.update_history()

    def check_changes(self):
        changes = self.tracker.get_changes()
        
        self.changes_list.clear()
        if changes:
            for change_type, file in changes:
                item = QListWidgetItem()
                if change_type == "New":
                    item.setForeground(Qt.GlobalColor.green)
                elif change_type == "Modified":
                    item.setForeground(Qt.GlobalColor.blue)
                else:
                    item.setForeground(Qt.GlobalColor.red)
                item.setText(f"{change_type}: {file}")
                self.changes_list.addItem(item)
            self.statusBar().showMessage(f"Found {len(changes)} changes")
        else:
            self.statusBar().showMessage("No changes detected")

    def update_history(self):
        self.history_list.clear()
        saves = self.tracker.get_saves()
        
        for save in saves:
            dt = datetime.strptime(save['timestamp'], "%Y%m%d_%H%M%S")
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            self.history_list.addItem(f"{formatted_time} - {save['comment']}")
        
        self.save_count_label.setText(f"Saves: {len(saves)}")

    def prompt_save(self):
        comment, ok = QInputDialog.getText(self, 'Save', 'Comment for this save:')
        if ok and comment:
            self.tracker.save_state(comment)
            self.update_history()
            self.statusBar().showMessage("State saved successfully")

    def prompt_restore(self):
        saves = self.tracker.get_saves()
        if not saves:
            self.statusBar().showMessage("No saves found")
            return

        items = []
        for save in saves:
            dt = datetime.strptime(save['timestamp'], "%Y%m%d_%H%M%S")
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            items.append(f"{formatted_time} - {save['comment']}")

        save, ok = QInputDialog.getItem(self, 'Restore', 'Select save:', items, 0, False)
        if ok and save:
            timestamp = datetime.strptime(save.split(' - ')[0], "%Y-%m-%d %H:%M:%S")\
                               .strftime("%Y%m%d_%H%M%S")
            self.tracker.restore_state(timestamp)
            self.statusBar().showMessage("State restored successfully")
            self.check_changes()

if __name__ == '__main__':
    app = QApplication([])
    window = TrackerGUI()
    window.show()
    app.exec()
