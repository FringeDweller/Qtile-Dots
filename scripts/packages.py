import subprocess
import os
import shutil

def check_ssh():
    print("Checking if OpenSSH is installed...")
    installed = subprocess.run(['sudo', 'pacman', '-Q', 'openssh'], capture_output=True)
    if installed.returncode != 0:
        print("OpenSSH is not installed. Installing and enabling...")
        subprocess.run(['sudo', 'pacman', '-Sy', 'openssh'])
        subprocess.run(['sudo', 'systemctl', 'enable', 'ssh'])
        subprocess.run(['sudo', 'systemctl', 'start', 'ssh'])
    else:
        print("OpenSSH is already installed.")

def check_packages():
    print("Checking required packages...")
    required_packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "thunar", "picom", 
        "rofi", "alacritty", "dunst", "neofetch", "ttf-font-awesome", 
        "zsh", "qemu-full", "virt-manager", "virt-viewer", "dnsmasq", 
        "bridge-utils", "libguestfs", "ebtables", "vde2", "openbsd-netcat", 
        "mesa", "neovim", "geany", "geany-plugins"
    ]
    for package in required_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-Sy', package])
        else:
            print(f"{package} is already installed.")

def check_yay():
    print("Checking if Yay is installed...")
    installed = subprocess.run(['sudo', 'pacman', '-Q', 'yay'], capture_output=True)
    if installed.returncode != 0:
        print("Yay is not installed. Installing using git...")
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/yay.git'])
        os.chdir('yay')  # Change the working directory to 'yay'
        subprocess.run(['makepkg', '-si'])
        os.chdir('..')  # Change back to the parent directory
        shutil.rmtree('yay')  # Remove the yay folder
    else:
        print("Yay is already installed.")

def clone_dots():
    print("Cloning FringeDweller/dots repository to /home...")
    if not os.path.exists('/home/dots'):
        subprocess.run(['git', 'clone', 'https://github.com/FringeDweller/dots.git', '/home/dots'])
    else:
        print("dots repository already exists in /home.")

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

def set_default_shell():
    print("Setting zsh as default shell...")
    subprocess.run(['sudo', 'chsh', '-s', '/bin/zsh'])

def check_optional_packages():
    print("Checking optional packages...")
    optional_packages = ["xrdp", "xorgxrdp", "octopi", "microsoft-edge-stable-bin"]
    for package in optional_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing using Yay...")
            subprocess.run(['yay', package])
        else:
            print(f"{package} is already installed.")

def main():
    print("Starting system configuration...")
    check_ssh()
    check_packages()
    check_yay()
    clone_dots()
    create_symlinks()
    set_default_shell()
    check_optional_packages()
    print("System configuration completed.")

if __name__ == "__main__":
    main()
