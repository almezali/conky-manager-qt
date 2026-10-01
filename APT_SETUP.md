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

## GitHub Actions secrets

The repository workflow signs the APT metadata with a dedicated GPG key.

Create these repository secrets:

- APT_GPG_PRIVATE_KEY
- APT_GPG_PASSPHRASE

Generate a dedicated signing key:

    gpg --full-generate-key
    gpg --list-secret-keys --keyid-format LONG
    gpg --armor --export-secret-keys YOUR_KEY_ID > conky-manager-qt-apt-private.asc

Put the contents of conky-manager-qt-apt-private.asc into APT_GPG_PRIVATE_KEY.

If the key has a passphrase, put that passphrase into APT_GPG_PASSPHRASE.

**Never commit the private key or passphrase to the repository.**

## GitHub Pages

Open:

https://github.com/almezali/conky-manager-qt/settings/pages

Set **Source** to **GitHub Actions**.

The repository is published by:

.github/workflows/apt-repository.yml

## Publishing

The workflow runs automatically when a GitHub Release is published.

It downloads the .deb packages from that release, generates APT metadata, signs the repository, and deploys it to GitHub Pages.

A manual workflow run selects the current GitHub Latest Release.

This means the APT repository does not need a version number manually changed in this document when a new Latest Release is published.

## Current Release Check

The GitHub Latest Release currently has these Debian packages:

- `conky-manager-q_1.0-2_x86_64.deb`
- `conky-manager-q_1.0-2_aarch64.deb`

The same release also contains Arch, RPM and AppImage assets, but the APT repository publishes only the `.deb` packages.

## Verify the repository

After publishing, these files should be available:

    https://almezali.github.io/conky-manager-qt/apt.gpg
    https://almezali.github.io/conky-manager-qt/dists/stable/InRelease
    https://almezali.github.io/conky-manager-qt/dists/stable/Release.gpg
    https://almezali.github.io/conky-manager-qt/dists/stable/main/binary-amd64/Packages
    https://almezali.github.io/conky-manager-qt/dists/stable/main/binary-arm64/Packages

## Notes

- The repository is signed with GPG.
- APT verifies the repository using the installed keyring.
- The APT repository contains Debian packages from the GitHub Latest Release.
- Publishing a new GitHub Release automatically updates the repository.
- A manual workflow run can be used to resync the repository with the current Latest Release.
