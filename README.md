# 🌀 Turnstile Integration with HRMS (Python)

A lightweight Python module that reads event data from turnstile systems (e.g. FaceID, RFID), prepares it for processing, and sends it to a backend HRMS system for logging and further analysis.

This utility can be run on a local device, edge gateway, or integrated as part of a cron job or systemd service.

---

## 📦 Features

- Collects access events (entry/exit) from biometric or RFID-based turnstiles
- Prepares and enriches payload with timestamp, device ID, UUID, and snapshot placeholder
- Sends data to a backend HRMS system via REST API
- Includes utility helpers for time formatting, JSON building, and response handling

---

## 📁 Project Structure

```
turnstile-integration/
├── run.py             # Main execution script
├── payload.py         # Event payload preparation
├── utils.py           # Timestamp, UUID, JSON formatter, log helpers
├── __init__.py        # (optional module init)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/turnstile-integration.git
cd turnstile-integration
```

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Configure API Endpoint

Open `run.py` and set your API endpoint:

```python
url = "http://localhost:9981/api/turnstile"
```

You can also configure authentication headers if required.

### 4. Run the Script

```bash
python run.py
```

Expected output:

```
[INFO] Sending payload to backend...
[200 OK] Payload accepted.
```

---

## 🔧 Configuration

All payloads are currently mocked inside `payload.py`. You can adapt this file to:

- Pull real data from the turnstile SDK
- Handle live device streams via sockets or TCP/IP
- Attach face snapshot images as base64 (to be added)

---

## 🛡 Security

- No sensitive data is logged
- Network requests can include bearer tokens or API keys
- Logs can be redirected to secure volume or remote log server

---

## 🔮 Future Improvements

- Add retry + exponential backoff for failed syncs
- Support snapshot upload to `/media/snapshot`
- Add local queue with SQLite fallback
- Dockerize for deployment on edge devices

---

## 👨‍💻 Author

Created and maintained by **Vakhobiddin Bobokulov**  
Pull requests and issues are welcome!