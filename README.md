# DOS — Advanced Cyber Attack Tool

> **Author:** Sujal Lamichhane  
> **Website:** [sujallamichhane.com.np](https://sujallamichhane.com.np)  
> **Purpose:** Controlled Lab

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

## Requirements

| Requirement | Details |
|---|---|
| Python | 3.8 or higher |
| pip | Comes with Python 3.8+ |
| Scapy | Installed inside the venv |
| OS | Linux / Kali Linux (recommended) |
| Privileges | Must run as `root` / `sudo` |

---

## Setup & Installation

### Step 1 — Clone or download the script

```bash
git clone https://github.com/yourusername/kali-dada.git
cd kali-dada
```

Or if you downloaded it manually:

```bash
cd /path/to/kali_dada
```

---

### Step 2 — Create a virtual environment

```bash
python3 -m venv venv
```

This creates a `venv/` folder in the current directory containing an isolated Python environment.

---

### Step 3 — Activate the virtual environment

```bash
source venv/bin/activate
```

Your terminal prompt will change to show `(venv)` — confirming the environment is active.

To deactivate later when you are done:

```bash
deactivate
```

---

### Step 4 — Install dependencies

```bash
pip install scapy
```

---

### Step 5 — Run the tool

Scapy requires raw socket access, so the script must be run as root. Use the **full path** to the venv Python binary so root uses the venv's packages:

```bash
sudo venv/bin/python kali_dada.py
```

> **Why `venv/bin/python` and not just `sudo python3`?**  
> `sudo` resets the `PATH` and uses the system Python, which does not have your venv's Scapy installed. Using the full path forces root to use the correct interpreter.

---

## Quick Start (all steps in one block)

```bash
# 1. Enter the project directory
cd /path/to/kali-dada

# 2. Create the virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install Scapy
pip install scapy

# 5. Run as root using the venv interpreter
sudo venv/bin/python kali_dada.py
```

---

## Usage

On launch you will see a legal warning, then be prompted to confirm:

```
Type 'I AGREE' to continue:
```

Type `I AGREE` (any capitalisation accepted — `i agree`, `I Agree`, etc.) and press Enter.
You will then see the main menu:

```
  [1] Advanced TCP SYN Flood
  [2] Advanced UDP Flood
  [3] ICMP Ping Flood
  [4] HTTP GET Flood
  ──────────────────
  [5] Exit
```

Select an option, enter a target IP, then follow the prompts for port, duration, and thread count.
Each field shows a default value in brackets — press Enter to accept it.

---

## Attack Modules

### 1. Advanced TCP SYN Flood *(Layer 3/4)*

Sends high-volume TCP SYN packets with spoofed source IPs and fragmented packets to fill the
target's half-open connection table, preventing legitimate connections.

| | |
|---|---|
| Requires | Scapy + root |
| Default port | 80 |
| Default threads | 5 |
| Primary defence | SYN cookies (RFC 4987), stateful firewall |

---

### 2. Advanced UDP Flood *(Layer 3/4)*

Sends random-length (64–1500 byte) UDP datagrams. Two modes available:
- **Spoofed mode** — uses Scapy with forged source IPs (requires root)
- **Socket mode** — uses OS UDP socket for maximum raw throughput

| | |
|---|---|
| Requires | Root for spoofed mode only |
| Default port | 53 |
| Default threads | 5 |
| Primary defence | BCP38 anti-spoofing, ingress rate limiting |

---

### 3. ICMP Ping Flood *(Layer 3)*

Storms the target with ICMP Echo Requests using randomised payloads and spoofed source IPs,
overwhelming ICMP processing and consuming bandwidth.

| | |
|---|---|
| Requires | Scapy + root |
| Default threads | 5 |
| Primary defence | ICMP rate limiting, perimeter firewall rules |

---

### 4. HTTP GET Flood *(Layer 7)*

Fires rapid HTTP GET requests with randomised paths and rotating User-Agent strings,
mimicking legitimate browser traffic to bypass L3/L4 filters.

| | |
|---|---|
| Requires | Standard sockets — no root needed |
| Default port | 80 |
| Default threads | 20 |
| Primary defence | WAF, CAPTCHA, JS challenge, Cloudflare Bot Fight Mode |

---

## Live Stats

During any active attack a live counter updates in place every 0.3 seconds:

```
Sent:   18,432   OK:  18,301   Err:    131   PPS:   1,245.7   Time:   14.8s
```

A full summary is printed after each run showing total sent, successes, errors, duration, and
average packets per second.

---

## Stopping an Attack

Press `Ctrl+C` at any time to gracefully stop the current attack and return to the menu.
The tool will **not** exit — you can start a new attack or choose option **5** to quit.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Operation not permitted` | Run with `sudo venv/bin/python kali_dada.py` |
| `Scapy not found` | Activate the venv first, then `pip install scapy` |
| `sudo: venv/bin/python: command not found` | Use the absolute path: `sudo /full/path/to/venv/bin/python kali_dada.py` |
| SYN / ICMP flood shows 0 packets | Verify Scapy: `venv/bin/python -c "import scapy; print('OK')"` |
| Very low PPS on UDP / SYN | Increase thread count; ensure no firewall is blocking outbound raw sockets |

---

## Project Structure

```
kali-dada/
├── kali_dada.py      # Main script — all modules in a single file
├── venv/             # Virtual environment (created by you, not committed to git)
└── README.md         # This file
```

---

## Ethical Use

Always:

- Use **only** on systems you own or have **explicit written permission** to test
- Operate in an **isolated lab or VM environment**
- Never target production systems, public infrastructure, or third-party services
