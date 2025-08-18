# CyberXploit-Pro
A beginner-friendly penetration testing toolkit with a GUI. Includes web vulnerability testing, Nmap integration, WHOIS lookups, and Kali command references. For educational and authorized use only.
## ✨ Features

- **Web Vulnerability Testing**  
  Basic fuzzing for common injection points (SQL Injection, XSS payloads).

- **Nmap Integration**  
  Run `nmap` scans directly from the interface with options for service/version detection.

- **WHOIS Lookup**  
  Fetch registrar, domain creation, expiration, and contact details.

- **Kali Command Reference**  
  Quick access to common pentesting commands (Nmap, SQLMap, Hydra, Nikto).

---

## 🚀 Installation

1. Clone this repository:
   -bash
   git clone https://github.com/your-username/cyberxploit-pro.git
   cd cyberxploit-pro
2. pip install requests,python-whois
3. Install Nmap (required for scanning):
Download Nmap
Update the NMAP_PATH variable in main.py to point to your Nmap executable.

## Requirements
Python 3.8+
requests
python-whois
tkinter (comes pre-installed with Python on most systems)
Nmap (external tool)

##▶️ Usage
Run the application:
python3 main.py

Enter a target IP, URL, or domain, then choose one of the following:

1.Web Vulnerability Test → checks for possible SQLi/XSS issues

2.Nmap Scan → runs a system/network scan

3.WHOIS Lookup → fetches domain information

4.Kali Commands → displays common pentesting commands
