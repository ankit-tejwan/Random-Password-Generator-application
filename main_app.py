"""
Password Locker - Beautiful & Clean Desktop Application
Theme: Light Pink & Magenta
Powered by Qt (PySide6 / PyQt6)
"""

import sys
import os
import string
import secrets
import math
import platform
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# Dual support for PySide6 and PyQt6 with graceful error handling
try:
    from PySide6.QtCore import Qt, QTimer, QSize
    from PySide6.QtGui import QFont, QIcon, QColor, QPalette, QPixmap, QKeySequence, QShortcut
    from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QGridLayout,
        QLabel,
        QPushButton,
        QSlider,
        QRadioButton,
        QButtonGroup,
        QCheckBox,
        QLineEdit,
        QProgressBar,
        QFrame,
        QMessageBox,
        QDialog,
        QListWidget,
        QListWidgetItem,
        QScrollArea,
        QGraphicsDropShadowEffect,
        QComboBox,
    )
    QT_BINDING = "PySide6"
except ImportError:
    try:
        from PyQt6.QtCore import Qt, QTimer, QSize
        from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QPixmap, QKeySequence, QShortcut
        from PyQt6.QtWidgets import (
            QApplication,
            QMainWindow,
            QWidget,
            QVBoxLayout,
            QHBoxLayout,
            QGridLayout,
            QLabel,
            QPushButton,
            QSlider,
            QRadioButton,
            QButtonGroup,
            QCheckBox,
            QLineEdit,
            QProgressBar,
            QFrame,
            QMessageBox,
            QDialog,
            QListWidget,
            QListWidgetItem,
            QScrollArea,
            QGraphicsDropShadowEffect,
            QComboBox,
        )
        QT_BINDING = "PyQt6"
    except ImportError:
        print("=" * 64, file=sys.stderr)
        print("Error: PySide6 or PyQt6 is required to run Password Locker.", file=sys.stderr)
        print("Please install dependencies by running:", file=sys.stderr)
        print("    pip install -r requirements.txt", file=sys.stderr)
        print("or directly:", file=sys.stderr)
        print("    pip install PySide6", file=sys.stderr)
        print("=" * 64, file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------
# THEMES CONFIGURATION (1. Pink, 2. Purple, 3. Ocean Blue, 4. Warm Night)
# ---------------------------------------------------------
LOG_FILE_NAME = "password_history.log"

THEMES = {
    "pink": {
        "name": "Pink",
        "display": "🌸 Pink",
        "canvas_bg": "#FFF5F9",
        "card_bg": "#FFFFFF",
        "card_border": "#F3CFE1",
        "subcard_bg": "#FFF9FC",
        "subcard_border": "#F7E1ED",
        "text_main": "#2B1625",
        "header_title": "#C2185B",
        "header_subtitle": "#8C627D",
        "section_heading": "#9C276A",
        "badge_bg": "#FCE4EC",
        "badge_text": "#C2185B",
        "badge_border": "#F8BBD0",
        "pwd_bg": "#FFF0F5",
        "pwd_text": "#C2185B",
        "pwd_border": "#F48FB1",
        "pwd_focus_border": "#D81B60",
        "pwd_selection": "#E91E63",
        "btn_primary_grad_start": "#E91E63",
        "btn_primary_grad_end": "#D81B60",
        "btn_primary_hover_start": "#F06292",
        "btn_primary_hover_end": "#E91E63",
        "btn_primary_pressed": "#C2185B",
        "btn_copy_bg": "#FCE4EC",
        "btn_copy_text": "#C2185B",
        "btn_copy_border": "#F48FB1",
        "btn_copy_hover_bg": "#F8BBD0",
        "btn_copy_hover_text": "#880E4F",
        "btn_copy_hover_border": "#EC407A",
        "btn_copy_pressed": "#F48FB1",
        "btn_secondary_bg": "#FFFFFF",
        "btn_secondary_text": "#7A586E",
        "btn_secondary_border": "#E5C3D6",
        "btn_secondary_hover_bg": "#FFF0F6",
        "btn_secondary_hover_text": "#C2185B",
        "btn_secondary_hover_border": "#F06292",
        "radio_hover_bg": "#FFF0F6",
        "indicator_border": "#F06292",
        "indicator_checked": "#D81B60",
        "slider_groove": "#F8BBD0",
        "slider_subpage_start": "#F06292",
        "slider_subpage_end": "#D81B60",
        "slider_handle_border": "#D81B60",
        "slider_handle_hover": "#FCE4EC",
        "strength_bg": "#F8E2ED",
        "strength_text_default": "#8C627D",
        "scrollbar_bg": "#FFF5F9",
        "scrollbar_handle": "#F48FB1",
        "scrollbar_handle_hover": "#D81B60",
        "shadow_rgba": (233, 30, 99, 25),
        "combo_bg": "#FFFFFF",
        "combo_border": "#E5C3D6",
        "combo_text": "#7A586E",
    },
    "purple": {
        "name": "Purple",
        "display": "💜 Purple",
        "canvas_bg": "#F8F4FD",
        "card_bg": "#FFFFFF",
        "card_border": "#E1D5F5",
        "subcard_bg": "#FAF6FE",
        "subcard_border": "#EFE7FB",
        "text_main": "#231535",
        "header_title": "#7B1FA2",
        "header_subtitle": "#6E5587",
        "section_heading": "#7B1FA2",
        "badge_bg": "#EDE7F6",
        "badge_text": "#6A1B9A",
        "badge_border": "#D1C4E9",
        "pwd_bg": "#F9F5FD",
        "pwd_text": "#5E178C",
        "pwd_border": "#CE93D8",
        "pwd_focus_border": "#7B1FA2",
        "pwd_selection": "#8E24AA",
        "btn_primary_grad_start": "#8E24AA",
        "btn_primary_grad_end": "#6A1B9A",
        "btn_primary_hover_start": "#AB47BC",
        "btn_primary_hover_end": "#8E24AA",
        "btn_primary_pressed": "#4A148C",
        "btn_copy_bg": "#EDE7F6",
        "btn_copy_text": "#6A1B9A",
        "btn_copy_border": "#CE93D8",
        "btn_copy_hover_bg": "#E1BEE7",
        "btn_copy_hover_text": "#4A148C",
        "btn_copy_hover_border": "#BA68C8",
        "btn_copy_pressed": "#CE93D8",
        "btn_secondary_bg": "#FFFFFF",
        "btn_secondary_text": "#5E4B72",
        "btn_secondary_border": "#D7C7EB",
        "btn_secondary_hover_bg": "#F3EBF9",
        "btn_secondary_hover_text": "#6A1B9A",
        "btn_secondary_hover_border": "#AB47BC",
        "radio_hover_bg": "#F3EBF9",
        "indicator_border": "#AB47BC",
        "indicator_checked": "#7B1FA2",
        "slider_groove": "#D1C4E9",
        "slider_subpage_start": "#AB47BC",
        "slider_subpage_end": "#7B1FA2",
        "slider_handle_border": "#7B1FA2",
        "slider_handle_hover": "#EDE7F6",
        "strength_bg": "#EDE7F6",
        "strength_text_default": "#6E5587",
        "scrollbar_bg": "#F8F4FD",
        "scrollbar_handle": "#CE93D8",
        "scrollbar_handle_hover": "#7B1FA2",
        "shadow_rgba": (123, 31, 162, 28),
        "combo_bg": "#FFFFFF",
        "combo_border": "#D7C7EB",
        "combo_text": "#5E4B72",
    },
    "ocean_blue": {
        "name": "Ocean Blue",
        "display": "🌊 Ocean Blue",
        "canvas_bg": "#F0F8FF",
        "card_bg": "#FFFFFF",
        "card_border": "#CFE4F5",
        "subcard_bg": "#F6FBFF",
        "subcard_border": "#DCEBFA",
        "text_main": "#0D2236",
        "header_title": "#0277BD",
        "header_subtitle": "#486581",
        "section_heading": "#0288D1",
        "badge_bg": "#E1F5FE",
        "badge_text": "#0277BD",
        "badge_border": "#B3E5FC",
        "pwd_bg": "#F4FAFD",
        "pwd_text": "#01579B",
        "pwd_border": "#81D4FA",
        "pwd_focus_border": "#0288D1",
        "pwd_selection": "#0288D1",
        "btn_primary_grad_start": "#0288D1",
        "btn_primary_grad_end": "#01579B",
        "btn_primary_hover_start": "#29B6F6",
        "btn_primary_hover_end": "#0288D1",
        "btn_primary_pressed": "#004377",
        "btn_copy_bg": "#E1F5FE",
        "btn_copy_text": "#0277BD",
        "btn_copy_border": "#81D4FA",
        "btn_copy_hover_bg": "#B3E5FC",
        "btn_copy_hover_text": "#013A63",
        "btn_copy_hover_border": "#29B6F6",
        "btn_copy_pressed": "#81D4FA",
        "btn_secondary_bg": "#FFFFFF",
        "btn_secondary_text": "#486581",
        "btn_secondary_border": "#C9DDF0",
        "btn_secondary_hover_bg": "#EBF6FD",
        "btn_secondary_hover_text": "#0277BD",
        "btn_secondary_hover_border": "#29B6F6",
        "radio_hover_bg": "#EBF6FD",
        "indicator_border": "#29B6F6",
        "indicator_checked": "#0288D1",
        "slider_groove": "#B3E5FC",
        "slider_subpage_start": "#29B6F6",
        "slider_subpage_end": "#0288D1",
        "slider_handle_border": "#0288D1",
        "slider_handle_hover": "#E1F5FE",
        "strength_bg": "#DDF0FB",
        "strength_text_default": "#486581",
        "scrollbar_bg": "#F0F8FF",
        "scrollbar_handle": "#81D4FA",
        "scrollbar_handle_hover": "#0288D1",
        "shadow_rgba": (2, 136, 209, 25),
        "combo_bg": "#FFFFFF",
        "combo_border": "#C9DDF0",
        "combo_text": "#486581",
    },
    "warm_night": {
        "name": "Warm Night",
        "display": "🌙 Warm Night",
        "canvas_bg": "#181513",
        "card_bg": "#241F1C",
        "card_border": "#38312B",
        "subcard_bg": "#2A2420",
        "subcard_border": "#403730",
        "text_main": "#F5EDE4",
        "header_title": "#FFA726",
        "header_subtitle": "#A8998C",
        "section_heading": "#FFB74D",
        "badge_bg": "#36291E",
        "badge_text": "#FFB74D",
        "badge_border": "#5E442B",
        "pwd_bg": "#1C1815",
        "pwd_text": "#FFCC80",
        "pwd_border": "#5E442B",
        "pwd_focus_border": "#FFA726",
        "pwd_selection": "#E65100",
        "btn_primary_grad_start": "#F57C00",
        "btn_primary_grad_end": "#E65100",
        "btn_primary_hover_start": "#FFA726",
        "btn_primary_hover_end": "#F57C00",
        "btn_primary_pressed": "#BF360C",
        "btn_copy_bg": "#36291E",
        "btn_copy_text": "#FFB74D",
        "btn_copy_border": "#5E442B",
        "btn_copy_hover_bg": "#4A3828",
        "btn_copy_hover_text": "#FFE082",
        "btn_copy_hover_border": "#FFB74D",
        "btn_copy_pressed": "#5E442B",
        "btn_secondary_bg": "#241F1C",
        "btn_secondary_text": "#D7C7B8",
        "btn_secondary_border": "#3D352E",
        "btn_secondary_hover_bg": "#332B25",
        "btn_secondary_hover_text": "#FFA726",
        "btn_secondary_hover_border": "#FF9800",
        "radio_hover_bg": "#2E2721",
        "indicator_border": "#FFB74D",
        "indicator_checked": "#F57C00",
        "slider_groove": "#3D352E",
        "slider_subpage_start": "#FFA726",
        "slider_subpage_end": "#E65100",
        "slider_handle_border": "#FFA726",
        "slider_handle_hover": "#36291E",
        "strength_bg": "#332B25",
        "strength_text_default": "#A8998C",
        "scrollbar_bg": "#181513",
        "scrollbar_handle": "#5E442B",
        "scrollbar_handle_hover": "#FFA726",
        "shadow_rgba": (0, 0, 0, 80),
        "combo_bg": "#241F1C",
        "combo_border": "#3D352E",
        "combo_text": "#D7C7B8",
    },
}


def generate_stylesheet(theme_key: str = "pink") -> str:
    """Generates a complete, tailored Qt stylesheet for the chosen theme."""
    t = THEMES.get(theme_key, THEMES["pink"])
    return f"""
QMainWindow {{
    background-color: {t["canvas_bg"]};
}}

QWidget#CentralWidget {{
    background-color: {t["canvas_bg"]};
}}

/* Card Containers */
QFrame.CardFrame {{
    background-color: {t["card_bg"]};
    border: 1px solid {t["card_border"]};
    border-radius: 13px;
    padding: 13px;
}}

QFrame.SubCardFrame {{
    background-color: {t["subcard_bg"]};
    border: 1px solid {t["subcard_border"]};
    border-radius: 10px;
}}

/* Typography */
QLabel {{
    color: {t["text_main"]};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', 'DejaVu Sans', sans-serif;
}}

QLabel#HeaderTitle {{
    font-size: 22px;
    font-weight: 800;
    color: {t["header_title"]};
    letter-spacing: -0.4px;
}}

QLabel#HeaderSubtitle {{
    font-size: 11px;
    font-weight: 500;
    color: {t["header_subtitle"]};
}}

QLabel#SectionHeading {{
    font-size: 11px;
    font-weight: 700;
    color: {t["section_heading"]};
    text-transform: uppercase;
    letter-spacing: 0.7px;
}}

QLabel#ValueBadge {{
    background-color: {t["badge_bg"]};
    color: {t["badge_text"]};
    font-size: 13px;
    font-weight: 700;
    border-radius: 7px;
    padding: 2px 9px;
    border: 1px solid {t["badge_border"]};
}}

QLabel#ClockBadge {{
    background-color: {t["badge_bg"]};
    color: {t["badge_text"]};
    font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Monaco, Consolas, 'Ubuntu Mono', 'Liberation Mono', 'Courier New', monospace;
    font-size: 11.5px;
    font-weight: 700;
    border-radius: 8px;
    padding: 3px 9px;
    border: 1px solid {t["badge_border"]};
}}

/* Password Display LineEdit */
QLineEdit#PasswordDisplay {{
    background-color: {t["pwd_bg"]};
    color: {t["pwd_text"]};
    font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', Menlo, Monaco, Consolas, 'Ubuntu Mono', 'Liberation Mono', 'Courier New', monospace;
    font-size: 17px;
    font-weight: 700;
    border: 2px solid {t["pwd_border"]};
    border-radius: 10px;
    padding: 9px 12px;
    selection-background-color: {t["pwd_selection"]};
    selection-color: #FFFFFF;
}}

QLineEdit#PasswordDisplay:focus {{
    border: 2px solid {t["pwd_focus_border"]};
    background-color: #FFFFFF;
}}

/* Push Buttons */
QPushButton {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', 'DejaVu Sans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    border-radius: 9px;
    padding: 7px 13px;
    border: none;
}}

QPushButton#PrimaryButton {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {t["btn_primary_grad_start"]}, stop:1 {t["btn_primary_grad_end"]});
    color: #FFFFFF;
    border-radius: 10px;
    padding: 9px 16px;
    font-size: 13px;
}}

QPushButton#PrimaryButton:hover {{
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {t["btn_primary_hover_start"]}, stop:1 {t["btn_primary_hover_end"]});
}}

QPushButton#PrimaryButton:pressed {{
    background-color: {t["btn_primary_pressed"]};
}}

QPushButton#CopyButton {{
    background-color: {t["btn_copy_bg"]};
    color: {t["btn_copy_text"]};
    border: 1px solid {t["btn_copy_border"]};
    border-radius: 10px;
    padding: 9px 15px;
    font-size: 13px;
}}

QPushButton#CopyButton:hover {{
    background-color: {t["btn_copy_hover_bg"]};
    color: {t["btn_copy_hover_text"]};
    border-color: {t["btn_copy_hover_border"]};
}}

QPushButton#CopyButton:pressed {{
    background-color: {t["btn_copy_pressed"]};
}}

QPushButton#IconButton {{
    background-color: transparent;
    border: 1px solid {t["btn_secondary_border"]};
    border-radius: 8px;
    padding: 5px 9px;
    color: {t["btn_primary_grad_end"]};
    font-size: 12px;
}}

QPushButton#IconButton:hover {{
    background-color: {t["btn_copy_bg"]};
    border-color: {t["btn_copy_hover_border"]};
}}

QPushButton#SecondaryButton {{
    background-color: {t["btn_secondary_bg"]};
    color: {t["btn_secondary_text"]};
    border: 1px solid {t["btn_secondary_border"]};
    border-radius: 8px;
    padding: 6px 11px;
    font-size: 12px;
}}

QPushButton#SecondaryButton:hover {{
    background-color: {t["btn_secondary_hover_bg"]};
    color: {t["btn_secondary_hover_text"]};
    border-color: {t["btn_secondary_hover_border"]};
}}

/* Incognito Toggle Button */
QPushButton#IncognitoToggle {{
    background-color: {t["btn_secondary_bg"]};
    color: {t["btn_secondary_text"]};
    border: 1px solid {t["btn_secondary_border"]};
    border-radius: 8px;
    padding: 6px 11px;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton#IncognitoToggle:hover {{
    background-color: {t["btn_secondary_hover_bg"]};
    color: {t["btn_secondary_hover_text"]};
    border-color: {t["btn_secondary_hover_border"]};
}}

QPushButton#IncognitoToggle:checked {{
    background-color: #00BCD4;
    color: #FFFFFF;
    border: 1px solid #00ACC1;
    font-weight: 600;
}}

QPushButton#IncognitoToggle:checked:hover {{
    background-color: #00ACC1;
    color: #FFFFFF;
    border-color: #0097A7;
}}

/* Theme Selector ComboBox */
QComboBox#ThemeSelector {{
    background-color: {t["combo_bg"]};
    color: {t["combo_text"]};
    border: 1px solid {t["combo_border"]};
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 600;
    min-width: 145px;
}}

QComboBox#ThemeSelector:hover {{
    background-color: {t["btn_secondary_hover_bg"]};
    border-color: {t["btn_secondary_hover_border"]};
    color: {t["btn_secondary_hover_text"]};
}}

QComboBox#ThemeSelector::drop-down {{
    border: none;
    width: 18px;
}}

QComboBox#ThemeSelector QAbstractItemView {{
    background-color: {t["card_bg"]};
    border: 1px solid {t["card_border"]};
    border-radius: 8px;
    selection-background-color: {t["badge_bg"]};
    selection-color: {t["badge_text"]};
    color: {t["text_main"]};
    padding: 4px;
    font-size: 12px;
}}

/* Radio Buttons (Complexity Selector) */
QRadioButton {{
    font-size: 11px;
    font-weight: 600;
    color: {t["text_main"]};
    spacing: 6px;
    padding: 4px 7px;
    border-radius: 7px;
}}

QRadioButton:hover {{
    background-color: {t["radio_hover_bg"]};
}}

QRadioButton::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 8px;
    border: 2px solid {t["indicator_border"]};
    background-color: {t["card_bg"]};
}}

QRadioButton::indicator:hover {{
    border-color: {t["indicator_checked"]};
}}

QRadioButton::indicator:checked {{
    border: 4px solid {t["indicator_checked"]};
    background-color: {t["card_bg"]};
}}

/* Checkboxes */
QCheckBox {{
    font-size: 11px;
    color: {t["text_main"]};
    spacing: 6px;
}}

QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 4px;
    border: 2px solid {t["indicator_border"]};
    background-color: {t["card_bg"]};
}}

QCheckBox::indicator:hover {{
    border-color: {t["indicator_checked"]};
}}

QCheckBox::indicator:checked {{
    background-color: {t["indicator_checked"]};
    border: 2px solid {t["indicator_checked"]};
}}

/* Sliders */
QSlider::groove:horizontal {{
    height: 6px;
    background: {t["slider_groove"]};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {t["slider_subpage_start"]}, stop:1 {t["slider_subpage_end"]});
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {t["card_bg"]};
    border: 2px solid {t["slider_handle_border"]};
    width: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {t["slider_handle_hover"]};
    border-color: {t["indicator_checked"]};
}}

/* Progress Bar (Strength Meter) */
QProgressBar {{
    border: none;
    border-radius: 3px;
    background-color: {t["strength_bg"]};
    height: 6px;
    text-align: center;
}}

QProgressBar::chunk {{
    border-radius: 3px;
}}

/* Scrollbars */
QScrollBar:vertical {{
    border: none;
    background: {t["scrollbar_bg"]};
    width: 7px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical {{
    background: {t["scrollbar_handle"]};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {t["scrollbar_handle_hover"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* List Widget (History) */
QListWidget {{
    background-color: {t["card_bg"]};
    border: 1px solid {t["card_border"]};
    border-radius: 10px;
    padding: 5px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Ubuntu, 'Helvetica Neue', 'DejaVu Sans', sans-serif;
    font-size: 12px;
    color: {t["text_main"]};
}}

QListWidget::item {{
    padding: 8px;
    border-radius: 7px;
    margin-bottom: 3px;
    border: 1px solid {t["subcard_bg"]};
}}

QListWidget::item:hover {{
    background-color: {t["btn_secondary_hover_bg"]};
    border-color: {t["card_border"]};
}}

QListWidget::item:selected {{
    background-color: {t["badge_bg"]};
    color: {t["badge_text"]};
    border-color: {t["btn_copy_border"]};
}}
"""


APP_STYLESHEET = generate_stylesheet("pink")


# ---------------------------------------------------------
# PASSWORD GENERATION CORE LOGIC
# ---------------------------------------------------------
class PasswordGenerator:
    """Cryptographically secure password generation logic using `secrets`."""

    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SYMBOLS_SIMPLE = "!@#$%^&*"
    SYMBOLS_EXTENDED = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    AMBIGUOUS = "Il1O0o5S2Z"

    @classmethod
    def generate(cls, length: int, complexity: str, exclude_ambiguous: bool = False) -> str:
        """
        Generates a secure password based on chosen complexity level:
        - simple: lowercase + numbers, easy to read/type
        - complex: uppercase + lowercase + numbers + common symbols
        - hard: uppercase + lowercase + numbers + extended symbols
        - very hard: full set with guaranteed presence of each category and high randomness
        """
        length = max(4, min(128, length))

        if complexity == "simple":
            char_pool = cls.LOWERCASE + cls.DIGITS
            required = [secrets.choice(cls.LOWERCASE), secrets.choice(cls.DIGITS)]
        elif complexity == "complex":
            char_pool = cls.LOWERCASE + cls.UPPERCASE + cls.DIGITS + cls.SYMBOLS_SIMPLE
            required = [
                secrets.choice(cls.LOWERCASE),
                secrets.choice(cls.UPPERCASE),
                secrets.choice(cls.DIGITS),
                secrets.choice(cls.SYMBOLS_SIMPLE),
            ]
        elif complexity == "hard":
            char_pool = cls.LOWERCASE + cls.UPPERCASE + cls.DIGITS + cls.SYMBOLS_EXTENDED
            required = [
                secrets.choice(cls.LOWERCASE),
                secrets.choice(cls.UPPERCASE),
                secrets.choice(cls.DIGITS),
                secrets.choice(cls.SYMBOLS_EXTENDED),
            ]
        else:  # "very hard"
            char_pool = cls.LOWERCASE + cls.UPPERCASE + cls.DIGITS + cls.SYMBOLS_EXTENDED
            required = [
                secrets.choice(cls.LOWERCASE),
                secrets.choice(cls.LOWERCASE),
                secrets.choice(cls.UPPERCASE),
                secrets.choice(cls.UPPERCASE),
                secrets.choice(cls.DIGITS),
                secrets.choice(cls.DIGITS),
                secrets.choice(cls.SYMBOLS_EXTENDED),
                secrets.choice(cls.SYMBOLS_EXTENDED),
            ]

        if exclude_ambiguous:
            char_pool = "".join(ch for ch in char_pool if ch not in cls.AMBIGUOUS)
            required = [ch for ch in required if ch not in cls.AMBIGUOUS]
            if not char_pool:
                char_pool = string.ascii_lowercase

        if len(required) > length:
            required = required[:length]

        remaining_count = length - len(required)
        password_chars = required + [secrets.choice(char_pool) for _ in range(remaining_count)]

        # Fisher-Yates cryptographically secure shuffle
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

        return "".join(password_chars)

    @classmethod
    def calculate_entropy(cls, password: str) -> tuple[float, str, str]:
        """
        Evaluates password strength based on 3-tier length scale (4 to 16):
        - 4-7: Weak [Red color #E53935]
        - 8-13: Strong [Greenish yellow #9E9D24]
        - 14-16+: Hard [Dark green #2E7D32]
        Returns: (entropy_bits, rating_label, color_hex)
        """
        if not password:
            return 0.0, "Empty", "#BDBDBD"

        length = len(password)
        pool_size = 0
        if any(c.islower() for c in password):
            pool_size += 26
        if any(c.isupper() for c in password):
            pool_size += 26
        if any(c.isdigit() for c in password):
            pool_size += 10
        if any(c in string.punctuation for c in password):
            pool_size += 32

        if pool_size == 0:
            pool_size = 1

        entropy = length * math.log2(pool_size)

        # 3-tier scale:
        if length <= 7:
            return entropy, "Weak", "#E53935"       # Red
        elif 8 <= length <= 13:
            return entropy, "Strong", "#9E9D24"     # Greenish yellow
        else:
            return entropy, "Hard", "#2E7D32"       # Dark green


# ---------------------------------------------------------
# HISTORY & LOGGING MANAGER
# ---------------------------------------------------------
class HistoryManager:
    """
    Handles logging to a local text file and retrieval.
    Enforces a 365-day retention policy to prevent bulky log files.
    """

    RETENTION_DAYS = 365

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._last_purge_time = None
        # Auto-prune entries older than 365 days on launch
        self.purge_expired_entries(self.RETENTION_DAYS)

    def purge_expired_entries(self, retention_days: int = 365) -> int:
        """
        Removes log entries older than retention_days (365 days).
        Preserves header comments and returns the count of purged entries.
        """
        self._last_purge_time = datetime.now()
        if not self.log_path.exists():
            return 0

        now = datetime.now()
        preserved_lines = []
        purged_count = 0

        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    preserved_lines.append(line)
                    continue

                # Match format: [YYYY-MM-DD HH:MM:SS]
                if stripped.startswith("[") and len(stripped) >= 21 and stripped[20] == "]":
                    ts_str = stripped[1:20]
                    try:
                        entry_dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                        age_days = (now - entry_dt).total_seconds() / 86400.0
                        if age_days <= retention_days:
                            preserved_lines.append(line)
                        else:
                            purged_count += 1
                        continue
                    except ValueError:
                        pass

                preserved_lines.append(line)

            if purged_count > 0:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    f.writelines(preserved_lines)

            return purged_count
        except Exception as e:
            print(f"Error purging expired log entries: {e}", file=sys.stderr)
            return 0

    def append_entry(self, password: str, complexity: str, length: int):
        try:
            # Throttled purge: checks at most once every hour during active use
            now = datetime.now()
            if not self._last_purge_time or (now - self._last_purge_time).total_seconds() > 3600:
                self.purge_expired_entries(self.RETENTION_DAYS)

            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] Complexity: {complexity.upper():<10} | Length: {length:<2} | Password: {password}\n"
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"Error writing to log file: {e}", file=sys.stderr)

    def load_entries(self, limit: int = 50) -> list[str]:
        if not self.log_path.exists():
            return []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
            return lines[-limit:][::-1]  # Most recent first
        except Exception as e:
            print(f"Error reading log file: {e}", file=sys.stderr)
            return []

    def clear_history(self):
        try:
            if self.log_path.exists():
                with open(self.log_path, "w", encoding="utf-8") as f:
                    f.write("# Password Locker - Generated Password History Log\n")
                    f.write("# Format: [YYYY-MM-DD HH:MM:SS] Complexity | Length | Password\n\n")
        except Exception as e:
            print(f"Error clearing log file: {e}", file=sys.stderr)

    def open_in_default_editor(self) -> tuple[bool, str]:
        """
        Detects OS (Windows vs Linux vs macOS) and directly opens the log file
        in the system's default text editor.
        Returns: (success: bool, message: str)
        """
        # Purge any expired entries before opening
        self.purge_expired_entries(self.RETENTION_DAYS)

        # Ensure log file exists before attempting to open
        if not self.log_path.exists():
            try:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    f.write("# Password Locker - Generated Password History Log\n")
                    f.write("# Format: [YYYY-MM-DD HH:MM:SS] Complexity | Length | Password\n\n")
            except Exception as e:
                return False, f"Could not create log file: {e}"

        system_name = platform.system().lower()
        file_path_str = str(self.log_path.resolve())

        try:
            # 1. WINDOWS
            if "windows" in system_name or sys.platform.startswith("win"):
                try:
                    os.startfile(file_path_str)
                    return True, "Opened in Windows default text editor"
                except Exception:
                    if shutil.which("notepad.exe"):
                        subprocess.Popen(["notepad.exe", file_path_str])
                        return True, "Opened in Windows Notepad"
                    return False, "Could not launch text editor on Windows"

            # 2. LINUX / UNIX
            elif "linux" in system_name or sys.platform.startswith("linux") or "bsd" in system_name:
                # Try xdg-open first (official freedesktop standard for default app)
                if shutil.which("xdg-open"):
                    subprocess.Popen(["xdg-open", file_path_str])
                    return True, "Opened via Linux xdg-open"

                # Fallback to common Linux GUI text editors
                for editor in ["gedit", "kate", "kwrite", "mousepad", "xed", "pluma", "leafpad"]:
                    if shutil.which(editor):
                        subprocess.Popen([editor, file_path_str])
                        return True, f"Opened with {editor}"

                # Environment editor fallback ($VISUAL or $EDITOR)
                env_editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
                if env_editor and shutil.which(env_editor):
                    subprocess.Popen([env_editor, file_path_str])
                    return True, f"Opened with {env_editor}"

                return False, "No suitable text editor found on Linux (xdg-open / gedit not found)."

            # 3. macOS (Darwin)
            elif "darwin" in system_name or sys.platform == "darwin":
                # Try open -t (macOS standard for default text editor)
                try:
                    subprocess.Popen(["open", "-t", file_path_str])
                    return True, "Opened in macOS default editor"
                except Exception:
                    pass

                # Fallback to TextEdit
                try:
                    subprocess.Popen(["open", "-a", "TextEdit", file_path_str])
                    return True, "Opened in macOS TextEdit"
                except Exception:
                    pass

                # Fallback to generic open
                try:
                    subprocess.Popen(["open", file_path_str])
                    return True, "Opened with macOS open"
                except Exception as e_mac:
                    return False, f"Failed to open editor on macOS: {e_mac}"

            else:
                return False, f"Unsupported operating system: {platform.system()}"

        except Exception as e:
            return False, f"Failed to open editor: {e}"


