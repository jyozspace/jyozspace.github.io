# Windows and Ubuntu: sharing files

Your Windows desktop and Ubuntu terminal can reach the same files, but they use different path spellings. For this course, keep the working ROS project in **Ubuntu home**, and use Windows File Explorer when you want to download, copy or inspect files visually.

## Know which path you are looking at

Imagine that your Windows account is `Alex` and your Ubuntu account is `student`. These are examples; the two account names can be different.

| File location | Inside Ubuntu Bash | Inside Windows File Explorer |
| --- | --- | --- |
| Windows Downloads | `/mnt/c/Users/Alex/Downloads` | `C:\Users\Alex\Downloads` |
| Ubuntu home | `/home/student`, abbreviated `~` | `\\wsl.localhost\Ubuntu-24.04\home\student` |
| Course workspace | `~/ros2_ws` | `\\wsl.localhost\Ubuntu-24.04\home\student\ros2_ws` |

`/mnt/c` exposes the Windows C: drive inside Ubuntu. The `\\wsl.localhost` path exposes Ubuntu files to Windows; `\\wsl$` is another supported entry point. You are opening the original file, not an automatically synchronised second copy. Microsoft recommends keeping Linux projects in the Linux filesystem for performance. [Working across filesystems](https://learn.microsoft.com/en-us/windows/wsl/filesystems).

## Open the right home folder without guessing a username

**Ubuntu · Bash:**

```bash
cd ~
whoami
pwd
explorer.exe .
```

**Expected output — your account name will differ:**

```output
student
/home/student
```

A Windows File Explorer window opens at this Ubuntu directory. The dot in `explorer.exe .` means “the current directory.” Copy the downloaded `ros2-course-code.zip` into that window. Then return to Ubuntu:

```bash
ls -lh ~/ros2-course-code.zip
mkdir -p ~/ros2_ws/src
unzip ~/ros2-course-code.zip -d ~/ros2_ws/src
ls ~/ros2_ws/src
```

Expect four package directories: `ros2_course_bringup`, `ros2_course_cpp`, `ros2_course_interfaces` and `ros2_course_py`. Continue with [lecture 02's dependency and build commands](../lessons/02-lecture2-python-nodes.md). Moving a ZIP into home alone does not build its contents.

## Copy a file from either side

For command-line practice, replace `Alex` with your actual Windows account folder before running this **inside Ubuntu**:

```bash
cp "/mnt/c/Users/Alex/Downloads/ros2-course-code.zip" ~/
```

`cp` leaves the source ZIP in Downloads and creates a copy in Ubuntu home. Quotes keep spaces in a path together. To find your Windows folders, inspect `ls /mnt/c/Users`; the Downloads folder may have been moved or redirected, so File Explorer is often easier.

The reverse route is equally simple: open `~/ros2_ws` with `explorer.exe .` and copy a report into a Windows folder. Avoid working directly inside WSL's hidden virtual-disk backing files.

## Keep editing and permissions predictable

Linux distinguishes `Scan.py` from `scan.py`. Use the exact spelling in imports and commands. Save shell scripts with Linux **LF** line endings in your editor; an error containing `\r` or `^M` can indicate Windows line endings.

Files accessed through a Windows mounted drive have Windows permission rules underneath. A broad `chmod` is not a reliable fix for Windows access restrictions. Ubuntu-home files follow Linux ownership and permission rules; File Explorer access through the WSL share uses the distro's default Linux user. [WSL permissions](https://learn.microsoft.com/en-us/windows/wsl/file-permissions).

| Symptom | First check |
| --- | --- |
| ZIP not found | Run `pwd` and `ls`; check the actual download location. |
| `explorer.exe` not found | Enter `\\wsl.localhost` in File Explorer; check that Windows interoperability is enabled. |
| Slow builds in `/mnt/c/...` | Copy the source packages to `~/ros2_ws/src` and build there. |
| Cannot write a course file | Use `ls -l` to inspect its owner; avoid running `colcon build` with `sudo`. |

**Try it:** create `~/ros2_ws/file-check.txt` with a sentence in Ubuntu, open it through File Explorer, then explain why editing that file changes the one Ubuntu sees. File sharing does not attach a USB sensor or open a network port; those are the [USB](../annexes/wsl-usb.md) and [networking](../annexes/wsl-networking.md) appendices.

Reference checked 30 October 2026: [WSL automount and interoperability settings](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).
