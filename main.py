#Fire Emblem Alex Legion
#This game is a Fire Emblem Spin-off featuring my own unique characters named after my classmates
#The user controls an army that fights off the enemy's army for multiple levels to win
#There is also a great story line

#----DEFAULT MODULE IMPORTS
import os
from pygame import *
import time as time2
from math import *
from random import *
#----CUSTOM MODULE IMPORTS
from feclasses import *
from festaples import *
from feterrain import *
from feweapons import *
from fesprites import *
font.init()
#----METADATA----#
__author__ = "Yttrium Z (You Zhou)"
__date__ = "Incomplete"
__purpose__ = "Game for Grade 11 final project"
__name__ = "Fire Emblem Alex Legion"
__copyright__ = "Yttrium Z 2015-2016"
#----SETUP----#
os.environ['SDL_VIDEO_WINDOW_POS'] = '25,25'
screen = display.set_mode((1200,720))
display.set_caption("YTTRIUM Z PRESENTS ~~~~~~~FIRE EMBLEM ALEX LEGION~~~~~~~","Fire Emblem Alex Legion")
#----COLORS----#
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
#----FONTS----#
timesnr = font.SysFont("Times New Roman",15)
comicsans = font.SysFont("Comic Sans MS",25)
arial = font.SysFont("Arial",15)
monospace = font.SysFont("Monospace",15)
smallsans = font.SysFont("Comic Sans MS",15)
sans = font.SysFont("Comic Sans MS",20)
papyrus = font.SysFont("Papyrus",20)
#----IMAGE LOAD----#
logo = image.load("images/logo.png")
#TERRAIN
plain = Terrain("Plain",0,0,1)
#WEAPONS
real_knife = Weapon("Real Knife",99,1,1000,999,"Sword",600)
iron_bow = Weapon("Iron Bow",6,6,46,80,"Bow",100,0,2,46,False,[],2)
iron_lance = Weapon("Iron Lance",7,8,45,80,"Lance",100)
silver_lance = Weapon("Silver Lance",14,10,20,75,"Lance",100)
fire = Weapon("Fire",5,4,40,95,"Anima",100,0,1,40,True,"",2)
slim_sword = Weapon("Slim Sword",3,2,35,100,"Sword",200,5)
steel_sword = Weapon("Steel Sword",8,10,30,80,"Sword",200)
iron_sword = Weapon("Iron Sword",5,5,47,90,"Sword",100)
iron_axe = Weapon("Iron Axe",8,10,45,75,"Axe",100)
rapier = Weapon("Rapier",7,5,40,90,"Sword",700,10,1,40,False,["Cavalier","Paladin","Knight","General"],1,5,"Effective against knights, cavalry","Yoyo")
vulnerary = Consumable("Vulnerary",10,3,"Heals for 10 HP")

#TRANSLUCENT SQUARES
transBlue = Surface((30,30), SRCALPHA)
transBlue.fill((0,0,255,122))
transRed = Surface((30,30), SRCALPHA)
transRed.fill((255,0,0,122))
transBlack = Surface((1200,720), SRCALPHA)
transBlack.fill((0,0,0,122))
#----PERSONS----#
moved,attacked = set(),set() #sets of allies that already moved or attacked
#ALLIES
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":4,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
               [rapier.getInstance(),iron_bow.getInstance(),vulnerary.getInstance()],{"Sword":200},
               {"Sword":(yoyoAttackSprite,5),"Swordcrit":(yoyoCritSprite,29),"stand":yoyoStandSprite}) #test person
allies = [yoyo] #allies
#ENEMIES
dummy = Brigand("Dummy",0,0,
                  {"stren":3,"defen":3,"skl":3,"lck":0,
                   "spd":3,"con":3,"move":3,"res":0,"hp":33,"maxhp":33},{},[iron_bow.getInstance()],{"Bow":600},
                {"Bow":([],0),"Bowcrit":([],0),"stand":Surface((1,1))})
