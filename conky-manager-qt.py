#!/usr/bin/env python3
"""
Conky manager Qt - v0.1
Conky theme manager for KDE Plasma with a modern UI.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
    from PyQt5.QtGui import QColor, QFont, QIcon, QPainter, QPen, QPixmap
    from PyQt5.QtWidgets import (
        QApplication,
        QAction,
        QComboBox,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QMenu,
        QMessageBox,
        QPushButton,
        QSpinBox,
        QDoubleSpinBox,
        QTabWidget,
        QTextEdit,
        QVBoxLayout,
        QWidget,
        QFileDialog,
        QScrollArea,
    )
except ImportError:
    print("PyQt5 is required. Install it with: sudo pacman -S python-pyqt5")
    raise SystemExit(1)


APP_NAME = "Conky manager Qt"
APP_VERSION = "v0.1"

HOME = Path.home()
THEME_DIRS = [
    HOME / ".config" / "conky",
    HOME / ".conky",
]
BASE_DIR = HOME / ".local" / "share" / "conky-kde-manager"
LOG_FILE = BASE_DIR / "manager.log"
OPTIMIZED_DIR = BASE_DIR / "optimized"
SETTINGS_FILE = BASE_DIR / "settings.json"
PROFILES_FILE = BASE_DIR / "profiles.json"
AUTOSTART_DIR = HOME / ".config" / "autostart"
AUTOSTART_FILE = AUTOSTART_DIR / "conky-kde-manager.desktop"

BASE_DIR.mkdir(parents=True, exist_ok=True)
OPTIMIZED_DIR.mkdir(parents=True, exist_ok=True)
THEME_DIRS[0].mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


COLORS = {
    "primary": "#2563eb",
    "primary_dark": "#1d4ed8",
    "secondary": "#64748b",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "background": "#0f172a",
    "surface": "#1e293b",
    "surface_light": "#334155",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "border": "#475569",
}


DEFAULT_SETTINGS: dict[str, Any] = {
    "layer": "above",  # above | below
    "window_type": "dock",  # dock | desktop
    "smoothness": "balanced",  # ultra | balanced | performance
    "nice_level": 10,
    "max_instances": 1,
    "healthcheck_seconds": 1.2,
    "preview_seconds": 5,
}


def detect_environment():
    session = os.environ.get("XDG_SESSION_TYPE", "unknown")
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    return session, desktop


def load_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def save_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def is_conky_installed():
    return shutil.which("conky") is not None


def is_valid_theme(cfg_path: Path):
    try:
        text = cfg_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return "conky.config" in text or "own_window" in text or "TEXT" in text


def find_themes():
    themes: list[Path] = []
    for root_dir in THEME_DIRS:
        if not root_dir.is_dir():
            continue
        for cfg_file in root_dir.rglob("*.conf"):
            if cfg_file.is_file() and is_valid_theme(cfg_file):
                themes.append(cfg_file.resolve())
    return sorted(set(themes))


KDE_SETTINGS_NEW_BASE = {
    "update_interval": "1.0",
    "update_interval_on_battery": "1.5",
    "cpu_avg_samples": "2",
    "net_avg_samples": "2",
    "double_buffer": "true",
    "no_buffers": "true",
    "own_window": "true",
    "own_window_argb_visual": "true",
    "own_window_argb_value": "0",
    "own_window_transparent": "true",
    "draw_shades": "false",
    "draw_outline": "false",
    "draw_borders": "false",
    "draw_graph_borders": "false",
    "use_xft": "true",
    "xftalpha": "1.0",
}

KDE_SETTINGS_LEGACY_BASE = {
    "update_interval": "1.0",
    "cpu_avg_samples": "2",
    "net_avg_samples": "2",
    "double_buffer": "yes",
    "no_buffers": "yes",
    "own_window": "yes",
    "own_window_argb_visual": "yes",
    "own_window_argb_value": "0",
    "own_window_transparent": "yes",
    "draw_shades": "no",
    "draw_outline": "no",
    "draw_borders": "no",
    "draw_graph_borders": "no",
    "use_xft": "yes",
    "xftalpha": "1.0",
}


def compute_kde_settings(settings: dict, new_syntax: bool):
    smooth = settings.get("smoothness", "balanced")
    if smooth == "ultra":
        upd, cpu, net = "1.5", "3", "3"
    elif smooth == "performance":
        upd, cpu, net = "0.5", "2", "2"
    else:
        upd, cpu, net = "1.0", "2", "2"

    layer = settings.get("layer", "above")
    window_type = settings.get("window_type", "dock")

    if new_syntax:
        base = dict(KDE_SETTINGS_NEW_BASE)
        base["update_interval"] = upd
        base["cpu_avg_samples"] = cpu
        base["net_avg_samples"] = net
        base["own_window_type"] = f'"{window_type}"'
        base["own_window_hints"] = (
            '"undecorated,above,sticky,skip_taskbar,skip_pager"'
            if layer == "above"
            else '"undecorated,below,sticky,skip_taskbar,skip_pager"'
        )
        return base

    base = dict(KDE_SETTINGS_LEGACY_BASE)
    base["update_interval"] = upd
    base["cpu_avg_samples"] = cpu
    base["net_avg_samples"] = net
    base["own_window_type"] = window_type
    base["own_window_hints"] = (
        "undecorated,above,sticky,skip_taskbar,skip_pager"
        if layer == "above"
        else "undecorated,below,sticky,skip_taskbar,skip_pager"
    )
    return base


def _is_new_syntax(content: str):
    return "conky.config" in content and "conky.text" in content


def _patch_new_syntax(content: str, settings: dict):
    start_idx = content.find("conky.config")
    brace_idx = content.find("{", start_idx)
    if start_idx < 0 or brace_idx < 0:
        return content

    depth = 0
    end_idx = -1
    for idx in range(brace_idx, len(content)):
        char = content[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end_idx = idx
                break
    if end_idx == -1:
        return content

    block = content[brace_idx + 1:end_idx]
    kde = compute_kde_settings(settings, new_syntax=True)
    for key, value in kde.items():
        pattern = re.compile(rf"(^\s*{re.escape(key)}\s*=\s*.*?,\s*$)", re.MULTILINE)
        replacement = f"    {key} = {value},"
        if pattern.search(block):
            block = pattern.sub(replacement, block, count=1)
        else:
            block = f"{replacement}\n{block}"

    return content[: brace_idx + 1] + block + content[end_idx:]


def _patch_legacy_syntax(content: str, settings: dict):
    lines = content.splitlines()
    text_idx = len(lines)
    for idx, line in enumerate(lines):
        if line.strip().upper() == "TEXT":
            text_idx = idx
            break

    head = lines[:text_idx]
    tail = lines[text_idx:]
    key_to_idx: dict[str, int] = {}
    for idx, line in enumerate(head):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key = stripped.split()[0]
        key_to_idx[key] = idx

    kde = compute_kde_settings(settings, new_syntax=False)
    for key, value in kde.items():
        new_line = f"{key} {value}"
        if key in key_to_idx:
            head[key_to_idx[key]] = new_line
        else:
            head.insert(0, new_line)
    return "\n".join(head + tail) + "\n"


def optimize_for_kde(cfg_path: Path):
    try:
        content = cfg_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        raise RuntimeError(f"Failed to read theme file: {cfg_path}") from exc

    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    if _is_new_syntax(content):
        content = _patch_new_syntax(content, settings)
    else:
        content = _patch_legacy_syntax(content, settings)

    optimized_name = f"{cfg_path.parent.name}_{cfg_path.name}"
    new_path = OPTIMIZED_DIR / optimized_name
    new_path.write_text(content, encoding="utf-8")
    return new_path


def validate_conky_config(config_path: Path, timeout_sec: int = 6):
    try:
        check = subprocess.run(
            ["conky", "-c", str(config_path), "-C"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout_sec,
        )
        return check.returncode == 0
    except Exception:
        return False


def kill_running_conky():
    result = subprocess.run(
        ["pkill", "-x", "conky"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode in (0, 1)


def _start_conky_with_healthcheck(config_path: Path):
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    health_seconds = float(settings.get("healthcheck_seconds", 1.2))
    nice_level = int(settings.get("nice_level", 10))
    log_handle = LOG_FILE.open("a", encoding="utf-8")

    process = subprocess.Popen(
        ["nice", "-n", str(nice_level), "conky", "-q", "-c", str(config_path)],
        stdout=log_handle,
        stderr=log_handle,
    )
    waited = 0.0
    while waited < health_seconds:
        if process.poll() is not None:
            return process, False
        time.sleep(0.2)
        waited += 0.2
    return process, process.poll() is None


def run_conky(cfg_path: Path):
    if not validate_conky_config(cfg_path):
        raise RuntimeError(f"Invalid Conky config: {cfg_path}")

    optimized = optimize_for_kde(cfg_path)
    if validate_conky_config(optimized):
        process, healthy = _start_conky_with_healthcheck(optimized)
        if healthy:
            logging.info("Started optimized Conky: %s (pid=%s)", optimized, process.pid)
            return process.pid, optimized, "optimized"

    logging.warning("Optimized failed quickly or invalid; trying original: %s", cfg_path)
    process, healthy = _start_conky_with_healthcheck(cfg_path)
    if healthy:
        logging.info("Started original fallback: %s (pid=%s)", cfg_path, process.pid)
        return process.pid, cfg_path, "fallback-original"

    raise RuntimeError(f"Theme failed in both optimized and fallback mode: {cfg_path}")


class ModernButton(QPushButton):
    def __init__(self, text: str, color: str = "primary", parent=None):
        super().__init__(text, parent)
        self._color = color
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(34)
        self.setStyleSheet(self._style())

    def _style(self):
        bg = COLORS.get(self._color, COLORS["primary"])
        hover = COLORS.get(f"{self._color}_dark", bg)
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {COLORS['text']};
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_muted']};
            }}
        """


class ModernCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
            """
        )


class ThemeRunnerWorker(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal(int, int, int)  # started, fallback, limited_to

    def __init__(self, themes: list[Path], parent=None):
        super().__init__(parent)
        self.themes = themes

    def run(self):
        settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
        max_instances = int(settings.get("max_instances", 1))
        run_list = self.themes[:max_instances]
        limited_to = len(run_list)

        kill_running_conky()
        started = 0
        fallback = 0

        for theme in run_list:
            try:
                pid, _, mode = run_conky(theme)
                started += 1
                if mode == "fallback-original":
                    fallback += 1
                self.log.emit(f"Started: {theme.name} (pid={pid}, mode={mode})")
            except Exception as exc:
                self.log.emit(f"Failed: {theme} ({exc})")

        self.finished.emit(started, fallback, limited_to)


class RepairWorker(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal(int, int)  # ok, fail

    def __init__(self, themes: list[Path], parent=None):
        super().__init__(parent)
        self.themes = themes

    def run(self):
        ok = 0
        fail = 0
        for theme in self.themes:
            try:
                optimize_for_kde(theme)
                ok += 1
            except Exception as exc:
                fail += 1
                self.log.emit(f"Repair failed: {theme} ({exc})")
        self.finished.emit(ok, fail)


class ThemeHealthWorker(QThread):
    progress = pyqtSignal(str)
    item_status = pyqtSignal(str, str)  # label, status
    finished = pyqtSignal(int, int, int)  # ok, warn, bad

    def __init__(self, themes: list[ThemeItem], parent=None):
        super().__init__(parent)
        self.themes = themes

    def run(self):
        ok = 0
        warn = 0
        bad = 0
        for item in self.themes:
            label = item.label
            self.progress.emit(f"Checking: {label}")
            try:
                is_ok = validate_conky_config(item.path)
                if not is_ok:
                    self.item_status.emit(label, "broken")
                    bad += 1
                    continue

                # If optimized fails but original ok => warning
                optimized = optimize_for_kde(item.path)
                if validate_conky_config(optimized):
                    self.item_status.emit(label, "stable")
                    ok += 1
                else:
                    self.item_status.emit(label, "needs_fix")
                    warn += 1
            except Exception:
                self.item_status.emit(label, "broken")
                bad += 1
        self.finished.emit(ok, warn, bad)


@dataclass(frozen=True)
class ThemeItem:
    path: Path

    @property
    def label(self):
        return f"{self.path.parent.name}/{self.path.name}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session, self.desktop = detect_environment()
        self.settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
        self.profiles = load_json(PROFILES_FILE, {"profiles": {}, "last_profile": ""})

        self.themes: list[ThemeItem] = []
        self.filtered: list[ThemeItem] = []
        self.theme_status: dict[str, str] = {}  # label -> stable|needs_fix|broken
        self.worker: QThread | None = None
        self.preview_timer: QTimer | None = None

        self.init_ui()
        self.load_themes()
        self.refresh_profiles()
        self.refresh_log_view()
        self.show_wayland_notice()

    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.setMinimumSize(900, 620)
        self.resize(1024, 680)
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {COLORS['background']};
                color: {COLORS['text']};
            }}
            QMainWindow {{
                background-color: {COLORS['background']};
                color: {COLORS['text']};
            }}
            QLabel {{
                color: {COLORS['text']};
            }}
            QScrollArea {{
                background: transparent;
            }}
            QAbstractScrollArea::viewport {{
                background-color: {COLORS['background']};
            }}
            QGroupBox {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                margin-top: 12px;
                padding: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: {COLORS['text']};
                font-weight: 600;
            }}
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                background-color: {COLORS['surface_light']};
                border: 1px solid {COLORS['border']};
                border-radius: 7px;
                padding: 8px;
                color: {COLORS['text']};
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
                selection-background-color: {COLORS['primary']};
                border: 1px solid {COLORS['border']};
            }}
            QListWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                color: {COLORS['text']};
                padding: 6px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['primary']};
            }}
            QTextEdit {{
                background-color: #000000;
                color: #00ff00;
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }}
            QMenu {{
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary']};
            }}
            QMessageBox {{
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
            }}
            QMessageBox QLabel {{
                color: {COLORS['text']};
                background: transparent;
            }}
            QMessageBox QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['text']};
                border: none;
                border-radius: 7px;
                padding: 8px 14px;
                font-weight: 600;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QTabWidget::pane {{
                border: 0;
            }}
            QTabBar::tab {{
                background-color: {COLORS['surface']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                padding: 8px 12px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['surface_light']};
                border-color: {COLORS['primary']};
            }}
            """
        )
        self.setWindowIcon(self.create_app_icon())

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header = ModernCard()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 10, 14, 10)
        title = QLabel(APP_NAME)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        subtitle = QLabel(f"Session: {self.session} | Desktop: {self.desktop}")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']};")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        self.build_tab_themes()
        self.build_tab_profiles()
        self.build_tab_diagnostics()
        self.build_tab_settings()

        self.statusBar().showMessage("Ready")

    def create_app_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(COLORS["primary"]))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(COLORS["text"]), 2))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "C")
        painter.end()
        return QIcon(pixmap)

    def show_wayland_notice(self):
        if "wayland" in self.session.lower():
            QMessageBox.warning(
                self,
                "Wayland Notice",
                "Conky on Wayland can stutter under heavy window movement.\n"
                "For maximum smoothness, use a Plasma X11 session.",
            )

    # ---------------- Tabs ----------------
    def build_tab_themes(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setSpacing(10)

        top = ModernCard()
        top_l = QHBoxLayout(top)
        top_l.setContentsMargins(12, 10, 12, 10)
        top_l.addWidget(QLabel("Filter:"))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Type to filter themes...")
        self.filter_edit.textChanged.connect(self.apply_filter)
        top_l.addWidget(self.filter_edit, 1)
        self.btn_refresh = ModernButton("Refresh", "primary")
        self.btn_import = ModernButton("Import Theme Folder", "warning")
        self.btn_health = ModernButton("Health Scan", "warning")
        self.btn_refresh.clicked.connect(self.load_themes)
        self.btn_import.clicked.connect(self.import_theme)
        top_l.addWidget(self.btn_refresh)
        top_l.addWidget(self.btn_import)
        top_l.addWidget(self.btn_health)
        outer.addWidget(top)

        mid = QHBoxLayout()
        self.theme_list = QListWidget()
        self.theme_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.theme_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.theme_list.customContextMenuRequested.connect(self.open_theme_context_menu)
        mid.addWidget(self.theme_list, 2)

        right = QVBoxLayout()
        self.btn_run_selected = ModernButton("Run Selected", "primary")
        self.btn_run_all = ModernButton("Run All", "success")
        self.btn_stop = ModernButton("Stop All Conky", "danger")
        self.btn_repair = ModernButton("Smart Repair", "success")
        self.btn_preview = ModernButton("Preview (5s)", "warning")
        self.btn_edit = ModernButton("Edit Theme", "primary")
        self.btn_open_folder = ModernButton("Open Theme Folder", "primary")
        self.btn_open_log = ModernButton("Open Log File", "primary")
        self.btn_open_opt = ModernButton("Open Optimized Folder", "warning")
        for b in (
            self.btn_run_selected,
            self.btn_run_all,
            self.btn_stop,
            self.btn_repair,
            self.btn_preview,
            self.btn_edit,
            self.btn_open_folder,
            self.btn_open_log,
            self.btn_open_opt,
        ):
            right.addWidget(b)
        right.addStretch()
        mid.addLayout(right, 1)
        outer.addLayout(mid, 1)

        self.btn_run_selected.clicked.connect(self.run_selected)
        self.btn_run_all.clicked.connect(self.run_all)
        self.btn_stop.clicked.connect(self.stop_all)
        self.btn_repair.clicked.connect(self.smart_repair)
        self.btn_preview.clicked.connect(self.preview_selected)
        self.btn_edit.clicked.connect(self.edit_selected_theme)
        self.btn_open_folder.clicked.connect(self.open_selected_theme_folder)
        self.btn_open_log.clicked.connect(lambda: subprocess.Popen(["xdg-open", str(LOG_FILE)]))
        self.btn_open_opt.clicked.connect(lambda: subprocess.Popen(["xdg-open", str(OPTIMIZED_DIR)]))
        self.btn_health.clicked.connect(self.health_scan)

        self.tabs.addTab(tab, "Themes")

    def build_tab_profiles(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setSpacing(10)

        top = ModernCard()
        top_l = QHBoxLayout(top)
        top_l.setContentsMargins(12, 10, 12, 10)
        top_l.addWidget(QLabel("Profile name:"))
        self.profile_name = QLineEdit(self.profiles.get("last_profile", ""))
        self.profile_name.setPlaceholderText("My profile name...")
        top_l.addWidget(self.profile_name, 1)
        outer.addWidget(top)

        mid = QHBoxLayout()
        self.profile_list = QListWidget()
        mid.addWidget(self.profile_list, 2)

        right = QVBoxLayout()
        self.btn_profile_save = ModernButton("Save Profile (Selected Themes)", "success")
        self.btn_profile_add = ModernButton("Add Selected Themes to Profile", "warning")
        self.btn_profile_run = ModernButton("Run Profile", "primary")
        self.btn_autostart_on = ModernButton("Enable Autostart (Profile)", "warning")
        self.btn_autostart_off = ModernButton("Disable Autostart", "danger")
        self.btn_profile_delete = ModernButton("Delete Profile", "danger")
        self.btn_profile_reload = ModernButton("Reload Profiles", "warning")
        for b in (
            self.btn_profile_save,
            self.btn_profile_add,
            self.btn_profile_run,
            self.btn_autostart_on,
            self.btn_autostart_off,
            self.btn_profile_delete,
            self.btn_profile_reload,
        ):
            right.addWidget(b)
        right.addStretch()
        mid.addLayout(right, 1)
        outer.addLayout(mid, 1)

        self.btn_profile_save.clicked.connect(self.save_profile)
        self.btn_profile_add.clicked.connect(self.add_to_profile)
        self.btn_profile_run.clicked.connect(self.run_profile)
        self.btn_profile_delete.clicked.connect(self.delete_profile)
        self.btn_profile_reload.clicked.connect(self.refresh_profiles)
        self.btn_autostart_on.clicked.connect(self.enable_autostart)
        self.btn_autostart_off.clicked.connect(self.disable_autostart)

        details = ModernCard()
        details_l = QVBoxLayout(details)
        details_l.setContentsMargins(12, 10, 12, 10)
        self.profile_details_title = QLabel("Profile contents:")
        self.profile_details_title.setStyleSheet(f"color:{COLORS['text_muted']};")
        self.profile_details = QListWidget()
        details_l.addWidget(self.profile_details_title)
        details_l.addWidget(self.profile_details)
        outer.addWidget(details)
        self.profile_list.currentItemChanged.connect(lambda *_: self.show_profile_details())

        self.tabs.addTab(tab, "Profiles")

    def build_tab_diagnostics(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setSpacing(10)

        top = ModernCard()
        top_l = QHBoxLayout(top)
        top_l.setContentsMargins(12, 10, 12, 10)
        self.btn_validate = ModernButton("Validate Selected Theme", "primary")
        self.btn_log_refresh = ModernButton("Refresh Log View", "warning")
        top_l.addWidget(self.btn_validate)
        top_l.addWidget(self.btn_log_refresh)
        top_l.addStretch()
        outer.addWidget(top)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        outer.addWidget(self.log_view, 1)

        self.btn_validate.clicked.connect(self.validate_selected_theme)
        self.btn_log_refresh.clicked.connect(self.refresh_log_view)

        self.tabs.addTab(tab, "Diagnostics")

    def build_tab_settings(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        outer.setSpacing(10)

        header = ModernCard()
        header_l = QVBoxLayout(header)
        header_l.setContentsMargins(12, 10, 12, 10)
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        hint = QLabel("Professional runtime settings for KDE compatibility and performance.")
        hint.setStyleSheet(f"color:{COLORS['text_muted']};")
        header_l.addWidget(title)
        header_l.addWidget(hint)
        outer.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        outer.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        body_l = QVBoxLayout(body)
        body_l.setSpacing(10)
        body_l.setContentsMargins(0, 0, 0, 0)

        # --- Window / Layer card ---
        card_window = ModernCard()
        cw_l = QVBoxLayout(card_window)
        cw_l.setContentsMargins(12, 12, 12, 12)
        cw_title = QLabel("Window behavior")
        cw_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        cw_desc = QLabel("Controls how Conky integrates with KDE Plasma windows.")
        cw_desc.setStyleSheet(f"color:{COLORS['text_muted']};")
        cw_l.addWidget(cw_title)
        cw_l.addWidget(cw_desc)

        form1 = QFormLayout()
        form1.setLabelAlignment(Qt.AlignLeft)
        form1.setFormAlignment(Qt.AlignTop)
        form1.setHorizontalSpacing(14)
        form1.setVerticalSpacing(10)

        self.combo_layer = QComboBox()
        self.combo_layer.addItem("Above windows (overlay)", "above")
        self.combo_layer.addItem("Below windows (background)", "below")
        current_layer = self.settings.get("layer", "above")
        for i in range(self.combo_layer.count()):
            if self.combo_layer.itemData(i) == current_layer:
                self.combo_layer.setCurrentIndex(i)
                break
        self.combo_layer.setToolTip("Above is best for always-visible widgets. Below is best for wallpaper-like setups.")

        self.combo_window_type = QComboBox()
        self.combo_window_type.addItem("Dock (recommended)", "dock")
        self.combo_window_type.addItem("Desktop", "desktop")
        current_type = self.settings.get("window_type", "dock")
        for i in range(self.combo_window_type.count()):
            if self.combo_window_type.itemData(i) == current_type:
                self.combo_window_type.setCurrentIndex(i)
                break
        self.combo_window_type.setToolTip("Dock is usually best on KDE. Desktop may behave differently per compositor/session.")

        form1.addRow("Layer:", self.combo_layer)
        form1.addRow("Window type:", self.combo_window_type)
        cw_l.addLayout(form1)
        body_l.addWidget(card_window)

        # --- Performance card ---
        card_perf = ModernCard()
        cp_l = QVBoxLayout(card_perf)
        cp_l.setContentsMargins(12, 12, 12, 12)
        cp_title = QLabel("Performance")
        cp_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        cp_desc = QLabel("Reduce lag and keep KDE responsive while Conky is running.")
        cp_desc.setStyleSheet(f"color:{COLORS['text_muted']};")
        cp_l.addWidget(cp_title)
        cp_l.addWidget(cp_desc)

        form2 = QFormLayout()
        form2.setHorizontalSpacing(14)
        form2.setVerticalSpacing(10)

        self.combo_smooth = QComboBox()
        self.combo_smooth.addItem("Ultra smooth (less CPU)", "ultra")
        self.combo_smooth.addItem("Balanced", "balanced")
        self.combo_smooth.addItem("Performance (faster updates)", "performance")
        current_smooth = self.settings.get("smoothness", "balanced")
        for i in range(self.combo_smooth.count()):
            if self.combo_smooth.itemData(i) == current_smooth:
                self.combo_smooth.setCurrentIndex(i)
                break
        self.combo_smooth.setToolTip("Changes update interval and averaging to prioritize smoothness or faster refresh.")

        self.spin_nice = QSpinBox()
        self.spin_nice.setRange(-5, 19)
        self.spin_nice.setValue(int(self.settings.get("nice_level", 10)))
        self.spin_nice.setToolTip("Higher = lower priority (less impact). Lower = more responsive but may stutter KDE.")

        self.spin_max = QSpinBox()
        self.spin_max.setRange(1, 6)
        self.spin_max.setValue(int(self.settings.get("max_instances", 1)))
        self.spin_max.setToolTip("How many Conky instances can run at once. 1 is safest for stability.")

        self.spin_health = QDoubleSpinBox()
        self.spin_health.setRange(0.4, 5.0)
        self.spin_health.setSingleStep(0.1)
        self.spin_health.setValue(float(self.settings.get("healthcheck_seconds", 1.2)))
        self.spin_health.setToolTip("Wait time to decide if Conky started successfully.")

        form2.addRow("Smoothness mode:", self.combo_smooth)
        form2.addRow("Nice level:", self.spin_nice)
        form2.addRow("Max instances:", self.spin_max)
        form2.addRow("Healthcheck (sec):", self.spin_health)
        cp_l.addLayout(form2)
        body_l.addWidget(card_perf)

        # --- Preview / Tools card ---
        card_tools = ModernCard()
        ct_l = QVBoxLayout(card_tools)
        ct_l.setContentsMargins(12, 12, 12, 12)
        ct_title = QLabel("Preview & tools")
        ct_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        ct_desc = QLabel("Preview a theme temporarily without committing to a full run.")
        ct_desc.setStyleSheet(f"color:{COLORS['text_muted']};")
        ct_l.addWidget(ct_title)
        ct_l.addWidget(ct_desc)

        form3 = QFormLayout()
        form3.setHorizontalSpacing(14)
        form3.setVerticalSpacing(10)

        self.spin_preview = QSpinBox()
        self.spin_preview.setRange(2, 60)
        self.spin_preview.setValue(int(self.settings.get("preview_seconds", 5)))
        self.spin_preview.setToolTip("Preview duration in seconds (temporary run, then stop).")
        form3.addRow("Preview seconds:", self.spin_preview)
        ct_l.addLayout(form3)
        body_l.addWidget(card_tools)

        body_l.addStretch()

        # Bottom action bar
        actions = ModernCard()
        actions_l = QHBoxLayout(actions)
        actions_l.setContentsMargins(12, 10, 12, 10)
        self.btn_reset_settings = ModernButton("Reset to Defaults", "warning")
        self.btn_apply_settings = ModernButton("Apply", "primary")
        self.btn_save_settings = ModernButton("Save Settings", "success")
        actions_l.addWidget(self.btn_reset_settings)
        actions_l.addStretch()
        actions_l.addWidget(self.btn_apply_settings)
        actions_l.addWidget(self.btn_save_settings)
        outer.addWidget(actions)

        self.btn_apply_settings.clicked.connect(self.save_settings)
        self.btn_save_settings.clicked.connect(self.save_settings)
        self.btn_reset_settings.clicked.connect(self.reset_settings_ui)

        self.tabs.addTab(tab, "Settings")

    def reset_settings_ui(self):
        self.settings = dict(DEFAULT_SETTINGS)

        # Layer
        for i in range(self.combo_layer.count()):
            if self.combo_layer.itemData(i) == self.settings.get("layer"):
                self.combo_layer.setCurrentIndex(i)
                break
        # Window type
        for i in range(self.combo_window_type.count()):
            if self.combo_window_type.itemData(i) == self.settings.get("window_type"):
                self.combo_window_type.setCurrentIndex(i)
                break
        # Smoothness
        for i in range(self.combo_smooth.count()):
            if self.combo_smooth.itemData(i) == self.settings.get("smoothness"):
                self.combo_smooth.setCurrentIndex(i)
                break

        self.spin_nice.setValue(int(self.settings.get("nice_level", 10)))
        self.spin_max.setValue(int(self.settings.get("max_instances", 1)))
        self.spin_health.setValue(float(self.settings.get("healthcheck_seconds", 1.2)))
        self.spin_preview.setValue(int(self.settings.get("preview_seconds", 5)))
        self.statusBar().showMessage("Settings reset (not saved).")

    # ---------------- Actions ----------------
    def set_busy(self, busy: bool):
        for btn in (
            self.btn_run_selected,
            self.btn_run_all,
            self.btn_refresh,
            self.btn_import,
            self.btn_repair,
            self.btn_profile_save,
            self.btn_profile_run,
            self.btn_profile_delete,
            self.btn_autostart_on,
            self.btn_autostart_off,
            self.btn_save_settings,
            self.btn_validate,
            self.btn_health,
            self.btn_preview,
            self.btn_edit,
            self.btn_open_folder,
            self.btn_profile_add,
        ):
            btn.setEnabled(not busy)

    def load_themes(self):
        self.themes = [ThemeItem(p) for p in find_themes()]
        self.apply_filter()
        self.statusBar().showMessage(f"Loaded {len(self.themes)} valid theme(s).")

    def apply_filter(self):
        q = self.filter_edit.text().strip().lower() if hasattr(self, "filter_edit") else ""
        self.filtered = [t for t in self.themes if q in t.label.lower()]
        self.theme_list.clear()
        for item in self.filtered:
            lw = QListWidgetItem(item.label)
            status = self.theme_status.get(item.label, "")
            if status == "stable":
                lw.setForeground(QColor(COLORS["success"]))
            elif status == "needs_fix":
                lw.setForeground(QColor(COLORS["warning"]))
            elif status == "broken":
                lw.setForeground(QColor(COLORS["danger"]))
            self.theme_list.addItem(lw)

    def selected_theme_paths(self):
        paths: list[Path] = []
        for it in self.theme_list.selectedItems():
            label = it.text()
            for theme in self.filtered:
                if theme.label == label:
                    paths.append(theme.path)
                    break
        return paths

    def _selected_theme_item(self):
        items = self.theme_list.selectedItems()
        if not items:
            return None
        label = items[0].text()
        for theme in self.filtered:
            if theme.label == label:
                return theme
        return None

    def open_theme_context_menu(self, pos):
        theme = self._selected_theme_item()
        if not theme:
            return
        menu = QMenu(self)
        act_open = QAction("Open theme file", self)
        act_edit = QAction("Edit theme file", self)
        act_folder = QAction("Open containing folder", self)
        act_validate = QAction("Validate (original + optimized)", self)
        act_preview = QAction("Preview (temporary)", self)
        act_open_opt = QAction("Open optimized file", self)

        act_open.triggered.connect(lambda: subprocess.Popen(["xdg-open", str(theme.path)]))
        act_edit.triggered.connect(lambda: subprocess.Popen(["xdg-open", str(theme.path)]))
        act_folder.triggered.connect(lambda: subprocess.Popen(["xdg-open", str(theme.path.parent)]))
        act_validate.triggered.connect(self.validate_selected_theme)
        act_preview.triggered.connect(self.preview_selected)
        act_open_opt.triggered.connect(lambda: subprocess.Popen(["xdg-open", str(optimize_for_kde(theme.path))]))

        for a in (act_open, act_edit, act_folder):
            menu.addAction(a)
        menu.addSeparator()
        menu.addAction(act_open_opt)
        menu.addSeparator()
        menu.addAction(act_validate)
        menu.addAction(act_preview)
        menu.exec_(self.theme_list.mapToGlobal(pos))

    def edit_selected_theme(self):
        theme = self._selected_theme_item()
        if not theme:
            QMessageBox.information(self, "Info", "Select a theme first.")
            return
        subprocess.Popen(["xdg-open", str(theme.path)])

    def open_selected_theme_folder(self):
        theme = self._selected_theme_item()
        if not theme:
            QMessageBox.information(self, "Info", "Select a theme first.")
            return
        subprocess.Popen(["xdg-open", str(theme.path.parent)])

    def preview_selected(self):
        theme = self._selected_theme_item()
        if not theme:
            QMessageBox.information(self, "Info", "Select a theme first.")
            return
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Please wait until the current operation finishes.")
            return

        seconds = int(load_json(SETTINGS_FILE, DEFAULT_SETTINGS).get("preview_seconds", 5))
        try:
            kill_running_conky()
            pid, _, mode = run_conky(theme.path)
        except Exception as exc:
            QMessageBox.critical(self, "Preview Error", str(exc))
            return

        self.statusBar().showMessage(f"Preview started ({seconds}s): {theme.path.name} [{mode}]")
        if self.preview_timer:
            self.preview_timer.stop()
        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(lambda: self._stop_preview(pid))
        self.preview_timer.start(seconds * 1000)

    def _stop_preview(self, pid: int):
        try:
            os.kill(pid, 15)
        except Exception:
            pass
        kill_running_conky()
        self.statusBar().showMessage("Preview stopped.")

    def run_selected(self):
        themes = self.selected_theme_paths()
        if not themes:
            QMessageBox.information(self, "Info", "Select at least one theme.")
            return
        self.run_themes(themes)

    def run_all(self):
        if not self.themes:
            QMessageBox.information(self, "Info", "No valid themes found.")
            return
        self.run_themes([t.path for t in self.themes])

    def run_themes(self, themes: list[Path]):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Please wait until the current operation finishes.")
            return

        self.set_busy(True)
        self.statusBar().showMessage("Starting themes...")

        worker = ThemeRunnerWorker(themes)
        worker.log.connect(self.append_log)
        worker.finished.connect(self.on_run_finished)
        self.worker = worker
        worker.start()

    def on_run_finished(self, started: int, fallback: int, limited_to: int):
        self.set_busy(False)
        self.statusBar().showMessage(f"Started {started} theme(s). Fallback used: {fallback}. Limited to {limited_to}.")
        self.refresh_log_view()

    def smart_repair(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Please wait until the current operation finishes.")
            return
        self.set_busy(True)
        self.statusBar().showMessage("Running smart repair...")

        worker = RepairWorker([t.path for t in self.themes])
        worker.log.connect(self.append_log)
        worker.finished.connect(self.on_repair_finished)
        self.worker = worker
        worker.start()

    def on_repair_finished(self, ok: int, fail: int):
        self.set_busy(False)
        self.statusBar().showMessage(f"Smart repair complete. Success: {ok}, Failed: {fail}.")
        QMessageBox.information(self, "Repair", f"Optimized {ok} theme(s), failed {fail}.")

    def stop_all(self):
        kill_running_conky()
        self.statusBar().showMessage("Stopped all running Conky instances.")

    def import_theme(self):
        folder = QFileDialog.getExistingDirectory(self, "Import Theme Folder", str(HOME))
        if not folder:
            return
        source = Path(folder)
        destination = THEME_DIRS[0] / source.name
        try:
            if destination.exists():
                reply = QMessageBox.question(
                    self,
                    "Overwrite",
                    f"'{destination.name}' exists. Replace it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if reply != QMessageBox.Yes:
                    return
                shutil.rmtree(destination)
            shutil.copytree(source, destination)
            self.load_themes()
        except Exception as exc:
            QMessageBox.critical(self, "Import Error", str(exc))

    # -------- Profiles --------
    def refresh_profiles(self):
        self.profiles = load_json(PROFILES_FILE, {"profiles": {}, "last_profile": ""})
        self.profile_list.clear()
        for name in sorted(self.profiles.get("profiles", {}).keys()):
            self.profile_list.addItem(name)
        self.show_profile_details()

    def selected_profile_name(self):
        item = self.profile_list.currentItem()
        return item.text() if item else ""

    def save_profile(self):
        name = self.profile_name.text().strip()
        if not name:
            QMessageBox.critical(self, "Error", "Enter a profile name.")
            return
        themes = self.selected_theme_paths()
        if not themes:
            QMessageBox.critical(self, "Error", "Select at least one theme in Themes tab.")
            return
        self.profiles.setdefault("profiles", {})[name] = [str(p) for p in themes]
        self.profiles["last_profile"] = name
        save_json(PROFILES_FILE, self.profiles)
        self.refresh_profiles()
        self.statusBar().showMessage(f"Saved profile: {name}")

    def add_to_profile(self):
        name = self.selected_profile_name() or self.profile_name.text().strip()
        if not name:
            QMessageBox.critical(self, "Error", "Select a profile first.")
            return
        if name not in self.profiles.get("profiles", {}):
            QMessageBox.critical(self, "Error", f"Profile not found: {name}")
            return
        themes = self.selected_theme_paths()
        if not themes:
            QMessageBox.critical(self, "Error", "Select themes in Themes tab first.")
            return
        current = set(self.profiles.get("profiles", {}).get(name, []))
        for t in themes:
            current.add(str(t))
        self.profiles["profiles"][name] = sorted(current)
        save_json(PROFILES_FILE, self.profiles)
        self.refresh_profiles()
        self.statusBar().showMessage(f"Updated profile: {name} (+{len(themes)})")

    def show_profile_details(self):
        if not hasattr(self, "profile_details"):
            return
        name = self.selected_profile_name() or self.profile_name.text().strip()
        self.profile_details.clear()
        if not name:
            self.profile_details_title.setText("Profile contents: (no profile selected)")
            return
        items = self.profiles.get("profiles", {}).get(name, [])
        self.profile_details_title.setText(f"Profile contents: {name} ({len(items)} theme(s))")
        for p in items:
            self.profile_details.addItem(p)

    def delete_profile(self):
        name = self.selected_profile_name()
        if not name:
            return
        reply = QMessageBox.question(self, "Delete", f"Delete profile '{name}'?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        self.profiles.get("profiles", {}).pop(name, None)
        save_json(PROFILES_FILE, self.profiles)
        self.refresh_profiles()

    def run_profile(self):
        name = self.selected_profile_name() or self.profile_name.text().strip()
        if not name:
            QMessageBox.critical(self, "Error", "Select a profile.")
            return
        theme_paths = self.profiles.get("profiles", {}).get(name)
        if not theme_paths:
            QMessageBox.critical(self, "Error", f"Profile not found: {name}")
            return
        themes = [Path(p) for p in theme_paths if Path(p).exists()]
        if not themes:
            QMessageBox.critical(self, "Error", "No existing themes in this profile.")
            return
        self.profiles["last_profile"] = name
        save_json(PROFILES_FILE, self.profiles)
        self.run_themes(themes)

    def enable_autostart(self):
        name = self.selected_profile_name() or self.profile_name.text().strip()
        if not name:
            QMessageBox.critical(self, "Error", "Select a profile first.")
            return
        if name not in self.profiles.get("profiles", {}):
            QMessageBox.critical(self, "Error", f"Profile not found: {name}")
            return
        AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
        exec_path = str(Path(__file__).resolve())
        desktop = "\n".join(
            [
                "[Desktop Entry]",
                "Type=Application",
                f"Name={APP_NAME}",
                "Comment=Start Conky profile on login",
                f'Exec=python "{exec_path}" --run-profile "{name}"',
                "X-KDE-autostart-after=panel",
                "X-KDE-StartupNotify=false",
                "Terminal=false",
                "",
            ]
        )
        try:
            AUTOSTART_FILE.write_text(desktop, encoding="utf-8")
            QMessageBox.information(self, "Autostart", f"Enabled autostart for profile: {name}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to enable autostart: {exc}")

    def disable_autostart(self):
        try:
            if AUTOSTART_FILE.exists():
                AUTOSTART_FILE.unlink()
            QMessageBox.information(self, "Autostart", "Autostart disabled.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to disable autostart: {exc}")

    # -------- Settings --------
    def save_settings(self):
        self.settings = {
            "layer": self.combo_layer.currentData(),
            "window_type": self.combo_window_type.currentData(),
            "smoothness": self.combo_smooth.currentData(),
            "nice_level": int(self.spin_nice.value()),
            "max_instances": int(self.spin_max.value()),
            "healthcheck_seconds": float(self.spin_health.value()),
            "preview_seconds": int(self.spin_preview.value()),
        }
        save_json(SETTINGS_FILE, self.settings)
        self.statusBar().showMessage("Settings saved.")

    # -------- Diagnostics --------
    def validate_selected_theme(self):
        themes = self.selected_theme_paths()
        if not themes:
            QMessageBox.information(self, "Info", "Select a theme in Themes tab first.")
            return
        cfg = themes[0]
        ok_original = validate_conky_config(cfg)
        optimized = optimize_for_kde(cfg)
        ok_opt = validate_conky_config(optimized)
        QMessageBox.information(
            self,
            "Validation",
            f"Theme: {cfg.name}\nOriginal: {'OK' if ok_original else 'FAIL'}\nOptimized: {'OK' if ok_opt else 'FAIL'}",
        )

    def refresh_log_view(self, lines: int = 250):
        try:
            text = LOG_FILE.read_text(encoding="utf-8", errors="ignore")
            tail = "\n".join(text.splitlines()[-lines:])
        except Exception:
            tail = "(Log file not available yet.)"
        self.log_view.setPlainText(tail)

    def append_log(self, line: str):
        self.log_view.append(line)

    def health_scan(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "Busy", "Please wait until the current operation finishes.")
            return
        self.set_busy(True)
        self.statusBar().showMessage("Health scan running...")

        worker = ThemeHealthWorker(self.themes)
        worker.progress.connect(lambda msg: self.statusBar().showMessage(msg))
        worker.item_status.connect(self._set_theme_status)
        worker.finished.connect(self._health_scan_finished)
        self.worker = worker
        worker.start()

    def _set_theme_status(self, label: str, status: str):
        self.theme_status[label] = status

    def _health_scan_finished(self, ok: int, warn: int, bad: int):
        self.set_busy(False)
        self.apply_filter()
        self.statusBar().showMessage(f"Health scan complete. Stable: {ok}, Needs fix: {warn}, Broken: {bad}.")


def run_profile_cli(profile_name: str):
    if not is_conky_installed():
        return 1
    profiles = load_json(PROFILES_FILE, {"profiles": {}})
    theme_paths = profiles.get("profiles", {}).get(profile_name, [])
    themes = [Path(p) for p in theme_paths if Path(p).exists()]
    if not themes:
        return 1
    kill_running_conky()
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    max_instances = int(settings.get("max_instances", 1))
    for theme in themes[:max_instances]:
        try:
            run_conky(theme)
        except Exception:
            pass
    return 0


def main():
    if "--run-profile" in sys.argv:
        try:
            idx = sys.argv.index("--run-profile")
            profile_name = sys.argv[idx + 1]
        except Exception:
            return 1
        return run_profile_cli(profile_name)

    if not is_conky_installed():
        print("Conky is not installed. Install it first, then run this app again.")
        return 1

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName(APP_NAME)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
