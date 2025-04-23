# 📶 TraceNet - Network Usage Monitor

**TraceNet** is a lightweight, intuitive Python application designed to monitor and analyze your computer’s network activity in real-time. Whether you're curious about your bandwidth usage, connected devices, or which apps are hogging your internet, TraceNet gives you visibility and control—all from a simple GUI.

---

## ✨ Features

- **📡 Real-Time Traffic Monitoring**  
  Continuously tracks network data sent and received, updating every second.

- **🖥️ Connected Device Insights**  
  Detects and displays the number of devices currently connected to your network.

- **📶 Network SSID Detection**  
  Shows the name (SSID) of the Wi-Fi network you're connected to.

- **📦 Application Activity**  
  Lists applications currently using the network, along with the number of active connections for each.

- **⚠️ Bandwidth Threshold Alerts**  
  Set a daily usage limit (in MB) and receive automatic alerts when it’s exceeded.

- **📤 Export Reports**  
  Save your network usage data in CSV or professionally formatted PDF reports.

---

## 📋 Requirements

Make sure you have **Python 3.x** installed. The app depends on the following libraries:

| Library     | Purpose                                         |
|-------------|-------------------------------------------------|
| `psutil`    | Collects system and network I/O statistics      |
| `pystray`   | Enables creation of a system tray icon          |
| `Pillow`    | Handles tray icon drawing and rendering         |
| `fpdf`      | Generates PDF reports                           |
| `tkinter`   | Provides the graphical user interface (GUI)     |
| `csv`       | Used for exporting usage data in CSV format     |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Muhammad-BinMushtaq/TraceNet.git
cd TraceNet


### Clone the repository:

Clone this repository or download the code to your local machine.
```bash

  https://github.com/Muhammad-BinMushtaq/TraceNet.git
```

### Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Usage

To start using NetTrack, simply run the main script:

```bash
python3 nettrack.py
```

