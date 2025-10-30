import json
import datetime
import ipaddress

# -------------------------
# Function 1: Load firewall rules from JSON
# -------------------------
def load_rules(filename="firewall_rules.json"):
    try:
        with open(filename, "r") as f:
            rules = json.load(f)
        return rules
    except FileNotFoundError:
        print("Error: Rules file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None


# -------------------------
# Function 2: Log result to file
# -------------------------
def log_result(entry):
    with open("logs.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.datetime.now()} - {entry}\n")


# -------------------------
# Function 3: Validate IP format
# -------------------------
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# -------------------------
# Function 4: Check firewall rule for IP and Port
# -------------------------
def check_firewall(ip, port, rules):
    # IP check
    if ip in rules.get("blocked_ips", []):
        result = f"❌ Access denied for IP {ip}."
    elif ip in rules.get("allowed_ips", []):
        result = f"✅ Access granted for IP {ip}."
    else:
        result = f"⚠️ IP {ip} not explicitly listed. Default action: BLOCKED."

    # Port check
    if port in rules.get("blocked_ports", []):
        result += f" Port {port} is BLOCKED."
    elif port in rules.get("allowed_ports", []):
        result += f" Port {port} is ALLOWED."
    else:
        result += f" Port {port} not listed. Default action: BLOCKED."

    return result


# -------------------------
# Function 5: Main simulator loop
# -------------------------
def main():
    rules = load_rules()
    if not rules:
        return

    print("\n=== BASIC FIREWALL SIMULATOR ===")
    while True:
        ip = input("\nEnter IP to check (or 'exit' to quit): ").strip()
        if ip.lower() == "exit":
            break

        if not is_valid_ip(ip):
            print("Invalid IP format. Try again.")
            continue

        try:
            port = int(input("Enter port number: "))
        except ValueError:
            print("Invalid port number. Must be an integer.")
            continue

        result = check_firewall(ip, port, rules)
        print(result)
        log_result(f"Checked IP {ip}, Port {port} -> {result}")

    print("\nExiting firewall simulator. Logs saved in logs.txt.")


if __name__ == "__main__":
    main()
