# CPP Version

So as we said in the other python version we want to be able to make our code as small of a footprint as possible. 
Using cpp we can reduce the total compiled size to about 90kb (with very little opti) 

> **_NOTE:_**  Get the C/C++ extensions official
> Also I might have missed some installs you need (you can always use GPT if you're getting some errors in build)

How to use CMake basics:

- Create the CMakeLists.txt file in your code directory (this is like the guide for CMake to understand what to compile)
- Now ``` mkdir build ```to create the output folder
- Then ``` cd build ``` to move to the folder
- ``` cmake .. ``` Checks the build
- ``` make ``` Creates the final output

- Can ```sudo rm -rf build``` to delete the build folder totally.

- Repeat the process with each iteration of code :)
- ``` cd .. ``` to move one back

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



----

I again added it to my start up programs removed the old python version. 

Now we can check for footprint. 

![htop](/media/image.png)


Using about 0,0 - 0,3% of CPU which is great. 
405M of VIRT memory (about 30-40mb of actual RAM). 

The total file size is now bellow 100kb. 

> **_NOTE:_** There are 4 instances because of how Qt handles threading I believe. 



We can compare to our python version:

![image](https://github.com/user-attachments/assets/bb4db4e9-fdc7-43b5-87e5-67be26746d42)


You can then go further and add notifications are anything that you need. Say you need a shortcut to a specific command or setting, it's all at the end of your fingertips.

Which uses about 250mb more VRAM
And 0,2% extra CPU. 

This is negligeable but the CPP version does run more natively. 
