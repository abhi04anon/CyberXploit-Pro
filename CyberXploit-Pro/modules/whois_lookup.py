"""
CyberXploit Pro - WHOIS Lookup Module
"""

from typing import Callable


class WhoisLookup:

    def lookup(self, target: str, log_fn: Callable[[str, str], None] = print):
        # Strip protocol if present
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]

        try:
            import whois as python_whois  # python-whois
        except ImportError:
            log_fn("[!] python-whois not installed.", "warn")
            log_fn("    Run: pip install python-whois", "warn")
            self._socket_whois(domain, log_fn)
            return

        try:
            w = python_whois.whois(domain)
            fields = {
                "Domain Name":      w.domain_name,
                "Registrar":        w.registrar,
                "WHOIS Server":     w.whois_server,
                "Creation Date":    w.creation_date,
                "Updated Date":     w.updated_date,
                "Expiration Date":  w.expiration_date,
                "Name Servers":     w.name_servers,
                "Status":           w.status,
                "Emails":           w.emails,
                "Registrant Org":   w.org,
                "Country":          w.country,
            }
            for label, value in fields.items():
                if value:
                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)
                    log_fn(f"  {label:<22}: {value}", "data")
                else:
                    log_fn(f"  {label:<22}: N/A", "muted")

        except Exception as e:
            log_fn(f"[X] WHOIS failed: {e}", "error")
            log_fn("    Trying raw socket WHOIS…", "warn")
            self._socket_whois(domain, log_fn)

    # ------------------------------------------------------------------ raw socket fallback

    def _socket_whois(self, domain: str, log_fn: Callable):
        """Minimal raw WHOIS query against whois.iana.org."""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect(("whois.iana.org", 43))
                s.sendall((domain + "\r\n").encode())
                data = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
            log_fn(data.decode(errors="ignore"), "data")
        except Exception as e:
            log_fn(f"[X] Raw WHOIS also failed: {e}", "error")
