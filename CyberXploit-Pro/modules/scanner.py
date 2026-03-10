"""
CyberXploit Pro - Port Scanner Module
Cross-platform: uses nmap if available, otherwise pure-Python socket scanning.
"""

import socket
import subprocess
import shutil
import sys
import concurrent.futures
from typing import Callable

from config.settings import COMMON_PORTS, PORT_SERVICES


class PortScanner:
    """
    Attempts an nmap scan first; falls back to threaded socket scanning
    if nmap is not found in PATH.
    """

    TIMEOUT = 1.0  # seconds per socket probe

    def scan(self, target: str, log_fn: Callable[[str, str], None] = print):
        nmap_path = self._find_nmap()
        if nmap_path:
            log_fn(f"[+] nmap found at: {nmap_path}", "info")
            self._nmap_scan(target, nmap_path, log_fn)
        else:
            log_fn("[!] nmap not found – falling back to built-in socket scanner.", "warn")
            log_fn("    Install nmap for deeper results: https://nmap.org/download.html", "warn")
            self._socket_scan(target, log_fn)

    # ------------------------------------------------------------------ nmap

    def _find_nmap(self) -> str | None:
        """Return the nmap executable path or None."""
        path = shutil.which("nmap")
        if path:
            return path
        # Windows common install locations
        if sys.platform == "win32":
            candidates = [
                r"C:\Program Files (x86)\Nmap\nmap.exe",
                r"C:\Program Files\Nmap\nmap.exe",
                r"D:\Nmap\nmap.exe",
            ]
            for c in candidates:
                if shutil.os.path.isfile(c):
                    return c
        return None

    def _nmap_scan(self, target: str, nmap_path: str, log_fn: Callable):
        cmd = [nmap_path, "-Pn", "-sV", "--open", "-T4", target]
        log_fn(f"[+] Running: {' '.join(cmd)}", "info")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            for line in result.stdout.splitlines():
                tag = "info" if "open" in line else "data"
                log_fn(line, tag)
            if result.stderr:
                log_fn(f"[!] Nmap stderr: {result.stderr.strip()}", "warn")
        except subprocess.TimeoutExpired:
            log_fn("[X] Nmap timed out after 120 seconds.", "error")
        except Exception as e:
            log_fn(f"[X] Nmap error: {e}", "error")

    # ------------------------------------------------------------------ socket fallback

    def _socket_scan(self, target: str, log_fn: Callable):
        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror as e:
            log_fn(f"[X] Could not resolve host '{target}': {e}", "error")
            return

        log_fn(f"[+] Resolved {target} → {ip}", "info")
        log_fn(f"[+] Scanning {len(COMMON_PORTS)} common ports…", "info")

        open_ports = []

        def probe(port: int):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.TIMEOUT)
                    if s.connect_ex((ip, port)) == 0:
                        return port
            except Exception:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
            futures = {ex.submit(probe, p): p for p in COMMON_PORTS}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)

        if not open_ports:
            log_fn("[-] No open ports found on common ports list.", "warn")
            return

        open_ports.sort()
        log_fn(f"\n{'PORT':<10}{'STATE':<10}SERVICE", "header")
        log_fn("-" * 32, "header")
        for port in open_ports:
            service = PORT_SERVICES.get(port, "unknown")
            log_fn(f"{port:<10}{'open':<10}{service}", "info")

        log_fn(f"\n[+] Found {len(open_ports)} open port(s).", "info")
