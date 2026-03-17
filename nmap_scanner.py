import subprocess

def check_nmap():
    try:
        subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def run_scan(target, choice):
    try:
        if choice == "1":
            cmd = ["nmap", "-sn", target]

        elif choice == "2":
            cmd = ["nmap", target]

        elif choice == "3":
            ports = input("Enter port range (e.g., 1-100): ")
            cmd = ["nmap", "-p", ports, target]

        elif choice == "4":
            cmd = ["nmap", "-sV", target]

        elif choice == "5":
            cmd = ["nmap", "-O", target]

        else:
            print("Invalid choice")
            return

        print("\nScanning...\n")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        print(result.stdout)

        save = input("Save results? (y/n): ").lower()
        if save == "y":
            with open("nmap_results.txt", "w") as f:
                f.write(result.stdout)
            print("Saved to nmap_results.txt")

    except subprocess.TimeoutExpired:
        print("Scan timed out")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    print("=== Nmap Scanner ===")

    if not check_nmap():
        print("Nmap not installed!")
        exit()

    target = input("Enter target IP or network: ")

    print("\n1. Host Discovery (-sn)")
    print("2. Port Scan (1-1000)")
    print("3. Custom Port Scan")
    print("4. Service Version (-sV)")
    print("5. OS Detection (-O)")

    choice = input("Enter choice: ")

    run_scan(target, choice)