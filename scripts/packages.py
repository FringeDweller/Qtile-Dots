import subprocess
import os
import shutil

def check_packages():
    print("Checking and installing required packages with pacman...")
    required_packages = [
        "git", "xorg", "xorg-xinit", "nitrogen", "thunar", "picom", 
        "rofi", "alacritty", "dunst", "neofetch", "ttf-font-awesome", 
        "zsh", "qemu-full", "virt-manager", "virt-viewer", "dnsmasq", 
        "bridge-utils", "libguestfs", "ebtables", "vde2", "openbsd-netcat", 
        "mesa", "neovim", "geany", "geany-plugins", "openssh",
        "udisks2", "gvfs", "pavucontrol", "qtile-extras"
    ]
    for package in required_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Qs', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-S', '--needed', package])

def check_yay():
    print("Checking and installing Yay...")
    installed = subprocess.run(['sudo', 'pacman', '-Qs', 'yay'], capture_output=True)
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
    print("Checking and installing optional packages with Yay...")
    optional_packages = ["octopi", "brave-bin", "nomachine"]
    for package in optional_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Qs', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing using Yay...")
            subprocess.run(['yay', '-S', package])

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

def set_default_shell(user, shell):
    print(f"Setting {shell} as the default shell for {user}...")
    subprocess.run(['sudo', 'chsh', '-s', shell, user])

def create_symlinks():
    print("Creating symbolic links for the dots folders...")
    dots_path = os.path.expanduser('~/dots')
    config_path = os.path.expanduser('~/.config')

    if not os.path.exists(config_path):
        print(f"Target directory {config_path} does not exist. Aborting symlink creation.")
        return

    for folder_name in os.listdir(dots_path):
        source_dir = os.path.join(dots_path, folder_name)
        target_dir = os.path.join(config_path, folder_name)

        if os.path.isdir(source_dir):
            if not os.path.exists(target_dir):
                try:
                    os.symlink(source_dir, target_dir)
                    print(f"Created symlink: {source_dir} -> {target_dir}")
                except Exception as e:
                    print(f"Error creating symlink: {e}")
            else:
                print(f"Symlink already exists: {source_dir} -> {target_dir}")

def main():
    print("Starting system configuration...")
    check_packages()
    check_yay()
    check_optional_packages()
    check_ssh()
    check_nomachine()
    check_udisks2()
    set_default_shell(os.getlogin(), '/bin/zsh')
    set_default_shell('root', '/bin/zsh')
    create_symlinks()
    print("System configuration completed.")

if __name__ == "__main__":
    main()
