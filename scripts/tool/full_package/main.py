# main.py
import sys
from PyQt6.QtWidgets import QApplication
from controller.tracker_controller import TrackerController
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    controller = TrackerController()
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()