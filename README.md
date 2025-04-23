# TraceNet - Network Usage Monitor

TraceNet is a lightweight Python application that monitors and tracks the network usage on your computer. It provides real-time information on the amount of data sent and received over the network, as well as information on connected devices, active applications using the network, and the current network SSID. It also supports exporting usage data to CSV or PDF formats.

## Features
- **Real-time Traffic Monitoring**: Tracks the amount of data sent and received over the network in real-time.
- **Device Monitoring**: Displays the number of devices connected to the network.
- **Network SSID**: Displays the SSID of the connected Wi-Fi network.
- **Applications Using Network**: Lists the applications using the network and the number of connections each application has.
- **Threshold Alert**: Notifies you when your network usage exceeds a set threshold (in MB).
- **Data Export**: Allows you to export network usage data in CSV or PDF formats.

## Requirements

To run this application, you need to have Python 3.x installed along with the following dependencies:

- `psutil` - To monitor system and network statistics.
- `pystray` - For creating a system tray icon.
- `Pillow` - For creating and managing the tray icon image.
- `fpdf` - To generate PDF reports.
- `tkinter` - For the graphical user interface (GUI).
- `csv` - For exporting data in CSV format.

## Installation

### Clone the repository:

Clone this repository or download the code to your local machine.
```bash

  https://github.com/Muhammad-BinMushtaq/TraceNet.git
```

### Create a virtual environment (recommended):

### Install the required dependencies:
```bash
pip install -r requirements.txt
```


