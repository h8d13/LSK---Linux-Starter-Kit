## This script will display a green/orange/red dot in the system tray until it hits any of the threshold values.
## Depending on distros there might need libraries or to allow notification tray applications

### sudo apt install -y libxcb1 libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 libxcb-render0 libxcb-render-util0
### sudo apt install -y qt6-base-dev qt6-wayland libqt5x11extras5

import sys
import psutil
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QFont, QRadialGradient
from functools import lru_cache

@dataclass(frozen=True)
class SystemThresholds:
    warning_cpu: float = 45.0
    warning_ram: float = 50.0
    warning_disk: float = 55.0
    cpu: float = 80.0
    ram: float = 85.0
    disk: float = 90.0

@dataclass(frozen=True)
class SystemMetrics:
    cpu: float
    ram: float
    disk: float

    @classmethod
    def get_current(cls):
        # Get all metrics at once to reduce system calls
        cpu = psutil.cpu_percent(interval=None)  # Non-blocking call
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return cls(
            cpu=cpu,
            ram=mem.percent,
            disk=disk.percent
        )

    def get_status(self, thresholds: SystemThresholds) -> str:
        if (self.cpu < thresholds.warning_cpu and 
            self.ram < thresholds.warning_ram and 
            self.disk < thresholds.warning_disk):
            return 'healthy'
        elif (self.cpu < thresholds.cpu and 
              self.ram < thresholds.ram and 
              self.disk < thresholds.disk):
            return 'warning'
        return 'critical'

class IconFactory:
    ICON_SIZE = 64
    CIRCLE_OFFSET = 12
    CIRCLE_SIZE = 40
    
    # Cache icons for each status
    @staticmethod
    @lru_cache(maxsize=3)  # Only 3 possible states
    def create_system_icon(status: str) -> QIcon:
        pixmap = QPixmap(IconFactory.ICON_SIZE, IconFactory.ICON_SIZE)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        gradient = IconFactory._get_health_gradient(status)
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            IconFactory.CIRCLE_OFFSET, 
            IconFactory.CIRCLE_OFFSET, 
            IconFactory.CIRCLE_SIZE, 
            IconFactory.CIRCLE_SIZE
        )
        painter.end()
        
        return QIcon(pixmap)

    @staticmethod
    def _get_health_gradient(status: str) -> QRadialGradient:
        gradient = QRadialGradient(32, 32, 25)
        
        if status == 'healthy':
            gradient.setColorAt(0, QColor(50, 255, 50))
            gradient.setColorAt(0.8, QColor(0, 200, 0))
            gradient.setColorAt(1, QColor(0, 150, 0))
        elif status == 'warning':
            gradient.setColorAt(0, QColor(255, 165, 0))
            gradient.setColorAt(0.8, QColor(255, 140, 0))
            gradient.setColorAt(1, QColor(255, 120, 0))
        else:  # critical
            gradient.setColorAt(0, QColor(255, 50, 50))
            gradient.setColorAt(0.8, QColor(200, 0, 0))
            gradient.setColorAt(1, QColor(150, 0, 0))
        return gradient

class SystemMonitorTray(QSystemTrayIcon):
    UPDATE_INTERVAL = 3000  # 3 seconds
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thresholds = SystemThresholds()
        self._cached_status = None
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        metrics = SystemMetrics.get_current()
        status = metrics.get_status(self.thresholds)
        self.setIcon(IconFactory.create_system_icon(status))
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
        self.timer.start(self.UPDATE_INTERVAL)

    def update_metrics(self):
        metrics = SystemMetrics.get_current()
        status = metrics.get_status(self.thresholds)
        
        # Only update icon if status changed
        if status != self._cached_status:
            self.setIcon(IconFactory.create_system_icon(status))
            self._cached_status = status
        
        # Update tooltip and status text
        self.setToolTip(self._format_tooltip(metrics))
        self.status_action.setText(self._format_status(metrics))

    @staticmethod
    def _format_tooltip(metrics: SystemMetrics) -> str:
        return (
            f"<div style='font-family: Segoe UI; padding: 5px;'>"
            f"<b>System Monitor</b><br>"
            f"CPU Usage: {metrics.cpu:2.1f}%<br>"
            f"RAM Usage: {metrics.ram:2.1f}%<br>"
            f"Disk Usage: {metrics.disk:2.1f}%<br>"
            f"<br><i>Right-click for menu</i></div>"
        )

    @staticmethod
    def _format_status(metrics: SystemMetrics) -> str:
        return f"CPU: {metrics.cpu:2.1f}% | RAM: {metrics.ram:2.1f}% | Disk: {metrics.disk:2.1f}%"

    @staticmethod
    @lru_cache(maxsize=1)  # Cache the menu style
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

