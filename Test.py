import os
import subprocess
import sys
import requests
from colorama import init, Fore, Style

# Initialize Colorama
init()

# Configuration
REPO_OWNER = "your-username"  # Replace with your GitHub username
REPO_NAME = "example-repo"    # Replace with your GitHub repository name
VERSION_FILE = "version.txt"  # File to store the current version

# List of required libraries
REQUIRED_LIBRARIES = ['requests', 'colorama']

def install_libraries():
    print(f"{Fore.BLUE}Installing required libraries...{Style.RESET_ALL}")
    for lib in REQUIRED_LIBRARIES:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    release_info = response.json()
    return release_info['tag_name']

def download_and_extract_release(tag_name):
    url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/tags/{tag_name}.zip"
    response = requests.get(url)
    zip_path = f"{REPO_NAME}-{tag_name}.zip"
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    subprocess.run(["unzip", "-o", zip_path])
    os.remove(zip_path)

def update_script():
    latest_version = get_latest_release()
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            current_version = f.read().strip()
    else:
        current_version = "0.0.0"

    if latest_version != current_version:
        print(f"{Fore.CYAN}New version available: {latest_version}{Style.RESET_ALL}")
        download_and_extract_release(latest_version)
        with open(VERSION_FILE, 'w') as f:
            f.write(latest_version)
        print(f"{Fore.CYAN}Update completed. Please restart the script.{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}You are using the latest version.{Style.RESET_ALL}")

def main():
    print(f"{Fore.MAGENTA}{Back.BLACK}Example Script - Checking for updates...{Style.RESET_ALL}")
    install_libraries()
    print(f"{Fore.BLUE}Scanning for new version...{Style.RESET_ALL}")
    update_script()

if __name__ == "__main__":
    main()
