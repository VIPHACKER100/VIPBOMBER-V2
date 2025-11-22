#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
VIPBOMBER-V2 - Advanced SMS/CALL/MAIL Testing Tool
Created By: VIPHACKER100
Version: 2.0
"""

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
import platform
from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add current directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.decorators import MessageDecorator
    from utils.provider import APIProvider
except ImportError as e:
    print(f"Error importing local modules: {e}")
    print("Please ensure all project files are present")
    sys.exit(1)

try:
    import requests
    from colorama import Fore, Style, init as colorama_init
    import urllib3
    # Disable SSL warnings for better user experience
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError as e:
    print(f"\tMissing dependency: {e}")
    print("Please install required packages using:")
    print("pip3 install -r requirements.txt")
    sys.exit(1)

# Initialize colorama for Windows compatibility
colorama_init()

# Compiled validators with improved patterns
PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')  # E.164 compliant
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$')
COUNTRY_CODE_PATTERN = re.compile(r'^[1-9]\d{0,3}$')

class Config:
    """Configuration class for VIPBOMBER-V2"""
    MAX_LIMITS = {
        "sms": 500,
        "call": 50,
        "mail": 1000
    }
    
    DELAY_RANGES = {
        "min": 0.5,
        "max": 10.0
    }
    
    THREAD_RANGES = {
        "min": 1,
        "max": 50
    }

def read_isdcodes():
    """Read ISD codes from JSON file with error handling"""
    try:
        isd_file = Path("isdcodes.json")
        if not isd_file.exists():
            raise FileNotFoundError("isdcodes.json not found")
        
        with open(isd_file, 'r', encoding='utf-8') as file:
            isdcodes = json.load(file)
        
        if "isdcodes" not in isdcodes:
            raise ValueError("Invalid isdcodes.json format")
            
        return isdcodes["isdcodes"]
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error reading ISD codes: {e}")
        print("Please ensure isdcodes.json exists and is valid")
        return {}

def get_version():
    """Get current version with fallback"""
    try:
        version_file = Path(".version")
        if version_file.exists():
            return version_file.read_text().strip()
    except Exception:
        pass
    return '2.0'

def clear_screen():
    """Clear terminal screen cross-platform"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display VIPBOMBER-V2 banner"""
    clear_screen()
    
    banner_text = f"""
{Fore.RED}
╦  ╦╦╔═╗╔═╗╔╦╗╔═╗╦ ╦╔═╗╦═╗
╚╗╔╝║║ ╦║╣  ║ ║ ║║║║╠═╣╠╦╝
 ╚╝ ╩╚═╝╚═╝ ╩ ╚═╝╚╩╝╩ ╩╩╚═
{Fore.CYAN}
╔══════════════════════════════════════╗
║         VIP BOMBER V2.0             ║
║      Created by: VIPHACKER100       ║
╚══════════════════════════════════════╝
{Fore.RESET}"""
    
    print(banner_text)
    
    # Version and contributor info
    version_info = f"{Fore.GREEN}Version: {__VERSION__}{Fore.RESET}"
    contributors = f"{Fore.YELLOW}Contributors: {', '.join(__CONTRIBUTORS__)}{Fore.RESET}"
    
    print(version_info)
    print(contributors)
    print()

