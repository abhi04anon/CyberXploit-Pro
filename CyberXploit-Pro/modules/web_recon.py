"""
CyberXploit Pro - Web Recon Module
Gathers HTTP headers, server info, redirect chains, and probes common paths.
This is a passive reconnaissance tool — no exploitation is performed.
"""

from typing import Callable
import urllib.request
import urllib.error
import urllib.parse
import ssl
import socket


INTERESTING_HEADERS = [
    "server", "x-powered-by", "x-aspnet-version", "x-generator",
    "x-frame-options", "content-security-policy", "strict-transport-security",
    "x-content-type-options", "access-control-allow-origin",
    "x-runtime", "via", "set-cookie",
]

COMMON_PATHS = [
    "/robots.txt", "/sitemap.xml", "/.well-known/security.txt",
    "/admin", "/login", "/wp-admin", "/phpmyadmin",
    "/api", "/api/v1", "/swagger", "/graphql",
    "/.git/HEAD", "/.env", "/config.php",
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def _normalise(target: str) -> str:
    if not target.startswith(("http://", "https://")):
        return "https://" + target
    return target


class WebRecon:

    TIMEOUT = 6

    def run(self, target: str, log_fn: Callable[[str, str], None] = print):
        base_url = _normalise(target)
        log_fn(f"[+] Target URL: {base_url}", "info")

        self._check_headers(base_url, log_fn)
        self._probe_paths(base_url, log_fn)

    # ------------------------------------------------------------------ header inspection

    def _check_headers(self, url: str, log_fn: Callable):
        log_fn("\n[+] HTTP Response Headers:", "header")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=self.TIMEOUT, context=CTX) as resp:
                log_fn(f"    Status : {resp.status} {resp.reason}", "info")
                log_fn(f"    Final URL : {resp.url}", "data")

                headers = dict(resp.headers)
                for h, v in headers.items():
                    tag = "warn" if h.lower() in INTERESTING_HEADERS else "data"
                    log_fn(f"    {h}: {v}", tag)

                # Security header audit
                log_fn("\n[+] Security Header Audit:", "header")
                security_headers = [
                    "Strict-Transport-Security",
                    "Content-Security-Policy",
                    "X-Frame-Options",
                    "X-Content-Type-Options",
                    "Referrer-Policy",
                    "Permissions-Policy",
                ]
                for sh in security_headers:
                    present = sh in headers
                    status = "✔ Present" if present else "✘ MISSING"
                    tag = "info" if present else "warn"
                    log_fn(f"    {sh:<40} {status}", tag)

        except urllib.error.HTTPError as e:
            log_fn(f"    HTTP {e.code}: {e.reason}", "warn")
        except Exception as e:
            log_fn(f"[X] Header check failed: {e}", "error")

    # ------------------------------------------------------------------ path probing

    def _probe_paths(self, base_url: str, log_fn: Callable):
        log_fn("\n[+] Probing Common Paths:", "header")
        for path in COMMON_PATHS:
            url = base_url.rstrip("/") + path
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=self.TIMEOUT, context=CTX) as resp:
                    log_fn(f"    [FOUND {resp.status}] {path}", "info")
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    log_fn(f"    [403 FORBIDDEN] {path}", "warn")
                # 404 is expected noise — suppress it
            except Exception:
                pass  # Connection refused, timeout, etc.
