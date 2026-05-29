import customtkinter as ctk
import webbrowser
import threading
import time
import random

try:
    from pynput import mouse as pynput_mouse
    from pynput import keyboard as pynput_keyboard
    PYNPUT_OK = True
except ImportError:
    PYNPUT_OK = False

# ── Appearance ────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

DARK_BG            = "#1a1a1f"
DARK_SURFACE       = "#111115"
DARK_CARD          = "#22222a"
BORDER             = "#2e2e38"
TEXT_MUTED         = "#6b6b7a"
TEXT_DIM           = "#44444f"
GREEN              = "#16a34a"
GREEN_HOVER        = "#15803d"
GREEN_ACTIVE_BG    = "#1e3a1e"
GREEN_ACTIVE_TEXT  = "#4ade80"
BLUE_ACTIVE_BG     = "#172540"
BLUE_ACTIVE_BORDER = "#60a5fa"
BLUE_ACTIVE_TEXT   = "#60a5fa"

# ── Window ────────────────────────────────────────────────────────────────────
window = ctk.CTk()
window.geometry("370x760")
window.resizable(False, False)
window.title("WeakMindz AutoClicker")
window.configure(fg_color=DARK_BG)

# ── State ─────────────────────────────────────────────────────────────────────
selected_button   = "left"
selected_location = "current"
picked_x          = None
picked_y          = None
is_running        = False
click_thread      = None

hotkey_start  = "F6"
hotkey_stop   = "F7"
waiting_for   = None   # "start" | "stop" | None

_BUTTON_MAP = {
    "left":   pynput_mouse.Button.left   if PYNPUT_OK else None,
    "right":  pynput_mouse.Button.right  if PYNPUT_OK else None,
    "middle": pynput_mouse.Button.middle if PYNPUT_OK else None,
}

# ── Click loop ────────────────────────────────────────────────────────────────
def _click_loop():
    if not PYNPUT_OK:
        return
    mc = pynput_mouse.Controller()
    while is_running:
        try:
            cps = max(1, min(100, int(cps_entry.get())))
        except (ValueError, Exception):
            cps = 10

        btn = _BUTTON_MAP.get(selected_button, pynput_mouse.Button.left)

        if selected_location == "pick" and picked_x is not None and picked_y is not None:
            mc.position = (int(picked_x), int(picked_y))

        mc.press(btn)
        mc.release(btn)

        if selected_location == "pick" and picked_x is not None and picked_y is not None:
            # small jitter around the locked point when in jitter mode
            pass

        base_delay = 1.0 / cps
        if click_mode_var.get() == "Jitter":
            delay = base_delay + random.uniform(-base_delay * 0.2, base_delay * 0.2)
            delay = max(0.01, delay)
        else:
            delay = base_delay

        time.sleep(delay)

# ── Controls ──────────────────────────────────────────────────────────────────
def start_pressed():
    global is_running, click_thread
    if is_running:
        return
    is_running = True
    status_label.configure(text="● Running", text_color="#4ade80")
    click_thread = threading.Thread(target=_click_loop, daemon=True)
    click_thread.start()

def stop_pressed():
    global is_running
    is_running = False
    status_label.configure(text="● Idle", text_color=TEXT_MUTED)

def open_github():
    webbrowser.open("https://github.com/WeakMindz/AutoCliker")

def toggle_theme():
    ctk.set_appearance_mode("dark" if not theme_switch.get() else "light")

def increment_cps():
    try:
        val = int(cps_entry.get())
        cps_entry.delete(0, "end")
        cps_entry.insert(0, str(min(val + 1, 100)))
    except ValueError:
        pass

def decrement_cps():
    try:
        val = int(cps_entry.get())
        cps_entry.delete(0, "end")
        cps_entry.insert(0, str(max(val - 1, 1)))
    except ValueError:
        pass

def select_click_mode(mode):
    click_mode_var.set(mode)
    active   = dict(fg_color=GREEN_ACTIVE_BG, border_color=GREEN_ACTIVE_TEXT, text_color=GREEN_ACTIVE_TEXT)
    inactive = dict(fg_color="transparent",   border_color=BORDER,            text_color=TEXT_MUTED)
    btn_normal.configure(**(active if mode == "Normal" else inactive))
    btn_jitter.configure(**(active if mode == "Jitter" else inactive))
    mode_desc.configure(text="Steady, fixed click rate" if mode == "Normal"
                             else "Randomised timing — human-like")

