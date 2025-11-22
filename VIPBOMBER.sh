#!/bin/bash

# Colors for output
RED='\e[1;31m'
GREEN='\e[1;32m'
YELLOW='\e[1;33m'
BLUE='\e[1;34m'
CYAN='\e[1;36m'
WHITE='\e[1;37m'
RESET='\e[0m'

# Global variables
DISTRO=""
PYTHON="python3"
PIP="pip3"
SUDO="sudo"
INSTALL=""

# Error handling
set -euo pipefail
trap 'echo -e "${RED}An error occurred at line $LINENO${RESET}"; exit 1' ERR

detect_distro() {
    local distro_detected=""
    
    # Check for Termux first
    if [[ "$OSTYPE" == linux-android* ]] || [[ $(uname -o) == "Android" ]]; then
        distro_detected="termux"
        echo -e "${GREEN}Detected environment: Termux${RESET}"
    elif [[ "$OSTYPE" == "darwin"* ]] || [[ $(uname) == "Darwin" ]]; then
        distro_detected="darwin"
        echo -e "${GREEN}Detected environment: macOS${RESET}"
    elif [ -f "/etc/os-release" ]; then
        distro_detected=$(source /etc/os-release && echo $ID)
        echo -e "${GREEN}Detected distribution: $distro_detected${RESET}"
    else
        # Try to detect from /etc files
        distro_detected=$(ls /etc/ | grep -E '(release|version)' | head -1 | sed 's/[-_].*//' | tr '[:upper:]' '[:lower:]')
        
        if [ -z "$distro_detected" ]; then
            distro_detected="unknown"
            echo -e "${YELLOW}Could not detect distribution${RESET}"
        fi
    fi

    DISTRO="$distro_detected"
}

setup_environment() {
    declare -A backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get update && apt-get -y install"
        ["ubuntu"]="apt update && apt -y install"
        ["kali"]="apt update && apt -y install"
        ["termux"]="pkg update && pkg install -y"
        ["fedora"]="dnf -y install"
        ["centos"]="yum -y install"
        ["redhat"]="yum -y install"
        ["opensuse"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["alpine"]="apk update && apk add"
        ["darwin"]="brew install"
    )

    # Set package manager
    if [ -n "${backends[$DISTRO]:-}" ]; then
        INSTALL="${backends[$DISTRO]}"
    else
        echo -e "${YELLOW}Unsupported distribution: $DISTRO${RESET}"
        echo -e "${YELLOW}Please install dependencies manually${RESET}"
        INSTALL=""
    fi

    # Platform-specific adjustments
    if [ "$DISTRO" == "termux" ]; then
        PYTHON="python"
        PIP="pip"
        SUDO=""
    elif [ "$DISTRO" == "darwin" ]; then
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Homebrew is required on macOS. Please install it from https://brew.sh/${RESET}"
            exit 1
        fi
    fi
}

check_dependencies() {
    local missing_deps=()
    local basic_deps=("git" "$PYTHON")
    
    echo -e "${CYAN}Checking dependencies...${RESET}"
    
    for dep in "${basic_deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done

    # Check Python modules
    if ! $PYTHON -c "import requests" &> /dev/null; then
        missing_deps+=("python-requests")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${YELLOW}Missing dependencies: ${missing_deps[*]}${RESET}"
        return 1
    fi
    
    echo -e "${GREEN}All basic dependencies are satisfied${RESET}"
    return 0
}

install_dependencies() {
    echo -e "${CYAN}Installing dependencies for $DISTRO...${RESET}"
    
    local packages=()
    
    case $DISTRO in
        arch)
            packages=("git" "python" "python-pip" "figlet" "toilet")
            ;;
        debian|ubuntu|kali|termux)
            if [ "$DISTRO" == "termux" ]; then
                packages=("git" "python" "figlet" "toilet")
            else
                packages=("git" "python3" "python3-pip" "figlet" "toilet")
            fi
            ;;
        fedora|centos|redhat)
            packages=("git" "python3" "python3-pip" "figlet" "toilet")
            ;;
        darwin)
            packages=("git" "python3" "figlet" "toilet")
            ;;
        *)
            echo -e "${RED}Automatic dependency installation not supported for $DISTRO${RESET}"
            echo -e "${YELLOW}Please install git, python3, pip3, figlet, and toilet manually${RESET}"
            return 1
            ;;
    esac

    if [ -n "$INSTALL" ]; then
        echo -e "${BLUE}Running: $SUDO $INSTALL ${packages[*]}${RESET}"
        if [ "$DISTRO" == "termux" ]; then
            eval "$INSTALL ${packages[*]}"
        else
            eval "$SUDO $INSTALL ${packages[*]}"
        fi
        
        # Install Python requirements
        echo -e "${CYAN}Installing Python packages...${RESET}"
        if [ -f "requirements.txt" ]; then
            $PIP install -r requirements.txt
        else
            $PIP install requests colorama
        fi
    else
        return 1
    fi
}

