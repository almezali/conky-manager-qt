# Debian APT Repository Setup

This repository publishes Conky Manager Qt Debian packages through a signed APT repository.

## GitHub Actions secrets

Create these repository secrets:

- `APT_GPG_PRIVATE_KEY`
- `APT_GPG_PASSPHRASE`

Generate a dedicated signing key:

```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG
gpg --armor --export-secret-keys YOUR_KEY_ID > conky-manager-qt-apt-private.asc
```

Put the contents of `conky-manager-qt-apt-private.asc` into `APT_GPG_PRIVATE_KEY`.

If the key has a passphrase, put that passphrase into `APT_GPG_PASSPHRASE`.

## GitHub Pages

Open:

https://github.com/almezali/conky-manager-qt/settings/pages

Set **Source** to **GitHub Actions**.

## Publishing

The workflow runs automatically when a GitHub Release is published.

It downloads the packages from that release, so the APT repository follows the actual latest GitHub Release. A manual workflow run also selects the current latest release.

The repository supports:

- amd64
- arm64

APT repository URL:

https://almezali.github.io/conky-manager-qt/

Public key:

https://almezali.github.io/conky-manager-qt/apt.gpg
