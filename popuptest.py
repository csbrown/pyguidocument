from Tkinter import *
from PIL import Image, ImageTk

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.username = 'Bob' # a default name
        background = Image.open('CC.png')
        background_image= ImageTk.PhotoImage(background)  
    
        drawing_area = Canvas(self, width=background.size[0], height=background.size[1])
        drawing_area.pack(side='top', fill='both', expand='yes')
        drawing_area.create_image(0, 0, image=background_image, anchor='nw')
    
        e = Entry(self, width = 50)
        e.pack()
        e.focus_set()
    
        e.bind("<Return>", self.gettext)

        drawing_area.bind("<ButtonPress-1>", self.b1down)
 
    def gettext(self):
        blah = 1

    def msg_box(self, msg='User name?', extra=True):
        top = self.top = Toplevel(self)
        label0 = Label(top, text=msg)
        label0.pack()

        if extra:
            self.entry0 = Entry(top)
            self.entry0.pack()

            button2 = Button(top, text='Submit', command=self.submit_name)
            button2.pack()

        button3 = Button(top, text='Cancel',
                                command=lambda: self.top.destroy())
        button3.pack()

    def submit_name(self):
        data = self.entry0.get()
        if data:
            self.username = data
            self.top.destroy()


    #Mouse button 1 down
    def b1down(self, event):
        self.msg_box()


gui = GUI()
gui.mainloop()
