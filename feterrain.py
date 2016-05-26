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
