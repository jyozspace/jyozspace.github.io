# Annex F: run the phone capstone on WSL 2

[Annex E](../annexes/android-connections.md) introduces the two capstone options: wired USB and wireless. This annex adds the Windows/Ubuntu forwarding steps for those same options.

Windows hosts the laptop desktop and USB tools; Ubuntu 24.04 inside WSL 2 runs ROS 2 Jazzy, phone_bridge and the optional mapper. The Android phone sends to the same receiver used on native Ubuntu. Start with the USB route below, then choose a tested Wi-Fi route if you need more freedom to walk.

## Prepare Ubuntu and graphics

Use an up-to-date WSL 2 installation. In Windows PowerShell:

```powershell
wsl --update
wsl --install -d Ubuntu-24.04
wsl -l -v
```

Confirm that Ubuntu-24.04 reports version 2. Complete the course setup and package build **inside Ubuntu**. Keep ~/ros2_ws and ~/phone_slam_ws in the Linux home directory. Test rviz2 before adding phone data. With current Windows graphics drivers, WSLg can display Linux GUI applications; follow Microsoft’s [WSLg instructions](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps).

The optional ORB-SLAM3 engine and Pangolin viewer need the same build and calibration rehearsal described in Phone lab setup. Test their OpenGL support separately. If RViz has a driver issue, `LIBGL_ALWAYS_SOFTWARE=1 rviz2` can help diagnose it; software rendering may be too slow for the live mapping workload. A recorded bag is useful for comparing transport and processing problems.

## USB route: Windows ADB to the WSL receiver

This route uses Windows’ normal localhost forwarding into WSL. The phone remains attached to Windows ADB. ROS stays in Ubuntu, so USB passthrough into WSL is unnecessary for this setup. Use a data-capable cable and the official [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools).

1. Install the classroom APK on Android. Enable Developer options and USB debugging for this lab, connect the cable and authorize your own computer on the phone.
2. In Ubuntu, source Jazzy and the course overlay, then start phone_bridge with the certificate and key prepared in Phone lab setup. Its default host is 0.0.0.0, allowing WSL’s forwarding path to reach it.
3. In Windows PowerShell, verify that the receiver port is reachable locally:

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 8443
adb devices
adb reverse tcp:8443 tcp:8443
adb reverse --list
```

Expect TcpTestSucceeded True, one authorized device and a reverse rule for tcp:8443. Run these adb commands from Windows, using the Platform Tools executable. If there are several devices, choose the intended serial with `adb -s SERIAL reverse tcp:8443 tcp:8443`. A phone listed as unauthorized needs its on-device approval.

4. In the Android app, enter **wss://127.0.0.1:8443/ws/android**, the receiver token and certificate SHA-256 printed inside Ubuntu. Tap Start. The reverse rule carries the phone’s localhost socket through USB to Windows localhost, which forwards to the running WSL server.
5. In another sourced Ubuntu terminal, inspect the topics and open image_view. Confirm real camera pixels and native sensor messages before starting SLAM.

![WSL USB route diagram: Android localhost passes through adb reverse to Windows localhost and then to the ROS receiver in Ubuntu.](../assets/wsl-route.svg)

If Windows cannot reach localhost:8443, check that the Ubuntu receiver is running, no Windows process already owns that port, and WSL’s localhost forwarding is enabled. An explicit `localhostForwarding=true` belongs under [wsl2] in %UserProfile%\.wslconfig for NAT networking. Preserve any other settings. Configuration changes require a WSL restart; save and stop other WSL work before `wsl --shutdown`, then start Ubuntu and the receiver again.

USB is a good first connection test and a compact desk experiment. Plan walking motion around the cable’s length and trip risk. For a larger room loop, use a rehearsed Wi-Fi route. Stop capture at the end, remove the reverse rule with `adb reverse --remove tcp:8443`, and revoke USB debugging authorization if this was a temporary lab computer. See the official [ADB reverse example](https://developer.android.com/develop/ui/views/layout/webapps/access-local-server) for the port-forwarding mechanism.

## Wi-Fi route 1: mirrored networking on Windows 11

Microsoft supports mirrored networking on Windows 11 22H2 and newer. It can make a WSL server directly reachable from the LAN. Follow the current [WSL networking guide](https://learn.microsoft.com/en-us/windows/wsl/networking), especially the Hyper-V firewall section. In %UserProfile%\.wslconfig, add or update this setting while preserving the file’s other values:

```ini
[wsl2]
networkingMode=mirrored
```

Save and stop WSL work before restarting WSL. Connect Windows to the phone hotspot and identify Windows’ Wi-Fi IPv4 address with Get-NetIPConfiguration. Start phone_bridge inside Ubuntu, then allow TCP 8443 through the applicable Windows/Hyper-V firewall policy. A local administrator can create a Hyper-V rule limited to this port:

```powershell
New-NetFirewallHyperVRule -Name "RosPhone8443" -DisplayName "ROS phone lab 8443" `
  -Direction Inbound -VMCreatorId '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' `
  -Protocol TCP -LocalPorts 8443
