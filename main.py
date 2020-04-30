import tkinter as tk
from index import *

root = tk.Tk()
sheets = startSession()
data = getJsonData('saved_records.json')
frame = tk.Frame(root)
frame.pack()
button = tk.Button(frame,text="Syncro", command=lambda: main(sheets,data))

button.pack()

root.mainloop()


