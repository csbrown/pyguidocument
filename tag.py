class panel:

    def __init__(self, length, width):
        self.boxes = [layer('default', (0,0,length,width))]

    def addlayer(self,layer):
        self.boxes.insert(0,layer)

    def liftlayer(self,tag):
        index = findlayer(tag)
        if index:
            self.boxes.insert(0,self.boxes.pop(index))

    def findlayer(self,tag):
        for i in range(len(self.boxes)):
            if self.boxes[i].tag == tag:
                return i
        return None

    def gettoplayer(self, x_coord, y_coord):
        for i in range(len(self.boxes)):
            if self.boxes[i].inlayer(x_coord, y_coord):
                return self.boxes[i]
        return None

    def removelayer(self, tag):
        index = self.findlayer(tag)
        if index != None:
            print self.boxes.pop(index)
        

class layer:

    def __init__(self,tag,box = None):
        self.tag = tag
        self.box = box
        self.text = ''

    def setroot(self, rootnode):
        self.rootnode = rootnode

    def addbox(self, box):
        if not self.box:
            self.box = box
        else:
            self.box = (min(self.box[0], box[0]),
                        min(self.box[1], box[1]),
                        max(self.box[2], box[2]),
                        max(self.box[3], box[3])
                       )

    def appendtext(self, text):
        self.text += text

    def gettext(self):
        return self.text

    def settext(self,text):
        self.text = text

    def inlayer(self, x_coord, y_coord):
        if self.box[0] <= x_coord <= self.box[2] and self.box[1] <= y_coord <= self.box[3]:
            return True
        return False
