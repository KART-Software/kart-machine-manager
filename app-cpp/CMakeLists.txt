cmake_minimum_required(VERSION 3.16)
project(kart-machine-manager-cpp VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Network)

add_executable(kmm
    src/main.cpp
    src/config.cpp
    src/canbus.cpp
    src/stores.cpp
    src/udp_transmitter.cpp
    src/cloud.cpp
    src/gui/widgets.cpp
    src/gui/mainwindow.cpp
    icons.qrc
)

target_include_directories(kmm PRIVATE src)
target_link_libraries(kmm PRIVATE Qt6::Widgets Qt6::Network)
target_compile_options(kmm PRIVATE -Wall -Wextra)

install(TARGETS kmm RUNTIME DESTINATION bin)
