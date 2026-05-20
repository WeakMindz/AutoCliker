import customtkinter as ctk
import webbrowser

# This creates the full path to the icon file


# Use that full path

# Main window
window = ctk.CTk()
window.geometry('350x500')
window.title('WeakMindz AutoClicker')


def switch_on():
    state = switch.get()
    if state == 1:
        ctk.set_appearance_mode("dark")
    else: 
        ctk.set_appearance_mode("light")
def start_pressed():
    print("Started")
def stop_pressed():
    print("Stopped")
def help_pressed():
    url = "https://github.com/WeakMindz/AutoCliker"
    webbrowser.open(url)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

StartButton =ctk.CTkButton(window,
                       text='Start',
                       command=start_pressed,
                       fg_color = "green")
StartButton.grid(row=190,column=0,sticky='sw',padx=20,pady=20)

StopButton =ctk.CTkButton(window,
                       text='Stop',
                       fg_color = "red",
                       command=start_pressed)
StopButton.grid(row=190,column=10,sticky='se',padx=20,pady=20)


switch = ctk.CTkSwitch(window,
                       text='Theme Toggle',
                       command=switch_on)
switch.grid(row=0, column=10, sticky="ne", padx=20, pady=20)

mode_list = ["Normal","Jitter"]
mode_label = ctk.CTkLabel(window, text="Mode")
mode_label.place(relx=0.05, rely=0.35)
modemenu = ctk.CTkOptionMenu(window,
                             values=mode_list)
modemenu.place(relx=0.05, rely=0.40)
cps_label = ctk.CTkLabel(window, text="Type CPS: ")
cps_label.place(relx=0.05, rely=0.5)
cps_testbox = ctk.CTkTextbox(window,
                             height=20,
                             width=140,
                             fg_color='grey',
                             text_color="white",
                             font=("Arial",30))

HelpButton =ctk.CTkButton(window,
                       text='Help',
                       fg_color = 'grey',
                       command=help_pressed)
HelpButton.grid(row=100,column=10,sticky='se',padx=20,pady=20)
                            
cps_testbox.place(relx=0.05, rely=0.55)
# Wait for interaction with the GUI
window.mainloop()