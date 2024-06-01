#!/bin/sh

GREEN='\033[0;32m'
RED='\033[1;31m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
    echo ""
    echo -e "${RED}[-] Please run as root${NC}"
    echo ""
    exit 1
else
    echo -e "${GREEN}[+] Installing Dependencies for Hunter Pentesting Framework${NC}"
    echo ""
    pip3 install sockets scapy pyautogui termcolor >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}[-] Failed to install dependencies.${NC}"
        echo ""
        exit 1
    fi
    echo ""
    cp hunter /usr/bin/hunter
    chmod +x /usr/bin/hunter
    mkdir -p /usr/bin/scripts
    cp -r ./scripts/* /usr/bin/scripts/
    echo -e "${GREEN}[+] Hunter Successfully Installed. Type 'sudo hunter' in your terminal to check.${NC}"
fi
