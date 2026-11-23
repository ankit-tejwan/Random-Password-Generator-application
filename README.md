# Password Locker ✨

A clean, modern, and cross-platform desktop password generator and locker application featuring an elegant **Light Pink & Magenta** aesthetic.

![Python](https://img.shields.io/badge/Python-3.10%2B-pink)
![GUI](https://img.shields.io/badge/GUI-PySide6%20%2F%20PyQt6-magenta)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Key Features

1. **Cross-Platform Compatibility (Windows, Linux, macOS)**
   - Runs natively across Windows 10/11, macOS, and Linux (Ubuntu, Debian, Fedora, Arch).
   - Cross-platform typography fallback stack automatically aligns with the host OS.
   - Detects the native OS and directly opens history in the system default text editor:
     - **Windows**: `os.startfile` / Notepad
     - **Linux**: `xdg-open` / GNOME Text Editor / Kate / Gedit / Mousepad / `$EDITOR`
     - **macOS**: `open -t` / TextEdit

2. **🎨 4 Built-in Themes with 100% Offline Auto Day/Night Scheduling**
   - **Automatic Day/Night Mode (Default)**: Directly synchronizes with the host OS hardware clock without any internet connectivity or external API:
     - **🌙 Night Time (7:00 PM – 6:00 AM local time)**: Automatically switches to **🌙 Warm Night** to protect eyes from strain.
     - **☀️ Daylight Time (6:00 AM – 7:00 PM local time)**: Periodically rotates among vibrant daytime themes (**🌸 Pink**, **💜 Purple**, **🌊 Ocean Blue**).
   - Instant 1-click manual theme switcher in header (or press `Ctrl+T` / `Cmd+T`):
     - **🌸 Pink**: Soft light rose palette with warm pastel cards and magenta accents.
     - <img width="852" height="914" alt="image" src="https://github.com/user-attachments/assets/aa5cc958-11d4-42d8-bf10-e6a4ba0f65de" />

     - **💜 Purple**: Regal, elegant lavender & purple palette with rich violet accents.
     - <img width="852" height="914" alt="image" src="https://github.com/user-attachments/assets/853e6b58-6ecc-4b68-858b-75d06d59c1c4" />


     - **🌊 Ocean Blue**: Crisp, refreshing coastal palette with cyan, azure, and deep navy tones.
     - <img width="852" height="914" alt="image" src="https://github.com/user-attachments/assets/6c26f67d-3750-4f44-8b08-68523d3ef6f8" />

     - **🌙 Warm Night**: Eye-friendly warm dark mode with espresso charcoal background, ivory typography, and golden amber accents.
     - <img width="852" height="914" alt="image" src="https://github.com/user-attachments/assets/cecf487e-7cba-4d2e-8ea1-f1bed7ee3270" />

   - All modal dialogs and drop shadows dynamically adapt to the active theme.

3. **🕒 Live Digital Clock & Timezone Badge (Dual-Deck Header)**
   - Display Format: `🕒 HH:MM:SS AM/PM [Timezone] | DD/MM/YY` (e.g. `🕒 12:45:10 PM IST | 23/11/26`).
   - Monospace live ticking clock badge located at eye-level in the top-right header.
   - 100% offline timezone and system clock detection (adapts across Windows, Linux, and macOS).
   - Automatically adapts badge borders, background, and text colors to the active theme.
   - Hovering reveals the full system date, timezone name, UTC offset, and auto-theme mode.

4. **Fluid Responsive Layout (Zero Scrollbars)**
   - Calibrated default dimensions (640 x 660) with zero horizontal or vertical scrollbars.
   - Smooth layout constraints that adapt gracefully if the window is resized.

4. **Safe On-Close Exit Confirmation**
   - Intercepts accidental window closure with a themed warning dialog.

5. **Cryptographically Secure Generator**
   - Powered by Python's `secrets` module (CSPRNG) rather than pseudo-random numbers.
   - 4 Security Complexity Tiers:
     - **Simple**: Lowercase + digits (easy to read and type).
     - **Complex**: Lowercase + uppercase + numbers + standard symbols (`!@#$%^&*`).
     - **Hard**: Mixed case + digits + extended punctuation (`!@#$%^&*()_+-=[]{}|;:,.<>?`).
     - **Very Hard**: Maximum entropy with guaranteed multi-class characters.
   - **Exclude Ambiguous Characters**: Easily strip confusing characters like `0`, `O`, `1`, `l`, `I`.

6. **3-Tier Visual Strength Meter (Length 4 to 16)**
   - **4 – 7 Chars**: `Weak` [🔴 Red color `#E53935`]
   - **8 – 13 Chars**: `Strong` [🟡 Greenish-Yellow `#9E9D24`]
   - **14 – 16 Chars**: `Hard` [🟢 Dark Green `#2E7D32`]

7. **⌨️ Standard Cross-Platform Keyboard Shortcuts**
   - `Ctrl+G` / `Cmd+G` or `F5`: Generate new password
   - `Ctrl+C` / `Cmd+C`: Copy password to clipboard
   - `Ctrl+T` / `Cmd+T`: Cycle / switch theme (Pink ➔ Purple ➔ Ocean Blue ➔ Warm Night)
   - `Ctrl+I` / `Cmd+I`: Toggle Incognito Mode on/off
   - `Ctrl+H` / `Cmd+H`: Open history in default system text editor
   - `Esc`: Close confirmation prompt

8. **Smooth Clipboard Copy with Visual Feedback**
   - One-click copy with an instant, smooth visual state change to `"✓ Copied to Clipboard!"` and automated reset.

9. **365-Day Retention & Smart Log Management**
   - Automatically maintains a **365-day (1 year) retention policy** — entries older than 365 days are silently purged on startup and upon generation to keep the file lightweight and secure.
   - Dedicated **"📜 History"** button directly launches the log file in your system's default text editor.
   - Dedicated **"🗑️ Clear"** button in the header allows 1-click manual wiping with safety confirmation.

10. **🕵️ 100% Zero-Trace Incognito Mode Toggle**
    - Dedicated toggle button (`🕵️ Incognito`) in the header right next to History.
    - **When ON**:
      - Button fills with vibrant **Cyan** (`#00BCD4`) without any shift in dimensions.
      - All logging to disk is completely blocked (zero trace).
      - Auto-log options are suspended.
      - On closing the app, the history log is completely wiped and cleared for 100% privacy.

---

## 🚀 How to Run

### Requirements
- Python 3.10 or newer
- `PySide6` (recommended) or `PyQt6`

### Installation & Execution
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch Password Locker
python main_app.py
```

### OS Notes
- **Windows**: Run `python main_app.py` or double-click `main_app.py`. App icon binds directly to Windows Taskbar.
- **Linux**: Ensure Python 3 and Qt dependencies are available (`sudo apt install python3-pip` on Ubuntu/Debian). Run `python3 main_app.py`.
- **macOS**: Run `python3 main_app.py`. Shortcuts automatically map to `Cmd`.

---

## 📁 File Structure
```
Password_locker/
├── main_app.py             # Main application source code (cross-platform)
├── requirements.txt        # Dependency requirements (PySide6)
├── .gitignore              # Git ignore rules (protects user privacy)
├── icon.ico                # Application window & taskbar icon
├── icon.jpg                # High-res branding asset
├── password_history.log    # Local timestamped password log (git-ignored)
└── README.md               # Documentation
```
