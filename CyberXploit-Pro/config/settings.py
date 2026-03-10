"""
CyberXploit Pro - Configuration & Theme Settings
"""

TOOL_NAME = "CyberXploit Pro"
VERSION = "2.0.0"
WINDOW_SIZE = "1000x780"

THEME = {
    "bg":          "#1A1A2E",
    "header_bg":   "#16213E",
    "console_bg":  "#0D0D1A",
    "console_fg":  "#C0FFB3",
    "entry_bg":    "#222244",
    "tab_bg":      "#16213E",
    "tab_active":  "#1A1A2E",
    "fg":          "#E0E0E0",
    "accent":      "#00FFB2",
    "muted":       "#7A8A9A",
    # Buttons
    "btn_green":   "#1A6B3A",
    "btn_blue":    "#1A3F6B",
    "btn_purple":  "#4A1A6B",
    "btn_orange":  "#6B3D1A",
    "btn_danger":  "#6B1A1A",
    "btn_gray":    "#3A3A4A",
}

# Common ports to scan when nmap is unavailable
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
    443, 445, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017,
]

PORT_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB",
}
