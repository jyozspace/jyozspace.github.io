# Windows and Ubuntu: attaching a USB sensor

A USB cable does not automatically make a device available to Ubuntu in WSL 2. If a Linux driver needs direct access to a USB serial adapter, microcontroller or supported sensor, **usbipd-win** can attach the device to WSL. The driver then runs inside Linux, where it can feed a ROS node.

## Choose the correct route

| Your task | Where the device is used | Appropriate mechanism |
| --- | --- | --- |
| Linux ROS driver reads a USB device | Ubuntu | USB attachment with usbipd-win |
| Course Android app sends images over a USB cable | Windows ADB keeps the phone | `adb reverse` forwards a TCP connection; follow [Annex F](../annexes/wsl-capstone.md). |
| Copy a ZIP between Windows and Ubuntu | Either filesystem | [File sharing](../annexes/wsl-files.md); no USB attachment required |

The Android capstone's ADB route does **not** require the following procedure. Attaching that phone to WSL would remove it from Windows ADB while attached.

## Prepare once on Windows

These instructions target the instructor's **Windows 11 + WSL 2** route and usbipd-win **5 or newer**. Update WSL and use Ubuntu-24.04 with VERSION 2. Install usbipd-win from its official release or with the following **Windows PowerShell** command; approve the installer when Windows prompts:

```powershell
winget install --interactive --exact dorssel.usbipd-win
```

The interactive installer makes any requested restart visible. It installs a USB sharing service and a firewall rule; on a managed laptop, follow your organisation's installation policy. [Microsoft USB setup](https://learn.microsoft.com/en-us/windows/wsl/connect-usb).

Open a fresh PowerShell window after installation so it finds the newly installed `usbipd` command.

## Share, then attach the selected device

Connect the intended sensor. Close Windows applications that are using it, and leave an Ubuntu terminal open.

**Administrator PowerShell:**

```powershell
usbipd list
```

Find the sensor by its description and VID:PID. The **BUSID identifies the connected device**. In the commands below, `4-4` is an example: replace it with the BUSID you actually found, then share only that device:

```powershell
usbipd bind --busid 4-4
usbipd list
```

Expected: the selected device's STATE changes to `Shared`. Binding is persistent. Close the administrator terminal; attachment itself can use **normal PowerShell**:

```powershell
usbipd attach --wsl --busid 4-4
usbipd list
```

Expected: its STATE is `Attached`. Windows cannot use it while it is attached to WSL. Unplugging or restarting WSL detaches it, so recheck the BUSID and attach again when needed. [usbipd-win's WSL workflow](https://github.com/dorssel/usbipd-win/wiki/WSL-support).

## Verify Linux sees the hardware before starting ROS

**Ubuntu · Bash:**

```bash
sudo apt update
sudo apt install -y usbutils
lsusb
```

Look for your sensor's vendor/product IDs and description; bus and device numbers vary. This establishes **USB visibility**, not a working ROS driver. A serial device may expose `/dev/ttyUSB0` or `/dev/ttyACM0`; a camera or specialised sensor has different driver requirements. Use the sensor vendor's Linux/ROS documentation to identify the supported driver, permissions and launch command.

If the device is visible but access is denied, inspect its device-node permissions and install the vendor's specific udev rules before reattaching. Do not run every ROS node as root or grant every user access to all USB devices. A visible device can still lack a compatible kernel driver; USB cameras and high-bandwidth sensors need their own qualification. [usbipd-win compatibility and limitations](https://github.com/dorssel/usbipd-win).

## Return the device to Windows

Stop the Linux driver, then in **normal PowerShell**:

```powershell
usbipd detach --busid 4-4
```

Expected: the device is available to Windows again, with its sharing state still `Shared`. For a temporary lab machine, remove the persistent sharing afterwards using **administrator PowerShell**:

```powershell
usbipd unbind --busid 4-4
```

**Checkpoint:** distinguish “Windows lists the USB device,” “WSL lists it with `lsusb`,” and “a ROS topic contains real measurements.” These are three separate checks. Record the device model, Linux driver, BUSID and observed topic before calling the sensor ready.

Commands and references checked 30 October 2026. For the phone project, return to [USB or wireless Android connections](../annexes/android-connections.md).