```

Scope applicable Windows host rules to the phone address and lab interface as shown in the NAT example below. Managed computers may require IT to approve firewall rules. Keep the firewall enabled. In Android, use wss://WINDOWS_HOTSPOT_IP:8443/ws/android and the printed certificate pin/token. A successful phone pairing establishes the actual route; Windows localhost alone checks only the host side. Remove the temporary Hyper-V rule afterward with `Remove-NetFirewallHyperVRule -Name "RosPhone8443"`.

## Wi-Fi route 2: NAT with an explicit TCP proxy

Use this route when WSL uses NAT and the phone cannot reach it directly. First identify three actual IPv4 addresses:

| Placeholder | Where to find it |
| --- | --- |
| WINDOWS_HOTSPOT_IP | Get-NetIPConfiguration: Windows Wi-Fi interface connected to the phone hotspot |
| WSL_IP | `wsl -d Ubuntu-24.04 hostname -I`: select Ubuntu’s current IPv4 address |
| PHONE_IP | The hotspot gateway shown by Windows, checked against the phone’s hotspot settings |

The phone connects to WINDOWS_HOTSPOT_IP. Windows forwards that TCP connection to WSL_IP. The proxy preserves TLS end to end. Replace the placeholders before running these **administrator PowerShell** commands:

```powershell
$courseWindowsIP = 'WINDOWS_HOTSPOT_IP'
$courseWslIP = 'WSL_IP'
$coursePhoneIP = 'PHONE_IP'
netsh interface portproxy add v4tov4 listenaddress=$courseWindowsIP listenport=8443 connectaddress=$courseWslIP connectport=8443
New-NetFirewallRule -DisplayName 'ROS phone lab NAT 8443' -Direction Inbound `
  -Action Allow -Protocol TCP -LocalPort 8443 -LocalAddress $courseWindowsIP `
  -RemoteAddress $coursePhoneIP
netsh interface portproxy show v4tov4
```

Keep phone_bridge running on 0.0.0.0 inside Ubuntu. In Android use wss://WINDOWS_HOTSPOT_IP:8443/ws/android with the current pin and token. WSL’s private IP can change after restart; inspect it and update the proxy before reconnecting. A firewall/proxy setup is specific to this machine and lab network.

After the lab, use the same Windows IP value to remove the temporary route and rule:

```powershell
netsh interface portproxy delete v4tov4 listenaddress=$courseWindowsIP listenport=8443
Remove-NetFirewallRule -DisplayName 'ROS phone lab NAT 8443'
```

## Complete the same ROS and mapping exercise

Once connected, the ROS commands, camera calibration, monocular backend and bag workflow are identical to the native-Ubuntu lesson. Keep ROS_LOCALHOST_ONLY=1 and ROS_DOMAIN_ID consistent across Ubuntu terminals. The phone communicates with a TCP receiver; it does not need ROS discovery across the Windows/WSL boundary.

Check /phone/camera/image_raw, /phone/camera/camera_info, /phone/imu/accelerometer and /phone/imu/gyroscope. Calibrate the Android app’s actual image mode. Run the separately prepared mapper and set RViz Fixed Frame to phone_slam_world. For replay, stop live sources and use /clock with use_sim_time on consumers.

Record which route worked, all relevant software versions, the app’s camera ID/clock source and topic rates. On this authoring host, no live WSL/phone mapping run has been performed. Rehearse the selected route on classroom machines, including any VPN or institutional firewall, before relying on it during a lecture.