show_banner() {
    clear
    echo -e "${RED}"
    if command -v figlet &> /dev/null; then
        figlet -f standard "VIPBOMBER-V2"
    else
        echo "╔══════════════════════════╗"
        echo "║      VIPBOMBER-V2       ║"
        echo "╚══════════════════════════╝"
    fi
    
    echo -e "${CYAN}"
    if command -v toilet &> /dev/null; then
        toilet -f term --gay "By VIPHACKER100"
    else
        echo "┌──────────────────────────┐"
        echo "│   Created By: VIPHACKER100 │"
        echo "└──────────────────────────┘"
    fi
    echo -e "${RESET}"
    
    echo -e "${GREEN}Telegram: https://t.me/TBombChat${RESET}"
    echo -e "${BLUE}YouTube: https://www.youtube.com/@VIPHACKER100${RESET}"
    echo -e "${YELLOW}GitHub: https://github.com/VIPHACKER100${RESET}"
    echo
    echo -e "${CYAN}╔════════════════════════════════════════╗${RESET}"
    echo -e "${CYAN}║           LEGAL DISCLAIMER            ║${RESET}"
    echo -e "${CYAN}║  Use responsibly and at your own risk ║${RESET}"
    echo -e "${CYAN}║   Only test on your own systems       ║${RESET}"
    echo -e "${CYAN}╚════════════════════════════════════════╝${RESET}"
    echo
}

pause() {
    echo -e "${YELLOW}Press any key to continue...${RESET}"
    read -n1 -r -s key
}

show_menu() {
    while true; do
        show_banner
        echo -e "${WHITE}╔════════════════════════════════════════╗${RESET}"
        echo -e "${WHITE}║             MAIN MENU                  ║${RESET}"
        echo -e "${WHITE}╠════════════════════════════════════════╣${RESET}"
        echo -e "${WHITE}║  1. Start SMS Bomber                   ║${RESET}"
        echo -e "${WHITE}║  2. Start CALL Bomber                  ║${RESET}"
        echo -e "${WHITE}║  3. Start MAIL Bomber                  ║${RESET}"
        echo -e "${WHITE}║  4. Check for Updates                  ║${RESET}"
        echo -e "${WHITE}║  5. Dependency Check                   ║${RESET}"
        echo -e "${WHITE}║  6. Exit                              ║${RESET}"
        echo -e "${WHITE}╚════════════════════════════════════════╝${RESET}"
        echo
        echo -e "${CYAN}Select an option (1-6): ${RESET}"
        read -r choice

        case $choice in
            1)
                echo -e "${GREEN}Starting SMS Bomber...${RESET}"
                $PYTHON bomber.py --sms
                pause
                ;;
            2)
                echo -e "${GREEN}Starting CALL Bomber...${RESET}"
                $PYTHON bomber.py --call
                pause
                ;;
            3)
                echo -e "${GREEN}Starting MAIL Bomber...${RESET}"
                $PYTHON bomber.py --mail
                pause
                ;;
            4)
                echo -e "${CYAN}Checking for updates...${RESET}"
                if git rev-parse --is-inside-work-tree &> /dev/null; then
                    git pull
                    echo -e "${GREEN}Updated successfully!${RESET}"
                else
                    echo -e "${YELLOW}Not a git repository. Manual update required.${RESET}"
                fi
                pause
                ;;
            5)
                echo -e "${CYAN}Running dependency check...${RESET}"
                if ! check_dependencies; then
                    echo -e "${YELLOW}Would you like to install missing dependencies? (y/N): ${RESET}"
                    read -r answer
                    if [[ "$answer" =~ ^[Yy]$ ]]; then
                        install_dependencies
                    fi
                fi
                pause
                ;;
            6)
                echo -e "${GREEN}Thank you for using VIPBOMBER-V2!${RESET}"
                echo -e "${BLUE}Stay ethical!${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option! Please select 1-6.${RESET}"
                pause
                ;;
        esac
    done
}

# Main execution flow
main() {
    show_banner
    echo -e "${CYAN}Initializing VIPBOMBER-V2...${RESET}"
    
    # Detect distribution
    detect_distro
    
    # Setup environment
    setup_environment
    
    # Check and install dependencies if needed
    if ! check_dependencies; then
        echo -e "${YELLOW}Some dependencies are missing.${RESET}"
        echo -e "${CYAN}Attempting to install dependencies...${RESET}"
        if ! install_dependencies; then
            echo -e "${RED}Failed to install dependencies automatically.${RESET}"
            echo -e "${YELLOW}Please install them manually and run again.${RESET}"
            exit 1
        fi
    fi

    # Create update flag file if it doesn't exist
    if [ ! -f .update ]; then
        echo "VIPBOMBER-V2 initialized $(date)" > .update
    fi

    pause
    show_menu
}

# Run main function
main "$@"