# 🛡️ Cybersecurity Attack Testing Tool  

## ⚠️ WARNING  
🚨 **THIS TOOL IS FOR EDUCATIONAL AND TESTING PURPOSES ONLY.** 🚨  
**THE AUTHOR IS NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS TOOL.**  
**USING THIS TOOL ON UNAUTHORIZED SYSTEMS MAY VIOLATE LAWS.**  

---

## 🔥 Created by  
👤 **Sujal Lamichhane**  
🛡️ **Cyber Security Enthusiast**  
🌐 **Website:** [sujallamichhane.com.np](https://sujallamichhane.com.np)  

---

## 📌 Features  
- **SYN Flood Attack** (TCP-based DoS attack)  
- **UDP Flood Attack** (Overwhelming a target with UDP packets)  
- **Ping of Death** (Sending oversized ICMP packets)  
- **Packet Tracking** (Total packets sent, packet loss, and server status check)  
- **Hacker-Themed Interface** (Styled for Linux terminal users)  

---

## 🔧 Installation  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-repo/Packet-Attack.git
cd Packet-Attack
2️⃣ Set Up a Virtual Environment (Optional but Recommended)
bash

python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows (PowerShell)
3️⃣ Install Dependencies
bash

pip install -r requirements.txt
🚀 Usage
Run the Script with Superuser Privileges
bash

sudo python3 main.py
Select an Attack Type
makefile

1: TCP SYN Flood
2: UDP Flood
3: Ping of Death
4: Exit
📌 Enter the attack number, target IP, port (if required), and duration.

Example Attack
bash

sudo python3 main.py
yaml

1: TCP SYN Flood
2: UDP Flood
3: Ping of Death
4: Exit
Enter your choice: 1
Enter target IP: 192.168.1.10
Enter target port: 80
Enter attack duration (seconds): 30
🛠️ Troubleshooting
Permission Denied (Linux)
If you get a PermissionError, run:

bash

sudo chmod +x main.py
Script Execution Disabled (Windows)
If PowerShell prevents activation, allow scripts:

powershell

Set-ExecutionPolicy Unrestricted -Scope Process
❗ Disclaimer
🚨 This tool is strictly for security research and educational purposes.
Unauthorized use may result in legal consequences.
🔗 Author Website: sujallamichhane.com.np

💻 Happy Hacking!
