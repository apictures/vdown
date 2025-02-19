Project Setup Guide

This guide provides step-by-step instructions on how to install dependencies from requirements.txt on Termux, Linux, and Windows.

---

Installation on Termux

1. Update and Upgrade Packages:
   pkg update && pkg upgrade -y
2. Install Python and Pip:
   pkg install python -y
3. Install Required Packages from requirements.txt:
   Navigate to your project directory and run:
   pip install -r requirements.txt

Note: If you encounter missing dependencies, install them using:
   pkg install <package-name>

---

Installation on Linux (Ubuntu/Debian-Based Distros)

1. Update System:
   sudo apt update && sudo apt upgrade -y
2. Install Python and Pip:
   sudo apt install python3 python3-pip -y
3. Install Required Packages from requirements.txt:
   Navigate to your project directory and run:
   pip3 install -r requirements.txt

For other Linux distributions:
- Fedora: sudo dnf install python3 python3-pip
- Arch Linux: sudo pacman -S python python-pip

If you run into permission errors, try:
pip install --user -r requirements.txt
Or use a virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

---

Installation on Windows

1. Download and Install Python:
   - Download Python from the official website: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH".

2. Open Command Prompt (cmd) or PowerShell and verify installation:
   python --version
   pip --version

3. Navigate to Your Project Directory:
   cd path\to\your\project

4. Install Required Packages from requirements.txt:
   pip install -r requirements.txt

If you get permission errors, use:
pip install --user -r requirements.txt
Or create a virtual environment:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

---

Running the Application

1. Clone the Repository:
   git clone https://github.com/apictures/vdown.git
2. Navigate to the Project Directory:
   cd vdown
3. Install Dependencies:
   pip install -r requirements.txt
4. Run the Application:
   python app.py

---

Troubleshooting
- Ensure Python and Pip are installed correctly by checking their versions.
- If you get permission errors, try using --user or a virtual environment.
- If dependencies fail to install, check for missing system packages and install them accordingly.

---

This guide ensures a smooth setup for all users. If you encounter any issues, feel free to ask for help!
