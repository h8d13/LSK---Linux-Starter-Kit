# Internal
import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
# External
from ascii import ASCIIRenderer

class PlasmaEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCII Plasma")
        
        # Create ASCII renderer
        self.renderer = ASCIIRenderer(width=80, height=60)
        self.setCentralWidget(self.renderer)
        
        # Initialize plasma parameters
        self.time = 0
        
        # Setup animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plasma)
        self.timer.start(50)  # 50ms = 20 fps

    def calculate_plasma(self, x, y, time):
        value = np.sin(x * 0.1 + time)
        value += np.sin(y * 0.1 + time)
        value += np.sin((x + y) * 0.1 + time)
        value += np.sin(np.sqrt((x*x + y*y) * 0.1) + time)
        return value

    def update_plasma(self):
        self.time += 0.2
        plasma = np.zeros((self.renderer.grid_height, self.renderer.grid_width))
        
        for y in range(self.renderer.grid_height):
            for x in range(self.renderer.grid_width):
                value = self.calculate_plasma(x, y, self.time)
                plasma[y, x] = (value + 4) / 8
        
        self.renderer.set_intensity(plasma)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlasmaEffect()
    window.show()
    sys.exit(app.exec())
