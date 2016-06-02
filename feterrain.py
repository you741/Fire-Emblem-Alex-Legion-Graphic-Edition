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
