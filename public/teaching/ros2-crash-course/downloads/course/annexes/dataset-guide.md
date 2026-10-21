# Phone lab setup: before the live class

Prepare the Android APK, a secure connection, measured camera calibration and a qualified mapping backend before lecture 5. The phone is a sensor client. ROS and the mapper run on Ubuntu, either natively or inside WSL 2.

## Choose a connection route

Choose [Option 1: wired USB or Option 2: wireless](../annexes/android-connections.md). On native Ubuntu, USB uses adb reverse tcp:8443 tcp:8443 with wss://127.0.0.1:8443/ws/android. Run ADB on the computer hosting the receiver. For wireless, connect the laptop to the phone’s hotspot and inspect its actual IPv4 address with ip -4 addr. Give each classroom hotspot a distinct name/password. A separate hotspot keeps each pair’s addressing separate; nearby hotspots still share radio airtime. Keep ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST and consistent ROS_DOMAIN_ID values in all Ubuntu terminals.

For WSL, start with [Annex F’s USB route](../annexes/wsl-capstone.md): Windows ADB forwards the phone’s socket to Windows localhost, and WSL’s normal localhost forwarding reaches the Ubuntu receiver. The same annex gives mirrored-network and scoped NAT-proxy routes for Wi-Fi. Rehearse the selected route before class and retain the firewall’s protections.

Install the classroom test APK from Resources on Android 8.0 or newer. Open it and inspect the form without starting sensors yet. The native app needs an endpoint, a fresh token and the receiver certificate SHA-256. Annex E gives the shared pairing checks and route-specific setup.

## Create a receiver certificate and pair Android

The receiver uses TLS for every phone connection. For a short private lab, create a self-signed development certificate inside Ubuntu. The native app authenticates it by its exact fingerprint, so the phone’s global CA trust store stays unchanged.

```bash
mkdir -p ~/phone-lab
cd ~/phone-lab
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout laptop-key.pem -out laptop.pem -days 30 \
  -subj '/CN=phone-lab' \
  -addext 'subjectAltName=DNS:localhost,IP:127.0.0.1'
chmod 600 laptop-key.pem
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_course_py phone_bridge --cert laptop.pem --key laptop-key.pem
```

Keep the private key on the laptop and outside published files. The terminal prints an Android endpoint template, a token and the certificate SHA-256. Enter the actual reachable address ending /ws/android, that token and the fingerprint in the APK. With USB reverse configured, the address is wss://127.0.0.1:8443/ws/android. With Wi-Fi, use the laptop’s hotspot IPv4 address. The app checks the copied leaf pin and validity dates, identifying the server through that pin.

Tap Start, grant camera permission if requested and tap Start again. Pass condition: the app reports streaming, its camera mode/clock source is visible, and image_view on Ubuntu shows the phone’s actual scene. Inspect ROS rates and native motion counters. Stop and background the app to verify that capture ends. Repeat with a wrong pin or token to verify rejection, then restore the correct values.

![Simulated native pairing screen. Compare the camera ID, size, timestamp source and counters with your own run.](../assets/android-screen.svg)

## Calibrate the actual transmitted mode

Record the Android app's camera ID, native unrotated image dimensions, clock source and focus mode before collecting a target dataset. A calibration belongs to that exact pixel geometry. Switching USB and wireless keeps the same calibration when this camera mode is unchanged.

Follow [Annex C](../annexes/calibration.md): measure the target’s square size and inner-corner count, collect varied sharp views, fit and inspect the result, save the ROS YAML and validate it on new views. The receiver supports the Save workflow; it exposes no set_camera_info service for Commit.

Restart phone_bridge with --calibration ~/phone-lab/camera.yaml. Confirm CameraInfo dimensions and intrinsics, then convert supported measured pinhole plumb_bob values for the optional mapper from the unpacked backend/source folder:

```bash
python3 maintenance/tools/calibration_to_orb.py \
  ~/phone-lab/camera.yaml ~/phone-lab/phone-orb.yaml --fps 10
```