enemies = []
#----CHAPTERS----#
#MAPS
chapter0 = [[plain for i in range(40)] for j in range(24)]
#CHAPTER DATA
#Stored in tuples
#(allyCoordinates,Enemies,Goal)
chapterData = [([(0,0)],createEnemyList([dummy],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies")] #chapter data, chapter is determined by index
oldAllies = [a.getInstance() for a in allies] #keeps track of allies before the fight
#----GLOBAL VARIABLES----#
name = "" #name of player
player = None
#important variables for the Game class
chapter = 0
mode = "freemove" #mode Game Mode is in
goal = ""
selected = None #selected Person
selectedItem = None #selected Item
attackableEnemies = [] #attackable enemies of the selected person
selectedEnemy = 0 #selected Enemy
menu = None #options in menu
menuselect = 0 #option selected in the menu
framecounter = 0
filler = Surface((1200,720))
selectx,selecty = 0,0 #select points
#----GLOBAL FUNCTIONS----#
#LIKE TURN STARTING, GAME OVER SCREENS, SAVING
#PRETTY MUCH GLOBAL AFFECTORS (Sorry I'm really bad at naming things)
def startTurn():
    "starts the turn"
    global allies,enemies,moved,attacked
    screenBuff = screen.copy() #sets the screenBuffer to cover up the text
    screen.blit(transform.scale(transBlue,(1200,60)),(0,330)) #blits the text "PLAYER PHASE" on a translucent blue strip
    screen.blit(papyrus.render("PLAYER PHASE",True,WHITE),(450,340))
    moved.clear() #empties moved and attacked
    attacked.clear()
    display.flip() #updates screen
    time.wait(1000)
    screen.blit(screenBuff,(0,0)) #covers up text
    display.flip()
def gameOver():
    "game over screen - might be a class later"
    for i in range(50):
        screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fadinge effect
        display.flip()
        time.wait(50)
    screen.blit(papyrus.render("GAME OVER",True,(255,0,0)),(500,300))
    display.flip()
def start():
    "starts a chapter, also serves a restart"
    global mode,allies,enemies,goal,selectx,selecty
    selectx,selecty = 0,0
    allyCoords,newenemies,goal = chapterData[chapter]
    enemies = [e.getInstance() for e in newenemies]
    allies = [a.getInstance() for a in oldAllies]
    for i in range(len(allyCoords)):
        allies[i].x,allies[i].y = allyCoords[i] #sets all ally coords
        exec("global "+allies[i].name.lower()+"\n"+allies[i].name.lower()+"=allies[i]")
    moved.clear()
    attacked.clear()
    mode = "freemove"
    screen.fill(GREEN) #replace this with map sprite later
    drawGrid(screen)
    startTurn()
#----DRAWING FUNCTIONS----#
def drawItemMenu(person,x,y):
    "draws an item menu for a person"
    if x + 8 > 39:
        x -= 9
    if y + 5 > 24:
        y -= 4
    draw.rect(screen,BLUE,(x*30,y*30,240,150))
    for i in range(5):
        if i < len(person.items):
            col = WHITE
            if type(person.items[i]) == Weapon:
                if not person.canEquip(person.items[i]):
                    #if the person cannot equip, the color goes grey
                    col = (160,160,160)
            screen.blit(sans.render(person.items[i].name,True,col),(x*30,(y+i)*30))
            screen.blit(sans.render(str(person.items[i].dur)+"/"+str(person.items[i].maxdur),True,col),((x+6)*30,(y+i)*30)) #blits durability
    draw.rect(screen,WHITE,(x*30,(y+menuselect)*30,240,30),1) #draws selected item
#USER INTERFACE FUNCTION
def moveSelect():
    "moves selector"
    global selectx,selecty
    kp = key.get_pressed()
    if kp[K_UP]:
        selecty -= 1
    if kp[K_DOWN]:
        selecty += 1
    if kp[K_LEFT]:
        selectx -= 1
    if kp[K_RIGHT]:
        selectx += 1
    if mode in ["freemove","move"]:
        selectx = min(39,max(0,selectx))
        selecty = min(23,max(0,selecty))
#----PERSON ACTIONS----#
#ATTACK FUNCTIONS
def checkDead(ally,enemy):
    "checks if an ally or an enemy is dead; also removes ally or enemy from list"
    if ally.hp == 0:
        allies.remove(ally)
        if ally in moved:
            moved.remove(ally)
        return True
    if enemy.hp == 0:
        enemies.remove(enemy)
        if ally in moved:
            moved.remove(enemy)
        return True
    return False
def attack(person,person2):
    "attack animation of person to person2"
    #sets who is the ally and who is the enemy
    if person in allies:
        ally = person
        enemy = person2
    else:
        ally = person2
        enemy = person
    filler = screen.copy()
    screen.fill(BLACK) #blackens screen
    display.flip()
    time.wait(200)
    draw.rect(screen,GREEN,(0,0,1200,600))
    draw.rect(screen,BLUE,(900,220,300,50)) #ally name rectangle
    draw.rect(screen,(255,0,0),(0,220,300,50)) #enemy name rectangle
    #draws ally and enemy's names
    screen.blit(sans.render(stripNums(ally.name),True,WHITE),(920,220))
    screen.blit(sans.render(stripNums(enemy.name),True,WHITE),(50,220))
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for Person 1 and 2
    screen.blit(person.anims["stand"],(0,200))
    screen.blit(person2.anims["stand"],(0,200))
    draw.rect(screen,BLUE,(700,600,500,120)) #draws ally health background
    draw.rect(screen,(255,0,0),(0,600,500,120)) #draws enemy health background
    drawHealthBar(screen,ally,870,615)
    drawHealthBar(screen,enemy,170,615)
    screen.blit(sans.render(str(ally.hp),True,WHITE),(1032,620))
    screen.blit(sans.render(str(enemy.hp),True,WHITE),(332,620))
    display.flip()
    time.wait(200)
    #sets variables for person drawing
    #differs based on which is enemy and which is ally
    if person2 == enemy:
        x,y = 725,300
        hpx,hpy = 870,615
        isenemy = False
        x2,y2 = 25,300
        hpx2,hpy2 = 170,615
    else:
        x,y = 25,300
        hpx,hpy = 170,615
        isenemy = True
        x2,y2 = 725,300
        hpx2,hpy2 = 870,615
    #Draws damage for attack 1
    screen.blit(actionFiller,(0,0)) #covers both persons
    singleAttack(screen,person,person2,x2,y2,hpx2,hpy2,not isenemy,eval("chapter"+str(chapter)))
    if checkDead(ally,enemy):
        return False #ends the function if either ally or enemy is dead
    #Draws damage for attack 2
    if canAttackTarget(person2,person):
        #if person2 can attack
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,person2,person,x,y,hpx,hpy,isenemy,eval("chapter"+str(chapter)))
    if checkDead(ally,enemy):
        return False
    #Draws damage for attack 3
    screen.blit(actionFiller,(0,0)) #covers both persons
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy):
        singleAttack(screen,ally,enemy,25,300,170,615,True,eval("chapter"+str(chapter)))
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally):
        singleAttack(screen,enemy,ally,725,300,870,615,False,eval("chapter"+str(chapter)))
    display.flip()
    time.wait(1000)
    screen.blit(filler,(0,0))
    checkDead(ally,enemy)

