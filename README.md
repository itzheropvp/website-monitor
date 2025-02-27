# 🖥️ Website Monitor

A **real-time website monitoring tool** that checks a website for **availability and content changes**. If any changes are detected or the website goes down, the application will **log the event**.

## 🚀 Features

✅ **Website Uptime Monitoring** – Detects if a website is **up or down**.  
✅ **Content Change Detection** – Alerts when the website content is modified.  
✅ **Modern GUI with Dark Theme** – Uses **ttkbootstrap** for a sleek look.  
✅ **Timestamps & Logging** – Saves all changes in a log file (`website_monitor.log`).  
✅ **Start/Stop Monitoring** – Control the monitoring process with buttons.  

## 📥 Installation

### 1️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed. Then, run:
```sh
pip install requests beautifulsoup4 ttkbootstrap
```

## 🎯 Usage

1. **Clone this repository**:
   ```sh
   git clone https://github.com/itzheropvp/website-monitor.git
   cd website-monitor
   ```

2. **Run the script**:
   ```sh
   python monitor.py
   ```

3. **Start Monitoring**:
   - Enter the website URL in the script.
   - Click **Start Monitoring** to begin.
   - Click **Stop Monitoring** to pause tracking.

## ⚙️ Configuration
You can modify the setting of the URL and INTERVAL inside the program when you run it.

## 📝 Logging
- All events are **saved in `website_monitor.log`**.
- Format: `[Timestamp] Event message`

## 📌 Example Notifications
- **Website Down** 🚨  
  ```
  [2025-02-25 12:00:00] 🚨 Website DOWN! example.com is not reachable!
  ```
- **Content Changed** 🔄  
  ```
  [2025-02-25 12:05:30] 🔄 Content Change on example.com
  ```
- **Status Change** ⚠️  
  ```
  [2025-02-25 12:10:45] ⚠️ Status changed: 200 → 500
  ```

## 📜 License
This project is open-source and licensed under the **MIT License**.

---

⭐ **Star this repository** if you find it useful! 😊
