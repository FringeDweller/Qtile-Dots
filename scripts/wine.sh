#!/bin/bash

# Install wine and its dependencies
sudo pacman -Sy wine wine-mono wine-gecko

# Install optional dependencies for wine
sudo pacman -S --asdeps --needed $(pacman -Si wine | sed -n '/^Opt/,/^Conf/p' | sed '$d' | sed 's/^Opt.*://g' | sed 's/^\s*//g' | tr '\n' ' ')
