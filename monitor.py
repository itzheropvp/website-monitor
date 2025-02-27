import requests
import time
import difflib
import logging
import threading
import json
import os
from datetime import datetime

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing important modules. Running pip...")
    try:
        os.system('pip install ttkbootstrap beautifulsoup4')
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *
        from bs4 import BeautifulSoup
    except Exception as e:
        print(f"Error installing required libraries: {e}")
        sys.exit(1)

logging.basicConfig(
    filename="website_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

monitoring = False
config = {
    "url": "",
    "interval": 10,
}

def get_website_content(url):
    """Fetch website content and return its text representation."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(), response.status_code 
        else:
            return None, response.status_code
    except requests.RequestException:
        return None, None

def monitor_website():
    """Continuously check the website for changes."""
    global monitoring
    last_content, last_status = get_website_content(config["url"])

    while monitoring:
        time.sleep(config["interval"])
        current_content, current_status = get_website_content(config["url"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if current_status is None:
            log_and_display(f"{timestamp} 🚨 Website {config['url']} is DOWN!", "red")
            status_label.config(text="Website: DOWN ❌", foreground="red")
        elif current_status != last_status:
            log_and_display(f"{timestamp} ⚠️ Status changed: {last_status} → {current_status}", "orange")

        if last_content and current_content and last_content != current_content:
            diff = difflib.unified_diff(last_content.splitlines(), current_content.splitlines(), lineterm="")
            log_and_display(f"{timestamp} 🔄 Change detected on {config['url']}:", "blue")
            for line in diff:
                log_and_display(line, "secondary")
        last_content, last_status = current_content, current_status

def log_and_display(message, color="primary"):
    """Log message and display it in the GUI."""
    logging.info(message)
    log_box.insert(ttk.END, message + "\n", color)
    log_box.tag_config(color, foreground=color)
    log_box.see(ttk.END)

def start_monitoring():
    """Start monitoring in a separate thread."""
    global monitoring
    if not monitoring:
        config["url"] = url_entry.get()
        config["interval"] = int(interval_entry.get())
        monitoring = True
        log_and_display(f'Started monitoring {config["url"]} every {config["interval"]} seconds...', "green")
        start_button.config(state=DISABLED)
        stop_button.config(state=NORMAL)
        status_label.config(text="Website: Monitoring 🔄", foreground="green")
        thread = threading.Thread(target=monitor_website, daemon=True)
        thread.start()

def stop_monitoring():
    """Stop monitoring."""
    global monitoring
    monitoring = False
    start_button.config(state=NORMAL)
    stop_button.config(state=DISABLED)
    status_label.config(text="Website: Stopped ⏸️", foreground="orange")

def save_config():
    """Save the current configuration to a file."""
    with open("config.json", "w") as f:
        json.dump(config, f)
    log_and_display("Configuration saved.", "green")

def load_config():
    """Load configuration from a file."""
    try:
        with open("config.json", "r") as f:
            loaded_config = json.load(f)
            config.update(loaded_config)
            url_entry.delete(0, ttk.END)
            url_entry.insert(0, config["url"])
            interval_entry.delete(0, ttk.END)
            interval_entry.insert(0, str(config["interval"]))
        log_and_display("Configuration loaded.", "green")
    except FileNotFoundError:
        log_and_display("No configuration file found.", "red")

def export_logs():
    """Export logs to a file."""
    with open("website_monitor_logs.txt", "w") as f:
        f.write(log_box.get("1.0", ttk.END))
    log_and_display("Logs exported to website_monitor_logs.txt.", "green")

def clear_logs():
    """Clear the log box."""
    log_box.delete("1.0", ttk.END)
    log_and_display("Logs cleared.", "green")

root = ttk.Window(themename="cosmo") 
root.title("Website Monitor")
root.geometry("800x600")

title_label = ttk.Label(root, text="Website Monitor", font=("Arial", 18, "bold"), bootstyle=PRIMARY)
title_label.pack(pady=10)

url_frame = ttk.Frame(root)
url_frame.pack(pady=5)

url_label = ttk.Label(url_frame, text="URL:", font=("Arial", 12))
url_label.grid(row=0, column=0, padx=5)

url_entry = ttk.Entry(url_frame, width=50)
url_entry.insert(0, config["url"])
url_entry.grid(row=0, column=1, padx=5)

interval_frame = ttk.Frame(root)
interval_frame.pack(pady=5)

interval_label = ttk.Label(interval_frame, text="Check Interval (seconds):", font=("Arial", 12))
interval_label.grid(row=0, column=0, padx=5)

interval_entry = ttk.Entry(interval_frame, width=10)
interval_entry.insert(0, str(config["interval"]))
interval_entry.grid(row=0, column=1, padx=5)

status_label = ttk.Label(root, text="Website: Not Monitoring ⏸️", font=("Arial", 12), bootstyle=WARNING)
status_label.pack(pady=10)

log_frame = ttk.Frame(root)
log_frame.pack(pady=10, fill=BOTH, expand=True)

log_box = ttk.Text(log_frame, wrap="word", height=15, width=80, font=("Consolas", 10))
log_box.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = ttk.Scrollbar(log_frame, command=log_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
log_box.config(yscrollcommand=scrollbar.set)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Start Monitoring", bootstyle=SUCCESS, command=start_monitoring)
start_button.grid(row=0, column=0, padx=5)

stop_button = ttk.Button(button_frame, text="Stop Monitoring", bootstyle=DANGER, command=stop_monitoring, state=DISABLED)
stop_button.grid(row=0, column=1, padx=5)

save_config_button = ttk.Button(button_frame, text="Save Config", bootstyle=INFO, command=save_config)
save_config_button.grid(row=0, column=2, padx=5)

load_config_button = ttk.Button(button_frame, text="Load Config", bootstyle=INFO, command=load_config)
load_config_button.grid(row=0, column=3, padx=5)

export_logs_button = ttk.Button(button_frame, text="Export Logs", bootstyle=INFO, command=export_logs)
export_logs_button.grid(row=0, column=4, padx=5)

clear_logs_button = ttk.Button(button_frame, text="Clear Logs", bootstyle=WARNING, command=clear_logs)
clear_logs_button.grid(row=0, column=5, padx=5)

root.mainloop()