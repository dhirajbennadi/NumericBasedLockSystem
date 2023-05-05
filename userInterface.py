import serial
import time
from datetime import datetime
import random
from threading import Timer

import tkinter as tk

#Global variables
ser = None
entry = None

root = tk.Tk()

#Screen unit to pixel
# Dimensions of the Window
root.geometry("400x200")
root.title("ZigBee Based Numeric Lock System")

# create a Text widget for output
output_text = tk.Text(root, height=5, width=30)
output_text.pack()

# label = tk.Label(root, text="Enter the Device Name :")
# label.pack()

# entry = tk.Entry(root)
# entry.pack()


def activate_buttons():
    time.sleep(5)
    ser.write(b'Device1')
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "Device Information Sent!\n")
    output_text.config(state=tk.DISABLED)
    time.sleep(4)
    #entry.delete(0, tk.END)
    incoming = ser.readline().strip()
    #print(incoming)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    print(incoming)
    output_text.insert(tk.END, "Key Received : " + str(incoming) )
    output_text.config(state=tk.DISABLED)
    #entry.delete(0, tk.END)
    time.sleep(2)

    

submit_button = tk.Button(root, text="Send", command=activate_buttons)
submit_button.pack()



# Enable USB Communication
ser = serial.Serial('COM3', 115200,timeout=.5)

while True:
    root.mainloop()








