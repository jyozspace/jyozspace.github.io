# Annex E: connect Android by USB or wireless

Use the same Android APK, ROS receiver and calibration for both options. The connection changes how packets reach the laptop; it does not change the camera mode, ROS topics or SLAM workflow. Start with USB for a desk exercise. Wireless gives the phone more freedom to move during mapping.

![Two connection options: USB forwards the phone's localhost port to the laptop; wireless uses the laptop's address on the phone hotspot. Both reach the same ROS receiver.](../assets/android-connections.svg)

## Choose one route

| Connection detail | Option 1: wired USB | Option 2: wireless |
| --- | --- | --- |
| Physical connection | Data-capable USB cable | Laptop joins this phone's Wi-Fi hotspot |
| App endpoint | wss://127.0.0.1:8443/ws/android, after adb reverse | wss://LAPTOP_HOTSPOT_IP:8443/ws/android |
| Extra setup | Platform Tools, USB debugging and computer authorization | Hotspot credentials, reachable laptop interface and receiver-port firewall rule if needed |
| Movement | Limited by cable length; keep the laptop secure | Walk slowly within reliable Wi-Fi coverage |
| WSL host | Run ADB in Windows; Windows localhost forwards into Ubuntu | Follow the mirrored/NAT details in Annex F |

Both routes use certificate pinning and a fresh session token. Wireless here means the app sends data over Wi-Fi; wireless ADB and USB tethering are unnecessary for these instructions.

## Prepare the receiver once

Install the [Android APK](../../downloads/nodes-to-maps-sensor-debug.apk). Follow [Phone lab setup](../annexes/dataset-guide.md) to create the receiver certificate and start phone_bridge inside Ubuntu. Keep the certificate SHA-256 and session token visible in the terminal. A fresh receiver process creates a fresh token; a replacement certificate needs its new fingerprint.

The receiver listens on port 8443. On native Ubuntu, its default 0.0.0.0 binding supports either route. With WSL, use [Annex F](../annexes/wsl-capstone.md) for the Windows-to-Ubuntu boundary. ROS commands and mapping continue to run inside Ubuntu.

## Option 1: wired USB on native Ubuntu

Install ADB and the Ubuntu device rules, then connect an unlocked Android phone with a data-capable cable:

```bash
sudo apt update
sudo apt install adb android-sdk-platform-tools-common
adb devices
```

On the phone, enable Developer options and USB debugging, then authorize your own laptop when prompted. Expect one serial followed by device. An unauthorized entry needs phone approval; an empty list suggests a cable, USB mode or Linux device-access issue. Follow Android's [hardware-device setup](https://developer.android.com/studio/run/device) for Linux group/rule requirements, then reconnect as needed.

With the receiver running on this Ubuntu laptop:

```bash
adb reverse tcp:8443 tcp:8443
adb reverse --list
```

Expect a reverse rule containing tcp:8443 twice. If several devices are attached, select the intended one with adb -s SERIAL reverse tcp:8443 tcp:8443, replacing SERIAL with the value from adb devices.

In the app, enter wss://127.0.0.1:8443/ws/android, the receiver fingerprint and token. ADB carries this phone-local connection over USB to the laptop's port 8443. Tap Start camera + sensors, grant camera permission if requested, and tap Start again. Keep the app visible.

For Windows with WSL, run these ADB commands in **Windows PowerShell** using the official [Platform Tools](https://developer.android.com/tools/releases/platform-tools). First verify Test-NetConnection -ComputerName 127.0.0.1 -Port 8443 succeeds while the receiver is running inside Ubuntu. The full sequence and troubleshooting are in [Annex F](../annexes/wsl-capstone.md). This route uses Windows ADB and requires no USB passthrough into WSL.

## Option 2: wireless on a phone hotspot

Enable the Android phone's Wi-Fi hotspot with a distinct classroom name and password. Connect only its paired laptop. Separate hotspots give each pair its own addressing, while all nearby devices still share radio airtime. Some phones restrict traffic back to connected clients; verify the actual phone-to-laptop route before the lesson.

On native Ubuntu, inspect the laptop's address on its connected Wi-Fi interface:

```bash
ip -4 addr
```

Use that interface's IPv4 address, excluding the /prefix suffix. Enter wss://LAPTOP_HOTSPOT_IP:8443/ws/android in the app, replacing LAPTOP_HOTSPOT_IP with the actual address. Enter the same receiver fingerprint and its current token. The phone's own hotspot/gateway address and the laptop's 127.0.0.1 are different destinations.

Keep the receiver listening on the reachable interface. If a firewall blocks the connection, allow TCP 8443 only from the phone's address on the intended lab interface. Keep the firewall enabled. On WSL, the Windows Wi-Fi address and Ubuntu's private NAT address may differ; follow Annex F's wireless forwarding and scoped firewall instructions.

ADB is used only for the USB option. A wireless mapping run needs the APK's Wi-Fi connection, not an ADB connection. Mobile internet is unnecessary after all course software and dependencies are available locally.

## Verify the same result on either route

In a sourced Ubuntu terminal, run these inspections one at a time:

```bash
ros2 topic hz /phone/camera/image_raw
ros2 topic echo /phone/diagnostics
ros2 run image_view image_view --ros-args -r image:=/phone/camera/image_raw
```

Expect increasing app counters, arriving ROS images and your actual camera scene. Inspect /phone/imu/accelerometer and /phone/imu/gyroscope separately. Record which sensors exist, image dimensions, camera clock source and observed rate. A port test proves reachability only; the image and topic checks establish that sensor data passes through the receiver.

To switch routes, stop capture, set up the new route, change the endpoint and restart. Keep the camera mode and calibration fixed. The certificate fingerprint stays the same while the receiver certificate stays the same; the token stays the same while that receiver process runs. Repeat the image/rate checks before mapping.

## Finish the lab

Stop capture and confirm the camera is released. For USB, run adb reverse --remove tcp:8443 on the computer where the rule was created, then disconnect the cable and disable USB debugging when finished. For wireless, disconnect the hotspot and remove temporary receiver-port/proxy rules using Annex F where applicable. Keep private keys and non-consented recordings outside published files.

Official references: [Android Debug Bridge](https://developer.android.com/tools/adb), [ADB reverse port forwarding](https://developer.android.com/develop/ui/views/layout/webapps/access-local-server), and [WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking).
