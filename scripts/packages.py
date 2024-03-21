import subprocess
import os
import shutil
import pwd

def check_packages():
    print("Checking and installing required packages with pacman...")
    required_packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "thunar", "picom", 
        "rofi", "alacritty", "dunst", "neofetch", "ttf-font-awesome", 
        "zsh", "qemu-full", "virt-manager", "virt-viewer", "dnsmasq", 
        "bridge-utils", "libguestfs", "ebtables", "vde2", "openbsd-netcat", 
        "mesa", "neovim", "geany", "geany-plugins", "openssh"
    ]
    for package in required_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-Sy', '--noconfirm', package])

def check_yay():
    print("Checking and installing Yay...")
    installed = subprocess.run(['sudo', 'pacman', '-Q', 'yay'], capture_output=True)
    if installed.returncode != 0:
        print("Yay is not installed. Installing using git...")
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/yay.git'])
        os.chdir('yay')  # Change the working directory to 'yay'
        subprocess.run(['makepkg', '-si', '--noconfirm'])
        os.chdir('..')  # Change back to the parent directory
        shutil.rmtree('yay')  # Remove the yay folder
    else:
        print("Yay is already installed.")

def check_optional_packages():
    print("Checking and installing optional packages with Yay...")
    optional_packages = ["xrdp", "xorgxrdp", "octopi", "microsoft-edge-stable-bin", "code-git"]
    for package in optional_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing using Yay...")
            subprocess.run(['yay', '-Sy', '--noconfirm', package])

def check_ssh():
    print("Checking and enabling SSH service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'sshd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'sshd'])

def check_xrdp():
    print("Checking and enabling XRDP service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'xrdp'])
    subprocess.run(['sudo', 'systemctl', 'start', 'xrdp'])

def set_zsh_default_shell():
    print("Setting Zsh as the default shell...")
    subprocess.run(['chsh', '-s', '/bin/zsh', pwd.getpwuid(os.getuid()).pw_name])

def create_symlinks():
    print("Creating symbolic links between /home/dots directories and ~/.config...")
    dots_path = '/home/dots'
    config_path = os.path.expanduser('~/.config')
    for root, dirs, files in os.walk(dots_path):
        for directory in dirs:
            source_dir = os.path.join(root, directory)
            target_dir = os.path.join(config_path, directory)
            if not os.path.exists(target_dir):
                os.symlink(source_dir, target_dir)
                print(f"Created symlink: {source_dir} -> {target_dir}")
            else:
                print(f"Symlink already exists: {source_dir} -> {target_dir}")

def main():
    print("Starting system configuration...")
    check_packages()
    check_yay()
    check_optional_packages()
    check_ssh()
    check_xrdp()
    set_zsh_default_shell()
    create_symlinks()
    print("System configuration completed.")

if __name__ == "__main__":
    main()
