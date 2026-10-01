# Debian / Ubuntu APT Repository

Conky Manager Qt is available through a signed Debian APT repository published with GitHub Pages.

## Repository

APT repository:

https://almezali.github.io/conky-manager-qt/

Public signing key:

https://almezali.github.io/conky-manager-qt/apt.gpg

The current GitHub **Latest Release** is the `latest` release, containing the **v1.0 / v1.0-2** builds.

The APT workflow follows the actual GitHub Latest Release, rather than a hard-coded version.

Supported architectures:

- amd64
- arm64

## Install on Debian / Ubuntu

### amd64

    sudo install -d -m 0755 /etc/apt/keyrings
    curl -fsSL https://almezali.github.io/conky-manager-qt/apt.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/conky-manager-qt.gpg
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/conky-manager-qt.gpg] https://almezali.github.io/conky-manager-qt stable main" | sudo tee /etc/apt/sources.list.d/conky-manager-qt.list
    sudo apt update
    sudo apt install conky-manager-qt

### arm64

Use the same setup with the arm64 architecture:

    sudo install -d -m 0755 /etc/apt/keyrings
    curl -fsSL https://almezali.github.io/conky-manager-qt/apt.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/conky-manager-qt.gpg
    echo "deb [arch=arm64 signed-by=/etc/apt/keyrings/conky-manager-qt.gpg] https://almezali.github.io/conky-manager-qt stable main" | sudo tee /etc/apt/sources.list.d/conky-manager-qt.list
    sudo apt update
    sudo apt install conky-manager-qt

## Update

Once the repository is installed, update Conky Manager Qt normally:

    sudo apt update
    sudo apt upgrade

New GitHub Releases are published to the APT repository automatically.

