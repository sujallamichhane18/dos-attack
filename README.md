# Cybersecurity Attack Testing Tool

## Disclaimer
**This tool is for educational and testing purposes only, strictly within an isolated environment. Unauthorized use of this tool may violate laws and is strictly prohibited. The author is not responsible for any misuse.**

## Description
This is a cybersecurity attack simulation tool that allows users to test different types of network-based attacks in a controlled environment. It supports the following attack types:
- **SYN Flood** (`syn`) – Simulates a TCP SYN flood attack.
- **UDP Flood** (`udp`) – Sends large amounts of UDP packets to a target.
- **Ping of Death** (`pod`) – Sends oversized ICMP packets to crash a target.

## Features
- Customizable attack duration
- Randomized source IP addresses for testing defense mechanisms
- Simple command-line interface (CLI)

## Installation & Setup
Follow the steps below to set up and run this tool.

### 1. Clone the Repository
```bash
git clone https://github.com/sujallamichhane18/packet-attack-tool.git
cd packet-attack-tool
```

### 2. Create a Virtual Environment (Optional but Recommended)
#### **For Windows (PowerShell)**
First, enable script execution (if disabled):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Then, create and activate the virtual environment:
```powershell
python -m venv venv
venv\Scripts\Activate
```

#### **For Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### **For Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running the Tool
To launch an attack, use:
```bash
python attack.py -t <TARGET_IP> -p <PORT> -d <DURATION> -a <ATTACK_TYPE>
```
Example of a SYN flood attack for 30 seconds on port 80:
```bash
python attack.py -t 192.168.1.10 -p 80 -d 30 -a syn
```

### 5. Attack Options
| Attack Type | Description |
|------------|-------------|
| `syn` | SYN Flood Attack |
| `udp` | UDP Flood Attack |
| `pod` | Ping of Death Attack |

### 6. Exiting the Virtual Environment
When you're done, deactivate the virtual environment:
```bash
deactivate
```

## Requirements
This tool requires:
- Python 3.x
- `scapy` library
- Administrative or root privileges (for certain attacks)

## Dependencies
All dependencies are listed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

## Legal Disclaimer
Use this tool **only** for educational and authorized penetration testing. Unauthorized use is illegal and punishable by law.

**Author:** Sujal Lamichhane   
**Happy Hacking!**

