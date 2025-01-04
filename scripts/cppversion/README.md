# CPP Version

So as we said in the other python version we want to be able to make our code as small of a footprint as possible. 
Using cpp we can reduce the total compiled size to about 90kb (with very little opti) 

How to use CMake basics:

- Create the CMakeLists.txt file in your code directory (this is like the guide for CMake to understand what to compile)
- Now ``` mkdir build ```to create the output folder
- Then ``` cd build ``` to move to the folder
- ``` cmake .. ``` Checks the build
- ``` make ``` Creates the final output

- Can ```sudo rm -rf build``` to delete the build folder totally.

- Repeat the process with each iteration of code :)

--- 

Some libraries I neeed (not sure all of them aha!) 

```
sudo apt install cmake build-essential qt6-base-dev qt6-tools-dev-tools \
                 libxcb-xinerama0-dev libxkbcommon-dev libopengl-dev \
                 qtbase6-dev qt6-base-dev libqt6core6 libqt6widgets6 \
                 qt6-tools-dev qt6-tools-private-dev qtchooser \
```

----

This would be different if you're using wayland. Some project structure:

### CMakeLists.txt: The build system configuration file that:

- Sets the C++ standard (C++20)
- Configures Qt's build requirements (AUTOMOC, AUTORCC, AUTOUIC)
- Defines the executable and its dependencies
- Links required libraries

### monitor.h: The header file containing:

- Class declarations
- Struct definitions (SystemThresholds, SystemMetrics)
- IconFactory class for system tray icons
- SystemMonitorTray class with Q_OBJECT macro for Qt's meta-object system

### monitor.cpp: The implementation file containing:

- All the actual code implementations for classes declared in monitor.h
- System metric calculations (CPU, RAM, Disk)
- UI setup and styling
- System tray icon management
- Event handling

### main.cpp: The entry point file that:

- Creates the QApplication instance
- Checks for system tray availability
- Creates and runs the monitor

---- 

```
monitor/
├── CMakeLists.txt ## This is simply a set up file for Cmake
├── main.cpp
├── monitor.h
└── monitor.cpp
```
