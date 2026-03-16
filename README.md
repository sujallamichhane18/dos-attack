# Kali Dada — Advanced Cyber Attack Simulation Tool

> **Author:** Sujal Lamichhane  
> **Website:** [sujallamichhane.com.np](https://sujallamichhane.com.np)  
> **Purpose:** Controlled Lab / Educational Demonstration

---

## ⚠ Legal Disclaimer

**This tool is strictly for EDUCATIONAL and CONTROLLED LAB environments only.**

Running any of these attacks against a system without **explicit written authorisation** is a criminal offence under:

- Computer Fraud and Abuse Act (CFAA) — USA
- Computer Misuse Act — UK
- IT Act 2000 — Nepal / India
- Equivalent laws worldwide

The author bears **zero responsibility** for any misuse.

---

## Overview

Kali Dada is a Python-based network stress-testing and DDoS simulation tool designed to help security researchers, students, and penetration testers understand how volumetric and application-layer attacks work — and how to defend against them.

It includes five attack modules, each with detailed educational commentary explaining the underlying technique, how defences work, and real-world context.

---

## Requirements

| Requirement | Details |
|---|---|
| Python | 3.8 or higher |
| Scapy | Required for SYN Flood, ICMP Flood, spoofed UDP |
| Root / sudo | Required for raw socket operations |
| OS | Linux recommended (Kali Linux ideal) |

### Install dependencies

```bash
pip3 install scapy
```

---

## Usage

```bash
sudo python3 kali_dada.py
```

You will be shown a legal warning and asked to type `I AGREE` before proceeding. The tool then presents an interactive menu.

---

## Attack Modules

### 1. Advanced TCP SYN Flood *(Layer 3/4)*

Sends a high volume of TCP SYN packets with **spoofed source IPs** and **fragmented packets**, filling the target's half-open connection table and denying service to legitimate clients.

| Detail | Value |
|---|---|
| Technique | IP spoofing + TCP fragmentation |
| Requires | Scapy, root |
| Primary Defence | SYN cookies (RFC 4987), SYN rate limiting, stateful firewall |

---

### 2. Advanced UDP Flood *(Layer 3/4)*

Sends random-length UDP datagrams (64–1500 bytes) to overwhelm the target's UDP processing stack. Supports two modes:

- **Scapy mode** — spoofed source IPs, requires root
- **Socket mode** — faster, no spoofing, uses OS UDP socket

| Detail | Value |
|---|---|
| Technique | Random-size UDP datagrams, optional IP spoofing |
| Requires | Root (for Scapy/spoofed mode) |
| Primary Defence | Ingress rate limiting, BCP38 anti-spoofing, upstream scrubbing |

---

### 3. ICMP Ping Flood *(Layer 3)*

Sends a storm of ICMP Echo Request (ping) packets with **spoofed source IPs** and **random payloads**, consuming the target's bandwidth and ICMP processing capacity.

| Detail | Value |
|---|---|
| Technique | High-rate ICMP Echo Requests with spoofed IPs |
| Requires | Scapy, root |
| Primary Defence | ICMP rate limiting, perimeter firewall rules |

---

### 4. Amplification Attack *(Simulation Only)*

**No real traffic is sent.** This module is a pure educational walk-through explaining how UDP reflection/amplification attacks (DNS, NTP, SSDP, Memcached) work and why they are so effective.

| Protocol | Max Amplification Factor |
|---|---|
| DNS reflection | ~54× |
| NTP monlist | ~556× |
| SSDP | ~30× |
| Memcached | ~51,200× |

Primary defences covered: BCP38 ingress filtering, disabling open resolvers, RTBH routing.

---

### 5. HTTP GET Flood *(Layer 7)*

Sends rapid HTTP GET requests with **randomised paths** and **rotating User-Agent strings** to bypass simple signature-based filters. Operates at the application layer, making it harder to distinguish from legitimate browser traffic at L3/L4.

| Detail | Value |
|---|---|
| Technique | Randomised GET requests mimicking browser traffic |
| Requires | Standard sockets only (no root needed) |
| Primary Defence | WAF, CAPTCHA, JS challenge, rate limiting, Cloudflare Bot Fight Mode |

---

## Live Statistics

During any active attack, the tool displays a live progress line:

```
Sent:   12,450   OK:  12,301   Err:   149   PPS:   415.3   Time:   30.0s
```

A full summary is printed after each run showing total packets sent, successes, errors, duration, and average packets per second.

---

## Signal Handling

Press `Ctrl+C` at any time to **gracefully stop the current attack** and return to the menu. The tool will not exit — you can launch a new attack or choose to quit from the menu.

---

## Project Structure

```
kali_dada.py          # Main script — all modules in a single file
```

---

## Ethical Use

This tool was built to demonstrate real-world attack techniques in a way that helps defenders understand what they are protecting against. Always:

- Use only on systems **you own** or have **written permission** to test
- Operate in an **isolated lab environment**
- Never target production systems, public infrastructure, or third-party services

---

## License

This project is for educational use only. All rights reserved by the author. Redistribution or use in a malicious context is strictly prohibited.
