


<h1 align="center">
  <br>
  <a href="https://github.com/VIPHACKER100/VIPBOMBER-V2"><img src="https://i.ibb.co/F4HBKqm/TBomb.png" alt="VIPBOMBER-V2"></a>
  <br>
  VIPBOMBER-V2
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.6%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-orange" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

<p align="center">A free and open-source SMS/Call/Email bombing application for educational and testing purposes</p>

## 🚀 What's New in VIPBOMBER-V2 3.0.0

### Major Enhancements
- **300+ API Endpoints**: Expanded support with over 300 integrated messaging and calling APIs
- **Global Coverage**: Support for multiple countries including India, US, Russia, China, UK, and more
- **Multiple Channels**: SMS, Call, Email, WhatsApp, and Telegram bombing capabilities
- **Enhanced Security**: Improved input validation and secure API handling
- **Better Performance**: Optimized threading and request management

### Technical Improvements
- **Secure Updater**: Removed use of shell=true in git update with timeout protections
- **Strict Input Validation**: E.164 phone number validation and robust email regex
- **Advanced Configuration**: JSON-based API management for easy extensibility
- **Cross-Platform Support**: Improved compatibility across all platforms
- **Modular Architecture**: Clean, maintainable codebase for community contributions

## ⚠️ IMPORTANT NOTES

> **Due to the overuse of script, some APIs may be offline. It's normal if you don't receive all messages.**

