# Cyrus Pro

**Cyrus Pro** is a lightweight terminal application for Kali Linux, built with Python and `prompt_toolkit`.

## Features

* Lightweight and fast
* Terminal-based interface
* Custom application icon
* Kali Linux application menu integration
* Simple installation with `install.sh`
* Simple removal with `uninstall.sh`

## Requirements

* Python 3
* `prompt_toolkit`

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Cyrus-Terminal
```

Make the installer executable:

```bash
chmod +x install.sh
```

Install:

```bash
sudo ./install.sh
```

After installation, launch **Cyrus Pro** from the Kali Linux application menu.

## Uninstallation

Run:

```bash
sudo ./uninstall.sh
```

## Project Structure

```text
Cyrus-Terminal/
├── cyrus-pro.py
├── install.sh
├── uninstall.sh
├── requirements.txt
├── README.md
├── LICENSE
├── assets/
│   └── icon.png
└── packaging/
    └── cyrus-pro.desktop
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Cyrus Pro
