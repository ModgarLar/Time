import tkinter as tk
import threading
import time
from tkinter import ttk
from index import *


def createFrame(frame,wb,data):
    frame.destroy()
    frame = tk.Frame(root)
    frame.pack()
    datos = main(wb,data)
    print(datos)

    tabControl = ttk.Notebook(frame)
    tabControl.pack()
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab1,text='Ticket')
    tabControl.add(tab2,text="Time Tracking")
    tabControl.pack(expand=1, fill="both")




root = tk.Tk()
wb = startSession()
data = getJsonData('saved_records.json')
frame = tk.Frame(root)
frame.pack()


button = tk.Button(frame,text="Syncro", command=lambda: createFrame(frame,wb,data))

button.pack()

root.mainloop()


