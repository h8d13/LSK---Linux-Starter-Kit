# ui/components/history_panel.py
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QListWidget
from datetime import datetime

class HistoryPanel(QGroupBox):
    def __init__(self, controller):
        super().__init__("Save History")
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.setAlternatingRowColors(True)
        layout.addWidget(self.history_list)
        self.setLayout(layout)

    def refresh(self):
        self.history_list.clear()
        for save in self.controller.get_saves():
            dt = datetime.strptime(save.timestamp, "%Y%m%d_%H%M%S")
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            self.history_list.addItem(f"{formatted_time} - {save.comment}")