import subprocess
import platform
import re

def get_param():
    return "-n" if platform.system().lower() == "windows" else "-c"

def ping_host(host):
    param = get_param()
    try:
        result = subprocess.run(
            ["ping", param, "4", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"\nHost: {host}")
            print("Status: Reachable")

            # Extract average time
            match = re.search(r'Average = (\d+)ms', result.stdout)
            if not match:
                match = re.search(r'avg[=/](\d+\.?\d*)', result.stdout)

            if match:
                print("Average Time:", match.group(1), "ms")
        else:
            print(f"{host} is unreachable")

    except subprocess.TimeoutExpired:
        print("Request timed out")
    except Exception as e:
        print("Error:", e)


def multiple_ping():
    hosts = input("Enter multiple IPs (comma separated): ").split(",")
    for host in hosts:
        ping_host(host.strip())


if __name__ == "__main__":
    print("=== Ping Scanner ===")

    choice = input("Single or Multiple? (s/m): ").lower()

    if choice == "s":
        host = input("Enter IP or hostname: ")
        ping_host(host)
    elif choice == "m":
        multiple_ping()
    else:
        print("Invalid choice")