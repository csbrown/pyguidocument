
from Tkinter import *
from PIL import Image, ImageTk
import sys
from tag import *
import pickle


class brush:

    def __init__(self):
        self.color = 'black'
        self.tag = 'default'
        self.width = 20
        self.stipple = 'gray12'


class Painter(Tk):

    #background should be local
    def __init__(self, backgroundfilename, previouswork = False, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)

        self.backgroundfilename = backgroundfilename
        self.background = Image.open(backgroundfilename)
        self.background_image= ImageTk.PhotoImage(self.background) 
        

        #Stuff for motion
        self.b1 = "up"
        self.xold, self.yold = None, None
    
        #Toggle between modes
        self.brushon = False
        
        #Keeps track of brush items   
        self.mybrush = brush()
    
        #Starts a tagging object
        if previouswork:
            self.mypanel = pickle.load(open(previouswork, 'r'))
        else:
            self.mypanel = panel(self.background.size[0], self.background.size[1])


        #The text widget which isn't up by default
        self.text_widget = None
        self.selectedlayer = None


        self.drawing_area = Canvas(self, width=self.background.size[0], height=self.background.size[1])
        self.drawing_area.pack(side='top', fill='both', expand='yes')
        self.drawing_area.create_image(20, 20, image=self.background_image, anchor='nw')

        self.entry = Entry(self, width = 50)
        self.entry.pack()
        self.entry.focus_set()

        self.entry.bind("<Return>", self.gettext)

        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)

    #Interprets the text from the text entry area.  This method is fragile because I'm lazy, so don't enter anything that won't work
    def textinterpreter(self,text):
        ooedtext = text.split('.')
        
        if ooedtext[0] == 'print':
            for box in self.mypanel.boxes:
                print box.tag, box.box
            

        if ooedtext[0] == 'dump':
            pickle.dump(self.mypanel, open(self.backgroundfilename.split('.')[0] + '.boxes', 'w'))          
            return
        
        if ooedtext[0] == 'rm' and len(ooedtext)>1:
            self.mypanel.removelayer(ooedtext[1])

        #Brush options
        if ooedtext[0] == 'brush' and len(ooedtext) > 1:
            
            ######################################
            #Brush toggles
            if ooedtext[1] == 'on':
                self.brushon = True
                return

            if ooedtext[1] == 'off':
                self.brushon = False
                return
                        
        

            ######################################
            #Brush values
            changes = ooedtext[1].split('=')
        
            if len(changes) < 2:
                print 'hey'
                return
            
            if changes[0].strip() == 'color':
                print 'bazinga!'
                self.mybrush.color = changes[1].strip()
                return
        
            if changes[0].strip() == 'tag':
                self.mybrush.tag = changes[1].strip()
                if self.mybrush.tag not in self.mypanel.boxes:
                    self.mypanel.addlayer(layer(self.mybrush.tag))
                else:
                    self.mypanel.liftlayer(self.mybrush.tag)
                return
        
            if changes[0].strip() == 'width':
                self.mybrush.width = int(changes[1].strip())
                return
        
            if changes[0].strip() == 'stipple':
                self.mybrush.stipple = changes[1].strip()
                return
        
                    
    #Callback to get text from the text entry area
    def gettext(self,event):
        self.textinterpreter(event.widget.get())
        event.widget.delete(0,END)
    
    def maketextwidget(self, x, y, text):

        self.text_widget = Text(self)

        self.text_widget.insert(0.0,text)

        self.text_widget.place(x = x, y = y) # show the widget

        self.text_widget.lift()

    ############################################
    #EVENTS
    ###########################################

    #Mouse button 1 down
    def b1down(self,event):
        self.b1 = "down"
        if not self.brushon:
            if self.text_widget:
                if self.selectedlayer:
                    self.selectedlayer.settext(self.text_widget.get(1.0,END))
                self.text_widget.destroy()
                self.text_widget=None
            else:
                self.selectedlayer = self.mypanel.gettoplayer(event.x, event.y)
                #Should exist if clicking inside the canvas, since default spans the whole thing, but check just in case...
                if self.selectedlayer:
                    self.maketextwidget(event.x, event.y, self.selectedlayer.gettext())        

            
            
            

    #Mouse button 1 up
    def b1up(self,event):
        self.b1 = "up"
        self.xold = None           # reset the line when you let go of the button
        self.yold = None


    #Mouse dragged
    def motion(self,event):
        canvas = event.widget
        if self.b1 == "down" and self.brushon:
            if self.xold is not None and self.yold is not None:
                box = canvas.bbox( 
                    canvas.create_line(self.xold,self.yold,event.x,event.y,smooth=TRUE,width=self.mybrush.width, stipple=self.mybrush.stipple, fill=self.mybrush.color)
                )
                print box
                self.mypanel.boxes[self.mypanel.findlayer(self.mybrush.tag)].addbox(box)               
                

            self.xold = event.x
            self.yold = event.y


if __name__ == "__main__":

    if len(sys.argv) > 2:
        paint = Painter(sys.argv[1], previouswork = sys.argv[2])
    else:
        paint = Painter(sys.argv[1])
    paint.mainloop()

    
    
