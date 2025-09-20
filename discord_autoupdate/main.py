#!/usr/bin/env python3
import subprocess
import requests
import re
import sys
import os
import shutil

DISCORD_API_URL = "https://discord.com/api/download?platform=linux&format=deb"

def get_installed_version():
    try:
        output = subprocess.check_output(
            ["dpkg", "-s", "discord"], text=True, stderr=subprocess.DEVNULL
        )
        for line in output.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
    except subprocess.CalledProcessError:
        return None
    return None

def get_latest_version():
    resp = requests.head(DISCORD_API_URL, allow_redirects=True)
    location = resp.url
    match = re.search(r"/(\d+\.\d+\.\d+)/", location)
    if match:
        return match.group(1)
    return None

def update_discord():
    tmp_file = "/tmp/discord-latest.deb"
    print("⬇️  Downloading latest Discord...")
    r = requests.get(DISCORD_API_URL, allow_redirects=True)
    with open(tmp_file, "wb") as f:
        f.write(r.content)

    print("📦 Installing...")
    subprocess.run(["sudo", "dpkg", "-i", tmp_file], check=False)
    subprocess.run(["sudo", "apt-get", "-f", "-y", "install"], check=False)
    os.remove(tmp_file)
    print("✅ Discord updated")

def run_discord():
    # If Discord is already running, don’t start again
    try:
        subprocess.check_output(["pgrep", "-x", "Discord"])
        print("🚀 Discord is already running")
        return
    except subprocess.CalledProcessError:
        pass

    # Try to find the Discord executable in PATH
    discord_cmd = shutil.which("discord") or shutil.which("Discord")
    if not discord_cmd:
        print("❌ Could not find Discord executable")
        return

    print("🚀 Starting Discord...")
    subprocess.Popen([discord_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically update and run Discord on Debian-based systems."
    )
    parser.add_argument("--update", action="store_true", help="Check for latest version and update before running Discord")
    parser.add_argument("--check", action="store_true", help="Show installed and latest Discord version")
    args = parser.parse_args()

    installed = get_installed_version()
    latest = get_latest_version()

    if args.check:
        print(f"Installed version: {installed or 'not installed'}")
        print(f"Latest version:    {latest or 'unknown'}")
        return

    if args.update:
        print(f"Installed version: {installed or 'not installed'}")
        print(f"Latest version:    {latest or 'unknown'}")
        if installed != latest:
            update_discord()
        else:
            print("✅ Discord is up to date.")

    # Always run Discord by default
    run_discord()

if __name__ == "__main__":
    main()