# ---------------------------------------------------------
# HISTORY VIEWER DIALOG
# ---------------------------------------------------------
class HistoryDialog(QDialog):
    """Clean dialog to inspect previously generated passwords in active theme."""

    def __init__(self, history_mgr: HistoryManager, parent=None):
        super().__init__(parent)
        self.history_mgr = history_mgr
        self.current_theme = getattr(parent, "current_theme", "pink")
        self.setWindowTitle("Password History & Logs")
        if parent and hasattr(parent, "icon_path") and parent.icon_path:
            self.setWindowIcon(QIcon(str(parent.icon_path)))
        self.resize(580, 480)
        self.setStyleSheet(generate_stylesheet(self.current_theme))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        title_label = QLabel("Saved Password Log")
        title_label.setObjectName("HeaderTitle")
        title_label.setStyleSheet("font-size: 20px;")
        desc_label = QLabel(f"Stored securely in local file: {self.history_mgr.log_path.name}")
        desc_label.setObjectName("HeaderSubtitle")
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.list_widget)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_copy_selected = QPushButton("📋 Copy Selected")
        self.btn_copy_selected.setObjectName("CopyButton")
        self.btn_copy_selected.clicked.connect(self.copy_selected)

        self.btn_clear = QPushButton("🗑️ Clear History")
        self.btn_clear.setObjectName("SecondaryButton")
        self.btn_clear.clicked.connect(self.clear_history)

        self.btn_close = QPushButton("Close")
        self.btn_close.setObjectName("PrimaryButton")
        self.btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_copy_selected)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)

        layout.addLayout(btn_layout)
        self.refresh_list()

    def refresh_list(self):
        self.list_widget.clear()
        entries = self.history_mgr.load_entries(100)
        if not entries:
            empty_item = QListWidgetItem("No saved passwords found in log.")
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.list_widget.addItem(empty_item)
            self.btn_copy_selected.setEnabled(False)
            return

        self.btn_copy_selected.setEnabled(True)
        for entry in entries:
            item = QListWidgetItem(entry)
            self.list_widget.addItem(item)

    def copy_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        text = item.text()
        if "Password: " in text:
            pwd = text.split("Password: ")[-1].strip()
        else:
            pwd = text
        QApplication.clipboard().setText(pwd)
        self.btn_copy_selected.setText("Copied! ✓")
        QTimer.singleShot(1500, lambda: self.btn_copy_selected.setText("📋 Copy Selected"))

    def clear_history(self):
        confirm = QMessageBox.question(
            self,
            "Clear Log Confirmation",
            "Are you sure you want to permanently clear the password history log?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.history_mgr.clear_history()
            self.refresh_list()


def get_app_dir() -> Path:
    """Returns the persistent directory where user data/logs should be stored (next to exe or script)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def get_bundle_dir() -> Path:
    """Returns the bundled resources directory (sys._MEIPASS for PyInstaller onefile, or script dir)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    return Path(__file__).resolve().parent


# ---------------------------------------------------------
# MAIN APPLICATION WINDOW
# ---------------------------------------------------------
class PasswordLockerApp(QMainWindow):
    """
    Main Password Locker Window.
    Features:
    - Fully resizable responsive UI with minimum constraints
    - On-close exit warning dialog
    - Light Pink & Magenta aesthetic with soft shadows
    - Simple, Complex, Hard, and Very Hard complexity types
    - Real-time entropy strength calculation
    - Automatic history logging
    - Smooth clipboard copy button with feedback animations
    """

    def __init__(self):
        super().__init__()
        self.base_dir = get_app_dir()
        self.bundle_dir = get_bundle_dir()
        self.icon_path = self.get_icon_path()
        self.history_mgr = HistoryManager(self.base_dir / LOG_FILE_NAME)

        self.current_theme = "pink"
        self.is_auto_theme_enabled = True
        self._last_day_slot = None
        self.display_card_shadow = None
        self.settings_card_shadow = None
        self.is_password_visible = True
        self.current_password = ""

        # Clock Live Update Timer (every 1 second)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.init_window_settings()
        self.init_ui()
        self.ui_initialized = True
        self.check_auto_theme(force=True, is_startup=True)
        self.setup_shortcuts()
        self.generate_password(log_to_file=True)

    @staticmethod
    def get_timezone_abbr(dt: datetime) -> str:
        """Derives a concise timezone acronym or UTC offset (e.g., IST, EST, UTC+05:30)."""
        tz_name = dt.tzname() or ""
        words = tz_name.split()
        if len(words) > 1:
            abbr = "".join([w[0].upper() for w in words if w[0].isalpha()])
        else:
            abbr = tz_name
        if not abbr or len(abbr) > 5 or not abbr.isalpha():
            offset = dt.strftime("%z")
            if offset and len(offset) >= 5:
                abbr = f"UTC{offset[:3]}:{offset[3:]}"
            else:
                abbr = "UTC"
        return abbr

    def update_clock(self):
        """Updates live digital clock every second and evaluates offline auto day/night theme."""
        now = datetime.now().astimezone()
        if hasattr(self, "clock_label"):
            time_str = now.strftime("%I:%M:%S %p")
            date_str = now.strftime("%d/%m/%y")
            tz_abbr = self.get_timezone_abbr(now)
            self.clock_label.setText(f"🕒 {time_str} {tz_abbr} | {date_str}")

            full_date = now.strftime("%A, %B %d, %Y")
            full_tz = now.tzname() or tz_abbr
            offset = now.strftime("%z")
            offset_fmt = f" (UTC{offset[:3]}:{offset[3:]})" if len(offset) >= 5 else ""
            mode_desc = "Auto (System Clock)" if self.is_auto_theme_enabled else "Manual"
            self.clock_label.setToolTip(
                f"Date: {full_date}\nTime: {time_str} {full_tz}{offset_fmt}\nTheme Mode: {mode_desc}"
            )

        # Seamless offline check for day/night transitions
        self.check_auto_theme()

    def get_icon_path(self) -> Path | None:
        """Finds icon.png, icon.ico, or icon.jpg in the bundle or application directory."""
        for base in [getattr(self, "bundle_dir", self.base_dir), self.base_dir]:
            for name in ["icon.ico", "icon.png", "icon.jpg"]:
                p = base / name
                if p.exists():
                    return p.resolve()
        return None

    def setup_shortcuts(self):
        """Sets up cross-platform standard keyboard shortcuts."""
        # Generate new password: Ctrl+G (Cmd+G on macOS) / F5
        QShortcut(QKeySequence("Ctrl+G"), self, lambda: self.generate_password(log_to_file=True))
        QShortcut(QKeySequence("F5"), self, lambda: self.generate_password(log_to_file=True))

        # Copy password to clipboard: Ctrl+C (Cmd+C on macOS)
        QShortcut(QKeySequence.StandardKey.Copy, self, self.copy_to_clipboard)

        # Toggle Incognito Mode: Ctrl+I (Cmd+I on macOS)
        QShortcut(QKeySequence("Ctrl+I"), self, lambda: self.btn_incognito.toggle())

        # Open History: Ctrl+H (Cmd+H on macOS)
        QShortcut(QKeySequence("Ctrl+H"), self, self.open_history)

        # Switch / Cycle Theme: Ctrl+T (Cmd+T on macOS)
        QShortcut(QKeySequence("Ctrl+T"), self, self.cycle_theme)

        # Close / Exit: Esc
        QShortcut(QKeySequence("Esc"), self, self.close)

    def init_window_settings(self):
        self.setWindowTitle("Password Locker ✨")
        # Set Window and Taskbar Icon
        if self.icon_path:
            self.setWindowIcon(QIcon(str(self.icon_path)))

        # Clean width & compact height fitting all cards seamlessly with zero scrollbars
        self.setMinimumSize(620, 640)
        self.resize(680, 700)

    def init_ui(self):
        # Central container with scrollbars disabled so right-side slider never appears
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; }")

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(22, 16, 22, 16)
        main_layout.setSpacing(12)

        # 1. HEADER SECTION (Dual-Deck: Row 1 = Title & Live Clock, Row 2 = Subtitle & Actions)
        header_container = QVBoxLayout()
        header_container.setSpacing(8)

        # Row 1: App Title & Branding (Left) + Live Digital Clock Badge (Right)
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(8)

        if self.icon_path:
            icon_img_lbl = QLabel()
            pix = QPixmap(str(self.icon_path)).scaled(
                28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            icon_img_lbl.setPixmap(pix)
            row1_layout.addWidget(icon_img_lbl)

        title = QLabel("Password Locker")
        title.setObjectName("HeaderTitle")
        row1_layout.addWidget(title)
        row1_layout.addStretch()

        # Live Digital Clock Badge
        self.clock_label = QLabel()
        self.clock_label.setObjectName("ClockBadge")
        self.update_clock()
        row1_layout.addWidget(self.clock_label)

        header_container.addLayout(row1_layout)

        # Row 2: Subtitle (Left) + Action Controls (Right)
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)

        subtitle = QLabel("Fast, cryptographically secure password generator & locker")
        subtitle.setObjectName("HeaderSubtitle")
        subtitle.setWordWrap(True)
        row2_layout.addWidget(subtitle, stretch=1)

        # Header Actions (Theme Selector, Incognito, History, Clear)
        header_actions_layout = QHBoxLayout()
        header_actions_layout.setSpacing(6)

        # Theme Selector Dropdown
        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName("ThemeSelector")
        self.theme_combo.addItem("✨ Auto (Day/Night)", "auto")
        self.theme_combo.addItem("🌸 Pink", "pink")
        self.theme_combo.addItem("💜 Purple", "purple")
        self.theme_combo.addItem("🌊 Ocean Blue", "ocean_blue")
        self.theme_combo.addItem("🌙 Warm Night", "warm_night")
        self.theme_combo.setToolTip("Theme Mode: Auto (Offline System Clock) or Manual Select [Ctrl+T / Cmd+T]")
        self.theme_combo.currentIndexChanged.connect(self.on_theme_combo_changed)

        # Incognito Toggle Button
        self.btn_incognito = QPushButton("🕵️ Incognito")
        self.btn_incognito.setObjectName("IncognitoToggle")
        self.btn_incognito.setCheckable(True)
        self.btn_incognito.setChecked(False)
        self.btn_incognito.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_incognito.setToolTip("Incognito Mode (Ctrl+I / Cmd+I): Zero logging to disk & automatically wipes history on exit for 100% privacy")
        self.btn_incognito.toggled.connect(self.on_incognito_toggled)

        self.btn_history = QPushButton("📜 History")
        self.btn_history.setObjectName("SecondaryButton")
        self.btn_history.setToolTip("History (Ctrl+H / Cmd+H): Directly opens password log in default text editor (Retained for 365 days)")
        self.btn_history.clicked.connect(self.open_history)

        self.btn_clear_log = QPushButton("🗑️ Clear")
        self.btn_clear_log.setObjectName("SecondaryButton")
        self.btn_clear_log.setToolTip("Permanently clears the password log file")
        self.btn_clear_log.clicked.connect(self.confirm_clear_log)

        header_actions_layout.addWidget(self.theme_combo)
        header_actions_layout.addWidget(self.btn_incognito)
        header_actions_layout.addWidget(self.btn_history)
        header_actions_layout.addWidget(self.btn_clear_log)
        row2_layout.addLayout(header_actions_layout)

        header_container.addLayout(row2_layout)
        main_layout.addLayout(header_container)

        # 2. PASSWORD DISPLAY CARD
        display_card = QFrame()
        display_card.setObjectName("DisplayCard")
        display_card.setProperty("class", "CardFrame")
        self.display_card_shadow = self.apply_card_shadow(display_card)

        display_card_layout = QVBoxLayout(display_card)
        display_card_layout.setContentsMargins(14, 14, 14, 14)
        display_card_layout.setSpacing(10)

        # Label above display
        display_title_layout = QHBoxLayout()
        display_title = QLabel("GENERATED PASSWORD")
        display_title.setObjectName("SectionHeading")
        display_title_layout.addWidget(display_title)
        display_title_layout.addStretch()

        # Visibility Toggle
        self.btn_toggle_vis = QPushButton("👁️ Hide")
        self.btn_toggle_vis.setObjectName("IconButton")
        self.btn_toggle_vis.setToolTip("Toggle password visibility")
        self.btn_toggle_vis.clicked.connect(self.toggle_password_visibility)
        display_title_layout.addWidget(self.btn_toggle_vis)

        display_card_layout.addLayout(display_title_layout)

        # Password Input Field
        self.password_input = QLineEdit()
        self.password_input.setObjectName("PasswordDisplay")
        self.password_input.setReadOnly(True)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        display_card_layout.addWidget(self.password_input)

        # Strength Bar & Info
        strength_layout = QHBoxLayout()
        strength_layout.setSpacing(8)

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(False)

        self.strength_label = QLabel("Strength: Calculating...")
        self.strength_label.setStyleSheet("font-size: 11px; font-weight: 600; color: #8C627D;")

        strength_layout.addWidget(self.strength_bar, stretch=3)
        strength_layout.addWidget(self.strength_label, stretch=2, alignment=Qt.AlignmentFlag.AlignRight)
        display_card_layout.addLayout(strength_layout)

        # Copy & Quick Re-generate Button Row
        action_btn_layout = QHBoxLayout()
        action_btn_layout.setSpacing(10)

        self.btn_copy = QPushButton("📋 Copy to Clipboard")
        self.btn_copy.setObjectName("CopyButton")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.setToolTip("Copy to Clipboard (Ctrl+C / Cmd+C)")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)

        self.btn_generate = QPushButton("🎲 Generate New")
        self.btn_generate.setObjectName("PrimaryButton")
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate.setToolTip("Generate New Password (Ctrl+G / Cmd+G / F5)")
        self.btn_generate.clicked.connect(lambda: self.generate_password(log_to_file=True))

        action_btn_layout.addWidget(self.btn_copy, stretch=1)
        action_btn_layout.addWidget(self.btn_generate, stretch=1)
        display_card_layout.addLayout(action_btn_layout)

        main_layout.addWidget(display_card)

        # 3. SETTINGS & CUSTOMIZATION CARD
        settings_card = QFrame()
        settings_card.setProperty("class", "CardFrame")
        self.settings_card_shadow = self.apply_card_shadow(settings_card)

        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(14, 14, 14, 14)
        settings_layout.setSpacing(12)

        # --- A. Length Section ---
        length_header = QHBoxLayout()
        length_title = QLabel("PASSWORD LENGTH")
        length_title.setObjectName("SectionHeading")

        self.length_badge = QLabel("12")
        self.length_badge.setObjectName("ValueBadge")

        length_header.addWidget(length_title)
        length_header.addStretch()
        length_header.addWidget(self.length_badge)
        settings_layout.addLayout(length_header)

        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(4, 16)
        self.length_slider.setValue(12)
        self.length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.length_slider.setTickInterval(2)
        self.length_slider.valueChanged.connect(self.on_length_changed)
        self.length_slider.sliderReleased.connect(lambda: self.generate_password(log_to_file=True))
        settings_layout.addWidget(self.length_slider)

        # --- B. Complexity Section ---
        complexity_title = QLabel("SECURITY COMPLEXITY")
        complexity_title.setObjectName("SectionHeading")
        settings_layout.addWidget(complexity_title)

        complexity_grid = QGridLayout()
        complexity_grid.setSpacing(8)

        self.radio_group = QButtonGroup(self)

        self.radio_simple = QRadioButton("Simple\n(abc, 123 - easy to read)")
        self.radio_complex = QRadioButton("Complex\n(abc, ABC, 123, !@#)")
        self.radio_hard = QRadioButton("Hard\n(Extended symbols)")
        self.radio_very_hard = QRadioButton("Very Hard\n(Maximum entropy)")

        self.radio_hard.setChecked(True)  # Default recommendation

        self.radio_group.addButton(self.radio_simple, 1)
        self.radio_group.addButton(self.radio_complex, 2)
        self.radio_group.addButton(self.radio_hard, 3)
        self.radio_group.addButton(self.radio_very_hard, 4)

        self.radio_group.buttonClicked.connect(lambda: self.generate_password(log_to_file=True))

        complexity_grid.addWidget(self.radio_simple, 0, 0)
        complexity_grid.addWidget(self.radio_complex, 0, 1)
        complexity_grid.addWidget(self.radio_hard, 1, 0)
        complexity_grid.addWidget(self.radio_very_hard, 1, 1)

        settings_layout.addLayout(complexity_grid)

        # --- C. Extra Options & Toggles ---
        options_title = QLabel("PREFERENCES")
        options_title.setObjectName("SectionHeading")
        settings_layout.addWidget(options_title)

        options_layout = QVBoxLayout()
        options_layout.setSpacing(8)

        self.chk_avoid_ambiguous = QCheckBox("Avoid ambiguous characters (0, O, 1, l, I)")
        self.chk_avoid_ambiguous.stateChanged.connect(lambda: self.generate_password(log_to_file=True))

        self.chk_auto_log = QCheckBox("Auto-log passwords (365 days retention)")
        self.chk_auto_log.setChecked(True)

        options_layout.addWidget(self.chk_avoid_ambiguous)
        options_layout.addWidget(self.chk_auto_log)
        settings_layout.addLayout(options_layout)

        main_layout.addWidget(settings_card)
        main_layout.addStretch()

        # Set central widget
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

    def apply_card_shadow(self, widget: QWidget):
        """Applies a subtle soft theme-tinted drop shadow to cards."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        t = THEMES.get(getattr(self, "current_theme", "pink"), THEMES["pink"])
        r, g, b, a = t["shadow_rgba"]
        shadow.setColor(QColor(r, g, b, a))
        shadow.setOffset(0, 4)
        widget.setGraphicsEffect(shadow)
        return shadow

    def apply_theme(self, theme_key: str):
        """Applies one of 4 themes: Pink, Purple, Ocean Blue, Warm Night."""
        if theme_key not in THEMES:
            theme_key = "pink"
        self.current_theme = theme_key
        t = THEMES[theme_key]
        self.setStyleSheet(generate_stylesheet(theme_key))

        # Update card drop shadow colors
        r, g, b, a = t["shadow_rgba"]
        if hasattr(self, "display_card_shadow") and self.display_card_shadow:
            self.display_card_shadow.setColor(QColor(r, g, b, a))
        if hasattr(self, "settings_card_shadow") and self.settings_card_shadow:
            self.settings_card_shadow.setColor(QColor(r, g, b, a))

        # Update strength bar styling
        if hasattr(self, "strength_bar") and self.current_password:
            _, rating, color = PasswordGenerator.calculate_entropy(self.current_password)
            self.strength_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    border-radius: 3px;
                    background-color: {t["strength_bg"]};
                    height: 6px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)

    def check_auto_theme(self, force: bool = False, is_startup: bool = False):
        """
        100% Offline System Clock Day/Night Theme Automation.
        - Night Time (19:00 - 06:00 / 7 PM - 6 AM local time): Automatically sets 'warm_night' (Theme 4)
        - Daylight Time (06:00 - 19:00 / 6 AM - 7 PM local time): Dynamically rotates among 'pink', 'purple', 'ocean_blue'.
          On startup, it remembers the previous theme and picks a DIFFERENT daytime theme so every launch gives a fresh theme.
          While running, it smoothly transitions to a new theme every 3 minutes.
        Requires zero internet - directly reads system time zone from OS hardware clock.
        """
        if not getattr(self, "is_auto_theme_enabled", True):
            return

        if not getattr(self, "ui_initialized", False) and not force:
            return

        now = datetime.now()
        hour = now.hour
        is_night = (hour >= 19 or hour < 6)

        if is_night:
            if self.current_theme != "warm_night" or force:
                self.apply_theme("warm_night")
                if hasattr(self, "theme_combo") and self.theme_combo.currentIndex() == 0:
                    self.theme_combo.setItemText(0, "✨ Auto (🌙 Warm Night)")
        else:
            day_themes = ["pink", "purple", "ocean_blue"]
            cache_file = self.base_dir / ".theme_cache"
            # 3-minute slot for active daylight rotation
            current_slot = (now.day, hour, now.minute // 3)

            if force or current_slot != getattr(self, "_last_day_slot", None) or self.current_theme not in day_themes:
                self._last_day_slot = current_slot

                last_theme = getattr(self, "current_theme", None)
                if is_startup and cache_file.exists():
                    try:
                        cached = cache_file.read_text(encoding="utf-8").strip()
                        if cached in day_themes:
                            last_theme = cached
                    except Exception:
                        pass

                available = [t for t in day_themes if t != last_theme]
                chosen = secrets.choice(available if available else day_themes)

                try:
                    cache_file.write_text(chosen, encoding="utf-8")
                except Exception:
                    pass

                self.apply_theme(chosen)
                if hasattr(self, "theme_combo") and self.theme_combo.currentIndex() == 0:
                    display_name = THEMES[chosen]["display"]
                    self.theme_combo.setItemText(0, f"✨ Auto ({display_name})")

    def on_theme_combo_changed(self, index: int):
        theme_key = self.theme_combo.currentData()
        if theme_key == "auto":
            self.is_auto_theme_enabled = True
            self.check_auto_theme(force=True)
        else:
            self.is_auto_theme_enabled = False
            self.theme_combo.setItemText(0, "✨ Auto (Day/Night)")
            self.apply_theme(theme_key)

    def cycle_theme(self):
        next_idx = (self.theme_combo.currentIndex() + 1) % self.theme_combo.count()
        self.theme_combo.setCurrentIndex(next_idx)

    def get_dialog_stylesheet(self) -> str:
        """Returns dialog stylesheet matching the active theme."""
        t = THEMES.get(getattr(self, "current_theme", "pink"), THEMES["pink"])
        return f"""
            QMessageBox {{
                background-color: {t["canvas_bg"]};
            }}
            QLabel {{
                color: {t["text_main"]};
                font-size: 13px;
            }}
            QPushButton {{
                background-color: {t["btn_copy_bg"]};
                color: {t["btn_copy_text"]};
                border: 1px solid {t["btn_copy_border"]};
                border-radius: 7px;
                padding: 6px 14px;
                font-weight: 600;
                min-width: 65px;
            }}
            QPushButton:hover {{
                background-color: {t["btn_primary_grad_end"]};
                color: #FFFFFF;
            }}
        """

    # ---------------------------------------------------------
    # UI EVENT HANDLERS & LOGIC
    # ---------------------------------------------------------
    def on_length_changed(self, value: int):
        self.length_badge.setText(str(value))
        # Update preview in real-time without clogging log file during dragging
        self.generate_password(log_to_file=False)

    def get_selected_complexity(self) -> str:
        selected_id = self.radio_group.checkedId()
        mapping = {1: "simple", 2: "complex", 3: "hard", 4: "very hard"}
        return mapping.get(selected_id, "hard")

    def generate_password(self, log_to_file: bool = False):
        length = self.length_slider.value()
        complexity = self.get_selected_complexity()
        exclude_ambiguous = self.chk_avoid_ambiguous.isChecked()

        password = PasswordGenerator.generate(
            length=length, complexity=complexity, exclude_ambiguous=exclude_ambiguous
        )
        self.current_password = password
        self.update_password_display()

        # Update Strength Meter
        entropy, rating, color = PasswordGenerator.calculate_entropy(password)
        # Scaled 4 to 16 range (25% to 100%)
        pct = min(100, max(25, int((len(password) / 16.0) * 100)))
        self.strength_bar.setValue(pct)
        t = THEMES.get(getattr(self, "current_theme", "pink"), THEMES["pink"])
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background-color: {t["strength_bg"]};
                height: 6px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        self.strength_label.setText(f"Strength: {rating}")
        self.strength_label.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color};")

        # Auto-log if enabled, requested, AND Incognito Mode is OFF (Zero trace in Incognito)
        if log_to_file and self.chk_auto_log.isChecked() and not self.btn_incognito.isChecked():
            self.history_mgr.append_entry(password, complexity, length)

    def update_password_display(self):
        if self.is_password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_input.setText(self.current_password)
            self.btn_toggle_vis.setText("👁️ Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_input.setText(self.current_password)
            self.btn_toggle_vis.setText("👁️ Show")

    def toggle_password_visibility(self):
        self.is_password_visible = not self.is_password_visible
        self.update_password_display()

    def copy_to_clipboard(self):
        """Copies password and triggers smooth visual feedback."""
        if not self.current_password:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(self.current_password)

        # Smooth Feedback Animation
        self.btn_copy.setText("✓ Copied to Clipboard!")
        self.btn_copy.setStyleSheet("""
            QPushButton#CopyButton {
                background-color: #E8F5E9;
                color: #2E7D32;
                border: 2px solid #81C784;
                font-weight: 700;
            }
        """)

        # Revert style after 1.8 seconds smoothly
        QTimer.singleShot(1800, self.reset_copy_button)

    def reset_copy_button(self):
        self.btn_copy.setText("📋 Copy to Clipboard")
        self.btn_copy.setStyleSheet("")  # Reverts to stylesheet default

    def open_history(self):
        """
        Detects OS (Windows / Linux / macOS) and opens password log directly in default text editor.
        """
        success, msg = self.history_mgr.open_in_default_editor()
        if success:
            self.btn_history.setText("✓ Editor Opened!")
            self.btn_history.setStyleSheet("""
                QPushButton#SecondaryButton {
                    background-color: #E8F5E9;
                    color: #2E7D32;
                    border: 1px solid #81C784;
                    font-weight: 700;
                }
            """)
            QTimer.singleShot(1800, self.reset_history_button)
        else:
            QMessageBox.warning(
                self,
                "Error Opening Log",
                f"Could not open log file in your system's text editor:\n{msg}\n\nFalling back to internal history viewer...",
            )
            self.open_history_dialog()

    def reset_history_button(self):
        self.btn_history.setText("📜 History")
        self.btn_history.setStyleSheet("")

    def confirm_clear_log(self):
        """
        Prompts confirmation and clears the password log file.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Clear History")
        msg_box.setText("Are you sure you want to clear the password history log?")
        msg_box.setInformativeText("This will permanently delete all saved entries.")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet(self.get_dialog_stylesheet())

        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.history_mgr.clear_history()
            self.btn_clear_log.setText("✓ Cleared!")
            self.btn_clear_log.setStyleSheet("""
                QPushButton#SecondaryButton {
                    background-color: #E8F5E9;
                    color: #2E7D32;
                    border: 1px solid #81C784;
                    font-weight: 700;
                }
            """)
            QTimer.singleShot(1800, self.reset_clear_log_button)

    def reset_clear_log_button(self):
        self.btn_clear_log.setText("🗑️ Clear")
        self.btn_clear_log.setStyleSheet("")

    def open_history_dialog(self):
        dialog = HistoryDialog(self.history_mgr, self)
        dialog.exec()

    def on_incognito_toggled(self, checked: bool):
        """
        Handles Incognito Mode on/off state.
        Zero logs are created, and logs are automatically wiped on exit.
        Color fills with vibrant Cyan without changing button dimensions.
        """
        if checked:
            self.chk_auto_log.setEnabled(False)
            self.chk_auto_log.setText("Auto-log passwords (DISABLED in Incognito)")
            self.btn_history.setEnabled(False)
            self.btn_history.setToolTip("History viewing is suspended while Incognito Mode is active")
            self.btn_incognito.setToolTip("Incognito Mode is ACTIVE (Cyan): Zero logging & auto-wipe on exit")
        else:
            self.chk_auto_log.setEnabled(True)
            self.chk_auto_log.setText("Auto-log passwords (365 days retention)")
            self.btn_history.setEnabled(True)
            self.btn_history.setToolTip("Directly opens password log in default text editor (Retained for 365 days)")
            self.btn_incognito.setToolTip("Incognito Mode: Zero logging to disk & automatically wipes history on exit for 100% privacy")

    # ---------------------------------------------------------
    # ON-CLOSE EXIT CONFIRMATION WARNING
    # ---------------------------------------------------------
    def closeEvent(self, event):
        """
        Intercepts window close to display a styled confirmation warning.
        If Incognito Mode is active, permanently purges the log file for 100% privacy.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Exit Confirmation")
        msg_box.setText("Are you sure you want to exit Password Locker?")
        if self.btn_incognito.isChecked():
            msg_box.setInformativeText("🕵️ Incognito Mode is active: All history logs will be permanently wiped on exit for 100% privacy.")
        else:
            msg_box.setInformativeText("Any unsaved preferences will be safely remembered.")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        msg_box.setStyleSheet(self.get_dialog_stylesheet())

        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            if self.btn_incognito.isChecked():
                # 100% Zero-Trace: permanently clear history on exit
                self.history_mgr.clear_history()
            event.accept()
        else:
            event.ignore()


# ---------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------
def main():
    # Set Windows Process Explicit ID so custom icon displays cleanly on Windows Taskbar
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("passwordlocker.app.pink.v1")
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("PasswordLocker")
    app.setApplicationDisplayName("Password Locker ✨")
    app.setOrganizationName("PasswordLocker")
    if not sys.platform.startswith("win"):
        app.setDesktopFileName("password-locker")

    # Set application-wide default icon for all windows & dialogs
    bundle_dir = get_bundle_dir()
    app_dir = get_app_dir()
    for base in [bundle_dir, app_dir]:
        for icon_name in ["icon.ico", "icon.png", "icon.jpg"]:
            icon_file = base / icon_name
            if icon_file.exists():
                app.setWindowIcon(QIcon(str(icon_file.resolve())))
                break

    window = PasswordLockerApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
