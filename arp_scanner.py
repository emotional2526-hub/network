import subprocess
import re
import platform
import socket

# -------------------------------
# Get Local IP
# -------------------------------
def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "192.168.1.1"


# -------------------------------
# Get Network Range
# -------------------------------
def get_network_range():
    ip = get_local_ip()
    parts = ip.split(".")
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


# -------------------------------
# Ping to Populate ARP Table
# -------------------------------
def populate_arp(network):
    print("\n[+] Populating ARP table...\n")

    param = "-n" if platform.system().lower() == "windows" else "-c"

    for i in range(1, 20):   # scan small range (fast)
        target = f"{network}.{i}"
        subprocess.run(
            ["ping", param, "1", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


# -------------------------------
# Get ARP Table
# -------------------------------
def get_arp_table():
    try:
        result = subprocess.run(
            ["arp", "-a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        print("Error getting ARP:", e)
        return ""


# -------------------------------
# Parse ARP Output (All OS)
# -------------------------------
def parse_arp(output):
    entries = []

    lines = output.split("\n")

    for line in lines:
        # Windows format
        win = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9-]{17})', line)

        # Linux/Mac format
        unix = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([a-fA-F0-9:]{17})', line)

        if win:
            entries.append((win.group(1), win.group(2)))
        elif unix:
            entries.append((unix.group(1), unix.group(2)))

    return entries


# -------------------------------
# Display Results
# -------------------------------
def display(entries):
    print("\n=== ARP Scanner Results ===\n")
    print("IP Address\t\tMAC Address")
    print("------------------------------------------")

    for ip, mac in entries:
        print(f"{ip}\t{mac}")

    print("\nTotal Devices Found:", len(entries))


# -------------------------------
# Save to File
# -------------------------------
def save_to_file(entries):
    with open("arp_results.txt", "w") as f:
        for ip, mac in entries:
            f.write(f"{ip} - {mac}\n")
    print("\n[+] Results saved to arp_results.txt")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("=== ARP Scanner (Auto Network Detection) ===")

    network = get_network_range()
    print(f"[+] Detected Network: {network}.x")

    populate_arp(network)

    output = get_arp_table()
    entries = parse_arp(output)

    if not entries:
        print("\n[!] No devices found. Try running again or check network.")
    else:
        display(entries)

        choice = input("\nSave results? (y/n): ").lower()
        if choice == "y":
            save_to_file(entries)