# Find the first broken contract

Change one thing, collect evidence and retest. Separate Android permissions, USB/wireless transport, ROS messages and estimator assumptions.

## Installation and terminal setup issues

On a fresh Ubuntu WSL account, sudo normally asks for that account's Linux password. Type it locally when prompted; no characters are displayed. Build the learner workspace as your normal Linux user.

The ROS apt repository must be configured before apt can find ros-jazzy packages. Follow the official Jazzy repository instructions linked from setup, including Universe and ros2-apt-source, then run apt update.

For persistent ROS sourcing and DDS variables, use the labelled .bashrc block in Before you begin. Verify it from a fresh interactive Ubuntu Bash terminal. A noninteractive `bash -c` may skip the interactive portion of .bashrc; automation should source ROS explicitly. Existing terminals still need the overlay sourced after the first build.

## ROS or an executable is missing

Confirm Ubuntu 24.04 and source /opt/ros/jazzy/setup.bash. Build from ~/ros2_ws and source install/setup.bash in the terminal that runs the command. Check the first build/rosdep error. A Python script running directly does not prove its console_scripts entry point was installed.

If phone_bridge cannot import aiohttp, yaml, cv_bridge or OpenCV, install the declared Ubuntu dependencies and use the system Python matching Jazzy. A random pip virtual environment may hide ROS Python packages. The optional SLAM package lives in a separate workspace and requires the externally built engine.

If colcon warns that ros2_course_interfaces is already built in an underlay while rebuilding the same workspace, the course overlay is already sourced in the build shell. Sourcing /opt/ros/jazzy/setup.bash again does not clear the inherited overlay. For a clean build shell, run this from Ubuntu, then source only the underlay and build:

```bash
env -i HOME="$HOME" USER="$USER" PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin bash --noprofile --norc
source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

The first command opens a nested clean shell. Type exit when finished, then open a normal terminal for node exercises. This shell is for compilation; it intentionally lacks GUI and lab discovery variables. Do not add --allow-overriding indiscriminately: overriding packages from a different workspace can have real API/ABI consequences.

## The native Android app cannot pair

Check the endpoint ends in /ws/android, the 64-digit certificate SHA-256 matches the current receiver certificate, and the token belongs to this receiver session. A certificate replacement needs a new pin. Check the app’s error before changing a setting. Use the updated receiver and APK together.

For USB on native Ubuntu, verify the authorized adb device and reverse rule. On WSL, also verify Windows localhost:8443 before using the phone’s 127.0.0.1 endpoint. For Wi-Fi, use the actual laptop hotspot address. Annex F separates WSL mirrored and NAT routes and shows scoped firewall/proxy checks.

If camera setup fails, verify camera permission and that another app has released the camera. Record camera ID, size and timestamp source. UNKNOWN timing permits the labelled camera-only exercise; inertial suitability requires further qualification.

## The selected connection cannot reach the receiver

For native Ubuntu USB, confirm adb devices lists an authorized phone and adb reverse --list contains tcp:8443. For WSL USB, also test Windows localhost:8443 before pairing. Recreate the reverse rule after a cable/device reconnect when needed. [Annex E](../annexes/android-connections.md) walks through both hosts.

For wireless, confirm the laptop joined this phone's hotspot and the endpoint uses the laptop's actual Wi-Fi IPv4 address. Keep the firewall enabled and scope any TCP 8443 allowance to the phone and lab interface. WSL may need the mirrored/NAT forwarding described in Annex F. Some hotspot implementations restrict phone-to-client traffic; test that route or use USB.

Stop the app, correct the address, fingerprint or token, then restart. The receiver permits one paired phone. Private keys remain on the laptop; pairing tokens belong only in the current lab session.

## Camera or motion is unavailable

In Android, the app reports accelerometer and gyroscope availability separately. The two ROS topics preserve event times; a missing component stays unavailable. Start and Stop require the app to remain in the foreground. Inspect /phone/diagnostics for camera metadata and clock quality.

The Android app stops capture on backgrounding. Keep it visible and explicitly restart after switching apps. A phone with a missing motion sensor can still perform the camera-only mapping exercise; document which component is unavailable.

## ROS topics exist but data is silent

Jazzy prints a deprecation warning when ROS_LOCALHOST_ONLY is set. Remove the old export from your shell setup, run `unset ROS_LOCALHOST_ONLY`, set `export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`, and keep ROS_DOMAIN_ID and RMW_IMPLEMENTATION consistent. The updated .bashrc block also clears ROS_STATIC_PEERS for the local course lab. Stop existing nodes and the ROS CLI daemon before starting a fresh set of terminals; changing one shell does not change running processes.

Compare resolved names/types and `ros2 topic info TOPIC --verbose`. A best-effort offer cannot meet a reliable request; requesting best effort can connect to that publisher. Keep Jazzy/domain/localhost settings consistent. A listed topic is not proof that samples are arriving.

If the Android app’s counters increase but ROS does not receive, inspect the receiver error. It rejects malformed dimensions/JPEGs, stale or future stamps and non-increasing sequences. Pairing and clock handshake must complete before samples are accepted.

## Mapping will not initialize or loses tracking

Confirm measured calibration matches the transmitted lens, crop, dimensions and orientation. Translate through textured, well-lit, overlapping views. Pure rotation does not provide monocular depth. Motion blur, autofocus, stabilization, rolling shutter and moving people can degrade results. Slow replay reduces compute load; it cannot repair the captured pixels.

Watch tracking status and the engine viewer. The baseline map is sparse and arbitrary-scale. Receiving motion topics alone does not establish metric scale; an estimator must fuse qualified measurements. If ORB-SLAM3 cannot be built or qualified on the reference machine, mark that backend unverified and use the documented sensor transport exercise plus a real recorded mapping fallback.

## Frames or time do not agree

A coordinate transform changes the point values as well as their frame label. Camera–IMU alignment requires measured extrinsics before a TF edge can describe it. Inspect actual frame names, transform direction and measurement time. The bridge publishes optical images and device-frame motion measurements. Camera–IMU extrinsics remain a separate measured relationship.

The monocular phone_slam_world is not a gravity-aligned metric map frame. The optional adapter publishes visualization poses in its own arbitrary-scale world. During replay, publish /clock and use_sim_time on relevant consumers; stop competing live publishers first.
