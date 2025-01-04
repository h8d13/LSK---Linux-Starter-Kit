# ui/components/toolbar.py
from PyQt6.QtWidgets import QToolBar, QPushButton, QInputDialog
from ..styles import SAVE_BUTTON_STYLE, RESTORE_BUTTON_STYLE

class Toolbar(QToolBar):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        save_btn = QPushButton("Save Current State")
        save_btn.setStyleSheet(SAVE_BUTTON_STYLE)
        save_btn.clicked.connect(self.prompt_save)

        restore_btn = QPushButton("Restore Previous State")
        restore_btn.setStyleSheet(RESTORE_BUTTON_STYLE)
        restore_btn.clicked.connect(self.prompt_restore)

        self.addWidget(save_btn)
        self.addWidget(restore_btn)

    def prompt_save(self):
        comment, ok = QInputDialog.getText(self, 'Save', 'Comment for this save:')
        if ok and comment:
            self.controller.save_state(comment)

    def prompt_restore(self):
        saves = self.controller.get_saves()
        if not saves:
            return

        items = [f"{save.timestamp} - {save.comment}" for save in saves]
        save, ok = QInputDialog.getItem(self, 'Restore', 'Select save:', items, 0, False)
        
        if ok and save:
            timestamp = save.split(' - ')[0]
            self.controller.restore_state(timestamp)