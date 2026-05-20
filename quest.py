import webbrowser
import keyboard

def your_toggle_function():
    url = "https://github.com/WeakMindz/AutoCliker"
    print("Hotkey pressed! Opening browser...")
    webbrowser.open(url)

# 1. Link the F6 key (or use 'x' since you're just testing)
keyboard.add_hotkey('F6', your_toggle_function)

print("Script is running... Press F6 to test it. Press Ctrl+C in the terminal to exit.")

# 2. This is the missing piece: it blocks the script from closing
keyboard.wait()