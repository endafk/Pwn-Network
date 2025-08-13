<img src="mac-bypass.jpg" width="400" height="400"/>



# Pwn Pay-As-You-Go Wi-fi Networks 

## Requirements
- Linux
- Python 3.x
- Bettercap installed.
- NetworkManager installed(Any decent linux distro has it).

# Windows user?

I'm Working on it

## Installation
- Just yank Bettercap from your package manager, or make it using go from wiki.
### Clone the Repo
```bash
git clone https://github.com/endafk/Pwn-Network.git
```

# Usage

### Make the scripts executable

```
chmod +x connect.py pwn.py
```
### Scan the network

```
sudo ./pwn.py
```

### If you landed on some gold mine
```
sudo ./connect.py
```

# Notes

- Both scripts require root privileges
- The scripts will automatically detect your active WiFi connection(Connec t first before running them)
- Only use this on your own network or have proper permission.

## Troubleshooting

If you encounter issues:

That's your problem, not mine.



