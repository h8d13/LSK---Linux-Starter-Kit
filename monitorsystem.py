## This script will display a green dot in the system tray until it hits any of the threshold values.
## Depending on distros there might need libraries or to allow notification tray applications

### sudo apt install qt6-base-dev


import sys
import psutil
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QFont, QRadialGradient

@dataclass
class SystemThresholds:
    cpu: float = 80.0  # 80% CPU usage
    ram: float = 85.0  # 85% RAM usage
    disk: float = 90.0 # 90% disk usage

@dataclass
class SystemMetrics:
    cpu: float
    ram: float
    disk: float

    @classmethod
    def get_current(cls):
        return cls(
            cpu=psutil.cpu_percent(),
            ram=psutil.virtual_memory().percent,
            disk=psutil.disk_usage('/').percent
        )

    def is_healthy(self, thresholds: SystemThresholds) -> bool:
        return (self.cpu < thresholds.cpu and 
                self.ram < thresholds.ram and 
                self.disk < thresholds.disk)

class IconFactory:
    @staticmethod
    def create_system_icon(is_healthy: bool) -> QIcon:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = IconFactory._get_health_gradient(is_healthy)
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(12, 12, 40, 40)
        painter.end()
        
        return QIcon(pixmap)

    @staticmethod
    def _get_health_gradient(is_healthy: bool) -> QRadialGradient:
        gradient = QRadialGradient(32, 32, 25)
        if is_healthy:
            gradient.setColorAt(0, QColor(50, 255, 50))
            gradient.setColorAt(0.8, QColor(0, 200, 0))
            gradient.setColorAt(1, QColor(0, 150, 0))
        else:
            gradient.setColorAt(0, QColor(255, 50, 50))
            gradient.setColorAt(0.8, QColor(200, 0, 0))
            gradient.setColorAt(1, QColor(150, 0, 0))
        return gradient

class SystemMonitorTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thresholds = SystemThresholds()
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        self.setIcon(IconFactory.create_system_icon(True))
        self.setup_menu()
        self.setVisible(True)

    def setup_menu(self):
        menu = QMenu()
        menu.setStyleSheet(self._get_menu_style())
        
        self.status_action = menu.addAction("Updating...")
        self.status_action.setFont(QFont("Segoe UI", 9))
        self.status_action.setEnabled(False)
        
        menu.addSeparator()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        
        self.setContextMenu(menu)

    def start_monitoring(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)

    def update_metrics(self):
        metrics = SystemMetrics.get_current()
        is_healthy = metrics.is_healthy(self.thresholds)
        
        self.setIcon(IconFactory.create_system_icon(is_healthy))
        self.update_tooltip(metrics)
        self.update_status(metrics)

    def update_tooltip(self, metrics: SystemMetrics):
        tooltip = self._format_tooltip(metrics)
        self.setToolTip(tooltip)

    def update_status(self, metrics: SystemMetrics):
        status = self._format_status(metrics)
        self.status_action.setText(status)

    def _format_tooltip(self, metrics: SystemMetrics) -> str:
        return f"""
            <div style='font-family: Segoe UI; padding: 5px;'>
                <b>System Monitor</b><br>
                CPU Usage: {metrics.cpu:2.1f}%<br>
                RAM Usage: {metrics.ram:2.1f}%<br>
                Disk Usage: {metrics.disk:2.1f}%<br>
                <br>
                <i>Right-click for menu</i>
            </div>
        """

    def _format_status(self, metrics: SystemMetrics) -> str:
        return f"CPU: {metrics.cpu:2.1f}% | RAM: {metrics.ram:2.1f}% | Disk: {metrics.disk:2.1f}%"

    @staticmethod
    def _get_menu_style() -> str:
        return """
            QMenu {
                background-color: #2D2D2D;
                border: 1px solid #3D3D3D;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #404040;
                border-radius: 2px;
            }
            QMenu::item:disabled {
                color: #808080;
                background-color: transparent;
            }
            QMenu::separator {
                height: 1px;
                background: #3D3D3D;
                margin: 5px 0px;
            }
        """

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray not available!")
        return 1
    
    tray = SystemMonitorTray()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