def select_mouse_button(choice):
    global selected_button
    selected_button = choice
    active   = dict(fg_color=BLUE_ACTIVE_BG, border_color=BLUE_ACTIVE_BORDER, text_color=BLUE_ACTIVE_TEXT)
    inactive = dict(fg_color="transparent",  border_color=BORDER,             text_color=TEXT_MUTED)
    btn_left  .configure(**(active if choice == "left"   else inactive))
    btn_right .configure(**(active if choice == "right"  else inactive))
    btn_middle.configure(**(active if choice == "middle" else inactive))

def select_location_mode(mode):
    global selected_location
    selected_location = mode
    active   = dict(fg_color=BLUE_ACTIVE_BG, border_color=BLUE_ACTIVE_BORDER, text_color=BLUE_ACTIVE_TEXT)
    inactive = dict(fg_color="transparent",  border_color=BORDER,             text_color=TEXT_MUTED)
    btn_loc_current.configure(**(active if mode == "current" else inactive))
    btn_loc_pick   .configure(**(active if mode == "pick"    else inactive))
    if mode == "current":
        coord_x_label.configure(text="—")
        coord_y_label.configure(text="—")
        loc_hint.configure(text="Clicks follow your cursor in real time")
        btn_pick_coords.configure(state="disabled", fg_color="transparent",
                                  border_color=BORDER, text_color=TEXT_DIM)
    else:
        loc_hint.configure(text='Press "Pick" then click anywhere on screen')
        btn_pick_coords.configure(state="normal", fg_color=BLUE_ACTIVE_BG,
                                  border_color=BLUE_ACTIVE_BORDER, text_color=BLUE_ACTIVE_TEXT)

def start_pick():
    window.withdraw()
    loc_hint.configure(text="Click anywhere on screen…")
    def _capture():
        global picked_x, picked_y
        time.sleep(0.35)
        if PYNPUT_OK:
            captured = {}
            def on_click(x, y, button, pressed):
                if pressed:
                    captured["x"] = x
                    captured["y"] = y
                    return False
            with pynput_mouse.Listener(on_click=on_click) as listener:
                listener.join()
            picked_x = captured.get("x", 0)
            picked_y = captured.get("y", 0)
        else:
            picked_x = 0
            picked_y = 0
        window.after(0, _on_pick_done)
    threading.Thread(target=_capture, daemon=True).start()

def _on_pick_done():
    window.deiconify()
    coord_x_label.configure(text=str(picked_x))
    coord_y_label.configure(text=str(picked_y))
    loc_hint.configure(text=f"Locked to ({picked_x}, {picked_y})")

# ── Hotkeys ───────────────────────────────────────────────────────────────────
def _normalize_key(key):
    s = str(key).replace("Key.", "").replace("'", "")
    return s.upper()

def set_hotkey(target):
    global waiting_for
    waiting_for = target
    if target == "start":
        btn_set_start.configure(text="Press any key…", text_color="#facc15",
                                border_color="#facc15", fg_color="transparent")
    else:
        btn_set_stop.configure(text="Press any key…", text_color="#facc15",
                               border_color="#facc15", fg_color="transparent")

def _on_key_press(key):
    global waiting_for, hotkey_start, hotkey_stop
    label = _normalize_key(key)

    if waiting_for is not None:
        target = waiting_for
        waiting_for = None
        def _update():
            global hotkey_start, hotkey_stop
            if target == "start":
                hotkey_start = label
                btn_set_start.configure(text=f"Start: {label}",
                                        text_color=GREEN_ACTIVE_TEXT,
                                        border_color=GREEN_ACTIVE_TEXT,
                                        fg_color=GREEN_ACTIVE_BG)
            else:
                hotkey_stop = label
                btn_set_stop.configure(text=f"Stop: {label}",
                                       text_color="#f87171",
                                       border_color="#f87171",
                                       fg_color="#3a1e1e")
        window.after(0, _update)
        return

    if label == hotkey_start:
        window.after(0, start_pressed)
    elif label == hotkey_stop:
        window.after(0, stop_pressed)

def _start_kb_listener():
    if PYNPUT_OK:
        with pynput_keyboard.Listener(on_press=_on_key_press) as listener:
            listener.join()

