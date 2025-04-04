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
        
    print(f"{Colors.BLUE}[+] Scanning for MAC addresses...{Colors.ENDC}")
    
    # Run bettercap and capture its output
    result = subprocess.run("sudo bettercap -eval 'net.probe on; sleep 5; net.show; quit'", 
                          shell=True, capture_output=True, text=True)
    
    # Regex for MAC addresses (xx:xx:xx:xx:xx:xx format)
    mac_pattern = re.compile(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})')
    
    # Find all MAC addresses in the output
    mac_addresses = list(set(mac_pattern.findall(result.stdout)))
    
    # Write only MAC addresses to the file
    with open("mac_list.txt", "w") as file:
        for mac in mac_addresses:
            file.write(f"{mac}\n")
    
    if not mac_addresses:
        print(f"{Colors.RED}[-] No MAC addresses found. Exiting.{Colors.ENDC}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}[+] Found {len(mac_addresses)} unique MAC addresses{Colors.ENDC}")
    return mac_addresses

def change_mac(new_mac, connection_name):
    print(f"{Colors.BLUE}[+] Spoofing MAC Address: {new_mac}{Colors.ENDC}")

    subprocess.run(f'sudo nmcli connection modify "{connection_name}" wifi.cloned-mac-address {new_mac}', shell=True)

    print(f"{Colors.BLUE}[+] Turning WiFi off...{Colors.ENDC}")
    subprocess.run("sudo nmcli radio wifi off", shell=True)
    time.sleep(2)  # Wait for WiFi to turn off

    print(f"{Colors.BLUE}[+] Turning WiFi on...{Colors.ENDC}")
    subprocess.run("sudo nmcli radio wifi on", shell=True)
    time.sleep(2)  # Wait for WiFi to turn on

    print(f"{Colors.BLUE}[+] Reconnecting to {connection_name}...{Colors.ENDC}")
    subprocess.run(f'sudo nmcli connection up "{connection_name}"', shell=True)

def check_internet():
    print(f"{Colors.BLUE}[+] Checking internet access...{Colors.ENDC}")
    
    # List of reliable endpoints to check (IP and domain)
    endpoints = [
        ("8.8.8.8", "Google DNS"),
        ("1.1.1.1", "Cloudflare DNS"),
        ("google.com", "Google Domain")
    ]
    
    for endpoint, name in endpoints:
        try:
            # Try ping first (for IP addresses)
            if not endpoint.endswith('.com'):
                subprocess.run(
                    ["ping", "-c", "1", "-W", "5", endpoint],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
            else:
                # Try DNS resolution for domains(May vring up false positives)
                subprocess.run(
                    ["nslookup", endpoint],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10
                )
            print(f"{Colors.GREEN}[+] Internet access confirmed via {name}!{Colors.ENDC}")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"{Colors.YELLOW}[-] Failed to connect to {name}: {str(e)}{Colors.ENDC}")
            continue
        except Exception as e:
            print(f"{Colors.RED}[-] Unexpected error while checking {name}: {str(e)}{Colors.ENDC}")
            continue
    
    print(f"{Colors.RED}[-] No internet access detected from any endpoint. Trying another MAC...{Colors.ENDC}")
    return False

def get_active_wifi_connection():
    try:
        # connection name (WiFi is typically first in the list)
        result = subprocess.run(
            "nmcli -t -f NAME connection show --active",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            # Get all lines and filter out non-WiFi connections
            lines = result.stdout.strip().split('\n')
            
            # The first line should be the WiFi connection
            # We need to handle the case where the connection name might contain spaces
            connection_name = lines[0]
            
            # If the connection name is in quotes, remove them
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
    random.shuffle(mac_addresses)
    
    print(f"{Colors.BLUE}[+] Starting MAC address testing...{Colors.ENDC}")
    print(f"{Colors.YELLOW}[!] This may take a while. Please be patient.{Colors.ENDC}")
    
    working_mac_found = False
    working_mac = None
    
    for i, mac in enumerate(mac_addresses, 1):
        print(f"{Colors.BLUE}[+] Trying MAC {i}/{len(mac_addresses)}: {mac}{Colors.ENDC}")
        change_mac(mac, connection_name)
        time.sleep(5)  # Allow time for reconnection
        if check_internet():
            print(f"{Colors.GREEN}[+] Success with MAC: {mac}{Colors.ENDC}")
            working_mac_found = True
            working_mac = mac
            break
    
    if not working_mac_found:
        print(f"{Colors.RED}[!] No working MAC address found. Try again later.{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}[+] MAC spoofing completed successfully!{Colors.ENDC}")
        print(f"{Colors.GREEN}[+] Your connection is now using the MAC address: {working_mac}{Colors.ENDC}")
    
if __name__ == "__main__":
    main()
