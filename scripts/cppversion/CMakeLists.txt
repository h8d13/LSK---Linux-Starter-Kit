cmake_minimum_required(VERSION 3.16)
project(monitor)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Core Widgets REQUIRED)

add_executable(monitor
    main.cpp
    monitor.cpp
    monitor.h
)

target_link_libraries(monitor PRIVATE
    Qt6::Core
    Qt6::Widgets
)
