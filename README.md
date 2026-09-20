<div align="center">

# Conky Manager Qt

**Your desktop, finally the way you pictured it.**

*Find a Conky theme you love, get it running in seconds, and put it exactly where you want it — without opening a config file once.*

[![Latest release](https://img.shields.io/github/v/release/almezali/conky-manager-qt?style=flat-square&color=2f81f7&label=release)](https://github.com/almezali/conky-manager-qt/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/almezali/conky-manager-qt/total?style=flat-square&color=success&label=downloads)](https://github.com/almezali/conky-manager-qt/releases)
[![Release date](https://img.shields.io/github/release-date/almezali/conky-manager-qt?style=flat-square&color=blueviolet&label=released)](https://github.com/almezali/conky-manager-qt/releases/latest)


[![Written in Go](https://img.shields.io/badge/Go-1.21%2B-00ADD8?style=flat-square&logo=go&logoColor=white)](https://go.dev)
[![Toolkit](https://img.shields.io/badge/Qt-6-41CD52?style=flat-square&logo=qt&logoColor=white)](https://www.qt.io)
[![Platform](https://img.shields.io/badge/Linux-x86__64%20%7C%20aarch64-333?style=flat-square&logo=linux&logoColor=white)](#-installation)
[![X11](https://img.shields.io/badge/X11-supported-success?style=flat-square)](#-compatibility)
[![Wayland](https://img.shields.io/badge/Wayland-XWayland-yellow?style=flat-square&logo=wayland&logoColor=white)](#-compatibility)
[![Code size](https://img.shields.io/github/languages/code-size/almezali/conky-manager-qt?style=flat-square&color=orange)](https://github.com/almezali/conky-manager-qt)

[![Stars](https://img.shields.io/github/stars/almezali/conky-manager-qt?style=flat-square&color=yellow)](https://github.com/almezali/conky-manager-qt/stargazers)
[![Issues](https://img.shields.io/github/issues/almezali/conky-manager-qt?style=flat-square)](https://github.com/almezali/conky-manager-qt/issues)
[![Last commit](https://img.shields.io/github/last-commit/almezali/conky-manager-qt?style=flat-square)](https://github.com/almezali/conky-manager-qt/commits)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](#-contributing)

[Installation](#-installation) · [Features](#-features) · [Quick start](#-quick-start) · [Build from source](#-build-from-source) · [Troubleshooting](#-troubleshooting)

<br>

### ⬇️ Download now

**Pick your distribution — the package installs in one command.**

[![Arch x86_64](https://img.shields.io/badge/Arch%20Linux-x86__64%20·%20pkg.tar.zst-1793D1?style=for-the-badge&logo=archlinux&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-2-x86_64.pkg.tar.zst)
[![Arch aarch64](https://img.shields.io/badge/Arch%20Linux-aarch64%20·%20pkg.tar.zst-0F6A9C?style=for-the-badge&logo=archlinux&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-2-aarch64.pkg.tar.zst)

[![Debian x86_64](https://img.shields.io/badge/Debian%20%2F%20Ubuntu-x86__64%20·%20.deb-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0-2_x86_64.deb)
[![Debian aarch64](https://img.shields.io/badge/Debian%20%2F%20Ubuntu-aarch64%20·%20.deb-6E1424?style=for-the-badge&logo=debian&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0-2_aarch64.deb)

[![Fedora x86_64](https://img.shields.io/badge/Fedora%20%2F%20openSUSE-x86__64%20·%20.rpm-51A2DA?style=for-the-badge&logo=fedora&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-2.x86_64.rpm)
[![Fedora aarch64](https://img.shields.io/badge/Fedora%20%2F%20openSUSE-aarch64%20·%20.rpm-2C6C91?style=for-the-badge&logo=fedora&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-2.aarch64.rpm)

[![AppImage](https://img.shields.io/badge/Any%20distribution-x86__64%20·%20AppImage-FF6600?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-1.0-2-x86_64.AppImage)
[![Source](https://img.shields.io/badge/Build%20from-source-181717?style=for-the-badge&logo=github&logoColor=white)](#-build-from-source)

<sub>Requires **Conky** to be installed · works on X11 and XWayland · no runtime dependencies to install</sub>

</div>

---

## You know how this usually goes

You see a gorgeous desktop screenshot on r/unixporn. You track down the theme, download it, unpack it somewhere, and run it.

Nothing appears.

So you open the config. You fix a path. You run it again. Half of it shows up. The rings are missing because something called `lm_sensors` isn't installed, and nothing told you that. You finally get it looking right — and then it's sitting on top of your panel, so you start guessing at `gap_x` and `gap_y`, restarting Conky after every guess. An hour later the colors clash with your wallpaper, and you realize changing them means hunting hex values through a Lua script.

**Conky Manager Qt is the hour you get back.**

Browse themes from GNOME-Look, KDE-Look and Pling inside the app and install one with a click. Press **Scan**, and it tells you in plain language what each theme is missing — then fixes the broken paths itself and hands you the exact command to install whatever else it needs. Drag it to the corner of the screen you want with a nine-point grid and arrow keys, on the monitor you want. Recolor it with a palette, including the Lua parts that normally fight back. When it looks right, save the whole arrangement as a profile and have it waiting for you at every login.

It knows which desktop you're on — Plasma, GNOME, XFCE, Cinnamon, MATE, LXQt, Hyprland, Sway, Niri, COSMIC — and puts your widgets on the right layer without being asked. And it never touches your original theme files without keeping a backup you can look at and roll back.

One small native app. No runtime to install, nothing running in the background, and your themes stay plain Conky configs you can take anywhere.

---

## ✨ Features

### Theme library
- **Automatic discovery** across `~/.config/conky`, `~/.conky`, `~/.local/share/conky` and `/usr/share/conky`, plus any custom directories you add.
- **Live file watcher** — drop a theme into a scanned folder and the list refreshes itself.
- **Instant search** and smart filters: *All · Favorites · Running · Recently used · Needs fix · Broken*.
- **Full theme management** from the sidebar — clone, rename, move to trash (via `gio trash`, never a hard `rm`), export as an archive, mark as favorite.
- **Import anything**: a folder, or a `.zip` / `.tar` / `.tar.gz` / `.tar.bz2` / `.tar.xz` / `.7z` archive. The importer detects the real theme root inside the archive, strips `-main` / `-master` suffixes, and refuses path-traversal entries, oversized payloads and archive bombs.

### Built-in theme marketplace
- Browse **GNOME-Look.org**, **KDE-Look.org** and **Pling.com** through their OCS catalog APIs, straight from the app.
- Sort by most downloaded, recently updated or best rated; filter by category; search by theme, author or keyword.
- Inspect metadata and preview images before installing — author, downloads, rating, version.
- One-click download and install into `~/.conky`, with a live progress dialog, a strict host allowlist and SHA-256 verification of downloaded files.

### Health scan & smart repair
- **Health scan** grades every theme as *stable*, *needs fix* or *broken*, with a per-issue breakdown of what's wrong.
- **Missing asset detection** — resolves `${image ...}`, `lua_load`, `${exec ...}` and raw `~/.config/conky/...` references, then reports what's actually missing.
- **Dependency detection** — finds external commands a theme calls and tells you which are absent, with a ready-made install command for your package manager (`dnf` / `apt` / `pacman` / `zypper`), copyable to the clipboard.
- **Smart repair** builds a self-contained launch bundle per theme: asset paths relinked, fonts and Lua scripts resolved, compatibility symlinks created so themes written for a fixed install path run from wherever you put them.
- **Validate all / Fix all** for batch work across the whole library.

### Position control
- Nine-point **alignment grid** (top-left through bottom-right) with pixel-accurate X/Y gap spinners.
- **Arrow-key nudging** with a configurable step size.
- **Multi-monitor aware** — detects connected displays via `xrandr`, including geometry, scale factor and which one is primary, and lets you pin a theme to a specific screen.
- **Scale-aware gaps** for HiDPI setups, so offsets stay visually consistent across different scale factors.
- Per-theme positions are remembered; *Apply & Restart* previews the change immediately; *Reset* restores the theme's own values.

### Color engine
- Parses the theme's real color slots (`default_color`, `color0`–`color9`, …) and renders a native color picker for each.
- **Palette presets** plus a **Palette Manager** for saving your own; generate a full coordinated palette from a single accent color.
- **Smart Lua match** automatically recolors matching hex values inside Lua ring/gauge scripts — the part that normally breaks when you recolor a theme by hand.
- Recoloring is non-destructive and per-theme, and is applied to the launch bundle rather than smashing the original config.

### Profiles & autostart
- Group several themes into a named **profile** (a full clock + system-monitor + weather arrangement, for example) and launch them together.
- Duplicate, export and import profiles as portable `.conky-profile` files.
- **XDG autostart** with no `OnlyShowIn` filter, so the same profile loads under GNOME, KDE, XFCE, Cinnamon, MATE, LXQt, Hyprland, Niri, Sway and COSMIC.
- Headless launching via `--run-profile` for use in your own WM startup script or systemd user unit.

### Process management
- Run, stop, restart and preview individual themes, or the whole library at once.
- **Timed preview** with pause / resume / restart, so you can audition a theme without committing to it.
- Startup **healthcheck**: a theme that dies immediately is reported instead of silently failing.
- **Kill orphaned Conky** processes left behind by crashes or other launchers, with managed and unmanaged instances tracked separately — the app never blindly kills processes it didn't start unless you ask it to.
- Configurable `nice` level and maximum instance count.

### Editing & safety
- Built-in **config editor** with find, go-to-line, validate-before-save and revert.
- **Automatic backups** on every write to an original theme config, with a **Backup History** browser and a unified diff view of what changed.
- **Theme Details** panel showing size, file inventory, SHA-256, dependency status and health issues.
- Full application log, viewable in the Diagnostics tab or openable in your editor.

### Desktop integration
- Detects **KDE / Plasma, GNOME, XFCE, Cinnamon, MATE, LXQt, LXDE, Hyprland, Niri, Sway and COSMIC**, and whether you're on **X11, Wayland or XWayland**.
- Applies the correct `own_window_type` and layer per environment automatically — dock and *above* on KDE, desktop and *below* on GNOME/XFCE/MATE, override and *above* on wlroots compositors — or override it manually.
- Handles both **modern Lua-syntax** (`conky.config = {}`) and **legacy** Conky configs transparently.
- Performance presets: *Ultra smooth* (lower CPU), *Balanced*, *Performance* (faster updates).
- Light, dark and system-following UI themes.

---

## 📦 Installation

> **Requirement:** Conky itself must be installed. The app checks on startup and exits with a message if it isn't.
>
> `sudo pacman -S conky` · `sudo apt install conky-all` · `sudo dnf install conky` · `sudo zypper install conky`

Prebuilt packages are published for **x86_64** and **aarch64** (ARM64 — Raspberry Pi, Asahi, ARM laptops and SBCs).

### Arch Linux, Manjaro, EndeavourOS, Garuda

```bash
# x86_64
curl -LO https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1-x86_64.pkg.tar.zst
sudo pacman -U conky-manager-q-1.0-1-x86_64.pkg.tar.zst

# aarch64
curl -LO https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1-aarch64.pkg.tar.zst
sudo pacman -U conky-manager-q-1.0-1-aarch64.pkg.tar.zst
```

### Debian, Ubuntu, Linux Mint, Pop!\_OS, Zorin, elementary

```bash
# x86_64
curl -LO https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0_x86_64.deb
sudo apt install ./conky-manager-q_1.0_x86_64.deb

# aarch64
curl -LO https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0_aarch64.deb
sudo apt install ./conky-manager-q_1.0_aarch64.deb
```

### Fedora, RHEL, CentOS Stream, openSUSE, Nobara

```bash
# x86_64
sudo dnf install https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1.x86_64.rpm

# aarch64
sudo dnf install https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1.aarch64.rpm
```

openSUSE users: `sudo zypper install <url>`.

### AppImage — every other distribution

Works on Void, Gentoo, Slackware, NixOS, Alpine, Solus, immutable systems (Silverblue, Kinoite, Bazzite, SteamOS) and anything else with glibc.

```bash
curl -LO https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-x86_64.AppImage
chmod +x conky-manager-x86_64.AppImage
./conky-manager-x86_64.AppImage
```

<details>
<summary>Install the AppImage system-wide with a desktop entry</summary>

```bash
sudo install -Dm755 conky-manager-x86_64.AppImage /usr/local/bin/conky-manager-q
```

Then create `~/.local/share/applications/conky-manager-q.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Conky Manager Qt
Comment=Conky theme manager with a modern UI.
Exec=/usr/bin/conky-manager-q
Icon=conky-manager-q
Terminal=false
Categories=Utility;Settings;DesktopSettings;
```

</details>

### All packages at a glance

| Download | Architecture | Format | Made for | Installs with |
|---|:---:|:---:|---|---|
| [![dl](https://img.shields.io/badge/⬇-Get%20it-1793D1?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1-x86_64.pkg.tar.zst) `conky-manager-q-1.0-1-x86_64.pkg.tar.zst` | x86_64 | `pkg.tar.zst` | Arch, Manjaro, EndeavourOS, Garuda, Artix | `pacman -U` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-0F6A9C?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1-aarch64.pkg.tar.zst) `conky-manager-q-1.0-1-aarch64.pkg.tar.zst` | aarch64 | `pkg.tar.zst` | Arch ARM, Asahi, Pi running Arch | `pacman -U` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-A81D33?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0_x86_64.deb) `conky-manager-q_1.0_x86_64.deb` | x86_64 | `.deb` | Debian, Ubuntu, Mint, Pop!_OS, Zorin, MX | `apt install ./` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-6E1424?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q_1.0_aarch64.deb) `conky-manager-q_1.0_aarch64.deb` | aarch64 | `.deb` | Raspberry Pi OS, Ubuntu ARM, ARM laptops | `apt install ./` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-51A2DA?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1.x86_64.rpm) `conky-manager-q-1.0-1.x86_64.rpm` | x86_64 | `.rpm` | Fedora, Nobara, RHEL, CentOS, openSUSE | `dnf install` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-2C6C91?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-q-1.0-1.aarch64.rpm) `conky-manager-q-1.0-1.aarch64.rpm` | aarch64 | `.rpm` | Fedora ARM, openSUSE ARM | `dnf install` |
| [![dl](https://img.shields.io/badge/⬇-Get%20it-FF6600?style=flat-square)](https://github.com/almezali/conky-manager-qt/releases/download/latest/conky-manager-x86_64.AppImage) `conky-manager-x86_64.AppImage` | x86_64 | `AppImage` | Void, Gentoo, NixOS, Alpine, Solus, Silverblue, SteamOS | `chmod +x` and run |

<sub>All packages are cut from the same release. Not sure which one you need? Run `uname -m` — `x86_64` means a normal desktop or laptop, `aarch64` means ARM.</sub>

---

## 🚀 Quick start

Launch **Conky Manager Qt** from your application menu, or run `conky-manager-q` in a terminal.

1. **Get a theme.** Open *Tools → Theme marketplace*, search GNOME-Look / KDE-Look / Pling, pick something, hit install. Already have themes? Use the sidebar's **Import folder** or **Import archive** buttons — or just drop them in `~/.conky` and the watcher will pick them up.
2. **Scan before you run.** Click **🔍 Scan** in the Control tab. Anything marked *needs fix* or *broken* tells you exactly what's missing — usually assets or a command like `lm_sensors`. Hit **Smart repair** (⚒) to relink assets automatically, and copy the suggested install command for any missing dependency.
3. **Run it.** Select the theme and press **▶ Run**, or use **▶ Start** in the Preview card for a timed audition you can stop instantly.
4. **Place it.** Go to the **Position** tab, tick *Control position*, pick a monitor, choose an alignment cell, then nudge with the arrow buttons until it sits right. **Save for Theme** remembers it; **Apply & Restart** shows it live.
5. **Color it.** The **Colors** tab lists the theme's real color slots. Pick a palette preset or set each slot by hand, enable **Smart Lua match** if the theme uses Lua rings, then **Apply & Restart**.
6. **Make it permanent.** In the **Profiles** tab, name a profile, **Add Themes**, **Save Profile**, then **Enable Autostart**. Your arrangement now comes back on every login.

### Command line

```bash
conky-manager-q                      # launch the GUI
conky-manager-q --run-profile "Work" # launch a saved profile headlessly, no GUI
```

The `--run-profile` mode is what the generated autostart entry uses, and is the right hook for a `exec-once` line in a Hyprland/Sway config or a systemd user service.

### Where things live

| Path | Purpose |
|---|---|
| `~/.local/share/conky-manager/settings.json` | Application settings |
| `~/.local/share/conky-manager/positions.json` | Per-theme position overrides |
| `~/.local/share/conky-manager/colors.json` | Per-theme color overrides |
| `~/.local/share/conky-manager/profiles.json` | Saved profiles |
| `~/.local/share/conky-manager/palettes.json` | Custom color palettes |
| `~/.local/share/conky-manager/launch/` | Generated self-contained launch bundles |
| `~/.local/share/conky-manager/downloads/` | Marketplace download cache |
| `~/.local/share/conky-manager/manager.log` | Application log |
| `~/.config/autostart/conky-manager.desktop` | Autostart entry, when enabled |

Everything is plain JSON. Back it up, version it, edit it, delete it — the app rebuilds what it needs.

---

## 🔨 Build from source

### Prerequisites

- **Go 1.21 or newer**
- **Qt 6 development files** (`QtCore`, `QtGui`, `QtWidgets`)
- A C/C++ toolchain and `pkg-config` — the Qt bindings are cgo-based
- **Conky** at runtime

<details open>
<summary><b>Arch Linux</b></summary>

```bash
sudo pacman -S --needed go qt6-base base-devel pkgconf conky
```
</details>

<details>
<summary><b>Debian / Ubuntu</b></summary>

```bash
sudo apt install golang-go qt6-base-dev build-essential pkg-config conky-all
```
</details>

<details>
<summary><b>Fedora</b></summary>

```bash
sudo dnf install golang qt6-qtbase-devel gcc-c++ pkgconf-pkg-config conky
```
</details>

<details>
<summary><b>openSUSE</b></summary>

```bash
sudo zypper install go qt6-base-devel gcc-c++ pkg-config conky
```
</details>

### Compile

```bash
git clone https://github.com/almezali/conky-manager-qt.git
cd conky-manager-qt

go mod tidy
CGO_ENABLED=1 go build -ldflags="-s -w" -o conky-manager-q .

./conky-manager-q
```

### Install locally

```bash
sudo install -Dm755 conky-manager-q /usr/bin/conky-manager-q
```

Add a `.desktop` entry as shown in the AppImage section above if your build doesn't ship one.

> **Note on cgo:** the Qt 6 bindings compile C++ on first build, so the initial `go build` takes noticeably longer than a pure-Go project. Subsequent builds are cached and fast.

---

## 🧩 Compatibility

| | Status |
|---|---|
| **Display servers** | X11 ✅ · XWayland ✅ · Wayland ⚠️ (see below) |
| **Desktops** | KDE Plasma, GNOME, XFCE, Cinnamon, MATE, LXQt, LXDE, COSMIC |
| **Compositors** | Hyprland, Sway, Niri (via XWayland) |
| **Architectures** | x86_64, aarch64 |
| **Conky syntax** | Modern (`conky.config = {}`) and legacy, auto-detected |

**About Wayland:** Conky is an X11 application. On a Wayland session it runs through XWayland, and window placement rules are enforced by the compositor rather than by Conky. Conky Manager Qt detects this, shows a notice on startup, and applies override/above hints that work with wlroots-based compositors — but if your compositor refuses to honor them, you may need a compositor-level window rule. On Hyprland, for example:

```ini
windowrulev2 = noblur, class:^(conky)$
windowrulev2 = nofocus, class:^(conky)$
windowrulev2 = pin, class:^(conky)$
```

---

## 🔧 Troubleshooting

**"Conky is not installed."**
Install Conky through your package manager first. The app deliberately refuses to start without it rather than failing later in a confusing way.

**A theme runs but shows nothing / a blank box.**
Run **Health scan**, then **Smart repair**. This is almost always hard-coded asset paths from the theme's original author. If issues remain, open **Theme Details** for the full list.

**A theme is missing rings, graphs or icons.**
The theme depends on an external command or a Lua library. Health scan lists missing dependencies and gives you a copyable install command for your distro.

**The widget is behind the wallpaper (GNOME/XFCE).**
That's the desktop preset behaving normally. In *File → Settings → Window Behavior*, set the layer to **Above windows** and the window type to **Dock**.

**The widget covers my panel (KDE).**
Opposite case — set the layer to **Below windows** and type to **Desktop**.

**Conky processes left running after a crash.**
Control tab → **🧹 Kill Orphaned**. Managed instances are tracked in `runtime.json`; orphans are matched by process inspection.

**High CPU usage.**
*Settings → Performance → Ultra smooth*, and raise the `nice` level. Some marketplace themes poll every 0.5 s by default; the smoothness preset overrides that.

**Something else.**
Check `~/.local/share/conky-manager/manager.log` (Diagnostics tab → **Open Log**) and open an issue with the relevant lines.

---

## 🤝 Contributing

Issues and pull requests are welcome.

- **Bug reports** — include your distro, desktop environment, session type (`echo $XDG_SESSION_TYPE`), `conky --version`, and the relevant portion of `manager.log`.
- **Theme compatibility reports** are especially useful: if a theme from the marketplace doesn't render correctly after Smart Repair, say which one and what's missing. That's how the asset resolver improves.
- **Code** — keep it dependency-light and idiomatic Go. Run `gofmt` before submitting.

---



<div align="center">

**Made for people who think a desktop should look like something.**

[⬆ Back to top](#conky-manager-qt) · [Report an issue](https://github.com/almezali/conky-manager-qt/issues) · [Releases](https://github.com/almezali/conky-manager-qt/releases)

</div>
