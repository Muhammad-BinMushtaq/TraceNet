import psutil
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from fpdf import FPDF
import pystray
from PIL import Image, ImageDraw
import time
import csv
import socket
import os
import platform
import re

usage_history = []  # (timestamp, bytes_sent, bytes_recv)
alert_threshold_mb = 100  # Default alert if daily > 100MB

# ---------------------------
# System Tray Setup
# ---------------------------
def create_tray_icon():
    image = Image.new('RGB', (64, 64), "#0066CC")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 20, 44, 44), fill="white")
    return image

def quit_app(icon, item):
    icon.stop()
    root.quit()

def run_tray():
    icon = pystray.Icon("TraceNet", create_tray_icon(), menu=pystray.Menu(
        pystray.MenuItem("Quit", quit_app)
    ))
    icon.run()

# ---------------------------
# Monitor Thread
# ---------------------------
def monitor_traffic():
    prev = psutil.net_io_counters()
    while True:
        time.sleep(1)
        current = psutil.net_io_counters()
        sent = current.bytes_sent - prev.bytes_sent
        recv = current.bytes_recv - prev.bytes_recv
        prev = current

        usage_history.append((datetime.now(), sent, recv))
        update_gui(sent, recv)

        today_usage = sum((s + r) for t, s, r in usage_history if t.date() == datetime.now().date())
        if today_usage > alert_threshold_mb * 1024 * 1024:
            show_alert("Daily bandwidth limit exceeded!")
            time.sleep(60)

# ---------------------------
# Connected Devices
# ---------------------------
def get_connected_devices():
    devices = set()
    try:
        for conn in psutil.net_connections():
            if conn.raddr:
                devices.add(conn.raddr.ip)
    except Exception:
        pass
    return list(devices)

# ---------------------------
# Get Network SSID
# ---------------------------
def get_network_ssid():
    ssid = "N/A"
    try:
        if os.name == 'nt':
            output = os.popen("netsh wlan show interfaces").read()
            match = re.search(r"^\s*SSID\s*:\s*(.+)$", output, re.MULTILINE)
            if match:
                ssid = match.group(1).strip()
            else:
                ssid = "No Wi-Fi Connection"
        elif platform.system() == "Linux":
            if os.system("which iwgetid > /dev/null 2>&1") == 0:
                ssid = os.popen("iwgetid -r").read().strip()
                if not ssid:
                    ssid = "Not connected"
            else:
                output = os.popen("nmcli -t -f active,ssid dev wifi").read()
                for line in output.strip().split("\n"):
                    if line.startswith("yes:"):
                        ssid = line.split("yes:")[-1]
                        break
                else:
                    ssid = "No Wi-Fi Connection"
        else:
            ssid = "Unsupported OS"
    except Exception as e:
        ssid = f"Error: {str(e)}"
    return ssid

# ---------------------------
# Identify Applications
# ---------------------------
def get_apps_using_network():
    apps = {}
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            pid = proc.info['pid']
            name = proc.info['name']
            for conn in psutil.net_connections(kind='inet'):
                if conn.pid == pid:
                    apps[name] = apps.get(name, 0) + 1
    except Exception:
        pass
    return apps

# ---------------------------
# Export Reports
# ---------------------------
def export_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if not filename:
        return
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Bytes Sent', 'Bytes Received'])
        for t, s, r in usage_history:
            writer.writerow([t.strftime("%Y-%m-%d %H:%M:%S"), s, r])
    messagebox.showinfo("Export", f"Data exported to {filename}")

def export_pdf():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not filename:
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Bandwidth Usage Report", ln=True, align='C')
    pdf.ln(10)
    for t, s, r in usage_history[-50:]:
        line = f"{t.strftime('%Y-%m-%d %H:%M:%S')}  Sent: {s} bytes  Recv: {r} bytes"
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)
    messagebox.showinfo("Export", f"PDF report saved to {filename}")

# ---------------------------
# GUI Functions
# ---------------------------
def show_alert(msg):
    messagebox.showwarning("Alert", msg)

def update_gui(sent, recv):
    sent_label.config(text=f"Sent: {sent/1024:.2f} KB/s")
    recv_label.config(text=f"Received: {recv/1024:.2f} KB/s")
    devices = get_connected_devices()
    devices_label.config(text=f"Devices: {len(devices)}")
    ssid = get_network_ssid()
    ssid_label.config(text=f"Network SSID: {ssid}")

    apps = get_apps_using_network()
    app_usage = "\n".join([f"{app}: {count} connections" for app, count in apps.items()])
    app_usage_label.config(text=f"Apps using network:\n{app_usage}")

def set_threshold():
    global alert_threshold_mb
    try:
        val = int(threshold_entry.get())
        alert_threshold_mb = val
        messagebox.showinfo("Threshold Set", f"New limit: {val} MB/day")
    except:
        messagebox.showerror("Error", "Invalid number")

# ---------------------------
# GUI Setup
# ---------------------------
root = tk.Tk()
root.title("TraceNet - Network Monitor")
root.geometry("420x600")
root.config(bg='#E6F0FA')

heading = tk.Label(root, text="TraceNet", font=("Helvetica", 20, "bold"), bg="#004080", fg="white")
heading.pack(fill=tk.X, pady=10)

sent_label = tk.Label(root, text="Sent: 0 KB/s", font=("Arial", 12), bg='#E6F0FA')
sent_label.pack(pady=5)

recv_label = tk.Label(root, text="Received: 0 KB/s", font=("Arial", 12), bg='#E6F0FA')
recv_label.pack(pady=5)

devices_label = tk.Label(root, text="Devices: 0", font=("Arial", 12), bg='#E6F0FA')
devices_label.pack(pady=5)

ssid_label = tk.Label(root, text="Network SSID: N/A", font=("Arial", 12), bg='#E6F0FA')
ssid_label.pack(pady=5)

app_usage_label = tk.Label(root, text="Apps using network:", font=("Arial", 12), bg='#E6F0FA', justify=tk.LEFT, anchor="w")
app_usage_label.pack(pady=5, padx=10)

frame = tk.Frame(root, bg='#CCE0FF')
frame.pack(pady=10)

threshold_entry = tk.Entry(frame)
threshold_entry.pack(side=tk.LEFT, padx=5)

set_button = tk.Button(frame, text="Set Limit (MB)", command=set_threshold, bg="#3399FF", fg="white")
set_button.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root, bg='#E6F0FA')
btn_frame.pack(pady=20)

csv_btn = tk.Button(btn_frame, text="Export CSV", command=export_csv, bg="#00CC66", fg="white", width=12)
csv_btn.pack(side=tk.LEFT, padx=5)

pdf_btn = tk.Button(btn_frame, text="Export PDF", command=export_pdf, bg="#00CC66", fg="white", width=12)
pdf_btn.pack(side=tk.LEFT, padx=5)

# ---------------------------
# Threads
# ---------------------------
threading.Thread(target=monitor_traffic, daemon=True).start()
threading.Thread(target=run_tray, daemon=True).start()

# ---------------------------
# Mainloop
# ---------------------------
root.mainloop()
