# WeakMindz AutoClicker

A lightweight desktop auto clicker built with Python, featuring a dark-themed GUI powered by CustomTkinter.

---

## Changelog

### feat: add Start, Stop, Help buttons + CPS input + mode selector

- Add green Start button and red Stop button positioned bottom-left and bottom-right
- Add grey Help button linking to the GitHub repo via `webbrowser`
- Add Mode dropdown (`CTkOptionMenu`) with Normal and Jitter options
- Add CPS text input box (`CTkTextbox`) for typing a clicks-per-second value
- Add mode and CPS labels to the GUI
- Resize window to 350×500
- Rename window title to `WeakMindz AutoClicker`

### feat: add dark/light mode toggle via CTkSwitch

- Add CTkSwitch with `switch_on()` callback
- Toggle between dark/light appearance using `ctk.set_appearance_mode()`
- Switch positioned top-right with `grid sticky="ne"`

---

## Features

- Dark/light mode toggle switch
- Green Start button and red Stop button
- Mode selector: Normal or Jitter
- CPS (clicks per second) input box
- Help button linking to the GitHub repo
- Dark mode GUI via CustomTkinter

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
python main.py
```

A 350×500 window will appear with all controls ready to use.

---

## Instructions

1. **Launch the app** by running `python main.py`.
2. **Set your CPS** by typing a number into the CPS input box (e.g. `10` for 10 clicks per second).
3. **Choose a mode** from the dropdown:
   - `Normal` — clicks at a steady, fixed rate.
   - `Jitter` — adds slight randomness between clicks to simulate human behaviour.
4. **Press Start** (green button, bottom-left) to begin auto clicking.
5. **Press Stop** (red button, bottom-right) to stop auto clicking.
6. **Toggle the theme** using the switch in the top-right corner to switch between dark and light mode.
7. **Need help?** Press the Help button to open the GitHub page.

---

## Project Structure

```
main.py      # Main application file
README.md    # This file
```

---

## Known Issues / TODO

- [ ] Start and Stop buttons are not yet wired to the click loop (both currently call `start_pressed`)
- [ ] Click loop needs to run in a background thread so the GUI stays responsive
- [ ] CPS input box is not yet connected to the click speed
- [ ] Jitter mode is listed but not yet implemented
- [ ] Hotkey support not yet implemented (`keyboard` import unused)
- [ ] No right-click or middle-click support yet

---

## License

This project is for personal/educational use. Use responsibly and only on applications/games where auto clicking is permitted.