#----HELPFUL CLASSES----#
#any classes that help me code
class FilledSurface(Surface):
    "a surface we can make filled on declaration"
    #aids in my drawing efforts as I am too lazy to make a new surface everytime I want a filled one
    def __init__(self,dimensions,background=None,text=None,fontColor=None,fontFamily=None,tpos=None):
        super(FilledSurface,self).__init__(dimensions) #calls super
        if background != None:
            if type(background) in [Color,tuple]:
                self.fill(background) #fills the surface if the background is a color
            else:
                self.blit(background,(0,0))
        if text != None:
            #blits text if it isn't None
            if fontFamily == None:
                fontFamily = timesnr #sets default font
            if fontColor == None:
                fontColor = BLACK #sets default color
            if tpos == None:
                tpos = (0,0) #sets default text position
            self.blit(fontFamily.render(text,True,fontColor),tpos)
            
#----UI CLASSES----#
#these classes are the user interface classes - any classes that help user interaction are here
class Button():
    def __init__(self,x=0,y=0,width=0,height=0,background=Surface((1,1)),hlbackground=Surface((1,1)),func=[]):
        "sets all the class's members"
        self.x = x #co-ordinates
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = background #background of button
        self.hlbackground = hlbackground #background of button when highlighted
        self.func = func #func is a list of strings that contains commands to be executed
    def istouch(self,x=None,y=None):
        "checks if co-ordinates are touching Button"
        #default is mouse co-ordinates
        mx,my = mouse.get_pos()
        if x == None:
            x = mx
        if y == None:
            y = my
        return Rect(self.x,self.y,self.width,self.height).collidepoint(x,y) #returns boolean
    def draw(self,screen):
        "draws button on screen"
        if self.istouch():
            screen.blit(self.hlbackground,(self.x,self.y)) #if it's highlighted we draw the highlighted background
        else:
            screen.blit(self.background,(self.x,self.y))
    def click(self):
        "runs button's func"
        exec("\n".join(self.func))
        
