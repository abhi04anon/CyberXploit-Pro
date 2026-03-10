"""
CyberXploit Pro - DNS Lookup Module
Performs comprehensive DNS record enumeration using the standard library only.
"""

import socket
import subprocess
import shutil
from typing import Callable


RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]


class DNSLookup:

    def lookup(self, target: str, log_fn: Callable[[str, str], None] = print):
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]

        # Basic resolution via socket
        log_fn("\n[+] Address Resolution (socket):", "header")
        self._resolve(domain, log_fn)

        # Try dig/nslookup for richer records
        if shutil.which("dig"):
            log_fn("\n[+] DNS Records via dig:", "header")
            self._dig(domain, log_fn)
        elif shutil.which("nslookup"):
            log_fn("\n[+] DNS Records via nslookup:", "header")
            self._nslookup(domain, log_fn)
        else:
            log_fn("\n[!] Neither 'dig' nor 'nslookup' found in PATH.", "warn")
            log_fn("    Install BIND utils for fuller DNS info.", "warn")

        # Reverse DNS on each A record
        log_fn("\n[+] Reverse DNS (PTR):", "header")
        self._reverse(domain, log_fn)

    # ------------------------------------------------------------------ helpers

    def _resolve(self, domain: str, log_fn: Callable):
        try:
            infos = socket.getaddrinfo(domain, None)
            seen = set()
            for info in infos:
                family, _, _, _, addr = info
                ip = addr[0]
                if ip not in seen:
                    seen.add(ip)
                    proto = "IPv6" if family == socket.AF_INET6 else "IPv4"
                    log_fn(f"  {proto:<8} {ip}", "info")
        except Exception as e:
            log_fn(f"[X] Resolution failed: {e}", "error")

    def _dig(self, domain: str, log_fn: Callable):
        for rtype in RECORD_TYPES:
            try:
                result = subprocess.run(
                    ["dig", "+short", rtype, domain],
                    capture_output=True, text=True, timeout=8,
                )
                output = result.stdout.strip()
                if output:
                    log_fn(f"  {rtype:<8} {output}", "data")
            except Exception:
                pass

    def _nslookup(self, domain: str, log_fn: Callable):
        try:
            result = subprocess.run(
                ["nslookup", domain],
                capture_output=True, text=True, timeout=8,
            )
            for line in result.stdout.splitlines():
                log_fn(f"  {line}", "data")
        except Exception as e:
            log_fn(f"[X] nslookup error: {e}", "error")

    def _reverse(self, domain: str, log_fn: Callable):
        try:
            ips = list({info[4][0] for info in socket.getaddrinfo(domain, None)})
            for ip in ips:
                try:
                    host = socket.gethostbyaddr(ip)[0]
                    log_fn(f"  {ip} → {host}", "info")
                except Exception:
                    log_fn(f"  {ip} → (no PTR record)", "data")
        except Exception as e:
            log_fn(f"[X] Reverse DNS failed: {e}", "error")
