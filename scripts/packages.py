import os
import shutil
import subprocess
from datetime import datetime

def backup_config():
    print("Backing up configuration files...")
    config_files = [
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.config/qtile"),
        os.path.expanduser("~/.config/dunst"),
        os.path.expanduser("~/.config/picom"),
        os.path.expanduser("~/.config/rofi"),
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.expanduser(f"~/.config/backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    for file_path in config_files:
        if os.path.exists(file_path):
            backup_file = os.path.join(backup_dir, os.path.basename(file_path))
            if os.path.isdir(file_path):
                shutil.copytree(file_path, backup_file)
            else:
                shutil.copy(file_path, backup_file)
            print(f"Backup created: {backup_file}")
        else:
            print(f"File not found: {file_path}")

def check_packages():
    print("Checking and installing necessary packages...")
    packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "picom", "alacritty",
        "dunst", "neofetch", "ttf-font-awesome", "zsh", "qemu-full", "virt-manager",
        "virt-viewer", "dnsmasq", "bridge-utils", "libguestfs", "ebtables", "vde2",
        "openbsd-netcat", "mesa", "neovim", "openssh", "feh", "mc", "alsa-utils", "netbird", "python-pywal"
    ]
    subprocess.run(['sudo', 'pacman', '-S', '--needed'] + packages)

def check_paru():
    print("Checking and installing Paru...")
    if subprocess.run(['pacman', '-Q', 'paru']).returncode != 0:
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/paru.git', '/tmp/paru'])
        os.chdir("/tmp/paru")
        subprocess.run(['makepkg', '-si'])
        os.chdir("-")

def check_optional_packages():
    print("Checking and installing optional packages...")
    optional_packages = [
        "vscodium-bin", "nomachine", "udisks2", "gvfs", "vscodium-bin", "pavucontrol",
        "yazi", "ffmpegthumbnailer", "unarchiver", "jq", "poppler", "fd", "ripgrep",
        "fzf", "zoxide", "brave-bin", "python-psutil", "python-pulsectl-asyncio"
    ]
    subprocess.run(['sudo', 'paru', '-S'] + optional_packages)

def check_ssh():
    print("Checking and enabling SSH service...")
    subprocess.run(['sudo', 'pacman', '-S', '--needed', 'openssh'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'sshd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'sshd'])

def check_nomachine():
    print("Checking and enabling NoMachine service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'nxserver'])
    result = subprocess.run(['sudo', 'systemctl', 'is-active', 'nxserver'], capture_output=True)
    if result.returncode != 0:
        print("NoMachine service is not active. Starting NoMachine service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'nxserver'])
    else:
        print("NoMachine service is already active.")

def install_rofi_themes():
    print("Installing Rofi themes...")
    if not os.path.exists("/tmp/rofi"):
        subprocess.run(['git', 'clone', '--depth=1', 'https://github.com/adi1090x/rofi.git', '/tmp/rofi'])
        os.chdir("/tmp/rofi")
        subprocess.run(['chmod', '+x', 'setup.sh'])
        subprocess.run(['./setup.sh'])
        os.chdir("-")  # Switch back to the previous directory
    else:
        print("Rofi repository already exists. Skipping installation.")

def main():
    backup_config()
    check_packages()
    check_paru()
    check_optional_packages()
    check_ssh()
    check_nomachine()
    install_rofi_themes()
    create_folders()
    copy_files()

if __name__ == "__main__":
    main()