> **Termux version from Play Store is not supported. Please use the latest version from F-Droid or [download here](https://apkadmin.com/g6cz9o0r4mll/Termux_0.118.0.apk.html).**

### Critical Information
- The application requires active internet connection to contact APIs
- You will not be charged for any SMS/calls dispatched through this script
- For best performance, use single thread with appropriate delay time
- Always ensure you're using the latest version with Python 3.6+
- This application is for educational and authorized testing ONLY
- Contributors cannot be held responsible for any misuse

## 🔧 Compatibility

Check your Python version:
```shell
python --version
```
Required: **Python 3.6 or higher**

## ✨ Features

- **300+ Integrated APIs** across multiple services and countries
- **Unlimited Bombing** with intelligent abuse protection
- **Multi-threading Support** for high-performance operations
- **International API Support** with global coverage
- **JSON-based Configuration** for easy API management
- **Auto-update System** with notification features
- **Modular Codebase** easily embeddable in other projects
- **Cross-Platform** compatibility
- **Real-time Progress Tracking** with detailed statistics
- **Multiple Bombing Modes**: SMS, Call, Email, WhatsApp, Telegram

## 📦 Installation Methods

### Method 1: PIP Installation (Recommended)

```shell
pip3 install tbomb
tbomb
```

### Method 2: Direct Git Installation

#### For Termux
```shell
apt update && apt upgrade
pkg install git python python3 figlet toilet -y
git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git
cd VIPBOMBER-V2
bash VIPBOMBER.sh
```

#### Quick Termux Install (One Command)
```shell
apt update && apt upgrade && pkg install git -y && pkg install figlet && pkg install toilet && pkg install python -y && pkg install python2 -y && pkg install python3 -y && git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git && cd VIPBOMBER-V2 && bash VIPBOMBER.sh
```

#### For Linux (Debian/Ubuntu)
```shell
sudo apt update
sudo apt install git python3 python3-pip figlet toilet -y
git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git
cd VIPBOMBER-V2
bash VIPBOMBER.sh
```

#### For macOS
```shell
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install git python3 figlet toilet
git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git
cd VIPBOMBER-V2
pip3 install -r requirements.txt
python3 bomber.py
```

#### For Windows
```shell
# Using WSL (Recommended)
wsl --install
# Then follow Linux instructions

# OR Using Python directly
python -m pip install requests colorama
git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git
cd VIPBOMBER-V2
python bomber.py
```

#### For iSH (iOS)
```shell
apk update
apk add git python3 py3-pip ruby figlet toilet
gem install toilet
git clone https://github.com/VIPHACKER100/VIPBOMBER-V2.git
cd VIPBOMBER-V2
pip3 install -r requirements.txt
python3 bomber.py
```

## 🎯 Usage Guide

### Starting the Application
After installation, run:
```shell
tbomb
```
or
```shell
python3 bomber.py
```

### Available Options
- **SMS Bomb**: Send multiple SMS messages
- **Call Bomb**: Make multiple phone calls
- **Mail Bomb**: Send multiple emails
- **Update**: Check for and install updates
- **Dependency Check**: Verify and install required packages

### Configuration Tips
- **Threads**: Start with 1-5 threads for stability
- **Delay**: Use 1-5 seconds between requests to avoid detection
- **Target Validation**: Always verify target numbers/emails before starting
- **Legal Use**: Only test on your own systems with proper authorization

## 🛡️ Safety & Legal Disclaimer

### ⚠️ CRITICAL WARNING
This tool is designed **STRICTLY** for:
- Educational purposes
- Security research
- Authorized penetration testing
- System hardening exercises

### 🚫 PROHIBITED USES
- Harassment or spamming others
- Illegal activities
- Unauthorized testing
- Malicious attacks

### 🔒 Protection Measures
- Use OTP blockers and DND services
- Implement rate limiting on your services
- Monitor for unusual activity
- Keep systems updated

## 🌍 Supported Services

### SMS Services (300+ APIs)
- **Social Media**: Facebook, Instagram, Twitter, WhatsApp, Telegram
- **E-commerce**: Amazon, Flipkart, Myntra, Ajio, Daraz
- **Food Delivery**: Swiggy, Zomato, Uber Eats
- **Travel**: Ola, Uber, Rapido, MakeMyTrip
- **Finance**: Paytm, PhonePe, Banking APIs
- **Utilities**: Airtel, Jio, Vodafone services

### Call Services
- Multiple call bombing APIs
- International call support
- Voice OTP services

### Email Services
- **Email Providers**: Gmail, Outlook, Yahoo, ProtonMail
- **Social Media**: Facebook, Twitter, Instagram, LinkedIn
- **Cloud Services**: AWS, Azure, Google Cloud, DigitalOcean
- **Development**: GitHub, GitLab, Docker, Kubernetes

## 🔄 Update Information

### Automatic Updates
The application includes an auto-update feature that:
- Checks for new versions automatically
- Downloads and installs updates securely
- Maintains your configuration settings
- Verifies update integrity

### Manual Update
```shell
cd VIPBOMBER-V2
git pull
pip3 install -r requirements.txt --upgrade
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**Q:** "Poor Internet Connection Detected"
**A:** 
- Check your internet connection
- Verify `openssl` is installed
- Try pinging remote servers
- Reinstall if issues persist

**Q:** "Requirements not installed" error
**A:**
```shell
pip3 install -r requirements.txt
# OR
pip3 install tbomb --upgrade
```

**Q:** "Command 'tbomb' not found"
**A:**
```shell
sudo pip3 install tbomb
# OR
python3 -m tbomb
```

**Q:** High failure rate
**A:**
- Reduce thread count
- Increase delay between requests
- Some APIs may be temporarily offline
- Try different bombing modes

**Q:** Permission denied errors
**A:**
```shell
chmod +x VIPBOMBER.sh
# OR run with python directly
python3 bomber.py
```

## 🤝 Contributors

### Core Team
- **[VIPHACKER100](https://github.com/VIPHACKER100)** - Project Lead & Maintainer
- **[TheSpeedX](https://github.com/TheSpeedX)** - Original Creator
- **[t0xic0der](https://github.com/t0xic0der)** - https://atlasdoc.netlify.app
- **[Avinash](https://github.com/AvinashReddy3108)** - Core Developer
- **[scpketer](https://github.com/scpketer)** - Security Researcher
- **[0n1cOn3](https://github.com/0n1cOn3)** - Infrastructure
- **Rieltar** - Telegram: https://t.me/RieltarReborn
- **[Bishal](https://github.com/kbshal)** - API Development

### Special Thanks
- **34D30Y** - Major Donor
- **SC AMAN** - Contributor & Tester
- All our beta testers and community members

## 📋 TODO List

- [x] Complete Code Refactoring & Modernization
- [x] Add 300+ API Endpoints
- [x] Implement Advanced Security Features
- [x] Cross-Platform Compatibility
- [ ] Add Web Interface
- [ ] Mobile Application Version
- [ ] Advanced Analytics Dashboard
- [ ] API Rate Limit Management
- [ ] Custom API Integration System
- [ ] Real-time Monitoring Features

## ❓ Frequently Asked Questions

**Q:** Is there an official website or app?
**A:** The only official releases are on [GitHub](https://github.com/VIPHACKER100/VIPBOMBER-V2) and [PyPI](https://pypi.org/project/tbomb).

**Q:** Which countries are supported?
**A:** Multiple countries including India, US, Russia, China, UK with SMS support. Call support primarily in India.

**Q:** Why are there limits on bombing counts?
**A:** To prevent API abuse and ensure service availability for all users.

**Q:** Should I use a VPN?
**A:** Not necessary. VPNs may increase failure rates due to API restrictions.

**Q:** How can I contribute?
**A:** Fork the repository, make improvements, and submit pull requests. Report bugs and suggest features.

## 📞 Support

### Official Channels
- **Website**: https://viphacker100.com/
- **GitHub Issues**: [Create Issue](https://github.com/VIPHACKER100/VIPBOMBER-V2/issues)
- **Telegram**: https://t.me/VIPHACKER100

### Community
- Contributions, issues, and feature requests are welcome!
- Give us a ⭐ if you find this project useful!
- Help us improve by reporting bugs and suggesting features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Responsible Disclosure

If you discover any security vulnerabilities, please report them responsibly through GitHub issues or direct message. Do not exploit vulnerabilities in production systems.

---

<p align="center">
  <strong>Remember: With great power comes great responsibility. Use this tool wisely and ethically.</strong>
</p>

<p align="right">Last Updated: December 2023 | Version: 3.0.0</p>
```

