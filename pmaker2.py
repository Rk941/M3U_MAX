import os
import requests
import re
import cloudscraper
import tmuxp
from colorama import Fore, Style, init
from pyfiglet import figlet_format

init(autoreset=True)

# Function: Display ASCII Art
def ascii_art():
    print(Fore.GREEN + figlet_format("M3U MAX"))
    print(Fore.RED + "M3U PRO MAKER - PREMIUM" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n\tUltra M3U Maker - Build your own M3U Playlist!\n" + Style.RESET_ALL)

# Function: Extract M3U8 URL
def extract_m3u8_url(url):
    match = re.search(r'(https?://[^\s]+.m3u8)', url)
    return match.group(1) if match else url

# Function: Get Channel Name
def get_channel_name(url):
    url = extract_m3u8_url(url)
    name = url.split("/")[-1]
    name = re.sub(r"[-_.]", " ", name)
    name = re.sub(r"\d+", "", name).strip()
    name = name.replace("m3u8", "").strip()

    if len(name) < 3:
        name_match = re.search(r"https?://(?:www\.)?([^/]+)", url)
        if name_match:
            name = name_match.group(1).split('.')[0].replace("-", " ").title()
        else:
            name = "Unknown Channel"
    return name.title()

# Function: Fetch M3U from Online Source
def fetch_m3u(url):
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Error fetching M3U: {e}" + Style.RESET_ALL)
        return None

# Function: Create M3U Playlist
def create_m3u():
    ascii_art()
    channels = []
    print(Fore.CYAN + "➡️ Paste M3U links (one per line). Type 'DONE' when finished." + Style.RESET_ALL)

    channel_number = 1
    while True:
        link = input(Fore.GREEN + f"🔗 {channel_number}. Enter M3U Link (or 'DONE'): " + Style.RESET_ALL).strip()
        if link.upper() == "DONE":
            break
        elif not link.startswith("http"):
            print(Fore.RED + "❌ Invalid format! Enter a correct M3U link." + Style.RESET_ALL)
            continue

        link = extract_m3u8_url(link)
        name = get_channel_name(link)

        # Category selection
        categories = ["Movies", "Sports", "News", "Entertainment", "Music", "Kids", "Custom"]
        print(Fore.YELLOW + "Select Category:")
        for idx, cat in enumerate(categories, 1):
            print(f"{idx}. {cat}")
        choice = input(Fore.CYAN + "Enter category number (or Custom Name): " + Style.RESET_ALL)

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            if category == "Custom":
                category = input(Fore.CYAN + "Enter custom category: " + Style.RESET_ALL)
        else:
            category = choice

        channels.append({
            "number": channel_number,
            "name": name,
            "url": link,
            "category": category
        })
        channel_number += 1

    if not channels:
        print(Fore.RED + "❌ Error: No valid links provided!" + Style.RESET_ALL)
        return

    output_file = input(Fore.YELLOW + "📁 Enter output filename (default: auto_playlist.m3u): " + Style.RESET_ALL).strip()
    if not output_file:
        output_file = "auto_playlist.m3u"

    output_path = os.path.expanduser(f"~/storage/shared/{output_file}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            f.write(f'#EXTINF:-1 tvg-id="" tvg-name="{channel["name"]}" group-title="{channel["category"]}",{channel["number"]}. {channel["name"]}\n{channel["url"]}\n')

    print(Fore.BLUE + f"✅ M3U File Created: {output_path}" + Style.RESET_ALL)

# Function: Start TMUX Session
def start_tmux_session():
    session_name = "m3umax"
    script_path = os.path.expanduser("~/storage/shared/pmaker2.py")

    if not os.path.exists(script_path):
        print(Fore.RED + f"❌ Error: Script not found at {script_path}!" + Style.RESET_ALL)
        return

    os.system(f"tmux new-session -d -s {session_name} 'python {script_path}'")
    os.system(f"tmux attach-session -t {session_name}")

# Run Script
if __name__ == "__main__":
    create_m3u()