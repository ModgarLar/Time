import tkinter as tk
from tkinter import ttk
from index import *


def createFrame(frame,wb,data):
    datos = main(wb,data)
    print(datos)
    frame.destroy()
    frame = tk.Frame(root)
    tabControl = ttk.Notebook(frame)
    tabControl.pack()
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab1,text='Horario')
    tabControl.add(tab2,text="Time Tracking")
    tabControl.pack(expand=1, fill="both")
    frame.pack()



root = tk.Tk()
wb = startSession()
data = getJsonData('saved_records.json')
frame = tk.Frame(root)
frame.pack()


button = tk.Button(frame,text="Syncro", command=lambda: createFrame(frame,wb,data))

button.pack()

root.mainloop()


