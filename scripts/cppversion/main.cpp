#include "monitor.h"
#include <QApplication>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    app.setQuitOnLastWindowClosed(false);
    
    if (!QSystemTrayIcon::isSystemTrayAvailable()) {
        qDebug() << "System tray not available!";
        return 1;
    }
    
    SystemMonitorTray tray;
    return app.exec();
}
