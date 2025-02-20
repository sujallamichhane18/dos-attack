Here's an improved version of your cybersecurity attack testing tool documentation. I've made the formatting clearer, improved the readability, and added some extra instructions for clarity:

---

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
- **SYN Flood Attack**: TCP-based DoS (Denial of Service) attack to overwhelm a target.
- **UDP Flood Attack**: Flooding the target with UDP packets, causing service disruption.
- **Ping of Death**: Sending oversized ICMP packets to crash the target.
- **Packet Tracking**: Real-time statistics on the total packets sent, packet loss, and server status.
- **Hacker-Themed Interface**: Terminal-styled for a fun, hacker-like experience.

---

## 🔧 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-repo/Packet-Attack.git
cd dos-Attack
```

### 2️⃣ Set Up a Virtual Environment (Optional but Recommended)  
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows (PowerShell)
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1️⃣ Run the Script with Superuser Privileges  
```bash
sudo python3 main.py
```

### 2️⃣ Select an Attack Type  
Choose the attack type from the following options:
```bash
1: TCP SYN Flood
2: UDP Flood
3: Ping of Death
4: Exit
```

### 3️⃣ Enter Attack Details  
For the selected attack type, you'll be prompted to enter:
- **Target IP**
- **Target Port** (if applicable)
- **Attack Duration (in seconds)**

Example:
```bash
Enter your choice: 1
Enter target IP: 192.168.1.10
Enter target port: 80
Enter attack duration (seconds): 30
```

---

## 🛠️ Troubleshooting

### Permission Denied (Linux)  
If you get a `PermissionError`, run:
```bash
sudo chmod +x main.py
```

### Script Execution Disabled (Windows)  
If PowerShell prevents script execution, enable it by running:
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
```

---

## ❗ Disclaimer  
🚨 **This tool is strictly for educational and research purposes.** Unauthorized use may result in legal consequences. Ensure you have explicit permission to test the target systems.  
🔗 **Author Website**: [sujallamichhane.com.np](https://sujallamichhane.com.np)

---

💻 **Happy Hacking!**

---

