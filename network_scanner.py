import subprocess
import platform
import re
import csv
import threading
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="scan_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ---------------- PING ----------------
def ping_scan(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    try:
        result = subprocess.run(
            ['ping', param, '2', host],
            stdout=subprocess.PIPE,
            text=True
        )
        status = "Reachable" if result.returncode == 0 else "Not Reachable"
        logging.info(f"Ping {host} : {status}")
        return status
    except Exception as e:
        return "Error"


# ---------------- ARP ----------------
def arp_scan():
    result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE, text=True)
    pattern = r'(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9:-]{17})'
    entries = re.findall(pattern, result.stdout)
    logging.info("ARP scan executed")
    return entries


# ---------------- CSV SAVE ----------------
def save_to_csv(data):
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP Address", "MAC Address"])
        writer.writerows(data)
    logging.info("Saved ARP data to CSV")


# ---------------- NMAP ----------------
def nmap_scan(target):
    try:
        result = subprocess.run(['nmap', target], stdout=subprocess.PIPE, text=True)
        logging.info(f"Nmap scan on {target}")
        return result.stdout
    except:
        return "Nmap error"


# ---------------- MULTI-THREAD NETWORK SCAN ----------------
def scan_ip(ip):
    status = ping_scan(ip)
    print(ip, ":", status)

def network_scan(base_ip):
    print("\nScanning network...\n")
    threads = []

    for i in range(1, 50):  # bigger range
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=scan_ip, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    logging.info(f"Network scan completed for {base_ip}.0/24")


# ---------------- MAIN MENU ----------------
def main():
    print("=== Advanced Network Scanner ===")

    print("""
1. Ping Scan
2. ARP Scan
3. Nmap Scan
4. Network Range Scan
""")

    choice = input("Enter choice: ")

    if choice == '1':
        host = input("Enter host: ")
        result = ping_scan(host)
        print(result)

    elif choice == '2':
        entries = arp_scan()

        print("\nIP Address\tMAC Address")
        print("-"*40)

        for ip, mac in entries:
            print(f"{ip}\t{mac}")

        save = input("\nSave to CSV? (y/n): ")
        if save == 'y':
            save_to_csv(entries)
            print("Saved to output.csv")

    elif choice == '3':
        target = input("Enter target: ")
        print(nmap_scan(target))

    elif choice == '4':
        base = input("Enter base IP (e.g., 192.168.29): ")
        network_scan(base)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
