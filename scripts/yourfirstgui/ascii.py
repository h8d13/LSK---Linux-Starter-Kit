import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

class ASCIIRenderer(QWidget):
    def __init__(self, width=80, height=60):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: black;")
        
        self.grid_width = width
        self.grid_height = height
        self.ascii_chars = ['█', '▓', '▒', '░', '·', ' ']
        self.intensity = np.zeros((self.grid_height, self.grid_width))

    def set_intensity(self, intensity_array):
        """Update the intensity array that determines ASCII characters"""
        self.intensity = intensity_array
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.GlobalColor.white)
        
        cell_width = self.width() / self.grid_width
        cell_height = self.height() / self.grid_height
        
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                value = self.intensity[y, x]
                char_index = min(int(value * len(self.ascii_chars)), len(self.ascii_chars) - 1)
                char = self.ascii_chars[char_index]
                
                pos_x = x * cell_width
                pos_y = y * cell_height
                
                painter.drawText(
                    int(pos_x),
                    int(pos_y + cell_height),
                    char
                )
