#include "monitor.h"
#include <QApplication>
#include <QProcess>
#include <QDebug>
#include <sys/sysinfo.h>
#include <sys/statvfs.h>
#include <fstream>
#include <thread>

SystemMetrics SystemMetrics::getCurrentMetrics() {
    SystemMetrics metrics;
    metrics.cpu = getCpuUsage();
    metrics.ram = getRamUsage();
    metrics.disk = getDiskUsage();
    return metrics;
}

QString SystemMetrics::getStatus(const SystemThresholds& thresholds) const {
    if (cpu < thresholds.warning_cpu && 
        ram < thresholds.warning_ram && 
        disk < thresholds.warning_disk) {
        return "healthy";
    } else if (cpu < thresholds.cpu && 
               ram < thresholds.ram && 
               disk < thresholds.disk) {
        return "warning";
    }
    return "critical";
}

float SystemMetrics::getCpuUsage() {
    static long long previousIdle = 0;
    static long long previousTotal = 0;
    
    std::ifstream statFile("/proc/stat");
    std::string line;
    std::getline(statFile, line);
    
    long long user, nice, system, idle, iowait, irq, softirq, steal;
    sscanf(line.c_str(), "cpu %lld %lld %lld %lld %lld %lld %lld %lld",
           &user, &nice, &system, &idle, &iowait, &irq, &softirq, &steal);
    
    long long currentIdle = idle + iowait;
    long long currentTotal = user + nice + system + idle + iowait + irq + softirq + steal;
    
    long long idleDelta = currentIdle - previousIdle;
    long long totalDelta = currentTotal - previousTotal;
    
    float cpuUsage = 100.0 * (1.0 - static_cast<float>(idleDelta) / totalDelta);
    
    previousIdle = currentIdle;
    previousTotal = currentTotal;
    
    return cpuUsage;
}

float SystemMetrics::getRamUsage() {
    struct sysinfo si;
    if (sysinfo(&si) != 0) {
        return 0.0f;
    }

    unsigned long long totalRam = si.totalram;
    unsigned long long freeRam = si.freeram;
    unsigned long long buffersRam = si.bufferram;
    
    std::ifstream meminfo("/proc/meminfo");
    std::string line;
    unsigned long long cachedRam = 0;
    
    while (std::getline(meminfo, line)) {
        if (line.starts_with("Cached:")) {
            sscanf(line.c_str(), "Cached: %llu", &cachedRam);
            cachedRam *= 1024;
            break;
        }
    }

    unsigned long long usedRam = totalRam - freeRam - buffersRam - cachedRam;
    return (usedRam * 100.0) / totalRam;
}

float SystemMetrics::getDiskUsage() {
    struct statvfs fs;
    if (statvfs("/", &fs) != 0) {
        return 0.0f;
    }
    
    unsigned long long totalBlocks = fs.f_blocks;
    unsigned long long freeBlocks = fs.f_bfree;
    unsigned long long usedBlocks = totalBlocks - freeBlocks;
    
    return (usedBlocks * 100.0) / totalBlocks;
}

QIcon IconFactory::createSystemIcon(const QString& status) {
    QPixmap pixmap(ICON_SIZE, ICON_SIZE);
    pixmap.fill(Qt::transparent);
    
    QPainter painter(&pixmap);
    painter.setRenderHint(QPainter::Antialiasing);
    
    QRadialGradient gradient = getHealthGradient(status);
    painter.setBrush(gradient);
    painter.setPen(Qt::NoPen);
    painter.drawEllipse(CIRCLE_OFFSET, CIRCLE_OFFSET, CIRCLE_SIZE, CIRCLE_SIZE);
    
    return QIcon(pixmap);
}

