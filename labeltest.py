from Tkinter import *

def b1downonlabel(widget, entry):
    if widget.cget('state') == 'active':
        widget.configure(state = 'normal')
    else:
        widget.configure(state = 'active')
    

master = Tk()

w = Label(master, text="Hello, world!", bg = 'red', activebackground = 'blue', state = 'normal')
w.grid()
w.bind("<ButtonPress-1>", lambda entry: b1downonlabel(w, entry))

s = Label(master, text="Hello,\n squirrel!")
s.grid()

mainloop()
