TraceNet: How It Connects to Operating System Concepts
📌 Introduction
TraceNet is a Python-based network monitoring application that interacts with several Operating System (OS) functionalities, such as networking, processes, threading, and file handling.
This document explains how different OS concepts are used in TraceNet.

🛠️ OS Concepts Used in TraceNet
1. Processes and Threads
Concept:
In an OS, a process is a running instance of a program. A thread is a lightweight sub-process that runs within a process.

In TraceNet:

monitor_traffic and run_tray functions are run in separate threads.

This ensures the GUI remains smooth and responsive while background monitoring continues.

Code Example:

python
Copy
Edit
threading.Thread(target=monitor_traffic, daemon=True).start()
threading.Thread(target=run_tray, daemon=True).start()
2. Networking and System Resources
Concept:
The OS manages networking by providing access to network interfaces, sockets, and connections.

In TraceNet:

Uses psutil.net_io_counters() to monitor bytes sent/received.

Uses psutil.net_connections() to list active connections and connected devices.

Code Example:

python
Copy
Edit
prev = psutil.net_io_counters()
for conn in psutil.net_connections():
    if conn.raddr:
        devices.add(conn.raddr.ip)
3. File System Management
Concept:
The OS allows programs to create, write, and manage files through system calls.

In TraceNet:

Data is exported to CSV and PDF files.

File dialogs (tkinter.filedialog) are used to select paths.

Code Example:

python
Copy
Edit
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    for t, s, r in usage_history:
        writer.writerow([t.strftime("%Y-%m-%d %H:%M:%S"), s, r])
4. Inter-Process Communication (IPC)
Concept:
Processes communicate via shared memory, sockets, or other IPC methods managed by the OS.

In TraceNet:

Indirectly identifies which apps (processes) are using network connections via socket details.

Code Example:

python
Copy
Edit
for proc in psutil.process_iter(attrs=['pid', 'name']):
    for conn in psutil.net_connections(kind='inet'):
        if conn.pid == pid:
            apps[name] = apps.get(name, 0) + 1
5. System Calls and OS Services
Concept:
A system call allows user programs to interact with the OS to request information or services.

In TraceNet:

Executes commands like netsh wlan show interfaces on Windows and iwgetid or nmcli on Linux.

Retrieves the network SSID by interacting with the OS shell.

Code Example:

python
Copy
Edit
output = os.popen("netsh wlan show interfaces").read()
📊 Summary Table

OS Concept	TraceNet Usage
Processes and Threads	Background tasks (traffic monitoring, tray)
Networking	Monitor bytes sent/received, active connections
File System Management	Exporting data to CSV and PDF files
Inter-Process Communication	Mapping apps to network connections
System Calls	Fetching Wi-Fi SSID and network info
🏁 Conclusion
TraceNet is a real-world example of how a user-level application relies deeply on OS-level functionalities like process management, networking, file system access, and system calls to provide a powerful yet simple network monitoring solution.


