class Menu():
    def __init__(self, x=0,y=0,width=0,height=0,background=Surface((1,1)),selected=0,items=[]):
        self.x = x #co-rds
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = backgroud #background of the menu, will most likely be a rectangle that we stretch (<> -> <==========>)
        self.selected = selected #which item is being selected
        self.items = items #items in the menu (this will most likely be 2d with commands
    def moveSelect(self):
        "moves menu selector and returns new value"
        #moves self.selected up and down
        kp = key.get_pressed()
        if kp[K_UP]:
            self.selected -= 1
        elif kp[K_DOWN]:
            self.selected += 1
        #wrapping around seleced
        if self.selected < 0:
            self.selected = len(items) - 1
        elif self.selected >= len(items):
            self.selected = 0
 
