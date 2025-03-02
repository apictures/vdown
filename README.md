Project Setup Guide

This guide provides step-by-step instructions on how to install dependencies from requirements.txt on Termux, Linux, and Windows, and how to install Tor.

---

## Installation on Termux

1. **Update and Upgrade Packages:**
   ```sh
   pkg update && pkg upgrade -y
   ```
2. **Install Python and Pip:**
   ```sh
   pkg install python -y
   ```
3. **Install Tor:**
   ```sh
   pkg install tor -y
   ```
4. **Install Required Packages from requirements.txt:**   Navigate to your project directory and run:
   ```sh
   pip install -r requirements.txt
   ```
5. **Run Tor Manually (if needed):**
   ```sh
   tor
   ```

If you encounter missing dependencies, install them using:

```sh
pkg install <package-name>
```

---

## Installation on Linux (Ubuntu/Debian-Based Distros)

1. **Update System:**
   ```sh
   sudo apt update && sudo apt upgrade -y
   ```
2. **Install Python and Pip:**
   ```sh
   sudo apt install python3 python3-pip -y
   ```
3. **Install Tor:**
   ```sh
   sudo apt install tor -y
   ```
4. **Install Required Packages from requirements.txt:**   Navigate to your project directory and run:
   ```sh
   pip3 install -r requirements.txt
   ```
5. **Run Tor Manually (if needed):**
   ```sh
   tor
   ```

For other Linux distributions:

- **Fedora:**
  ```sh
  sudo dnf install python3 python3-pip tor
  ```
- **Arch Linux:**
  ```sh
  sudo pacman -S python python-pip tor
  ```

If you run into permission errors, try:

```sh
pip install --user -r requirements.txt
```

Or use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Installation on Windows

1. **Download and Install Python:**

   - Download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH".

2. **Download and Install Tor:**

   - Download the **Tor Expert Bundle** (not the browser) from [Tor Project](https://www.torproject.org/download/).
   - Extract it to `C:\Tor`.

3. **Open Command Prompt (cmd) or PowerShell and verify installation:**

   ```sh
   python --version
   pip --version
   ```

4. **Navigate to Your Project Directory:**

   ```sh
   cd path\to\your\project
   ```

5. **Install Required Packages from requirements.txt:**

   ```sh
   pip install -r requirements.txt
   ```

6. **Run Tor Manually (if needed):**

   ```sh
   C:\Tor\tor.exe
   ```

If you get permission errors, use:

```sh
pip install --user -r requirements.txt
```

Or create a virtual environment:

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Application

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/apictures/vdown.git
   ```
2. **Navigate to the Project Directory:**
   ```sh
   cd vdown
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Start Tor (if not already running):**
   - **Termux/Linux:**
     ```sh
     tor
     ```
   - **Windows:**
     ```sh
     C:\Tor\tor.exe
     ```
5. **Run the Application:**
   ```sh
   python app.py
   ```

---

## Troubleshooting

- Ensure Python and Pip are installed correctly by checking their versions.
- If you get permission errors, try using `--user` or a virtual environment.
- If dependencies fail to install, check for missing system packages and install them accordingly.
- If Tor is not working, try running it manually to check for errors.

---

This guide ensures a smooth setup for all users. If you encounter any issues, feel free to ask for help!
