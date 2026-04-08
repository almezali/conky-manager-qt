<div align="center">


# 🖥️ Conky Manager Qt

### A modern,Conky theme manager — built for KDE Plasma

---

## 📸 Screenshots

### Main Interface

  ![Main Interface](https://github.com/almezali/conky-manager-qt/blob/main/Screenshot-01.png)


> **The easiest way to manage Conky themes on KDE Plasma.**  
> Browse, run, repair, profile, and autostart your desktop widgets — all in one clean interface.

<br/>

</div>

---

## ✨ What is Conky Manager Qt?

**Conky Manager Qt** is a lightweight, self-contained GUI tool that takes the complexity out of managing [Conky](https://github.com/brndnmtthws/conky) desktop widgets on **KDE Plasma**. No config editing, no terminal gymnastics — just a polished Qt interface to control every aspect of your Conky setup.

It automatically scans for themes, optimizes their configs for KDE compatibility, runs health checks, and lets you build named profiles that launch on login.

---

## 🚀 Key Features

### 🎨 Theme Management
- **Auto-discovery** — Scans `~/.config/conky` and `~/.conky` for valid `.conf` files automatically
- **Live filter** — Instantly search and narrow down your theme list by name
- **Multi-select** — Select and run multiple themes simultaneously
- **Smart Repair** — Automatically patches broken configs for KDE/Wayland compatibility
- **5-second Preview** — Test a theme briefly before committing to it
- **Import Theme Folder** — Drop any folder of themes directly into the manager
- **Edit in-place** — Open any theme config in your default text editor
- **Context menu** — Right-click for quick per-theme actions

### 📁 Profile System
- **Save named profiles** — Group your favorite themes into named collections
- **One-click launch** — Run a full profile with a single button press
- **Autostart integration** — Write a `.desktop` entry to `~/.config/autostart` so your profile launches automatically at login
- **CLI profile runner** — `--run-profile "name"` for scripting and autostart

### 🔧 KDE Optimization Engine
- **Dual-syntax patching** — Handles both modern `conky.config {}` and legacy flat-file syntax
- **KDE Plasma settings** — Automatically injects correct `own_window_type`, `own_window_hints`, ARGB transparency, double-buffer, and more
- **Layer control** — Switch between *above* (overlay) and *below* (wallpaper-style) window layers
- **Optimized config cache** — Patched configs are saved to `~/.local/share/conky-kde-manager/optimized/` and never overwrite your originals
- **Fallback mode** — If the optimized config crashes, the manager transparently retries with your original

### ⚡ Performance Controls
| Mode | Update Interval | CPU Avg Samples | Net Avg Samples |
|------|----------------|-----------------|-----------------|
| **Ultra Smooth** | 1.5 s | 3 | 3 |
| **Balanced** | 1.0 s | 2 | 2 |
| **Performance** | 0.5 s | 2 | 2 |

- **Nice level** — Set process priority (default: 10) to keep KDE responsive
- **Max instances** — Limit simultaneous Conky processes to prevent overload
- **Healthcheck timer** — Configurable delay to detect early-crash themes before marking them as running

### 🩺 Diagnostics
- **Health Scan** — Validates every theme (original + optimized) and marks each as `Stable`, `Needs Fix`, or `Broken`
- **Theme Validator** — On-demand config validation via `conky -C`
- **Live log viewer** — Streams the last 250 lines of the internal log directly in the app
- **Log file access** — Open the full log in your system viewer with one click

---

## 📦 Installation

### Option 1 — AppImage (Recommended, No Dependencies)

Download the latest release:

```bash
wget https://github.com/almezali/conky-manager-qt/releases/latest/download/conky-manager-qt-x86_64.AppImage
chmod +x conky-manager-qt-x86_64.AppImage
./conky-manager-qt-x86_64.AppImage
```

> ✅ The AppImage bundles all dependencies. Works on any modern Linux x86_64 distribution.

---

### Option 2 — Run from Source

**Prerequisites:**

- Python 3.8+
- Conky installed
- PyQt5

**Install PyQt5:**

| Distro | Command |
|--------|---------|
| Arch / Manjaro | `sudo pacman -S python-pyqt5` |
| Ubuntu / Debian / Pop!\_OS | `sudo apt install python3-pyqt5` |
| Fedora / RHEL | `sudo dnf install python3-qt5` |
| openSUSE | `sudo zypper install python3-qt5` |
| NixOS | `nix-shell -p python3Packages.pyqt5` |
| Void Linux | `sudo xbps-install python3-PyQt5` |

**Run:**

```bash
git clone https://github.com/almezali/conky-manager-qt
cd conky-manager-qt
python conky-manager-qt.py
```

---

## 🖥️ Compatibility

| Distribution | Status | Notes |
|-------------|--------|-------|
| **KDE Neon** | ✅ Full | Native target |
| **Arch Linux + KDE** | ✅ Full | `pacman -S python-pyqt5 conky` |
| **Manjaro KDE** | ✅ Full | |
| **Kubuntu** | ✅ Full | |
| **EndeavourOS KDE** | ✅ Full | |
| **openSUSE KDE** | ✅ Full | |
| **Fedora KDE** | ✅ Full | |
| **Pop!\_OS** | ✅ Full | |
| **Ubuntu / GNOME** | ⚠️ Partial | Works, not KDE-optimized |
| **Wayland sessions** | ⚠️ Warning | Shows notice; X11 recommended for best results |

> **Note:** The KDE optimization engine targets Plasma + X11 for maximum compatibility. Wayland support is functional but may exhibit rendering differences depending on your compositor.

---

## 📂 File Locations

| Path | Purpose |
|------|---------|
| `~/.config/conky/` | Primary theme directory (auto-scanned) |
| `~/.conky/` | Secondary theme directory (auto-scanned) |
| `~/.local/share/conky-kde-manager/optimized/` | Patched theme configs (auto-generated) |
| `~/.local/share/conky-kde-manager/settings.json` | App settings |
| `~/.local/share/conky-kde-manager/profiles.json` | Saved profiles |
| `~/.local/share/conky-kde-manager/manager.log` | Runtime log |
| `~/.config/autostart/conky-kde-manager.desktop` | Autostart entry (when enabled) |

---

## ⌨️ CLI Usage

Run a saved profile headlessly (useful for autostart scripts):

```bash
python conky-manager-qt.py --run-profile "My Profile"
```

```bash
./conky-manager-qt-x86_64.AppImage --run-profile "My Profile"
```

---

## 🔍 How Smart Repair Works

When you click **Smart Repair**, the engine:

1. Reads your original `.conf` file
2. Detects whether it uses **new syntax** (`conky.config { }`) or **legacy syntax** (flat key-value)
3. Injects KDE-compatible settings — ARGB transparency, window hints, double buffering, layer mode
4. Writes the patched config to the **optimized cache** (your original is never modified)
5. Validates the result with `conky -C`
6. Falls back to your original automatically if the optimized version fails

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ for the Linux desktop community

**[⭐ Star this repo](https://github.com/almezali/conky-manager-qt)** if you find it useful!

</div>
