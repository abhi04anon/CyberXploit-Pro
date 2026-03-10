"""
CyberXploit Pro - Main Application Class
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading

from modules.scanner import PortScanner
from modules.web_recon import WebRecon
from modules.whois_lookup import WhoisLookup
from modules.dns_lookup import DNSLookup
from modules.cheatsheet import Cheatsheet
from config.settings import TOOL_NAME, THEME, WINDOW_SIZE


class CyberXploitApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(TOOL_NAME)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=THEME["bg"])
        self.root.resizable(True, True)

        # Module instances
        self.scanner = PortScanner()
        self.web_recon = WebRecon()
        self.whois = WhoisLookup()
        self.dns = DNSLookup()
        self.cheatsheet = Cheatsheet()

        self._build_ui()

    def _build_ui(self):
        """Build the main UI layout."""
        self._build_header()
        self._build_target_input()
        self._build_tabs()
        self._build_output()
        self._build_statusbar()

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=THEME["header_bg"], pady=8)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=f"⚡ {TOOL_NAME}",
            fg=THEME["accent"],
            bg=THEME["header_bg"],
            font=("Consolas", 22, "bold"),
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="Cross-Platform Cybersecurity Toolkit",
            fg=THEME["muted"],
            bg=THEME["header_bg"],
            font=("Consolas", 10),
        ).pack(side=tk.LEFT, padx=5, pady=8)

    def _build_target_input(self):
        input_frame = tk.Frame(self.root, bg=THEME["bg"], pady=8)
        input_frame.pack(fill=tk.X, padx=20)

        tk.Label(
            input_frame,
            text="Target (IP / URL / Domain):",
            fg=THEME["fg"],
            bg=THEME["bg"],
            font=("Consolas", 11),
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.target_entry = tk.Entry(
            input_frame,
            width=55,
            font=("Consolas", 11),
            bg=THEME["entry_bg"],
            fg=THEME["fg"],
            insertbackground=THEME["accent"],
            relief=tk.FLAT,
            bd=4,
        )
        self.target_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.target_entry.insert(0, "e.g. example.com or 192.168.1.1")
        self.target_entry.bind("<FocusIn>", self._clear_placeholder)
        self.target_entry.bind("<Return>", lambda e: self._route_action())

        tk.Button(
            input_frame,
            text="Clear Output",
            command=self._clear_output,
            bg=THEME["btn_danger"],
            fg="white",
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=10,
        ).pack(side=tk.RIGHT)

    def _build_tabs(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.TNotebook",
            background=THEME["bg"],
            borderwidth=0,
        )
        style.configure(
            "Custom.TNotebook.Tab",
            background=THEME["tab_bg"],
            foreground=THEME["fg"],
            font=("Consolas", 10, "bold"),
            padding=[12, 6],
        )
        style.map(
            "Custom.TNotebook.Tab",
            background=[("selected", THEME["tab_active"])],
            foreground=[("selected", THEME["accent"])],
        )

        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.X, padx=20, pady=(10, 0))

        tabs_buttons = [
            ("🔍  Port Scan", self._run_port_scan, THEME["btn_green"]),
            ("🌐  Web Recon", self._run_web_recon, THEME["btn_blue"]),
            ("📋  WHOIS", self._run_whois, THEME["btn_purple"]),
            ("🔎  DNS Lookup", self._run_dns, THEME["btn_orange"]),
            ("📖  Cheat Sheet", self._show_cheatsheet, THEME["btn_gray"]),
        ]

        btn_frame = tk.Frame(self.root, bg=THEME["bg"])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        for i, (label, fn, color) in enumerate(tabs_buttons):
            tk.Button(
                btn_frame,
                text=label,
                command=lambda f=fn: self._run_async(f),
                bg=color,
                fg="white",
                font=("Consolas", 10, "bold"),
                relief=tk.FLAT,
                padx=14,
                pady=8,
                cursor="hand2",
            ).grid(row=0, column=i, padx=6)

    def _build_output(self):
        output_frame = tk.Frame(self.root, bg=THEME["bg"])
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 5))

        tk.Label(
            output_frame,
            text="Output Console",
            fg=THEME["muted"],
            bg=THEME["bg"],
            font=("Consolas", 9),
            anchor="w",
        ).pack(fill=tk.X)

        self.result_text = scrolledtext.ScrolledText(
            output_frame,
            bg=THEME["console_bg"],
            fg=THEME["console_fg"],
            font=("Consolas", 10),
            relief=tk.FLAT,
            bd=6,
            wrap=tk.WORD,
            insertbackground=THEME["accent"],
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.configure(state=tk.NORMAL)

        # Tag colours for log levels
        self.result_text.tag_config("info", foreground="#00FF90")
        self.result_text.tag_config("warn", foreground="#FFD700")
        self.result_text.tag_config("error", foreground="#FF4444")
        self.result_text.tag_config("header", foreground="#00BFFF")
        self.result_text.tag_config("data", foreground="#E0E0E0")

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Ready.")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            fg=THEME["muted"],
            bg=THEME["header_bg"],
            font=("Consolas", 9),
            anchor="w",
            padx=10,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ------------------------------------------------------------------ helpers

    def _clear_placeholder(self, event):
        if self.target_entry.get().startswith("e.g."):
            self.target_entry.delete(0, tk.END)

    def _get_target(self):
        val = self.target_entry.get().strip()
        if val.startswith("e.g.") or not val:
            return None
        return val

    def _clear_output(self):
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

    def _log(self, message: str, tag: str = "data"):
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)

    def _set_status(self, msg: str):
        self.status_var.set(msg)

    def _run_async(self, fn):
        threading.Thread(target=fn, daemon=True).start()

    def _route_action(self):
        """Default Enter key action: port scan."""
        self._run_async(self._run_port_scan)

    # ------------------------------------------------------------------ actions

    def _run_port_scan(self):
        target = self._get_target()
        if not target:
            self._log("[!] Please enter a target first.", "warn")
            return
        self._log(f"\n{'='*60}", "header")
        self._log(f"  PORT SCAN → {target}", "header")
        self._log(f"{'='*60}", "header")
        self._set_status(f"Scanning {target}…")
        results = self.scanner.scan(target, log_fn=self._log)
        self._set_status("Port scan complete.")

    def _run_web_recon(self):
        target = self._get_target()
        if not target:
            self._log("[!] Please enter a target first.", "warn")
            return
        self._log(f"\n{'='*60}", "header")
        self._log(f"  WEB RECON → {target}", "header")
        self._log(f"{'='*60}", "header")
        self._set_status(f"Running web recon on {target}…")
        self.web_recon.run(target, log_fn=self._log)
        self._set_status("Web recon complete.")

    def _run_whois(self):
        target = self._get_target()
        if not target:
            self._log("[!] Please enter a target first.", "warn")
            return
        self._log(f"\n{'='*60}", "header")
        self._log(f"  WHOIS → {target}", "header")
        self._log(f"{'='*60}", "header")
        self._set_status(f"WHOIS lookup for {target}…")
        self.whois.lookup(target, log_fn=self._log)
        self._set_status("WHOIS complete.")

    def _run_dns(self):
        target = self._get_target()
        if not target:
            self._log("[!] Please enter a target first.", "warn")
            return
        self._log(f"\n{'='*60}", "header")
        self._log(f"  DNS LOOKUP → {target}", "header")
        self._log(f"{'='*60}", "header")
        self._set_status(f"DNS lookup for {target}…")
        self.dns.lookup(target, log_fn=self._log)
        self._set_status("DNS lookup complete.")

    def _show_cheatsheet(self):
        self._log(f"\n{'='*60}", "header")
        self._log("  PENETRATION TESTING CHEAT SHEET", "header")
        self._log(f"{'='*60}", "header")
        self.cheatsheet.display(log_fn=self._log)
        self._set_status("Cheat sheet loaded.")

    def run(self):
        self.root.mainloop()
