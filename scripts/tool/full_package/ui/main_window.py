# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
from .components.changes_panel import ChangesPanel
from .components.history_panel import HistoryPanel
from .components.status_bar import StatusBar
from .components.toolbar import Toolbar

class MainWindow(QMainWindow):
    def __init__(self, tracker_controller):
        super().__init__()
        self.controller = tracker_controller
        
        self.setWindowTitle("File State Tracker")
        self.setGeometry(100, 100, 800, 500)
        
        self.init_ui()
        
        # Setup auto-refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # Create components
        self.toolbar = Toolbar(self.controller)
        self.changes_panel = ChangesPanel()
        self.history_panel = HistoryPanel(self.controller)
        self.status_bar = StatusBar()

        # Add components to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.changes_panel)
        layout.addWidget(self.history_panel)
        
        central.setLayout(layout)
        self.setStatusBar(self.status_bar)

    def refresh(self):
        changes = self.controller.get_changes()
        self.changes_panel.update_changes(changes)
        self.history_panel.refresh()
        self.status_bar.update_status(len(changes))