####################################################################################################################
### Then to make this an executable:

# sudo apt install binutils
# pip install pyinstaller

# pyinstaller --onefile --windowed monitor.py

# This will create a one file executable in you curretn directory under ./dist/monitor
# You can now double click it like an app! (You might need to right click and run as program)

# Or you can chmod +x monitor.py
# Add a shebang at the start of the file:
# !/usr/bin/env python3

### But this kind of brings us to another debate... 50mb for a green/orange/red dot is a bit much. 
# Better solution is to make a setup + source code, the runner basically just checks for basic dependencies. 

import sys
import subprocess
from setuptools import setup, find_packages

def check_and_install(req_file="requirements.txt"):
    """
    Checks if each package in requirements.txt is importable.
    If not, installs it using pip.
    """
    try:
        with open(req_file, "r") as f:
            for line in f:
                package = line.strip()
                # Skip empty lines or commented lines
                if not package or package.startswith("#"):
                    continue

                # Extract the raw import name (e.g., 'psutil' from 'psutil==5.9.0')
                pkg_name = package.split("==")[0].split(">=")[0].split("<=")[0]
                try:
                    __import__(pkg_name)
                except ImportError:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except FileNotFoundError:
        print(f"Could not find {req_file}, skipping dependency check...")

# Before running the normal setup, ensure dependencies are installed
check_and_install()

setup(
    name="system-monitor-tray",
    version="0.1.0",
    description="A system tray monitor for CPU, RAM, and disk usage.",
    author="Your Name",
    author_email="example@example.com",
    packages=find_packages(),
    py_modules=["monitor"],  # Main script is monitor.py
    install_requires=[
        "psutil",
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            # Installs a command line entry point called "system-monitor"
            # that runs monitor.py's main() function.
            "system-monitor=monitor:main",
        ]
    },
)

## Then the user can simply: 
# python setup.py install
# then run system-monitor
# or python -m monitor


### You can then go a step further and create a full package with a TOML file and __init__ methods. 

#### Here I've made a version that needs 2 things: htop & pavucontrol

### This shows the power of being able to customize while using low level libraries:
###################################################################################################################################

import sys
import psutil
from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QFont, QRadialGradient
from functools import lru_cache

@dataclass(frozen=True)
class SystemThresholds:
    warning_cpu: float = 45.0
    warning_ram: float = 50.0
    warning_disk: float = 55.0
    cpu: float = 80.0
    ram: float = 85.0
    disk: float = 90.0

@dataclass(frozen=True)
class SystemMetrics:
    cpu: float
    ram: float
    disk: float

    @classmethod
    def get_current(cls):
        # Get all metrics at once to reduce system calls
        cpu = psutil.cpu_percent(interval=None)  # Non-blocking call
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return cls(
            cpu=cpu,
            ram=mem.percent,
            disk=disk.percent
        )

    def get_status(self, thresholds: SystemThresholds) -> str:
        if (self.cpu < thresholds.warning_cpu and 
            self.ram < thresholds.warning_ram and 
            self.disk < thresholds.warning_disk):
            return 'healthy'
        elif (self.cpu < thresholds.cpu and 
              self.ram < thresholds.ram and 
              self.disk < thresholds.disk):
            return 'warning'
        return 'critical'

