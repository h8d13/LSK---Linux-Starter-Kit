#pragma once

#include <QSystemTrayIcon>
#include <QMenu>
#include <QTimer>
#include <QPainter>
#include <QRadialGradient>
#include <memory>

struct SystemThresholds {
    const float warning_cpu = 45.0;
    const float warning_ram = 50.0;
    const float warning_disk = 55.0;
    const float cpu = 80.0;
    const float ram = 85.0;
    const float disk = 90.0;
};

struct SystemMetrics {
    float cpu;
    float ram;
    float disk;

    static SystemMetrics getCurrentMetrics();
    QString getStatus(const SystemThresholds& thresholds) const;

private:
    static float getCpuUsage();
    static float getRamUsage();
    static float getDiskUsage();
};

class IconFactory {
public:
    static constexpr int ICON_SIZE = 64;
    static constexpr int CIRCLE_OFFSET = 12;
    static constexpr int CIRCLE_SIZE = 40;

    static QIcon createSystemIcon(const QString& status);

private:
    static QRadialGradient getHealthGradient(const QString& status);
};

class SystemMonitorTray : public QSystemTrayIcon {
    Q_OBJECT

public:
    explicit SystemMonitorTray(QObject* parent = nullptr);

private slots:
    void updateMetrics();

private:
    static constexpr int UPDATE_INTERVAL = 3000;
    SystemThresholds thresholds;
    QString cachedStatus;
    QAction* statusAction;
    QTimer* timer;

    void setupUI();
    void setupMenu();
    void startMonitoring();
    static QString formatTooltip(const SystemMetrics& metrics);
    static QString formatStatus(const SystemMetrics& metrics);
    static QString getMenuStyle();
    void launchHtop();
    void launchPavucontrol();
};
