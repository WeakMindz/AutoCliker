<<<<<<< HEAD
import pyautogui
import time

#Might have to make it random 
cps = 10 
delay = 0.16 / cps
duration_seconds = 10  #time this runs for

print("3 seconds to start")
time.sleep(3)

start_time = time.time()


while time.time() - start_time < duration_seconds:
    pyautogui.click()
    time.sleep(delay)
        
    print("Finshed.")

=======
import pyautogui
import time
import random 
randomcps  = 0
def guard(randomcps):
    randomcps = random.randint(8,12)
    return randomcps 
#Might have to make it random 
cps = 10 
delay = 0.16 / cps
duration_seconds = 10  #time this runs for

print("3 seconds to start")
time.sleep(3)

start_time = time.time()


while time.time() - start_time < duration_seconds:
    pyautogui.click()
    time.sleep(delay)
        
    print("Finshed.")

>>>>>>> 20291c9397c4d71035c8c012150f23ac2e87641e
