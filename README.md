# WeakMindz AutoClicker

A lightweight desktop auto clicker built with Python, featuring a dark-themed GUI powered by CustomTkinter.

---

## Features

- Dark mode GUI via CustomTkinter
- Automated left mouse button clicking
- Configurable click interval (currently set to ~0.09s / ~11 clicks per second)
- Simple start/stop button interface

---

## Requirements

- Python 3.7+
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [pynput](https://pypi.org/project/pynput/)

Install dependencies with:

```bash
pip install customtkinter pynput
```

---

## How to Run

```bash
python autoclicker.py
```

A 400×300 dark-themed window will appear. Use the button to control clicking behavior.

---

## Usage

1. Launch the app.
2. Position your mouse where you want clicks to occur.
3. Press the button to start/stop the auto clicker.

> **Note:** The click loop currently runs at approximately **11 clicks per second** (0.09s delay between clicks).

---

## Project Structure

```
autoclicker.py   # Main application file
README.md        # This file
```

---

## Known Issues / TODO

- [ ] The click loop (`while clicking == True`) runs **before** `app.mainloop()` is called, meaning the GUI never renders and the loop never actually triggers (since `clicking` starts as `False`). This needs to be moved into a background thread.
- [ ] The button does not yet toggle the `clicking` variable — `button_event` only prints to console.
- [ ] No hotkey support implemented yet (keyboard import is unused).
- [ ] No CPS (clicks per second) selector in the UI.
- [ ] No support for right-click or middle-click yet.

---

## Planned Improvements

- Toggle clicking on/off via button and/or hotkey (e.g. F6)
- Adjustable CPS slider in the GUI
- Click type selector (left, right, middle)
- Random interval jitter to simulate human clicking (groundwork already imported via `random`)
- Hold-to-click mode

---

## License

This project is for personal/educational use. Use responsibly and only on applications/games where auto clicking is permitted.


