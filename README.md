
# Pwn Pay-As-You-Go Wi-fi Networks
## Because the router's "security" is a joke.

# What It Does

- Scans for connected devices on the Wi-Fi.

- Collects all the mac addresses of the hosts on that network and Randomly spoofs a MAC from those devices.

- Tries to get internet access. (Exploits mac based authentication- pwn a device that has access to the internet)

Automatically switches if the MAC doesn't work.


### Requirements

1. Linux (of course)
2. bettercap
3. sudo (don’t be soft)
### Clone the Repo
```bash
git clone https://github.com/endafk/Pwn-Network.git
```
### Usage

### Just run it like a boss:
```bash
sudo python3 pwn.py
```

- Sit back. Watch it fake its way online.

# Disclaimer

Only use this on your own network or have proper permission. Don’t be a script kiddie. Be a chad — but a legal one.