threading.Thread(target=_start_kb_listener, daemon=True).start()

# ── Layout ────────────────────────────────────────────────────────────────────
click_mode_var = ctk.StringVar(value="Normal")

root = ctk.CTkFrame(window, fg_color=DARK_BG, corner_radius=0)
root.pack(fill="both", expand=True, padx=18, pady=18)

# Status pill
status_frame = ctk.CTkFrame(root, fg_color=DARK_SURFACE, corner_radius=99,
                              border_width=1, border_color=BORDER)
status_frame.pack(pady=(0, 16))
status_label = ctk.CTkLabel(status_frame, text="● Idle", text_color=TEXT_MUTED,
                              font=ctk.CTkFont(size=12, weight="bold"))
status_label.pack(padx=18, pady=6)

if not PYNPUT_OK:
    ctk.CTkLabel(root, text="⚠ pynput not installed — run: pip install pynput",
                 text_color="#f87171", font=ctk.CTkFont(size=11)).pack(pady=(0, 8))

# CPS
ctk.CTkLabel(root, text="CLICKS PER SECOND", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w")

cps_row = ctk.CTkFrame(root, fg_color="transparent")
cps_row.pack(fill="x", pady=(6, 0))

cps_entry = ctk.CTkEntry(cps_row, width=90, height=52, corner_radius=10,
                          fg_color=DARK_SURFACE, border_color=BORDER, border_width=1,
                          text_color="white", font=ctk.CTkFont(size=26, weight="bold"),
                          justify="center")
cps_entry.insert(0, "10")
cps_entry.pack(side="left")

ctk.CTkLabel(cps_row, text="CPS", text_color=TEXT_MUTED,
             font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(10, 0))

stepper = ctk.CTkFrame(cps_row, fg_color="transparent")
stepper.pack(side="left", padx=(10, 0))
ctk.CTkButton(stepper, text="▲", width=30, height=24, corner_radius=6,
              fg_color=DARK_SURFACE, hover_color=DARK_CARD, border_width=1,
              border_color=BORDER, text_color=TEXT_MUTED,
              font=ctk.CTkFont(size=10), command=increment_cps).pack(pady=(0, 4))
ctk.CTkButton(stepper, text="▼", width=30, height=24, corner_radius=6,
              fg_color=DARK_SURFACE, hover_color=DARK_CARD, border_width=1,
              border_color=BORDER, text_color=TEXT_MUTED,
              font=ctk.CTkFont(size=10), command=decrement_cps).pack()

# Click mode
ctk.CTkLabel(root, text="CLICK MODE", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(18, 6))

mode_row = ctk.CTkFrame(root, fg_color="transparent")
mode_row.pack(fill="x")
mode_row.columnconfigure((0, 1), weight=1)

btn_normal = ctk.CTkButton(mode_row, text="Normal", height=38, corner_radius=8,
                            fg_color=GREEN_ACTIVE_BG, hover_color="#254825",
                            border_width=1, border_color=GREEN_ACTIVE_TEXT,
                            text_color=GREEN_ACTIVE_TEXT,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            command=lambda: select_click_mode("Normal"))
btn_normal.grid(row=0, column=0, padx=(0, 5), sticky="ew")

btn_jitter = ctk.CTkButton(mode_row, text="Jitter", height=38, corner_radius=8,
                            fg_color="transparent", hover_color=DARK_CARD,
                            border_width=1, border_color=BORDER, text_color=TEXT_MUTED,
                            font=ctk.CTkFont(size=13, weight="bold"),
                            command=lambda: select_click_mode("Jitter"))
btn_jitter.grid(row=0, column=1, padx=(5, 0), sticky="ew")

mode_desc = ctk.CTkLabel(root, text="Steady, fixed click rate",
                          text_color=TEXT_MUTED, font=ctk.CTkFont(size=11))
mode_desc.pack(anchor="w", pady=(6, 0))

# Mouse button
ctk.CTkLabel(root, text="MOUSE BUTTON", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(18, 6))

mouse_row = ctk.CTkFrame(root, fg_color="transparent")
mouse_row.pack(fill="x")
mouse_row.columnconfigure((0, 1, 2), weight=1)

_mb = dict(height=38, corner_radius=8, border_width=1,
           font=ctk.CTkFont(size=12, weight="bold"))

btn_left = ctk.CTkButton(mouse_row, text="Left",
                          fg_color=BLUE_ACTIVE_BG, border_color=BLUE_ACTIVE_BORDER,
                          text_color=BLUE_ACTIVE_TEXT, hover_color="#1e2d4a",
                          command=lambda: select_mouse_button("left"), **_mb)
btn_left.grid(row=0, column=0, padx=(0, 4), sticky="ew")

btn_right = ctk.CTkButton(mouse_row, text="Right",
                           fg_color="transparent", border_color=BORDER,
                           text_color=TEXT_MUTED, hover_color=DARK_CARD,
                           command=lambda: select_mouse_button("right"), **_mb)
btn_right.grid(row=0, column=1, padx=(4, 4), sticky="ew")

btn_middle = ctk.CTkButton(mouse_row, text="Middle",
                            fg_color="transparent", border_color=BORDER,
                            text_color=TEXT_MUTED, hover_color=DARK_CARD,
                            command=lambda: select_mouse_button("middle"), **_mb)
btn_middle.grid(row=0, column=2, padx=(4, 0), sticky="ew")

# Click location
ctk.CTkLabel(root, text="CLICK LOCATION", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(18, 6))

loc_card = ctk.CTkFrame(root, fg_color=DARK_SURFACE, corner_radius=10,
                         border_width=1, border_color=BORDER)
loc_card.pack(fill="x")

loc_tab_row = ctk.CTkFrame(loc_card, fg_color="transparent")
loc_tab_row.pack(fill="x", padx=10, pady=(10, 6))
loc_tab_row.columnconfigure((0, 1), weight=1)

btn_loc_current = ctk.CTkButton(loc_tab_row, text="Current position", height=34,
                                 corner_radius=8, border_width=1,
                                 fg_color=BLUE_ACTIVE_BG, border_color=BLUE_ACTIVE_BORDER,
                                 text_color=BLUE_ACTIVE_TEXT, hover_color="#1e2d4a",
                                 font=ctk.CTkFont(size=12, weight="bold"),
                                 command=lambda: select_location_mode("current"))
btn_loc_current.grid(row=0, column=0, padx=(0, 4), sticky="ew")

btn_loc_pick = ctk.CTkButton(loc_tab_row, text="Pick location", height=34,
                              corner_radius=8, border_width=1,
                              fg_color="transparent", border_color=BORDER,
                              text_color=TEXT_MUTED, hover_color=DARK_CARD,
                              font=ctk.CTkFont(size=12, weight="bold"),
                              command=lambda: select_location_mode("pick"))
btn_loc_pick.grid(row=0, column=1, padx=(4, 0), sticky="ew")

coord_row = ctk.CTkFrame(loc_card, fg_color="transparent")
coord_row.pack(fill="x", padx=10, pady=(0, 6))
coord_row.columnconfigure((0, 1), weight=1)

x_box = ctk.CTkFrame(coord_row, fg_color=DARK_CARD, corner_radius=8,
                      border_width=1, border_color=BORDER)
x_box.grid(row=0, column=0, padx=(0, 4), sticky="ew")
ctk.CTkLabel(x_box, text="X", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=10, pady=(6, 0))
coord_x_label = ctk.CTkLabel(x_box, text="—", text_color=TEXT_MUTED,
                               font=ctk.CTkFont(size=16, weight="bold", family="Courier"))
coord_x_label.pack(anchor="w", padx=10, pady=(0, 6))

y_box = ctk.CTkFrame(coord_row, fg_color=DARK_CARD, corner_radius=8,
                      border_width=1, border_color=BORDER)
y_box.grid(row=0, column=1, padx=(4, 0), sticky="ew")
ctk.CTkLabel(y_box, text="Y", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=10, pady=(6, 0))
coord_y_label = ctk.CTkLabel(y_box, text="—", text_color=TEXT_MUTED,
                               font=ctk.CTkFont(size=16, weight="bold", family="Courier"))
coord_y_label.pack(anchor="w", padx=10, pady=(0, 6))

btn_pick_coords = ctk.CTkButton(loc_card, text="⊕  Pick point on screen",
                                 height=34, corner_radius=8, border_width=1,
                                 fg_color="transparent", border_color=BORDER,
                                 text_color=TEXT_DIM, state="disabled",
                                 hover_color=DARK_CARD,
                                 font=ctk.CTkFont(size=12, weight="bold"),
                                 command=start_pick)
btn_pick_coords.pack(fill="x", padx=10, pady=(0, 6))

loc_hint = ctk.CTkLabel(loc_card, text="Clicks follow your cursor in real time",
                         text_color=TEXT_DIM, font=ctk.CTkFont(size=11))
loc_hint.pack(anchor="w", padx=10, pady=(0, 10))

# Hotkeys
ctk.CTkLabel(root, text="HOTKEYS", text_color=TEXT_DIM,
             font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", pady=(18, 6))

hk_card = ctk.CTkFrame(root, fg_color=DARK_SURFACE, corner_radius=10,
                        border_width=1, border_color=BORDER)
hk_card.pack(fill="x")

hk_row = ctk.CTkFrame(hk_card, fg_color="transparent")
hk_row.pack(fill="x", padx=10, pady=(10, 6))
hk_row.columnconfigure((0, 1), weight=1)

btn_set_start = ctk.CTkButton(hk_row, text=f"Start: {hotkey_start}",
                               height=38, corner_radius=8, border_width=1,
                               fg_color=GREEN_ACTIVE_BG, border_color=GREEN_ACTIVE_TEXT,
                               text_color=GREEN_ACTIVE_TEXT, hover_color="#254825",
                               font=ctk.CTkFont(size=12, weight="bold"),
                               command=lambda: set_hotkey("start"))
btn_set_start.grid(row=0, column=0, padx=(0, 5), sticky="ew")

btn_set_stop = ctk.CTkButton(hk_row, text=f"Stop: {hotkey_stop}",
                              height=38, corner_radius=8, border_width=1,
                              fg_color="#3a1e1e", border_color="#f87171",
                              text_color="#f87171", hover_color="#4a2020",
                              font=ctk.CTkFont(size=12, weight="bold"),
                              command=lambda: set_hotkey("stop"))
btn_set_stop.grid(row=0, column=1, padx=(5, 0), sticky="ew")

ctk.CTkLabel(hk_card, text="Click a button above then press any key to rebind",
             text_color=TEXT_DIM, font=ctk.CTkFont(size=11)).pack(
             anchor="w", padx=10, pady=(0, 10))

# Divider
ctk.CTkFrame(root, height=1, fg_color=BORDER, corner_radius=0).pack(fill="x", pady=16)

# Theme toggle
theme_row_frame = ctk.CTkFrame(root, fg_color="transparent")
theme_row_frame.pack(fill="x", pady=(0, 14))
ctk.CTkLabel(theme_row_frame, text="Dark mode", text_color=TEXT_MUTED,
             font=ctk.CTkFont(size=13)).pack(side="left")
theme_switch = ctk.CTkSwitch(theme_row_frame, text="", width=46,
                              button_color=GREEN, button_hover_color=GREEN_HOVER,
                              progress_color=GREEN, command=toggle_theme)
theme_switch.select()
theme_switch.pack(side="right")

# Action buttons
action_row = ctk.CTkFrame(root, fg_color="transparent")
action_row.pack(fill="x")
action_row.columnconfigure((0, 1), weight=1)

ctk.CTkButton(action_row, text="▶  Start", height=44, corner_radius=10,
              fg_color=GREEN, hover_color=GREEN_HOVER, text_color="white",
              font=ctk.CTkFont(size=14, weight="bold"),
              command=start_pressed).grid(row=0, column=0, padx=(0, 5), sticky="ew")

ctk.CTkButton(action_row, text="■  Stop", height=44, corner_radius=10,
              fg_color=DARK_SURFACE, hover_color=DARK_CARD,
              border_width=1, border_color=BORDER, text_color=TEXT_MUTED,
              font=ctk.CTkFont(size=14, weight="bold"),
              command=stop_pressed).grid(row=0, column=1, padx=(5, 0), sticky="ew")

ctk.CTkButton(root, text="? Help", height=36, corner_radius=8,
              fg_color="transparent", hover_color=DARK_CARD,
              border_width=1, border_color=BORDER, text_color=TEXT_DIM,
              font=ctk.CTkFont(size=12), command=open_github).pack(fill="x", pady=(10, 0))

# ── Run ───────────────────────────────────────────────────────────────────────
window.mainloop()
