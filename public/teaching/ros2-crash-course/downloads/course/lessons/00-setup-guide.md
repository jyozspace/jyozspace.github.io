# Your robotics workbench

Install Jazzy, learn the terminal, and prepare your phone as a sensor.

## What you need before starting

Use **ROS 2 Jazzy Jalisco on Ubuntu 24.04 LTS (Noble)** with Bash. Jazzy is a long-term-support release supported until May 2029. This operating-system and ROS pairing is used throughout the guide, so the installation commands and examples fit together.

You need basic Python variables, functions and classes. Robotics knowledge is not assumed. C++ classes and templates help with lecture 3, where a complete scaffold is supplied. A node is a ROS participant, a package is a unit of software, and a workspace is the directory where packages are built. The first lecture explains these ideas through experiments.

Allow 1–2 hours for setup and a separate capstone rehearsal. A laptop with 16 GB RAM and 30 GB free disk is comfortable. The project device is an Android 8.0+ phone with a rear camera and preferably accelerometer/gyroscope sensors. A native APK is supplied. The mapper uses camera images; unsupported motion sensors can be documented without blocking that part of the project.

The website has two reading modes. **Self-study** shows the full guide with exercises and model explanations. **Lecture** shows one section at a time with presentation controls and a timer. Your progress, notes and written answers are saved in this browser; export them from Resources before changing computers. The interactive labs illustrate concepts, while commands marked Ubuntu · Bash run in your Linux terminal.

## Native Ubuntu or Windows with WSL

Native Ubuntu and Ubuntu 24.04 inside WSL 2 can host the receiver. WSL adds a Windows-to-Ubuntu network boundary. [Annex F](../annexes/wsl-capstone.md) gives a USB route using Windows ADB and two Wi-Fi routes, with explicit checks at each boundary.

For Windows, run in administrator PowerShell, restart when requested, and create a Linux account:

```powershell
wsl --update
wsl --install -d Ubuntu-24.04
wsl -l -v
```

Confirm VERSION 2. From now on, run the course's Bash commands **inside Ubuntu**, not PowerShell. Store the workspace under the Linux home directory, where Linux file permissions and build tools work consistently. Test WSLg with RViz before class. Rehearse the WSL connection before class. Keep a reference bag or a prepared teaching laptop available if a student machine needs more setup time.

## Install the correct ROS distribution

Run `lsb_release -cs`; expect `noble`. Follow the official [Jazzy Ubuntu installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) for locale, Universe, ROS repository configuration and system updates before installing packages. Those repository instructions are maintained upstream. Then install the course tools:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop ros-dev-tools \
  ros-jazzy-turtlesim ros-jazzy-rqt-graph ros-jazzy-tf2-tools \
  ros-jazzy-cv-bridge ros-jazzy-image-view \
  ros-jazzy-camera-calibration python3-aiohttp python3-opencv \
  python3-numpy python3-yaml
source /opt/ros/jazzy/setup.bash
sudo rosdep init
rosdep update
```

Run rosdep init once only; if an existing configuration is reported, continue with update. Use the Ubuntu system Python that matches ROS. The base course does not require Gazebo, RTAB-Map or ORB-SLAM3 to be compiled. ORB-SLAM3 is a separately prepared optional backend for the final live demonstration, not an apt package supplied by this course.

## Use the terminal and source your environment

`pwd` prints your current directory; `ls` lists files; `cd` changes directory; `mkdir -p` creates a directory and missing parents. Tab completes paths, the up arrow recalls a command, and Ctrl+C stops a foreground program. A terminal running a node is busy; open another terminal for inspection commands.

The ROS installation is your **underlay**. Your built workspace supplies an **overlay** containing your own packages. Source the underlay in every terminal, then the overlay after a successful build. Keep ROS discovery local while the phone uses a WebSocket connection to just one ROS receiver:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_LOCALHOST_ONLY=1
export ROS_DOMAIN_ID=42
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

Use the same values in every lab terminal. ROS_DOMAIN_ID separates graphs; it is not authentication. ROS_LOCALHOST_ONLY affects ROS discovery, not the separate HTTPS/WSS server. A phone does not need DDS or ROS installed. For a physical ROS robot on another machine, deliberately reconfigure discovery and networking.

## Build and verify the supplied packages

Download the ROS workspace ZIP from Resources. Extract it and copy the four package directories from ros/workspace/src into ~/ros2_ws/src. The path `~/ros2_ws/src/ros2_course_py/package.xml` should exist, with the other three packages beside it. Place package.xml directly inside each package directory so colcon can discover the four packages.

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 pkg executables ros2_course_py
```

Expected: four packages finish and the executable list includes talker, listener and phone_bridge. Resolve the first dependency/compiler error before continuing. Rebuild after changing interfaces, package metadata, Python entry points or C++ code. Symlink installation does not remove all rebuild requirements.

Test the installed ROS environment in terminal A:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

In terminal B with the same environment:

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

Expected: the listener prints the talker's strings. Also run rviz2 and confirm a usable 3D window. Close the demo nodes before starting the lecture exercises.



![Simulated setup checkpoint: Jazzy on noble, four packages built, then a sourced overlay makes the executables visible.](../assets/setup-terminal.svg)


## Prepare the phone project before lecture five

Read [Phone lab setup](../annexes/dataset-guide.md) first. [Annex A](../annexes/android-development.md) explains the Android app, [Annex B](../annexes/bridge-development.md) traces the ROS receiver and [Annex C](../annexes/calibration.md) walks through calibration. WSL users should complete [Annex F](../annexes/wsl-capstone.md). The [visual guide](../annexes/visual-guide.md) collects expected-output illustrations.

Install the supplied classroom test APK on Android. Pair using the receiver’s endpoint, session token and certificate SHA-256. Test the chosen Wi-Fi or USB route, camera mode, timestamp source, sensor availability and Stop behavior before class. Keep ROS discovery local to the laptop. [Annex E](../annexes/android-connections.md) gives the two connection options: wired USB and wireless over the phone hotspot.

For mapping, prepare the optional ORB-SLAM3 backend, measure camera calibration in the exact transmitted image mode and rehearse initialization. The baseline result is a sparse monocular reconstruction with arbitrary scale. Native inertial streams are available for inspection and further development. Supply a consented, qualified reference bag and matching calibration for learners whose phone cannot complete the live exercise.

Official references: [Jazzy installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), [Android Camera2](https://developer.android.com/media/camera/camera2), [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking), and [WSLg](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps). Content reviewed 21 October 2026.
