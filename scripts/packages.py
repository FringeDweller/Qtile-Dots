import subprocess

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
        "mesa", "neovim"
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
        
def check_optional_packages():
    print("Checking optional packages...")
    optional_packages = ["xrdp", "xorgxrdp", "octopi", "microsoft-edge-stable-bin", "visual-studio-code-bin"]
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
    check_optional_packages()
    print("System configuration completed.")

if __name__ == "__main__":
    main()