class IconFactory:
    ICON_SIZE = 64
    CIRCLE_OFFSET = 12
    CIRCLE_SIZE = 40
    
    # Cache icons for each status
    @staticmethod
    @lru_cache(maxsize=3)  # Only 3 possible states
    def create_system_icon(status: str) -> QIcon:
        pixmap = QPixmap(IconFactory.ICON_SIZE, IconFactory.ICON_SIZE)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        gradient = IconFactory._get_health_gradient(status)
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            IconFactory.CIRCLE_OFFSET, 
            IconFactory.CIRCLE_OFFSET, 
            IconFactory.CIRCLE_SIZE, 
            IconFactory.CIRCLE_SIZE
        )
        painter.end()
        
        return QIcon(pixmap)

    @staticmethod
    def _get_health_gradient(status: str) -> QRadialGradient:
        gradient = QRadialGradient(32, 32, 25)
        
        if status == 'healthy':
            gradient.setColorAt(0, QColor(50, 255, 50))
            gradient.setColorAt(0.8, QColor(0, 200, 0))
            gradient.setColorAt(1, QColor(0, 150, 0))
        elif status == 'warning':
            gradient.setColorAt(0, QColor(255, 165, 0))
            gradient.setColorAt(0.8, QColor(255, 140, 0))
            gradient.setColorAt(1, QColor(255, 120, 0))
        else:  # critical
            gradient.setColorAt(0, QColor(255, 50, 50))
            gradient.setColorAt(0.8, QColor(200, 0, 0))
            gradient.setColorAt(1, QColor(150, 0, 0))
        return gradient

class SystemMonitorTray(QSystemTrayIcon):
    UPDATE_INTERVAL = 3000  # 3 seconds
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thresholds = SystemThresholds()
        self._cached_status = None
        self.setup_ui()
        self.start_monitoring()

    def setup_ui(self):
        metrics = SystemMetrics.get_current()
        status = metrics.get_status(self.thresholds)
        self.setIcon(IconFactory.create_system_icon(status))
        self.setup_menu()
        self.setVisible(True)

    def setup_menu(self):
        menu = QMenu()
        menu.setStyleSheet(self._get_menu_style())
        
        self.status_action = menu.addAction("Updating...")
        self.status_action.setFont(QFont("Segoe UI", 9))
        self.status_action.triggered.connect(self.launch_htop)
        
        menu.addSeparator()
        
        # Add the privacy action
        privacy_action = menu.addAction("Privacy")
        privacy_action.triggered.connect(self.launch_pavucontrol)
        
        menu.addSeparator()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        
        self.setContextMenu(menu)

    def launch_htop(self):
        try:
            import subprocess
            subprocess.Popen(['x-terminal-emulator', '-e', 'htop'])
        except Exception as e:
            print(f"Failed to launch htop: {e}")

    def launch_pavucontrol(self):
        try:
            import subprocess
            subprocess.Popen(['pavucontrol'])
        except Exception as e:
            print(f"Failed to launch pavucontrol: {e}")

    def start_monitoring(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(self.UPDATE_INTERVAL)

    def update_metrics(self):
        metrics = SystemMetrics.get_current()
        status = metrics.get_status(self.thresholds)
        
        # Only update icon if status changed
        if status != self._cached_status:
            self.setIcon(IconFactory.create_system_icon(status))
            self._cached_status = status
        
        # Update tooltip and status text
        self.setToolTip(self._format_tooltip(metrics))
        self.status_action.setText(self._format_status(metrics))

    @staticmethod
    def _format_tooltip(metrics: SystemMetrics) -> str:
        return (
            f"<div style='font-family: Segoe UI; padding: 5px;'>"
            f"<b>System Monitor</b><br>"
            f"CPU Usage: {metrics.cpu:2.1f}%<br>"
            f"RAM Usage: {metrics.ram:2.1f}%<br>"
            f"Disk Usage: {metrics.disk:2.1f}%<br>"
            f"<br><i>Right-click for menu</i></div>"
        )

    @staticmethod
    def _format_status(metrics: SystemMetrics) -> str:
        return f"CPU: {metrics.cpu:2.1f}% | RAM: {metrics.ram:2.1f}% | Disk: {metrics.disk:2.1f}%"

    @staticmethod
    @lru_cache(maxsize=1)  # Cache the menu style
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


## Pavucontrol let's you block microphone, etc or change sources when needed. 
### And htop gives you the full monitor of system on top our little icon system. 
### Make sure to install them. 

##### For an even cooler integration you can compile this code and launch it with start up apps. 
### Simply go to start up and select your executable.

## To compile with optimal settings (altho there are a lot more) pyinstaller --onefile --windowed --optimize=2 monitor.py

### If you're done with this tutorial go to CPPVERSION :)



