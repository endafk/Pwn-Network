<img src="mac-bypass.jpg" width="400" height="400"/>
# Pwn Pay-As-You-Go Wi-fi Networks 
## Because the router's "security" is a joke.
# These Scripts bypasses MAC based Authentication, allowing you to spoof an already active user, and bypass the Captive Portal.

## Features

- Automatically scans for MAC addresses using Bettercap
- Tests all found MAC addresses and saves working ones
- Interactive interface to select and switch between working MAC addresses
- Colorful terminal output for better visibility
- Automatic internet connection testing
- Works with NetworkManager (nmcli)

## Requirements


- Tries to get internet access. (Exploits mac based authentication- pwn a 
    device that has access to the internet)- Linux operating system
- Python 3.x
- Bettercap installed
- NetworkManager installed
- Sudo/administrator privileges

## Installation

1. Install the required dependencies:

1. Linux (of course)
2. bettercap
3. sudo (don’t be soft)
### Clone the Repo
```bash
git clone https://github.com/endafk/Pwn-Network.git
```

## Usage

### Step 1: Find Working MAC Addresses

Run the first script to scan for and test MAC addresses:

```bash
sudo python3 pwn.py
```

This script will:
- Scan for available MAC addresses using Bettercap
- Test each MAC address for internet connectivity
- Save working MAC addresses to `working_mac.txt`

### Step 2: Switch Between Working MAC Addresses

Once you have found working MAC addresses, you can use the second script to switch between them:

```bash
sudo python3 connect.py
```

This script will:
- Display a numbered list of working MAC addresses
- Let you select a MAC address to use
- Apply the selected MAC address
- Test the internet connection
- If successful, exit
- If unsuccessful, let you try another MAC address

## How It Works

### pwn.py
- Uses Bettercap to scan for MAC addresses on the network
- Tests each MAC address by:
  1. Changing the MAC address
  2. Cycling the WiFi connection
  3. Testing internet connectivity
- Saves working MAC addresses to `working_mac.txt`

### connect.py
- Reads working MAC addresses from `working_mac.txt`
- Provides an interactive interface to select MAC addresses
- Changes the MAC address using nmcli
- Tests internet connectivity
- Allows trying different MAC addresses until one works

## Notes

- Both scripts require root privileges
- The scripts will automatically detect your active WiFi connection
- Internet connectivity is tested using multiple reliable IPs (Google DNS, Cloudflare DNS, OpenDNS)
- Working MAC addresses are saved immediately as they are found
- You can interrupt the scripts at any time with Ctrl+C

## Troubleshooting

If you encounter issues:
1. Make sure you have all required dependencies installed
2. Run the scripts with sudo
3. Check if your WiFi connection is active
4. Ensure Bettercap is properly installed and configured
5. Check if NetworkManager is running

## License

Only use this on your own network or have proper permission. Don’t be a script kiddie. Be a chad — but a legal one.