Keep the camera mode, orientation and processing stable for the mapping run. Validate focus/stabilization behavior on the selected phone. Native timestamp metadata is useful evidence, while camera–IMU calibration and estimator qualification remain additional work for an inertial extension.

## Prepare the optional ORB-SLAM3 backend


This is instructor pre-work. The beginner workspace builds without ORB-SLAM3. A complete optional adapter is included under ros/slam/phone_orb_slam3, while ORB-SLAM3, its vocabulary and Pangolin are external dependencies. Read the [upstream build requirements](https://github.com/UZ-SLAMLab/ORB_SLAM3). Its published examples/build assumptions are not a promise that every Ubuntu 24.04 dependency combination compiles without adjustment.

Build a compatible Pangolin version and the upstream ORB-SLAM3 library on the reference teaching machine. Prefer a tested instructor image/container or documented pinned source revisions for class. Record the exact ORB-SLAM3, Pangolin, OpenCV, Eigen and compiler versions and any build patches. Prepare this stack on the instructor machine before class so lecture time can focus on ROS integration. The upstream engine and this optional adapter use GPL-3.0-or-later; they are separate from the Apache-2.0 beginner code. No third-party engine source/binary or vocabulary is bundled here.

Once `$HOME/ORB_SLAM3/lib/libORB_SLAM3.so` and the extracted Vocabulary/ORBvoc.txt exist, copy the supplied adapter into a separate workspace:

```bash
mkdir -p ~/phone_slam_ws/src
cp -r ros/slam/phone_orb_slam3 ~/phone_slam_ws/src/
source /opt/ros/jazzy/setup.bash
cd ~/phone_slam_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --cmake-args -DORB_SLAM3_ROOT=$HOME/ORB_SLAM3
source install/setup.bash
ros2 pkg executables phone_orb_slam3
```

Expected: phone_mono is installed. Start it with the vocabulary and measured ORB settings shown in lecture 5. It consumes camera images; native inertial topics remain inspection data. The adapter uses the inspected upstream Sophus-based API, but must be compiled and exercised against the instructor's exact engine revision before being called classroom-ready.

## Prepare a reference run and fallback

On a qualified phone/app, pair, inspect rates, calibrate, initialize by translating through a textured scene, make a short loop and observe tracking. Confirm both the engine viewer and the ROS diagnostic outputs. Stop normally and inspect keyframes.txt. Save a real viewer screenshot, a consented ROS 2 bag and its measured calibration before class.

Distribute a manifest containing phone model, OS/app version and APK checksum, camera ID/clock source, transmitted dimensions, client revision, FPS target, calibration/target details, bridge and backend revisions, input topic names, frame meanings, timestamp limitations, capture/replay commands and file SHA-256 checksums. The fallback bag must contain actual phone images and the matching calibration; a random stereo or ROS 1 bag is not interchangeable.

```bash
ros2 bag info ~/phone-lab/walk01
find ~/phone-lab/walk01 -type f -exec sha256sum {} \;
```

A recorded bag is not bundled. If the optional backend cannot be qualified before class, explicitly teach the working phone transport/ROS inspection exercise and show the recorded reference mapping demonstration. Record which stages were actually demonstrated, then schedule the remaining mapping qualification separately.

## Acceptance checklist

1. All learner machines use Jazzy / Ubuntu 24.04 and the four beginner packages build.
2. The actual phone pairs over pinned TLS on the chosen Wi-Fi or USB route; its camera timestamp source is recorded.
3. Pairing rejects a wrong certificate pin or token and the Android app releases sensors on Stop/backgrounding.
4. Camera frames arrive; native accelerometer/gyroscope availability, individual timestamps, axes and units are documented.
5. The Android camera ID/image mode matches measured calibration and its ORB settings.
6. The optional backend is compiled at recorded versions, initializes and produces a real sparse-map viewer result on a qualified phone.
7. The reference bag replays with matching calibration into a fresh backend process and a shared replay clock.
8. The instructor has a screenshot and recording fallback and explains sparse monocular reconstruction and the additional work needed for visual-inertial estimation.
