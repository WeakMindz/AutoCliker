import customtkinter as ctk
from pynput.mouse import Button, Controller 
from pynput import keyboard
import random
import time
#Object created 
mouse = Controller()
app = ctk.CTk() 
#Basic thing need to run this 
app.geometry("400x300")
app.title("WeakMindz AutoClicker")

ctk.set_appearance_mode("dark") 
clicking = False
def button_event():
    print("button pressed")
time.sleep(3)
clicking = True
button = ctk.CTkButton(app, text="CTkButton", command=button_event)
while clicking == True:
    mouse.click(Button.left)
    time.sleep(0.09)
def isClicking():
    cps = input("enter the cps")
    delay = 1/cps 
    time.sleep(delay)
app.mainloop()