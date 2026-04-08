# Trojan Horse Attack Simulation & SIEM Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-222222?style=for-the-badge&logo=recharts&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-4B8BBE?style=for-the-badge&logo=python&logoColor=white)

A professional full-stack cybersecurity project simulating a social engineering-based Trojan attack with a real-time behavioral monitoring system and an interactive SIEM-style dashboard.

---

## 🔍 Project Overview

This project is a comprehensive simulation designed for educational and defensive security research. It demonstrates how a seemingly harmless "System Cleaner" utility (the social engineering component) can execute a silent ransomware-style encryption attack in the background. 

Simultaneously, the project features a **Behavioral Monitoring Engine** that parses raw file system logs, identifies malicious patterns, and serves a **real-time SIEM Dashboard** to visualize the attack propagation, calculate risk scores, and alert security operations center (SOC) analysts.

---

## ✨ Key Features

- **Social Engineering Subagent**: A polished Tkinter-based "System Cleaner Pro" app that acts as the Trojan horse.
- **Ransomware-Style Encryption**: AES-256 (Fernet) encryption of a target folder to simulate a payload.
- **Real-Time Telemetry**: JSON-based logging system tracking file modifications and endpoint access.
- **Behavioral Detection Engine**: Custom Python logic that identifies rapid encryption bursts and cross-day clusters.
- **SIEM Dashboard**: A high-density React dashboard featuring:
  - **Non-CUMULATIVE Spikes**: Visualization of attack intensity (events/second).
  - **Risk Scoring**: Dynamic threat level calculation based on unique file impact and burst speed.
  - **Live Telemetry Stream**: Real-time log ingestion.
- **Recovery System**: An integrated decryption module triggered by a unique recovery key.

---

## 🏗️ Project Structure

| Directory | Description |
| :--- | :--- |
| `app/` | The fake "System Cleaner" Trojan application (GUI). |
| `trojan/` | Core attack logic, encryption modules, and configuration. |
| `trojan/data/` | Repository for `attack_log.json` and local telemetry. |
| `monitor/` | The backend detection engine and log parser. |
| `backend/` | Flask REST API serving analysis and raw logs to the frontend. |
| `frontend/` | React (Vite) dashboard using Tailwind CSS and Recharts. |

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/trojan-simulation-siem.git
cd trojan-simulation-siem
```

### 2. Prepare the Target Environment
Create a test folder on your Desktop to safely simulate the attack:
```bash
mkdir ~/Desktop/demo1
```
*(Add some non-critical files inside this folder like .txt or .jpg images for the demo)*

### 3. Install Python Dependencies
```bash
pip install cryptography flask flask-cors
```

### 4. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 5. Launch the System
For the full experience, run these components in separate terminals:

- **Start the SIEM Backend:**
  ```bash
  python backend/server.py
  ```
- **Start the Dashboard Frontend:**
  ```bash
  cd frontend && npm run dev
  ```
- **Launch the Trojan App:**
  ```bash
  python app/main_app.py
  ```

---

## 🎬 Demo Workflow

1. **Dashboard First**: Open the dashboard in your browser (usually `http://localhost:5173`). Observe the "System Online" status and empty metrics.
2. **The Social Engineering**: Launch the "System Cleaner Pro" app. Click **"Quick Scan"**.
3. **Silent Propagation**: While the fake progress bar moves, watch the dashboard. You will see **"Encryption Events"** spike and the **"Files Affected"** count rise in real-time.
4. **Threat Detection**: The SIEM alert panel will shift from **LOW** to **HIGH** risk as the detection engine identifies the rapid burst.
5. **Recovery**: Navigate to `~/Desktop/key.txt` to find the generated recovery key. Enter it into the "System Locked" interface of the app to restore your files.

---

## 📊 Dashboard Visuals

> [!NOTE]
> *Insert screenshots here for a professional portfolio look*

### SIEM Dashboard UI
![Dashboard Placeholder](https://via.placeholder.com/800x400?text=SIEM+Dashboard+Interface)

### Fake Application UI
![App Placeholder](https://via.placeholder.com/400x400?text=Social+Engineering+App+Tool)

---

## ⚙️ Configuration

- **Telemetry Logs**: Found at `trojan/data/attack_log.json`.
- **Encryption Keys**: Automatically saved to `~/Desktop/key.txt`.
- **Target Folder**: Modify `TARGET_FOLDER_NAME` in `trojan/utils.py` to target different directories.

---

## 🛡️ Security Disclaimer

> [!CAUTION]
> This software is for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**.
> - It is designed to run locally on a user-defined test folder.
> - It does **not** possess real malware traits such as network propagation, persistence, or privilege escalation.
> - Always run this simulation within a controlled environment. The authors are not responsible for any misuse or data loss.

---

## 🔮 Future Roadmap

- [ ] **Packaging**: Compile as a standalone `.app` or `.exe` for more realistic social engineering demos.
- [ ] **Advanced Anomaly Detection**: Implement machine learning-based entropy analysis for file encryption detection.
- [ ] **Multi-Device Monitoring**: Support for centralized monitoring of multiple simulated endpoints.
- [ ] **Elasticsearch Integration**: Migrate from local JSON to a full ELK stack integration.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

*This project simulates malicious behavior strictly for educational and defensive security research purposes.*
