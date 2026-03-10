# ⚡ CyberXploit Pro

> **Cross-platform cybersecurity reconnaissance toolkit** for educational and authorized penetration testing purposes.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen)

---

## ⚠️ Legal Disclaimer

> **This tool is for educational purposes and authorized security testing ONLY.**
> Running scans, lookups, or probes against systems you do not own or have explicit written permission to test is **illegal** and unethical. The author takes no responsibility for misuse.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Port Scanner** | Uses nmap if available; falls back to fast threaded socket scanning |
| 🌐 **Web Recon** | HTTP header inspection, security header audit, common path probing |
| 📋 **WHOIS Lookup** | Full WHOIS with raw socket fallback |
| 🔎 **DNS Lookup** | A/AAAA/MX/NS/TXT records + reverse PTR lookup |
| 📖 **Cheat Sheet** | Comprehensive pentest command reference (recon → post-exploitation) |

---

## 🖥️ Screenshots

<img width="1011" height="810" alt="image" src="https://github.com/user-attachments/assets/204972ba-d245-4297-a3cd-6bc59f71c6bd" />


---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **tkinter** (usually bundled with Python; on Linux: `sudo apt install python3-tk`)
- **nmap** *(optional but recommended)* — [Download](https://nmap.org/download.html)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/abhi04anon/CyberXploit-Pro.git
cd CyberXploit-Pro

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Run the tool
python main.py
```

### Windows

```powershell
git clone https://github.com/abhi04anon/CyberXploit-Pro.git
cd CyberXploit-Pro
pip install -r requirements.txt
python main.py
```

> **Tip (Windows):** Install nmap from [nmap.org](https://nmap.org/download.html) and add it to your PATH for best results.

### Linux / macOS

```bash
# Install system dependencies (Debian/Ubuntu)
sudo apt install python3-tk nmap dnsutils -y

# Or on Arch/Manjaro
sudo pacman -S python-tkinter nmap bind-tools

git clone https://github.com/abhi04anon/CyberXploit-Pro.git
cd CyberXploit-Pro
pip install -r requirements.txt
python main.py
```

---

## 📁 Project Structure

```
CyberXploit-Pro/
├── main.py                 # Entry point
├── app.py                  # Main application & UI class
├── requirements.txt
├── README.md
├── .gitignore
├── config/
│   ├── __init__.py
│   └── settings.py         # Theme, constants, port lists
└── modules/
    ├── __init__.py
    ├── scanner.py          # Port scanner (nmap + socket fallback)
    ├── web_recon.py        # HTTP header & path inspection
    ├── whois_lookup.py     # WHOIS lookup + raw socket fallback
    ├── dns_lookup.py       # DNS record enumeration
    └── cheatsheet.py       # Pentest command reference
```

---

## 🛠️ Module Details

### Port Scanner (`modules/scanner.py`)
- Auto-detects nmap across standard install paths on Windows, Linux, and macOS
- Falls back to a **100-thread socket scanner** covering 20 common ports
- No dependency on a hardcoded path

### Web Recon (`modules/web_recon.py`)
- Inspects all response headers and highlights interesting ones
- Audits presence/absence of **6 critical security headers**
- Probes 14 common paths (robots.txt, admin panels, API endpoints, exposed files)
- Handles redirects and HTTPS without third-party libraries

### WHOIS (`modules/whois_lookup.py`)
- Uses `python-whois` when installed
- Falls back to a raw **RFC 3912 socket WHOIS query** if the library is absent

### DNS Lookup (`modules/dns_lookup.py`)
- IPv4 + IPv6 address resolution via `socket`
- Uses `dig` or `nslookup` (whichever is in PATH) for A/AAAA/MX/NS/TXT records
- Reverse PTR lookup on all resolved IPs

---

## 🔧 Configuration

Edit `config/settings.py` to customise:

- **`COMMON_PORTS`** — ports scanned in socket fallback mode
- **`THEME`** — all UI colours
- **`WINDOW_SIZE`** — initial window dimensions

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-module`
3. Commit your changes: `git commit -m 'Add my-module'`
4. Push to the branch: `git push origin feature/my-module`
5. Open a Pull Request

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Nmap Project](https://nmap.org)
- [python-whois](https://pypi.org/project/python-whois/)
- The open-source security community
