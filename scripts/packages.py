def check_packages():
    print("Checking and installing required packages with pacman...")
    required_packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "thunar", "picom", 
        "rofi", "alacritty", "dunst", "neofetch", "ttf-font-awesome", 
        "zsh", "qemu-full", "virt-manager", "virt-viewer", "dnsmasq", 
        "bridge-utils", "libguestfs", "ebtables", "vde2", "openbsd-netcat", 
        "mesa", "neovim", "geany", "geany-plugins", "openssh", 
        "udisks2", "gvfs"
    ]
    for package in required_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-S', '--needed', package])

def check_udisks2():
    print("Checking and enabling udisks2 service...")
    subprocess.run(['sudo', 'systemctl', 'enable', 'udisks2'])
    result = subprocess.run(['sudo', 'systemctl', 'is-active', 'udisks2'], capture_output=True)
    if result.returncode != 0:
        print("udisks2 is not active. Starting udisks2 service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'udisks2'])
    else:
        print("udisks2 is already active.")

def main():
    print("Starting system configuration...")
    check_packages()
    check_udisks2()
    check_yay()
    check_optional_packages()
    check_ssh()
    check_nomachine()
    set_default_shell(os.getlogin(), '/bin/zsh')
    set_default_shell('root', '/bin/zsh')
    create_symlinks()
    print("System configuration completed.")

if __name__ == "__main__":
    main()

