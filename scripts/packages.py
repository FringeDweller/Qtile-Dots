import subprocess
import os
import shutil
from datetime import datetime

def backup_config():
    config_path = os.path.expanduser("~/.config")
    backup_folder = os.path.join(config_path, "backup")
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    backup_path = os.path.join(backup_folder, f"backup_{timestamp}")
    print(f"Copying ~/.config/ to {backup_path}...")
    try:
        shutil.copytree(config_path, backup_path)
        print("Backup completed successfully.")
    except shutil.Error as e:
        print(f"Error copying directory: {e}")

def check_packages():
    print("Checking and installing required packages with pacman...")
    required_packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "picom", 
        "rofi", "dunst", "neofetch", "ttf-font-awesome", 
        "qemu", "virt-manager", "virt-viewer", "dnsmasq", 
        "bridge-utils", "libguestfs", "ebtables", "vde2", "openbsd-netcat", 
        "mesa", "neovim", "openssh",
        "udisks2", "gvfs", "pavucontrol", "python-psutil", "feh", "nerd-fonts",
        "ffmpegthumbnailer", "unarchiver", "jq", "poppler", "fd", "ripgrep",
        "fzf", "zoxide", "alsa-utils", "mc", "python-pywal"
    ]
    for package in required_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-S', '--needed', package])

def check_paru():
    print("Checking and installing Paru...")
    installed = subprocess.run(['sudo', 'pacman', '-Q', 'paru'], capture_output=True)
    if installed.returncode != 0:
        print("Paru is not installed. Installing...")
        subprocess.run(['sudo', 'pacman', '-S', '--needed', 'base-devel'])
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/paru.git'])
        os.chdir('paru')  # Change the working directory to 'paru'
        subprocess.run(['makepkg', '-si'])
        os.chdir('..')  # Change back to the parent directory
        shutil.rmtree('paru')  # Remove the paru folder
    else:
        print("Paru is already installed.")

def check_optional_packages():
    print("Checking and installing optional packages with Paru...")
    optional_packages = [
        "brave-bin", "nomachine", "qtile-extras", 
        "python-pulsectl-asyncio", "udiskie", "vscodium"
    ]
    for package in optional_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing using Paru...")
            subprocess.run(['paru', '-S', package])

def check_ssh():
    print("Checking and enabling SSH service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'sshd'])
    result = subprocess.run(['sudo', 'systemctl', 'is-active', 'sshd'], capture_output=True)
    if result.returncode != 0:
        print("SSH is not active. Starting SSH service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'sshd'])
    else:
        print("SSH is already active.")

def check_nomachine():
    print("Checking and enabling NoMachine service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'nxserver'])
    result = subprocess.run(['sudo', 'systemctl', 'is-active', 'nxserver'], capture_output=True)
    if result.returncode != 0:
        print("NoMachine is not active. Starting NoMachine service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'nxserver'])
    else:
        print("NoMachine is already active.")

def check_udisks2():
    print("Checking and enabling udisks2 service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'udisks2'])
    result = subprocess.run(['sudo', 'systemctl', 'is-active', 'udisks2'], capture_output=True)
    if result.returncode != 0:
        print("udisks2 is not active. Starting udisks2 service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'udisks2'])
    else:
        print("udisks2 is already active.")

def create_folders():
    print("Creating necessary folders...")
    folders = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures")
    ]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        else:
            print(f"Folder already exists: {folder}")

def main():
    print("Starting system configuration...")
    backup_config()  # Backup existing config
    check_packages()
    check_paru()
    check_optional_packages()
    check_ssh()
    check_nomachine()
    check_udisks2()
    create_folders()
    print("System configuration completed.")

if __name__ == "__main__":
    main()