#----MODE CLASSES----#
#these classes are the different modes for the scren - must be in the main
class StartMenu():
    #start menu mode
    def __init__(self):
        "sets button list of mode"
        self.stopped = False
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"NEW GAME",WHITE,font.SysFont("Monospace",30),(30,10)),
                               FilledSurface((200,50),YELLOW,"NEW GAME",BLACK,font.SysFont("Monospace",30),(30,10)),
                               ["changemode(NewGame())"])] #START BUTTON
    def draw(self,screen):
        #draws mode on screen
        screen.blit(logo,(300,50))
    def run(self,screen):
        global running
        #runs the mode as if it were in the running loop
        for e in event.get():
            #event loop
            if e.type == QUIT:
               running = False #quits
            if e.type == MOUSEBUTTONDOWN:
                #checks if user clicked any buttons
                for b in self.buttons:
                    if b.istouch():
                        b.click()
        if self.stopped:
            return 0 #if we have stopped, we return to stop the method
        #draws buttons
        for b in self.buttons:
            b.draw(screen)
class NewGame():
    "this class let's user choose his name and class"
    def __init__(self):
        self.selectingname = True #is the user choosing his name?
        self.selectingclass = False #is the user selecting his class?
        self.typing = False #is the user typing his name?
        self.tbrect = Rect(400,300,500,50)
        self.name = "" #name user chosen
        self.ipos = 0 #insertion point position
        #name select buttons
        self.buttons1 = [Button(900,300,200,50,FilledSurface((200,50),BLUE,"SUBMIT",WHITE,font.SysFont("Monospace",30),(30,10)),
                               FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,font.SysFont("Monospace",30),(30,10)),
                               ["currmode.selectingname = False","currmode.selectingclass = True","screen.fill(BLACK)"])]
        #class select buttons
        self.buttons2 = [Button(300,300,200,50,FilledSurface((200,50),BLUE,"MAGE",WHITE,font.SysFont("Monospace",30),(30,10)),
                                FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,font.SysFont("Monospace",30),(30,10)),
                                ["global player",
                                 "player = Mage(self.name,0,0,{'stren':5,'defen':3,'spd':7,'res':5,'lck':5,'skl':6,'con':5,'move':5},{},[],{})"])]
    def draw(self,screen):
        #draws newgame screen
        screen.fill(BLACK)
        screen.blit(comicsans.render("ENTER NAME: ",True,WHITE),(self.tbrect[0]-250,self.tbrect[1]+10))
        draw.rect(screen,WHITE,self.tbrect)
    def run(self,screen):
        global running
        #runs new game screen
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                if self.selectingname:
                    #if the user is selecting his name
                    if self.tbrect.collidepoint(e.pos):
                        #if we are touching the textbox
                        self.typing = True
                    else:
                        self.typing = False
                if self.selectingname and len(self.name) > 0:
                    for b in self.buttons1:
                        if b.istouch():
                            b.click()
            if e.type == KEYDOWN:
                if self.typing:
                    if key.get_pressed()[K_BACKSPACE]:
                        self.name = self.name[:self.ipos-1] + self.name[self.ipos:]#deletes last character behind ipos in name if user backspaced
                        self.ipos -= 1
                    elif len(self.name) < 16:
                        self.name += e.unicode #Otherwise it adds what they typed to name
                        self.ipos += 1
        if self.selectingname:
            #draws submit button
            for b in self.buttons1:
                b.draw(screen)
            #if we are selecting name, we draw the textbox and what they typed
            draw.rect(screen,WHITE,self.tbrect)
            if self.typing:
                if time2.time() % 1 < 0.5:
                    #draws insertion point at right times to make it look like it's flashing
                    draw.line(screen,BLACK,(self.tbrect[0]+comicsans.render(self.name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]),
                              (self.tbrect[0]+comicsans.render(self.name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]+self.tbrect[3]))
            screen.blit(comicsans.render(self.name,True,BLACK),self.tbrect) #blits text on