def check_internet_connection():
    """Check internet connectivity with multiple fallback URLs"""
    test_urls = [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://www.github.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                return True
        except Exception:
            continue
    
    display_banner()
    mesg_decorator.FailureMessage("No internet connection detected")
    mesg_decorator.GeneralMessage("Please check your connection and try again")
    sys.exit(2)

def format_phone_number(phone_str):
    """Extract only digits from phone number"""
    return ''.join(filter(str.isdigit, phone_str))

def safe_int_input(prompt, default=None, min_val=None, max_val=None):
    """Safely get integer input with validation"""
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default
            value = int(value)
            
            if min_val is not None and value < min_val:
                mesg_decorator.WarningMessage(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                mesg_decorator.WarningMessage(f"Value must be at most {max_val}")
                continue
                
            return value
        except ValueError:
            mesg_decorator.FailureMessage("Please enter a valid number")
        except KeyboardInterrupt:
            raise

def safe_float_input(prompt, default=None, min_val=None, max_val=None):
    """Safely get float input with validation"""
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default
            value = float(value)
            
            if min_val is not None and value < min_val:
                mesg_decorator.WarningMessage(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                mesg_decorator.WarningMessage(f"Value must be at most {max_val}")
                continue
                
            return value
        except ValueError:
            mesg_decorator.FailureMessage("Please enter a valid number")
        except KeyboardInterrupt:
            raise

def update_vipbomber():
    """Update VIPBOMBER-V2 from repository"""
    mesg_decorator.SectionMessage("Updating VIPBOMBER-V2")
    
    # Try git update first
    if shutil.which('git'):
        try:
            mesg_decorator.GeneralMessage("Using git for update...")
            
            # Reset any local changes
            subprocess.run(["git", "checkout", "."], 
                         check=True, capture_output=True)
            
            # Pull latest changes
            result = subprocess.run(["git", "pull", "origin", "main"],
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                mesg_decorator.SuccessMessage("Update completed successfully!")
                mesg_decorator.GeneralMessage("Please restart VIPBOMBER-V2")
                sys.exit(0)
            else:
                mesg_decorator.FailureMessage("Git update failed")
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            mesg_decorator.FailureMessage(f"Git update error: {e}")
    
    # Fallback to manual update instructions
    mesg_decorator.WarningMessage("Automatic update failed")
    mesg_decorator.GeneralMessage("Please update manually:")
    mesg_decorator.GeneralMessage("1. Visit: https://github.com/VIPHACKER100/VIPBOMBER-V2")
    mesg_decorator.GeneralMessage("2. Download the latest release")
    mesg_decorator.GeneralMessage("3. Replace existing files")
    sys.exit(1)

def check_for_updates():
    """Check for available updates"""
    if DEBUG_MODE:
        mesg_decorator.WarningMessage("DEBUG MODE: Update check disabled")
        return
    
    mesg_decorator.SectionMessage("Checking for updates")
    
    try:
        # Use raw GitHub URL for version check
        version_url = "https://raw.githubusercontent.com/VIPHACKER100/VIPBOMBER-V2/main/.version"
        response = requests.get(version_url, timeout=10, verify=False)
        
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version != __VERSION__:
                mesg_decorator.WarningMessage(f"Update available: v{latest_version}")
                mesg_decorator.GeneralMessage("Current version: v" + __VERSION__)
                
                update_choice = input(mesg_decorator.CommandMessage(
                    "Would you like to update now? (y/N): ")).lower().strip()
                
                if update_choice in ['y', 'yes']:
                    update_vipbomber()
            else:
                mesg_decorator.SuccessMessage("VIPBOMBER-V2 is up to date")
        else:
            mesg_decorator.WarningMessage("Could not check for updates")
            
    except Exception as e:
        mesg_decorator.WarningMessage(f"Update check failed: {e}")

def show_notification():
    """Display notifications if available"""
    try:
        notify_url = "https://raw.githubusercontent.com/VIPHACKER100/VIPBOMBER-V2/main/.notify"
        response = requests.get(notify_url, timeout=5, verify=False)
        
        if response.status_code == 200:
            notification = response.text.strip()
            if notification and len(notification) > 5:
                mesg_decorator.SectionMessage(f"NOTICE: {notification}")
                print()
    except Exception:
        pass  # Silent fail for notifications

def get_phone_info():
    """Get validated phone number information"""
    while True:
        try:
            # Country code input
            cc = input(mesg_decorator.CommandMessage(
                "Enter country code (without +): ")).strip()
            
            cc = format_phone_number(cc)
            
            if not cc or not COUNTRY_CODE_PATTERN.match(cc):
                mesg_decorator.WarningMessage("Invalid country code format")
                continue
                
            if cc not in country_codes:
                mesg_decorator.WarningMessage(f"Country code +{cc} not supported")
                continue
            
            # Phone number input
            target = input(mesg_decorator.CommandMessage(
                f"Enter phone number (without +{cc}): ")).strip()
            
            target = format_phone_number(target)
            
            if len(target) < 4 or len(target) > 12:
                mesg_decorator.WarningMessage("Phone number length invalid (4-12 digits)")
                continue
            
            # Full E.164 validation
            full_number = f"+{cc}{target}"
            if not PHONE_PATTERN.match(full_number):
                mesg_decorator.WarningMessage("Invalid phone number format")
                continue
                
            return cc, target
            
        except KeyboardInterrupt:
            mesg_decorator.WarningMessage("Input cancelled")
            raise

def get_email_info():
    """Get validated email address"""
    while True:
        try:
            target = input(mesg_decorator.CommandMessage(
                "Enter target email: ")).strip().lower()
            
            if not EMAIL_PATTERN.match(target):
                mesg_decorator.WarningMessage("Invalid email address format")
                continue
                
            # Basic email validation
            if target.count('@') != 1:
                mesg_decorator.WarningMessage("Email must contain exactly one @")
                continue
                
            return target
            
        except KeyboardInterrupt:
            mesg_decorator.WarningMessage("Input cancelled")
            raise

def display_bombing_progress(cc, target, success, failed, total):
    """Display real-time bombing progress"""
    clear_screen()
    display_banner()
    
    mesg_decorator.SectionMessage("Bombing in Progress")
    mesg_decorator.GeneralMessage("Target       : +" + cc + " " + target if cc else target)
    mesg_decorator.GeneralMessage("Successful   : " + str(success))
    mesg_decorator.GeneralMessage("Failed       : " + str(failed))
    mesg_decorator.GeneralMessage("Remaining    : " + str(total - success - failed))
    mesg_decorator.GeneralMessage("Progress     : {:.1f}%".format(
        (success + failed) / total * 100))
    
    mesg_decorator.WarningMessage("For educational and testing purposes only!")
    print()

def bombing_worker(mode, cc, target, count, delay, max_threads):
    """Main bombing worker function"""
    api = APIProvider(cc, target, mode, delay=delay)
    
    clear_screen()
    display_banner()
    
    mesg_decorator.SectionMessage("Initializing VIPBOMBER-V2")
    mesg_decorator.GeneralMessage("Mode          : " + mode.upper())
    if cc:
        mesg_decorator.GeneralMessage("Target        : +" + cc + " " + target)
    else:
        mesg_decorator.GeneralMessage("Target        : " + target)
    mesg_decorator.GeneralMessage("Total         : " + str(count))
    mesg_decorator.GeneralMessage("Threads       : " + str(max_threads))
    mesg_decorator.GeneralMessage("Delay         : " + str(delay) + "s")
    mesg_decorator.GeneralMessage("API Version   : " + api.api_version)
    
    mesg_decorator.WarningMessage("USE RESPONSIBLY - FOR AUTHORIZED TESTING ONLY")
    print()
    
    # Check if any providers are available
    if len(APIProvider.api_providers) == 0:
        mesg_decorator.FailureMessage("No API providers available for this target")
        mesg_decorator.GeneralMessage("Country/target may not be supported")
        input(mesg_decorator.CommandMessage("Press ENTER to exit"))
        sys.exit(1)
    
    input(mesg_decorator.CommandMessage("Press ENTER to start bombing..."))
    
    success, failed = 0, 0
    total_attempts = 0
    
    try:
        while success < count and total_attempts < count * 2:  # Safety limit
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                # Submit jobs
                jobs = []
                for _ in range(min(count - success, max_threads * 2)):
                    jobs.append(executor.submit(api.hit))
                
                # Process results
                for job in as_completed(jobs):
                    result = job.result()
                    total_attempts += 1
                    
                    if result is None:
                        mesg_decorator.FailureMessage("Rate limit reached for target")
                        break
                    
                    if result:
                        success += 1
                    else:
                        failed += 1
                    
                    # Update progress display
                    display_bombing_progress(cc, target, success, failed, count)
                    
                    # Early completion check
                    if success >= count:
                        break
            
            # Small delay between batches
            if success < count:
                time.sleep(0.5)
                
    except KeyboardInterrupt:
        mesg_decorator.WarningMessage("Bombing interrupted by user")
    
    # Final results
    print("\n" + "="*50)
    mesg_decorator.SuccessMessage(f"Bombing completed!")
    mesg_decorator.GeneralMessage(f"Successful: {success}")
    mesg_decorator.GeneralMessage(f"Failed: {failed}")
    mesg_decorator.GeneralMessage(f"Success Rate: {success/(success+failed)*100:.1f}%")
    
    input(mesg_decorator.CommandMessage("Press ENTER to continue..."))

def start_bombing_mode(mode="sms"):
    """Main bombing mode controller"""
    mode = mode.lower().strip()
    
    try:
        clear_screen()
        display_banner()
        
        # System checks
        check_internet_connection()
        check_for_updates()
        show_notification()
        
        # Get target information
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
        elif mode == "mail":
            target = get_email_info()
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        
        # Get bombing parameters with validation
        limit = Config.MAX_LIMITS.get(mode, 100)
        
        mesg_decorator.SectionMessage("Configure Bombing Parameters")
        
        count = safe_int_input(
            mesg_decorator.CommandMessage(f"Number of {mode.upper()} to send (1-{limit}): "),
            min_val=1, max_val=limit
        )
        
        delay = safe_float_input(
            mesg_decorator.CommandMessage(f"Delay between requests ({Config.DELAY_RANGES['min']}-{Config.DELAY_RANGES['max']}s): "),
            min_val=Config.DELAY_RANGES['min'], max_val=Config.DELAY_RANGES['max']
        )
        
        max_threads = safe_int_input(
            mesg_decorator.CommandMessage(f"Number of threads (1-{Config.THREAD_RANGES['max']}): "),
            min_val=1, max_val=Config.THREAD_RANGES['max']
        )
        
        # Start bombing
        bombing_worker(mode, cc, target, count, delay, max_threads)
        
    except KeyboardInterrupt:
        mesg_decorator.WarningMessage("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        mesg_decorator.FailureMessage(f"Error: {e}")
        sys.exit(1)

def show_interactive_menu():
    """Show interactive mode menu"""
    menu_options = {
        "1": {"name": "SMS Bomb", "mode": "sms"},
        "2": {"name": "Call Bomb", "mode": "call"},
        "3": {"name": "Mail Bomb", "mode": "mail"},
        "4": {"name": "Check Updates", "action": "update"},
        "5": {"name": "Exit", "action": "exit"}
    }
    
    while True:
        clear_screen()
        display_banner()
        
        mesg_decorator.SectionMessage("Main Menu")
        for key, option in menu_options.items():
            print(f"  {Fore.CYAN}[{key}]{Fore.RESET} {option['name']}")
        print()
        
        try:
            choice = input(mesg_decorator.CommandMessage("Select option: ")).strip()
            
            if choice in menu_options:
                option = menu_options[choice]
                
                if "action" in option:
                    if option["action"] == "update":
                        update_vipbomber()
                    elif option["action"] == "exit":
                        mesg_decorator.SuccessMessage("Thank you for using VIPBOMBER-V2!")
                        sys.exit(0)
                else:
                    start_bombing_mode(option["mode"])
            else:
                mesg_decorator.FailureMessage("Invalid option selected")
                time.sleep(1)
                
        except KeyboardInterrupt:
            mesg_decorator.WarningMessage("Received interrupt - Exiting...")
            sys.exit(0)

# Global initialization
if __name__ == "__main__":
    # Initialize message decorator
    mesg_decorator = MessageDecorator("icon")
    
    # Python version check
    if sys.version_info < (3, 6):
        mesg_decorator.FailureMessage("VIPBOMBER-V2 requires Python 3.6 or higher")
        sys.exit(1)
    
    # Load country codes
    country_codes = read_isdcodes()
    if not country_codes:
        mesg_decorator.WarningMessage("Could not load country codes")
        mesg_decorator.GeneralMessage("Some features may not work correctly")
    
    # Set global variables
    __VERSION__ = get_version()
    __CONTRIBUTORS__ = ['VIPHACKER100', 'SpeedX', 't0xic0der', 'scpketer']
    
    DEBUG_MODE = False
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="VIPBOMBER-V2 - Advanced Testing Tool",
        epilog="Created by VIPHACKER100 - Use responsibly!"
    )
    
    parser.add_argument("-sms", "--sms", action="store_true",
                       help="Start SMS bombing mode")
    parser.add_argument("-call", "--call", action="store_true",
                       help="Start CALL bombing mode")
    parser.add_argument("-mail", "--mail", action="store_true",
                       help="Start MAIL bombing mode")
    parser.add_argument("-ascii", "--ascii", action="store_true",
                       help="Use ASCII-only output")
    parser.add_argument("-u", "--update", action="store_true",
                       help="Update VIPBOMBER-V2 to latest version")
    parser.add_argument("-v", "--version", action="store_true",
                       help="Show version information")
    parser.add_argument("-c", "--contributors", action="store_true",
                       help="Show contributors list")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Handle arguments
    if args.debug:
        DEBUG_MODE = True
        mesg_decorator.WarningMessage("DEBUG MODE ENABLED")
    
    if args.ascii:
        mesg_decorator = MessageDecorator("stat")
    
    if args.version:
        print(f"VIPBOMBER-V2 Version: {__VERSION__}")
        sys.exit(0)
        
    elif args.contributors:
        print("Contributors:", ", ".join(__CONTRIBUTORS__))
        sys.exit(0)
        
    elif args.update:
        update_vipbomber()
        
    elif args.mail:
        start_bombing_mode("mail")
    elif args.call:
        start_bombing_mode("call")
    elif args.sms:
        start_bombing_mode("sms")
    else:
        # Interactive mode
        show_interactive_menu()