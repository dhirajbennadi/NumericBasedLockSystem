import serial
import time
from datetime import datetime
import random
from threading import Timer

import tkinter as tk

#Global variables
ser = None
entry = None


# Enable USB Communication
ser = serial.Serial('COM4', 115200,timeout=.5)

flag = 0

def generateRandomNumber():
    random.seed(random.randint(0,1000))
    randomNumber = random.randint(0 , 100000)
    
    return randomNumber

listDevices = ["Device1", "Device2"]

def checkDeviceName(name):
    for i in listDevices:
        if(name == i):
            return True

    return False

# lockNumber is used to compare the lock to unlock/lock
lockNumber = 0
def setLockNumber(randomLockNumber):
    global lockNumber 
    lockNumber = randomLockNumber

def checkLock(randomNumber):
    global lockNumber
    if lockNumber == randomNumber:
        return True

    return False


def activate_buttons():
    text = entry.get()
    #print(text)
    
    if checkLock(int(text)):
        button2["state"] = "disabled"
        entry.delete(0, tk.END)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Device Unlocked")
        output_text.config(state=tk.DISABLED)
        
    else:
        button2["state"] = "normal"

    
root = tk.Tk()

#Screen unit to pixel
# Dimensions of the Window
root.geometry("400x200")
root.title("ZigBee Based Numeric Lock System")

# create a Text widget for output
output_text = tk.Text(root, height=5, width=20)
output_text.pack()


label = tk.Label(root, text="Enter the Numeric Code :")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="#", command=activate_buttons)
submit_button.pack()


def step1():
    global ser
    global flag
    time.sleep(5)
    if flag == 0:
        print("Reading")
        incoming = ser.readline().strip()
        print(incoming)
        retValue = checkDeviceName(incoming.decode())
        if retValue:
            flag = 1
            #output_text.insert(0, "Device Verified")
            print("Device Verified")
            output_text.delete("1.0", tk.END)
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, "Device Verified!\n")
            output_text.config(state=tk.DISABLED)
            time.sleep(1)
            step2()
            #time.sleep(30)
        ser.reset_input_buffer()
        #time.sleep(2)
        

def step2():
    global ser
    
    #incomingLine = ser.readline().strip()
    randomNumber = generateRandomNumber()
    #print(randomNumber)
    data = str(randomNumber)
    ser.write(data.encode('utf-8'))
    #output_text.delete('0',tk.END)
    #output_text.insert(tk.END, "Random Number Sent!")
    print("Random Number Sent")
    #output_text.delete(0, tk.END)
    #output_text.insert(tk.END, "Random Number Sent")
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "Random Number Sent!\n")
    output_text.config(state=tk.DISABLED)
    setLockNumber(randomNumber)
    time.sleep(1)

def step3():
    global flag
    time.sleep(30)
    #output_text.delete('0',tk.END)
    #output_text.insert(tk.END, "Time Elapsed, Verify device again !!")
    flag = 0   

step1Button = tk.Button(root, text="Step 1 : Verify Device", command=step1)
step1Button.pack()


button2 = tk.Button(root, text="Lock Status", state="normal")
button2.pack()

while True:
    root.mainloop()


while True:
    #root.mainloop()
    
    if flag == 0:
        incoming = ser.readline().strip()
        #print(incoming)
        #retValue = checkDeviceName("Device1")
        #print(retValue)
        retValue = checkDeviceName(incoming.decode())
        #print(retValue)
        if retValue:
            flag = 1
            #print("Device Verified")
            output_text.insert(tk.END, "Device Verified!")
        time.sleep(2)
    elif flag == 1:
        incoming = ser.readline().strip()
        randomNumber = generateRandomNumber()
        #print(randomNumber)
        data = str(randomNumber)
        ser.write(data.encode('utf-8'))
        output_text.delete('0',tk.END)
        output_text.insert(tk.END, "Random Number Sent!")
        #print("Random Number Sent")
        setLockNumber(randomNumber)
        flag = 2
        time.sleep(2)
    elif flag == 2:
        #Keep waiting for random
        
        time.sleep(30)
        output_text.delete('0',tk.END)
        output_text.insert(tk.END, "Time Elapsed, Verify device again !!")
        flag = 0
    
    
    root.update()
        
        
    '''
        userLockNumber = 0
        timeout = 10
        t = Timer(timeout, print, ['Sorry, times up'])
        t.start()
        prompt = "You have %d seconds to choose the correct answer...\n" % timeout
        #userLockNumber = input("Enter the Lock Number :")
        userLockNumber = input(prompt)
        #t.cancel()
        
        if checkLock(int(userLockNumber)) == True:
            print("Lock Opened")
            exit()
        else:
            print("Lock Number Error")
    '''







