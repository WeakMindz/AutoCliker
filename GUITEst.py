import customtkinter as ctk

# Main window
window = ctk.CTk()
window.geometry('555x550')
window.title('Switch')

def switch_on():
    state = switch.get()
    if state == 1:
        ctk.set_appearance_mode("dark")
    else: 
        ctk.set_appearance_mode("light")
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# CTkSwitch
switch = ctk.CTkSwitch(window,
                       text='Example Switch',
                       command=switch_on)
switch.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

# Wait for interaction with the GUI
window.mainloop()