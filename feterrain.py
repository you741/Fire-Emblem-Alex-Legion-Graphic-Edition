#Terrain classes
class Terrain():
    "terrain class"
    def __init__(self,name,adef,avo,hind,img=None):
        "initialize terrain"
        self.name = name
        self.adef = adef
        self.avo = avo
        self.hind = hind
        self.img = img
class Chest(Terrain):
    "chest class"
    def __init__(self,name,adef,avo,hind,img=None,item=None):
        self.name = name
        self.adef = adef
        self.avo = avo
        self.hind = hind
        self.img = img
        self.item = item
class Vendor(Terrain):
    "vendor class"
    def __init__(self,name,adef,avo,hind,img=None,items=[]):
        super(Vendor,self).__init__(name,adef,avo,hind,img)
        self.items = items
    def setItems(self,items):
        "sets items and returns the vendor"
        self.items = items
        return self.getInstance()
    def getInstance(self):
        return Vendor(self.name,self.adef,self.avo,self.hind,self.img,self.items)
class Armory(Terrain):
    "armory class"
    def __init__(self,name,adef,avo,hind,img=None,items=[]):
        super(Armory,self).__init__(name,adef,avo,hind,img)
        self.items = items
    def setItems(self,items):
        "sets items and returns the armory"
        self.items = items
        return self.getInstance()
    def getInstance(self):
        return Armory(self.name,self.adef,self.avo,self.hind,self.img,self.items)

class Village(Terrain):
    "village class"
    def __init__(self,name,adef,avo,hind,img=None,item=None,story=""):
        self.name = name
        self.adef = adef
        self.avo = avo
        self.hind = hind
        self.img = img
        self.item = item
        self.story = story
        self.visited = False
        if self.story != "":
            pass #get file here
    def setItems(self,item,story):
        self.item = item
        self.story = story
        return self.getInstance()
    def getInstance(self):
        return Village(self.name,self.adef,self.avo,self.hind,self.img,self.item,self.story)
