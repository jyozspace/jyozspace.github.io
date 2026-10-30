# Windows and Ubuntu: understanding network connections

A network connection needs a **destination address**, a **port** and a program listening there. Think of an address as choosing the computer and the port as choosing its service. In this course, port `8443` belongs to the phone receiver; it is unrelated to the path of a file or a USB BUSID.

## Whose localhost is it?

`localhost` and `127.0.0.1` mean the machine/environment making the connection. A phone's localhost ordinarily refers to the phone. Windows and WSL have integration that forwards certain local connections; `adb reverse` adds a separate phone-to-computer path.

| Connection | Address to understand |
| --- | --- |
| Ubuntu tool → Ubuntu service | `127.0.0.1:PORT` |
| Windows tool → WSL service | Windows localhost forwarding normally permits `127.0.0.1:PORT`. |
| WSL → Windows service in NAT mode | Use the Windows host address visible from WSL. |
| Phone on Wi-Fi → laptop receiver | Use the laptop's reachable Wi-Fi address, with the WSL route configured. |

In WSL's default **NAT** mode, Ubuntu has a virtual network address behind Windows. **Mirrored** mode on Windows 11 22H2 or newer changes this arrangement and supports host/WSL localhost connections, multicast and direct LAN access, subject to firewall policy. [Microsoft WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking).

## Observe forwarding with a tiny local test

This test serves one harmless sample file. It verifies the Windows-to-Ubuntu path without requiring ROS, a phone or a firewall exception.

**Ubuntu · Bash, terminal A:**

```bash
mkdir -p ~/wsl-network-check
cd ~/wsl-network-check
printf 'Hello from Ubuntu\n' > hello.txt
python3 -m http.server 8000 --bind 127.0.0.1
```

Keep this terminal running. Python's small HTTP server is a temporary learning tool, not the encrypted capstone receiver. [Python HTTP server CLI](https://docs.python.org/3/library/http.server.html#command-line-interface).

**Normal Windows PowerShell, terminal B:**

```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 8000
Invoke-RestMethod http://127.0.0.1:8000/hello.txt
```

**Expected observations — other diagnostic fields will also appear:**

```output
TcpTestSucceeded : True
Hello from Ubuntu
```

The first result proves that a connection opens; the second proves that the intended application responds. Stop the server with **Ctrl+C in Ubuntu terminal A**. This test does not prove that a separate phone can reach the laptop.

## From a local test to a real sensor

For a sensor that already supplies a network endpoint, its Linux driver usually connects to the sensor's actual reachable IP. A USB sensor needs [USB attachment](../annexes/wsl-usb.md) instead. For the Android capstone, the direction is reversed: **the phone connects to the receiver inside Ubuntu**.

Use [Annex F's complete route](../annexes/wsl-capstone.md) for either Windows ADB forwarding, mirrored Wi-Fi or an explicit NAT TCP proxy. It includes address discovery, a receiver bound to a reachable interface, scoped firewall rules, verification and cleanup. Use the phone's actual address and the required port when allowing inbound traffic; keep firewalls enabled.

In NAT mode, these **Ubuntu** commands help identify the two sides:

```bash
hostname -I
ip route show default
```

The first lists Ubuntu's interface addresses. In the second, the address following `via` on the default route identifies the Windows-side gateway in the usual NAT arrangement. Addresses can change after restarting WSL. `0.0.0.0` is a server's “listen on all IPv4 interfaces” setting, not the destination to type into a phone app.

## Keep ROS discovery separate from the phone connection

Our ROS nodes all run inside the same Ubuntu instance. Lecture 00 therefore sets `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` and one shared `ROS_DOMAIN_ID`. The phone speaks authenticated WebSocket/TCP to `phone_bridge`; it does not join DDS discovery.

A future multi-computer ROS robot is a different network exercise: discovery range, domain, endpoint QoS, multicast/unicast routing and firewall policy must agree. Forwarding TCP `8443` does not forward DDS traffic. Windows `netsh interface portproxy` supports TCP forwarding, so a single such rule cannot solve general ROS discovery. [Microsoft portproxy reference](https://learn.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-interface-portproxy).

## Diagnose the first failed boundary

1. Confirm the service process is still running. Inside Ubuntu, `ss -ltn` lists listening TCP sockets; look for the intended port and bind address.
2. Test inside Ubuntu, then from Windows. If only Windows fails, inspect WSL forwarding and port conflicts.
3. Test from the actual phone. If only the phone fails, inspect the chosen LAN route, address and scoped firewall policy.
4. Once transport works, inspect certificate pin/token and application messages. A successful port test does not establish valid ROS sensor data.

NAT's `localhostForwarding` setting and mirrored networking belong under `[wsl2]` in Windows `%UserProfile%\.wslconfig`. Preserve other settings. Applying changes with `wsl --shutdown` stops all running WSL distributions, so save work and stop nodes first. [WSL configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

**Checkpoint:** explain why a successful Windows localhost test, an arriving phone image and a working ROS subscriber are progressively stronger evidence. Reference review: 30 October 2026.