QRadialGradient IconFactory::getHealthGradient(const QString& status) {
    QRadialGradient gradient(32, 32, 25);
    
    if (status == "healthy") {
        gradient.setColorAt(0, QColor(50, 255, 50));
        gradient.setColorAt(0.8, QColor(0, 200, 0));
        gradient.setColorAt(1, QColor(0, 150, 0));
    } else if (status == "warning") {
        gradient.setColorAt(0, QColor(255, 165, 0));
        gradient.setColorAt(0.8, QColor(255, 140, 0));
        gradient.setColorAt(1, QColor(255, 120, 0));
    } else {
        gradient.setColorAt(0, QColor(255, 50, 50));
        gradient.setColorAt(0.8, QColor(200, 0, 0));
        gradient.setColorAt(1, QColor(150, 0, 0));
    }
    return gradient;
}

SystemMonitorTray::SystemMonitorTray(QObject* parent) 
    : QSystemTrayIcon(parent), thresholds() {
    setupUI();
    startMonitoring();
}

void SystemMonitorTray::updateMetrics() {
    auto metrics = SystemMetrics::getCurrentMetrics();
    QString status = metrics.getStatus(thresholds);
    
    if (status != cachedStatus) {
        setIcon(IconFactory::createSystemIcon(status));
        cachedStatus = status;
    }
    
    setToolTip(formatTooltip(metrics));
    statusAction->setText(formatStatus(metrics));
}

void SystemMonitorTray::setupUI() {
    auto metrics = SystemMetrics::getCurrentMetrics();
    QString status = metrics.getStatus(thresholds);
    setIcon(IconFactory::createSystemIcon(status));
    setupMenu();
    show();
}

void SystemMonitorTray::setupMenu() {
    auto menu = new QMenu();
    menu->setStyleSheet(getMenuStyle());
    
    statusAction = menu->addAction("Updating...");
    statusAction->setFont(QFont("Segoe UI", 9));
    connect(statusAction, &QAction::triggered, this, &SystemMonitorTray::launchHtop);
    
    menu->addSeparator();
    
    auto privacyAction = menu->addAction("Privacy");
    connect(privacyAction, &QAction::triggered, this, &SystemMonitorTray::launchPavucontrol);
    
    menu->addSeparator();
    auto exitAction = menu->addAction("Exit");
    connect(exitAction, &QAction::triggered, qApp, &QApplication::quit);
    
    setContextMenu(menu);
}

void SystemMonitorTray::startMonitoring() {
    timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &SystemMonitorTray::updateMetrics);
    timer->start(UPDATE_INTERVAL);
}

QString SystemMonitorTray::formatTooltip(const SystemMetrics& metrics) {
    return QString("<div style='font-family: Segoe UI; padding: 5px;'>"
                  "<b>System Monitor</b><br>"
                  "CPU Usage: %1%<br>"
                  "RAM Usage: %2%<br>"
                  "Disk Usage: %3%<br>"
                  "<br><i>Right-click for menu</i></div>")
            .arg(metrics.cpu, 0, 'f', 1)
            .arg(metrics.ram, 0, 'f', 1)
            .arg(metrics.disk, 0, 'f', 1);
}

QString SystemMonitorTray::formatStatus(const SystemMetrics& metrics) {
    return QString("CPU: %1% | RAM: %2% | Disk: %3%")
            .arg(metrics.cpu, 0, 'f', 1)
            .arg(metrics.ram, 0, 'f', 1)
            .arg(metrics.disk, 0, 'f', 1);
}

QString SystemMonitorTray::getMenuStyle() {
    return "QMenu {"
           "    background-color: #2D2D2D;"
           "    border: 1px solid #3D3D3D;"
           "    border-radius: 4px;"
           "    padding: 5px;"
           "}"
           "QMenu::item {"
           "    padding: 8px 25px;"
           "    color: #FFFFFF;"
           "}"
           "QMenu::item:selected {"
           "    background-color: #404040;"
           "    border-radius: 2px;"
           "}"
           "QMenu::item:disabled {"
           "    color: #808080;"
           "    background-color: transparent;"
           "}"
           "QMenu::separator {"
           "    height: 1px;"
           "    background: #3D3D3D;"
           "    margin: 5px 0px;"
           "}";
}

void SystemMonitorTray::launchHtop() {
    QProcess::startDetached("x-terminal-emulator", QStringList() << "-e" << "htop");
}

void SystemMonitorTray::launchPavucontrol() {
    QProcess::startDetached("pavucontrol");
}