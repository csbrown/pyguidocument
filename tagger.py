
from tag import *
import pickle

class tagnode:
    
    #parent should be either another tagnode or None for the root node
    def __init__(self, parent):
        self.parent = parent
        self.children = []
        self.text = ''

    def addchild(self, child):
        self.children.append(child)

    def appendtext(self, text):
        self.text += text

    def gettext(self):
        return self.text

    def settext(self,text):
        self.text = text

        
def main():
    global background
    root = Tk()

    background_image= ImageTk.PhotoImage(background)  

    drawing_area = Canvas(root, width=background.size[0], height=background.size[1])
    drawing_area.pack(side='top', fill='both', expand='yes')
    drawing_area.create_image(0, 0, image=background_image, anchor='nw')

    e = Entry(root, width = 50)
    e.pack()
    e.focus_set()

    e.bind("<Return>", gettext)

    drawing_area.bind("<Motion>", (lambda x: motion(drawing_area, x)))
    drawing_area.bind("<ButtonPress-1>", b1down)
    drawing_area.bind("<ButtonRelease-1>", b1up)
    root.mainloop()  






############################################
#EVENTS
###########################################

#Mouse button 1 down
def b1down(event):
    global b1
    b1 = "down"           # you only want to draw when the button is down
                          # because "Motion" events happen -all the time-

#Mouse button 1 up
def b1up(event):
    global b1, xold, yold
    b1 = "up"
    xold = None           # reset the line when you let go of the button
    yold = None


#Mouse dragged
def motion(canvas, event):
    if b1 == "down":
        global xold, yold, mybrush, mycolorbynumber
        if xold is not None and yold is not None:
            mycolorbynumber.boxes[mycolorbynumber.findtaggedbox(mybrush.tag)].addbox(
                canvas.bbox( 
                    event.widget.create_line(xold,yold,event.x,event.y,smooth=TRUE,width=mybrush.width, stipple=mybrush.stipple, fill=mybrush.color)
                )
            )                
            

        xold = event.x
        yold = event.y


if __name__ == "__main__":
    #The image to draw on and tag is the only command line argument for the program
    background = Image.open(sys.argv[1])

    #Stuff for motion
    b1 = "up"
    xold, yold = None, None

    #Keeps track of brush items    
    mybrush = brush()

    #Starts a tagging object
    mycolorbynumber = colorbynumber(background)
    main()

    pickle.load(open(sys.argv[1], 'r'))

