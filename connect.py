#!/usr/bin/env python3
import os
import sys
import subprocess
import time

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

def check_root():
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!] This script must be run as root (with sudo){Colors.ENDC}")
        print(f"{Colors.YELLOW}    Please run: sudo python3 {sys.argv[0]}{Colors.ENDC}")
        sys.exit(1)

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

    print(f"{Colors.RED}[-] No internet access detected.{Colors.ENDC}")
    return False

def change_mac(new_mac, connection_name):
    print(f"[+] Setting new MAC for '{connection_name}': {new_mac}")
    subprocess.run(
        f'sudo nmcli connection modify "{connection_name}" wifi.cloned-mac-address {new_mac}',
        shell=True,
        check=True # Fail hard if this command shits the bed
    )

    print(f"[+] Deactivating connection '{connection_name}'...")
    subprocess.run(
        f'sudo nmcli connection down "{connection_name}"',
        shell=True,
        check=True
    )
    time.sleep(1)

    print(f"[+] Activating connection '{connection_name}' with new MAC...")
    subprocess.run(
        f'sudo nmcli connection up "{connection_name}"',
        shell=True,
        check=True
    )
    print(f"[+] Connection command sent.")

def load_working_macs():
    try:
        if not os.path.exists("working_mac.txt"):
            print(f"{Colors.RED}[!] working_mac.txt not found. Please run pwn.py first to find working MACs.{Colors.ENDC}")
            sys.exit(1)
            
        with open("working_mac.txt", "r") as f:
            macs = [line.strip() for line in f if line.strip()]
            
        if not macs:
            print(f"{Colors.RED}[!] No MAC addresses found in working_mac.txt{Colors.ENDC}")
            sys.exit(1)
            
        return macs
    except Exception as e:
        print(f"{Colors.RED}[!] Error reading working_mac.txt: {str(e)}{Colors.ENDC}")
        sys.exit(1)

def display_macs(macs):
    print(f"\n{Colors.BOLD}Available MAC Addresses:{Colors.ENDC}")
    for i, mac in enumerate(macs, 1):
        print(f"{Colors.BLUE}[{i}] {mac}{Colors.ENDC}")
    print()

def get_user_choice(max_choice):
    while True:
        try:
            choice = input(f"{Colors.YELLOW}Select a MAC address (1-{max_choice}): {Colors.ENDC}")
            choice = int(choice)
            if 1 <= choice <= max_choice:
                return choice
            print(f"{Colors.RED}[!] Please enter a number between 1 and {max_choice}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}[!] Please enter a valid number{Colors.ENDC}")

def main():
    check_root()
    connection_name = get_active_wifi_connection()
    
    while True:
        macs = load_working_macs()
        display_macs(macs)
        
        choice = get_user_choice(len(macs))
        selected_mac = macs[choice - 1]
        
        change_mac(selected_mac, connection_name)
        
        if check_internet():
            print(f"{Colors.GREEN}[+] Successfully connected to internet with MAC: {selected_mac}{Colors.ENDC}")
            break
        else:
            print(f"{Colors.RED}[!] Failed to connect with MAC: {selected_mac}{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter to try another MAC address...{Colors.ENDC}")

if __name__ == "__main__":
    main() 
