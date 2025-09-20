#!/usr/bin/env python3
import subprocess
import requests
import re
import sys
import os
import shutil
import tempfile
from tkinter import messagebox, Tk

# URL for the Discord Linux .deb package
DISCORD_API_URL = "https://discord.com/api/download?platform=linux&format=deb"

def get_installed_version():
    """
    Retrieves the currently installed version of Discord using dpkg.
    Returns the version string or None if Discord is not installed.
    """
    try:
        output = subprocess.check_output(
            ["dpkg", "-s", "discord"], text=True, stderr=subprocess.DEVNULL
        )
        for line in output.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return None

def get_latest_version():
    """
    Retrieves the latest available Discord version from the download URL.
    Returns the version string or None if it can't be found.
    """
    try:
        resp = requests.head(DISCORD_API_URL, allow_redirects=True)
        resp.raise_for_status()
        location = resp.url
        match = re.search(r"/(\d+\.\d+\.\d+)/", location)
        if match:
            return match.group(1)
    except (requests.exceptions.RequestException, IndexError):
        return None
    return None

def update_discord(is_interactive=False):
    """
    Downloads and installs the latest Discord .deb package.
    Uses pkexec for privilege escalation if available, otherwise falls back to sudo.
    """
    if is_interactive:
        Tk().wm_withdraw() # Hides the main Tkinter window
        message = "A new version of Discord is available. Do you want to update now?"
        if not messagebox.askyesno("Discord Updater", message):
            print("❌ Update canceled by user.")
            return

    # Check for pkexec and build the command accordingly
    privilege_cmd = shutil.which("pkexec") or shutil.which("sudo")
    if not privilege_cmd:
        print("❌ Could not find 'pkexec' or 'sudo' for installation. Aborting.")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".deb", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    print("⬇️ Downloading latest Discord...")
    try:
        r = requests.get(DISCORD_API_URL, allow_redirects=True)
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            f.write(r.content)
        print("✅ Download complete.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download Discord: {e}")
        os.remove(tmp_path)
        return

    print("📦 Installing...")
    try:
        subprocess.run([privilege_cmd, "dpkg", "-i", tmp_path], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ dpkg installation failed. Attempting to fix dependencies...")
        subprocess.run([privilege_cmd, "apt-get", "-f", "-y", "install"], check=True)

    os.remove(tmp_path)
    print("✅ Discord updated.")

def run_discord():
    """
    Starts Discord if it is not already running.
    """
    # Check if Discord is already running
    try:
        subprocess.check_output(["pgrep", "-x", "Discord"])
        print("🚀 Discord is already running.")
        return
    except subprocess.CalledProcessError:
        pass

    # Find the Discord executable in PATH
    discord_cmd = shutil.which("discord") or shutil.which("Discord")
    if not discord_cmd:
        print("❌ Could not find Discord executable.")
        return

    print("🚀 Starting Discord...")
    subprocess.Popen([discord_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically update and run Discord on Debian-based systems."
    )
    parser.add_argument("--update", action="store_true", help="Only update Discord, do not run.")
    parser.add_argument("--check", action="store_true", help="Show installed and latest Discord version without updating or running.")
    args = parser.parse_args()

    installed = get_installed_version()
    latest = get_latest_version()

    print(f"Installed version: {installed or 'not installed'}")
    print(f"Latest version:    {latest or 'unknown'}")

    if args.check:
        return

    is_update_needed = installed != latest and latest is not None

    if is_update_needed:
        update_discord(is_interactive=True)
    else:
        print("✅ Discord is up to date.")

    if not args.update:
        run_discord()

if __name__ == "__main__":
    main()