class Game():
    def __init__(self):
        "initializes game"
        pass #the game uses global variables, so nothing goes here
    def draw(self,screen):
        "draws game on screen"
        global filler
        start()
        filler = screen.copy() #filler
    def run(self,screen):
        "runs the game"
        global running,mode,selectx,selecty,filler,framecounter,selected,selectedItem,selectedEnemy,attackableEnemies,menu,menuselect,chapter
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if mode == "gameover":
                    start()
                    continue
                kp = key.get_pressed()
                
                if mode in ["freemove","move"]:
                    #freemove moves freely; move picks a location
                    moveSelect() #handles movements by player
                    framecounter = 0
                
                if mode in ["optionmenu","itemattack","item"]:                    
                    #moves menu option
                    if kp[K_UP]:
                        menuselect -= 1
                    elif kp[K_DOWN]:
                        menuselect += 1
                    if mode == "optionmenu":
                        limit = len(menu)
                    elif mode == "item":
                        if selectedItem == None:
                            limit = len(selected.items)
                        elif type(selectedItem) == Weapon:
                            limit = 2
                        elif type(selectedItem) == Consumable:
                            limit = 2
                    else:
                        limit = 5
                    if menuselect < 0:
                        menuselect = limit - 1
                    elif menuselect >= limit:
                        menuselect = 0

                if mode == "attack":
                    #changes enemy selected
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        selectedEnemy += 1
                    if kp[K_LEFT] or kp[K_UP]:
                        selectedEnemy -= 1
                    if selectedEnemy == len(attackableEnemies):
                        selectedEnemy = 0
                    elif selectedEnemy == -1:
                        selectedEnemy = len(attackableEnemies)-1
                    selectx,selecty = attackableEnemies[selectedEnemy].x,attackableEnemies[selectedEnemy].y
                
                if e.unicode.lower() == "z":
                    #if the user pressed z
                    #handles clicks
                    if mode == "freemove":
                        for p in allies+enemies:
                            #checks if ally or enemy is clicked
                            if selectx == p.x and selecty == p.y and p not in moved:
                                mode = "move"
                                selected = p
                                self.oldx,self.oldy = p.x,p.y #keeps track of ally's position before so that we can backtrace
                                acoords = [(a.x,a.y) for a in allies]
                                encoords = [(e.x,e.y) for e in enemies]
                                if selected in allies:
                                    #we get movements below
                                    self.moveableSquares = getMoves(selected,selected.x,selected.y,selected.move,eval("chapter"+str(chapter)),acoords,encoords,{})
                                    self.attackbleSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackbleSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackbleSquares = [sq for sq in self.attackbleSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in acoords]
                                elif selected in enemies:
                                    self.moveableSquares = getMoves(selected,selected.x,selected.y,selected.move,eval("chapter"+str(chapter)),encoords,acoords,{})
                                    self.attackbleSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackbleSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackbleSquares = [sq for sq in self.attackbleSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we consistently fill moveable and attackable squares
                    
                    elif mode == "move":
                        #moves the unit if it is an ally
                        if (selectx,selecty) in [(x,y) for x,y,m in self.moveableSquares]+[(selected.x,selected.y)] and selected in allies:
                            selected.x,selected.y = selectx,selecty
                            mode = "optionmenu"
                            menu = []
                            menuselect = 0
                            #----Menu Creation
                            #ATTACK OPTION
                            if not (selected in attacked or selected.equip == None):
                                for w in [i for i in selected.items if type(i) == Weapon]:
                                    #checks every weapon if one yields in an attack we equip it and add attack
                                    if not selected.canEquip(w):
                                        continue
                                    if len(getAttackableEnemies(selected,enemies,weapon=w)) > 0:
                                        selected.equipWeapon(w)
                                        menu.append("attack")
                                        break
                            #ITEM OPTION
                            if len(selected.items) > 0:
                                menu.append("item")
                            #WAIT OPTION
                            menu.append("wait") #person can always wait

                    elif mode == "optionmenu":
                        #allows user to select options
                        if menu[menuselect] == "attack":
                            mode = "itemattack"
                            menuselect = 0
                        if menu[menuselect] == "item":
                            mode = "item"
                            menuselect = 0
                        if menu[menuselect] == "wait":
                            mode = "freemove"
                            moved.add(selected)
                            attacked.add(selected)

                    elif mode == "itemattack":
                        if menuselect < len(selected.items):
                            if type(selected.items[menuselect]) == Weapon:
                                if selected.canEquip(selected.items[menuselect]) and getAttackableEnemies(selected,enemies,weapon=selected.items[menuselect]):
                                    mode = "attack"
                                    selected.equipWeapon(selected.items[menuselect])
                                    attackableEnemies = getAttackableEnemies(selected,enemies)
                                    selectx,selecty = attackableEnemies[0].x,attackableEnemies[0].y
                                    selectedEnemy = 0

                    elif mode == "attack":
                        #does an attack
                        attack(selected,attackableEnemies[selectedEnemy])
                        attacked.add(selected)
                        moved.add(selected)
                        mode = "freemove"

                    elif mode == "item":
                        #handles item selection
                        if selectedItem == None:
                            menuselect = 0
                            selectedItem = selected.items[menuselect]
                        elif type(selectedItem) == Weapon:
                            pass
                        elif type(selectedItem) == Consumable:
                            pass

    ##                    mode = "freemove"
    ##                    moved.add(selected) #unit gets appended to moved
    ##                    if selected.mounted:
    ##                        #handle this later NOTEITHOIESHFOIAWHFIOAWEHIOFHNAWGHISEHFUIGWAHOIFEK
    ##                        #N O T I C E   M E   Y O U - S E N P A I ! ! !   H A N D L E   M O U N T E D   U N I T S ! ! ! ! ! ! ! ! ! ! !
    ##                        movesMem[selected.name] = getMoves(selected,selected.x,selected.y,selected.move,
    ##                                                           eval("chapter"+str(chapter)),[(a.x,a.y) for a in allies],[(e.x,e.y) for e in enemies],{})
    ##                        if selected not in attacked:
    ##                            self.attackbleSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in movesMem[selected.name]],selected)
    ##                            if self.attackbleSquares:
    ##                                #we memorize all attackables squares that we cannot move to
    ##                                attacksMem[selected.name] = [sq for sq in self.attackbleSquares if sq not in [(x,y) for x,y,m in movesMem[selected.name]] and sq != (selected.x,selected.y)]
                
                if e.unicode.lower() == "x":
                    #if the user pressed x
                    #handles backtracing
                    if mode == "move":
                        mode = "freemove"
                    elif mode == "optionmenu":
                        mode = "move"
                        selected.x,selected.y = self.oldx,self.oldy
                    elif mode == "itemattack":
                        mode = "optionmenu"
                        menuselect = 0
                    elif mode == "item":
                        mode = "optionmenu"
                        menuselect = 0
                    elif mode == "attack":
                        menuselect = 0
                        mode = "itemattack"

                if e.unicode == " ":
                    #restarts turn
                    #only temporary
                    startTurn()
        if mode == "gameover":
            return 0
        screen.blit(filler,(0,0)) #blits the filler
        if yoyo.hp == 0 and mode != "gameover":
            gameOver()
            mode = "gameover"
            return 0
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if kp[K_LEFT] or kp[K_RIGHT] or kp[K_UP] or kp[K_DOWN] and mode in ["freemove","move"]:
            #increases frame counter if we're holding something
            framecounter += 1
        if framecounter > 100 and mode in ["freemove","move"]:
            #if framecounter is greater than 60 we move more
            moveSelect()
            time.wait(50)
        #DRAWS PERSONS
        for p in allies+enemies:
            drawPerson(screen,p) #draws persons
        #--------------------HIGHLIGHTING A PERSON---------------#
        if mode == "freemove":
            for p in allies+enemies:
                if selectx == p.x and selecty == p.y:
                    #DRAWS PERSON MINI DATA BOX
                    pdbx,pdby = 0,0 #person data box x and y
                    if selectx < 20 and selecty <= 12:
                        pdby = 630
                    draw.rect(screen,BLUE,(pdbx,pdby,300,90)) #background box
                    screen.blit(sans.render(stripNums(p.name),True,WHITE),(pdbx+15,pdby+3)) #person's name
                    screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,WHITE),(pdbx+15,pdby+33)) #health
                    draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                    draw.line(screen,YELLOW,(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                    break
        #---------------DIFFERENT MODE DISPLAYS------------------#
        #MOVE MODE DISPLAY
        if mode == "move":
            #fills moveable and attackable squares
            fillSquares(screen,set([(x,y) for x,y,m in self.moveableSquares]),transBlue)
            if self.attackbleSquares:
                fillSquares(screen,self.attackbleSquares,transRed)
        #OPTION MENU MODE DISPLAY
        if mode == "optionmenu":
            #if it is menu mode we draw the menu
            menux,menuy = 36,2
            if selected.x >= 20:
                menux = 0
            draw.rect(screen,BLUE,(menux*30,menuy*30,120,len(menu)*30))
            for i in range(len(menu)):
                #for every option in menu, we write the text
                opt = menu[i].title()
                screen.blit(sans.render(opt,True,WHITE),(menux*30,(menuy+i)*30))
            draw.rect(screen,WHITE,(menux*30,(menuy+menuselect)*30,120,30),1) #draws selected option
        #ATTACK MODE DISPLAY
        if mode == "itemattack":
            #displays item selection menu for attack
            drawItemMenu(selected,selected.x+1,selected.y)
        if mode == "attack":
            fillSquares(screen,getAttackableSquares(selected.equip.rnge,selected.equip.maxrnge,selected.x,selected.y),transRed) #highlights all attackable squares
        #ITEM MODE DISPLAY
        if mode == "item":
            screen.blit(transBlack,(0,0))
            drawItemMenu(selected,14,8)
            if type(selectedItem) == Weapon:
                if selected.canEquip(selectedItem):
                    pass
        #---------------INFO DISPLAY BOXES----------------------#
        #TERRAIN DATA
        if mode == "freemove":
            tbx,tby = 1020,630 #terrain box x and y
            stage = eval("chapter"+str(chapter))
            if selectx >= 20:
                tbx = 0
            draw.rect(screen,BLUE,(tbx,tby,180,90))
            screen.blit(sans.render(stage[selecty][selectx].name,True,WHITE),(tbx+15,tby+3))
            draw.rect(screen,(255,230,200),(tbx,tby+30,180,60))
            screen.blit(sans.render("DEFENSE: "+str(stage[selecty][selectx].adef),True,BLACK),(tbx+15,tby+33))
            screen.blit(sans.render("AVOID: "+str(stage[selecty][selectx].avo),True,BLACK),(tbx+15,tby+63))
        #GOAL BOX
        if mode == "freemove":
            goalx,goaly = 1020,0
            if selecty <= 12 and selectx >= 20:
                goaly = 630
            draw.rect(screen,(50,50,180),(goalx,goaly,180,90))
            screen.blit(smallsans.render(goal,True,WHITE),(goalx+15,goaly+35))
        #---------------SELECTED SQUARE BOX----------------#
        if mode in ["freemove","move","attack"]:
            draw.rect(screen,WHITE,(selectx*30,selecty*30,30,30),1) #draws select box
        display.flip()
#----CHANGE MODE FUNCTION----#
def changemode(mode):
    "changes the screen's mode"
    global currmode
    currmode.stopped = True
    blackTransSurface = Surface((1200,736),SRCALPHA)
    blackTransSurface.fill((0,0,0,50))
    #blits translucent surface many times to make it black
    for i in range(50):
        screen.blit(blackTransSurface,(0,0))
        display.flip()
        time.wait(10) #delays it to make it look like it's fading
    currmode = mode
    mode.draw(screen)
#----FINALIZES SCREEN----#
running = True
currmode = Game() #sets current mode
currmode.draw(screen)
while running:
    currmode.run(screen) #runs current mode
    display.flip() #updates screen
quit()
