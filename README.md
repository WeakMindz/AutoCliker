# WeakMindz AutoClicker

A lightweight, fully-featured desktop auto clicker built with Python and CustomTkinter. Dark-themed, keyboard-controllable, and simple to use.

---

## Features

- Adjustable CPS (clicks per second) from 1 to 100 with stepper buttons
- Normal and Jitter click modes — Jitter adds randomised timing to simulate human behaviour
- Left, right, and middle mouse button support
- Click at your current cursor position or lock to a specific screen coordinate
- Rebindable start/stop hotkeys (default F6 / F7)
- Dark and light theme toggle
- Status indicator showing idle or running state

---

## Requirements

- Python 3.7 or higher
- customtkinter
- pynput

Install both dependencies with:

```
pip install customtkinter pynput
```

---

## How to Run

```
python main.py
```

---

## Usage

### CPS
Type a number between 1 and 100 into the CPS box, or use the up/down arrows to adjust. This controls how many times per second the auto clicker fires.

### Click Mode
- **Normal** — clicks at a steady, fixed interval
- **Jitter** — adds up to ±20% random variance between clicks to mimic natural human input

### Mouse Button
Choose between Left, Right, or Middle click. The selected button is highlighted in blue.

### Click Location
- **Current position** — the clicker fires wherever your cursor is at the time of each click
- **Pick location** — press the Pick button, the window minimises, then click anywhere on your screen to lock the clicker to those exact coordinates. The X and Y values will display in the app.

### Hotkeys
By default, **F6** starts the clicker and **F7** stops it. To rebind:
1. Click the green Start or red Stop hotkey button
2. It will flash yellow and say "Press any key…"
3. Press any key on your keyboard — it binds immediately

Hotkeys work even when the app is not in focus, so you can start and stop clicking without switching windows.

### Start / Stop Buttons
The green Start button and red Stop button at the bottom also control the clicker directly.

---

## Project Structure

```
main.py      — Full application (UI + click logic + hotkeys)
README.md    — This file
```

---

## Troubleshooting

**The clicker does nothing when I press Start**
Make sure pynput is installed: `pip install pynput`

**Hotkeys don't work**
Some systems require elevated permissions for global keyboard hooks. Try running the script as administrator (Windows) or with sudo (Linux/macOS).

**Pick location doesn't work**
The window minimises briefly while waiting for your click. If it doesn't restore, click the taskbar icon to bring it back — the coordinates should still have been captured.

**The app crashes on start**
Ensure you are on Python 3.7+ and have both `customtkinter` and `pynput` installed.

---

## Notes

- Use responsibly and only in applications or games where auto clicking is permitted.
- The Jitter mode is designed to be less detectable by basic anti-cheat systems, but is not guaranteed to bypass any specific software.

---

## License

Personal and educational use only.
