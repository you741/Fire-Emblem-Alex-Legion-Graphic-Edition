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
#---Initialization
init()
mixer.init()
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
GREY = (160,160,160,255)
#----FONTS----#
timesnr = font.SysFont("Times New Roman",15)
comicsans = font.SysFont("Comic Sans MS",25)
arial = font.SysFont("Arial",15)
monospace = font.SysFont("Monospace",30)
smallsans = font.SysFont("Comic Sans MS",15)
sans = font.SysFont("Comic Sans MS",20)
papyrus = font.SysFont("Papyrus",20)
#----MUSIC----#
bgMusic = mixer.Channel(0) #channel for background music
sndEffs = mixer.Channel(1) #channel for sound effects
#conquest = mixer.Sound("music/3-01-conquest.ogg")
#----IMAGE LOAD----#
logo = image.load("images/logo.png")
#TERRAIN
plain = Terrain("Plain",0,0,1)
#WEAPONS
real_knife = Weapon("Real Knife",99,1,1000,999,"Sword",600)
iron_bow = Weapon("Iron Bow",6,6,46,80,"Bow",100,0,2,46,False,[],2)
iron_lance = Weapon("Iron Lance",7,8,45,80,"Lance",100)
silver_lance = Weapon("Silver Lance",14,10,20,75,"Lance",100)
fire = Weapon("Fire",5,4,40,95,"Anima",100,0,1,40,True,maxrnge=2,anims=fireSprite)
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
name = "" #name of player
usedNames = ["yoyo"] #names the player cannot use
player = None #player is defined in NewGame or LoadGame
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
               [rapier.getInstance(),iron_bow.getInstance(),vulnerary.getInstance()],{"Sword":200},
               {"Sword":(yoyoAttackSprite,5),"Swordcrit":(yoyoCritSprite,29),"stand":yoyoStandSprite}) #test person
allies = [] #allies
#ENEMIES
bandit0 = Brigand("Bandit",0,0,
                  {"lv":1,"stren":5,"defen":4,"skl":3,"lck":0,
                   "spd":3,"con":8,"move":5,"res":0,"hp":20,"maxhp":20},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":(brigandAttackSprite,9),"Axecrit":(brigandCritSprite,11),"stand":brigandStandSprite},10)
enemies = []
#----CHAPTERS----#
#MAPS
chapter0 = [[plain for i in range(40)] for j in range(24)]
#CHAPTER DATA
#Stored in tuples
#(gainedAllies,allyCoordinates,Enemies,Goal,BackgroundImage)
#chapter data, chapter is determined by index
chapterData = [([yoyo],[(0,1),(0,0)],createEnemyList([bandit0],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies",image.load("images/Maps/prologue.png"))]
oldAllies = [] #keeps track of allies before the fight
allAllies = [] #all allies that exist
#CHAPTER MUSIC
#each index represents what music is played in the chapter of that index
#chapterMusic = [conquest]
#----GLOBAL VARIABLES----#
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
framecounter = 0 #counts frames
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
    screen.blit(papyrus.render("GAME OVER",True,RED),(500,300))
    display.flip()
def start():
    "starts a chapter, also serves a restart"
    global mode,allies,enemies,goal,selectx,selecty
    selectx,selecty = 0,0
    newAllies,allyCoords,newenemies,goal,backgroundImage = chapterData[chapter]
    for a in newAllies:
        if a not in oldAllies:
            oldAllies.append(a.getInstance()) #adds all new allies to the oldAllies - this should be moved to preFight class... but it doesn't exist yet
            allAllies.append(a.getInstance())
    enemies = [e.getInstance() for e in newenemies]
    allies = [a.getInstance() for a in oldAllies]
    for i in range(len(allyCoords)):
        global player
        allies[i].x,allies[i].y = allyCoords[i] #sets all ally coords
        if allies[i].name.lower() not in usedNames:
            #player gets it's own variable, so it is special
            player = allies[i]
        else:
            #sets name representing ally to be the new instance
            exec("global "+allies[i].name.lower()+"\n"+allies[i].name.lower()+"=allies[i]")
    moved.clear()
    attacked.clear()
    mode = "freemove"
    screen.blit(backgroundImage,(0,0))#draws map background on the screen
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
                    col = GREY
            screen.blit(sans.render(person.items[i].name,True,col),(x*30,(y+i)*30))
            screen.blit(sans.render(str(person.items[i].dur)+"/"+str(person.items[i].maxdur),True,col),((x+6)*30,(y+i)*30)) #blits durability
    draw.rect(screen,WHITE,(x*30,(y+menuselect)*30,240,30),1) #draws selected item
#----USER INTERFACE FUNCTION----#
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
        if enemy in moved:
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
    screen.fill(GREEN) #green screen
    display.flip()
    time.wait(200)
    draw.rect(screen,BLUE,(900,220,300,50)) #ally name rectangle
    draw.rect(screen,RED,(0,220,300,50)) #enemy name rectangle
    #draws ally and enemy's names
    screen.blit(sans.render(stripNums(ally.name),True,WHITE),(920,220))
    screen.blit(sans.render(stripNums(enemy.name),True,WHITE),(50,220))
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for Person 1 and 2
    screen.blit(person.anims["stand"],(0,200))
    screen.blit(person2.anims["stand"],(0,200))
    draw.rect(screen,BLUE,(700,600,500,120)) #draws ally health background
    draw.rect(screen,RED,(0,600,500,120)) #draws enemy health background
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
        #gains exp
        if enemy.hp == 0:
            expgain = getExpGain(ally,enemy,True) #gains exp on a kill
            drawExpGain(ally,expgain,screen)
            needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
            if needLevelUp:
                #level up
                ally.levelUp()
        display.flip()
        time.wait(1000)
        return False #ends the function if either ally or enemy is dead
    #Draws damage for attack 2
    person2hit = False #did person2 hit? (person 1 hits no matter what, so I don't need that)
    if canAttackTarget(person2,person):
        #if person2 can attack
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,person2,person,x,y,hpx,hpy,isenemy,eval("chapter"+str(chapter)))
        person2hit = True
    if checkDead(ally,enemy):#gains exp
        if enemy.hp == 0:
            expgain = getExpGain(ally,enemy,True) #gains exp on a kill
            drawExpGain(ally,expgain,screen)
            needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
            if needLevelUp:
                #level up
                ally.levelUp()
        display.flip()
        time.wait(1000)
        return False
    #Draws damage for attack 3
    screen.blit(actionFiller,(0,0)) #covers both persons
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy):
        singleAttack(screen,ally,enemy,25,300,170,615,True,eval("chapter"+str(chapter)))
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally):
        singleAttack(screen,enemy,ally,725,300,870,615,False,eval("chapter"+str(chapter)))
    kill = False
    if checkDead(ally,enemy):
        kill = True
    expgain = getExpGain(ally,enemy,kill) #experience points to gain
    expgain = min(100,expgain) #experience gain cannot exceed 100
    if ally == person2 and not person2hit:
        #if person2 did not hit and that was the ally, we only gain 1 exp
        expgain = 1
    drawExpGain(ally,expgain,screen)
    needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
    if needLevelUp:
        #level up
        ally.levelUp()
        drawLevelUp(screen,ally)
    time.wait(1000)
#----HELPFUL CLASSES----#
#any classes that help me code
class FilledSurface(Surface):
    "a surface we can make filled on declaration"
    #aids in my drawing efforts as I am too lazy to make a new surface everytime I want a filled one
    def __init__(self,dimensions,background=None,text="",fontColor=BLACK,fontFamily=timesnr,tpos=(0,0)):
        super(FilledSurface,self).__init__(dimensions) #calls super
        if background != None:
            if type(background) in [Color,tuple]:
                self.fill(background) #fills the surface if the background is a color
            else:
                self.blit(background,(0,0))
        self.blit(fontFamily.render(text,True,fontColor),tpos) #blits text
            
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
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"START",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"START",BLACK,monospace,(30,10)),
                               ["changemode(SelectSave())"])] #START BUTTON
    def draw(self,screen):
        "draws mode on screen"
        screen.blit(logo,(300,50))
    def playMusic(self):
        "plays menu music"
        #WIP
        pass
    def run(self,screen):
        "runs the mode as if it were in the running loop"
        global running
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
class SelectSave():
    def __init__(self):
        self.stopped = False
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"New Game",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"New Game",BLACK,monospace,(30,10)),
                               ["changemode(NewGame())"]),
                        Button(500,480,200,50,FilledSurface((200,50),BLUE,"New Game",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"New Game",BLACK,monospace,(30,10)),
                               ["changemode(NewGame())"]),
                        Button(500,540,200,50,FilledSurface((200,50),BLUE,"New Game",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"New Game",BLACK,monospace,(30,10)),
                               ["changemode(NewGame())"])]
    def draw(self,screen):
        "draws mode on screen"
        draw.rect(screen,WHITE,(100,100,100,100))
    def playMusic(self):
        "plays menu music"
        #WIP
        pass
    def run(self,screen):
        "runs the menus as if it were in the running loop"
        global running
        for e in event.get():
            #event loop
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
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
        self.ipos = 0 #insertion point position
        #name select buttons
        self.buttons1 = [Button(900,300,200,50,FilledSurface((200,50),BLUE,"SUBMIT",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,monospace,(30,10)),
                               ["currmode.selectingname = False","currmode.selectingclass = True","screen.fill(BLACK)"])]
        #class select buttons
        self.buttons2 = [Button(300,300,200,50,FilledSurface((200,50),BLUE,"MAGE",WHITE,monospace,(40,10)),
                                FilledSurface((200,50),YELLOW,"MAGE",BLACK,monospace,(40,10)),
                                ["global player,oldAllies",
                                 """player = Mage(name,0,0,{'lv':1,'hp':17,'maxhp':17,'stren':5,'defen':1,'spd':7,'res':5,'lck':5,'skl':6,'con':5,'move':5},
{'maxhp':55,'defen':10,'res':50,'stren':35,'spd':50,'skl':50,'lck':55},
[fire.getInstance()],
{'Anima':200},
{'stand':playerMageStandSprite,'Anima':(playerMageAttackSprite,10),'Animacrit':(playerMageCritSprite,21)})
allies.append(player)
oldAllies = [a.getInstance() for a in allies] #keeps track of allies before the fight
allAllies.append(player) #normally the saving would be done withing the PreFight class... but it doesn't exist yet
""",
                                "changemode(Game())"])]
    def draw(self,screen):
        "draws newgame screen"
        screen.fill(BLACK)
        screen.blit(comicsans.render("ENTER NAME: ",True,WHITE),(self.tbrect[0]-250,self.tbrect[1]+10))
        draw.rect(screen,WHITE,self.tbrect)
    def playMusic(self):
        "does not have music - same as menu"
        pass
    def run(self,screen):
        "runs new game screen within the running loop"
        global running,name
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                if self.selectingname:
                    #if the user is selecting his name, we check if user presses text box
                    if self.tbrect.collidepoint(e.pos):
                        #clicking the textbox allows user to type
                        self.typing = True
                    else:
                        #clicking away from the textbox disallows typing
                        self.typing = False
                    if len(name) > 0 and name.lower() not in usedNames:
                        #handles button presses
                        for b in self.buttons1:
                            if b.istouch():
                                b.click()
                if self.selectingclass:
                    #if the user is selecting his class, we check for button presses
                    for b in self.buttons2:
                        if b.istouch():
                            b.click()
            if e.type == KEYDOWN:
                #handles key presses
                if self.typing:
                    #if we are typing we handle the textbox editing
                    #backspace deletes a characer, enter submits, and any valid character is added to name
                    #arrow keys move insertion point
                    kp = key.get_pressed()
                    if kp[K_BACKSPACE] and 0 < self.ipos:
                        name = name[:self.ipos-1] + name[self.ipos:]#deletes last character behind ipos in name if user backspaced
                        self.ipos -= 1
                    elif kp[K_RETURN] and len(name) > 0 and name.lower() not in usedNames:
                        #if user presses return and there exists a valid name
                        self.buttons1[0].click() #triggers the submit button click
                    elif kp[K_LEFT]:
                        #moves insertion point to the left
                        self.ipos -= 1
                        self.ipos = min(len(name),max(0,self.ipos)) #limits insertion point
                    elif kp[K_RIGHT]:
                        #moves insertion point to the right
                        self.ipos += 1
                        self.ipos = min(len(name),max(0,self.ipos)) #limits insertion point
                    elif len(name) < 16 and e.unicode.lower() in "abcdefghijklmnopqrstuvwxyz0123456789 " and e.unicode != "":
                        #if user enters a valid character (letter or number) we append it to name
                        name = name[:self.ipos] + e.unicode + name[self.ipos:]
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
                    draw.line(screen,BLACK,(self.tbrect[0]+comicsans.render(name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]),
                              (self.tbrect[0]+comicsans.render(name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]+self.tbrect[3]))
            screen.blit(comicsans.render(name,True,BLACK),self.tbrect) #blits text on
        elif self.selectingclass:
            #draws class select buttons
            for b in self.buttons2:
                b.draw(screen)
            
class Game():
    def __init__(self):
        "initializes game"
        self.clickedFrame = framecounter #the frame user clicked (pressed z)
    def draw(self,screen):
        "draws game on screen"
        global filler
        start()
        filler = screen.copy() #filler
    def playMusic(self):
        "plays music for the chapter"
 #       bgMusic.play(chapterMusic[chapter],-1)
    def run(self,screen):
        "runs the game in the running loop"
        global running,mode,selectx,selecty,filler,framecounter,selected,selectedItem,selectedEnemy,attackableEnemies,menu,menuselect,chapter
        #----EVENT LOOP----#
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if mode == "gameover":
                    start()
                    continue
                kp = key.get_pressed()
                #MOVEMENT OF SELECTION CURSOR OR MENU OPTOIN
                if mode in ["freemove","move"]:
                    #freemove moves freely; move picks a location
                    moveSelect() #handles movements by player
                    self.clickedFrame = framecounter #sets the clickedFrame to self
                if mode in ["optionmenu","itemattack"] or (mode == "item" and selectedItem == None):                    
                    #moves selected menu item
                    if kp[K_UP]:
                        menuselect -= 1
                    elif kp[K_DOWN]:
                        menuselect += 1
                    if mode == "optionmenu":
                        limit = len(menu)
                    elif mode == "item":
                        limit = len(selected.items)
                    else:
                        limit = 5
                    if menuselect < 0:
                        menuselect = limit - 1
                    elif menuselect >= limit:
                        menuselect = 0
                elif mode == "item" and selectedItem != None:
                    #if the user is in the submenu for an item, we deal with that
                    #an item submenu has 2 options in it
                    if kp[K_UP]:
                        self.optselected -= 1
                    elif kp[K_DOWN]:
                        self.optselected += 1
                    if self.optselected >= 2:
                        self.optselected = 0
                    elif self.optselected < 0:
                        self.optselected = 1
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
                #---------Z--------#
                if e.unicode.lower() == "z":
                    #if the user pressed z
                    #handles clicks
                    #FREE MOVE MODE
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
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in acoords]
                                elif selected in enemies:
                                    self.moveableSquares = getMoves(selected,selected.x,selected.y,selected.move,eval("chapter"+str(chapter)),encoords,acoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we consistently fill moveable and attackable squares
                    #MOVE MODE
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
                    #OPTION MENU CLICK
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
                    #ATTACK CLICKS
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
                    #ITEM MODE CLICK
                    elif mode == "item":
                        #handles item selection
                        if selectedItem == None:
                            #selects an item and creates a submenu
                            self.optselected = 0 #option selected for the submenu
                            selectedItem = selected.items[menuselect]
                        elif type(selectedItem) == Weapon:
                            #if a weapon is selected, we check whether user equips or discards
                            #0 is equip, 1 is discard
                            if self.optselected:
                                #discard option
                                selected.items.remove(selectedItem) #removes selectedItem from items
                                if selectedItem == selected.equip:
                                    selected.equip = None #no more equipped weapon
                                    #if the removed item was the equipped, item, we try to equip a new weapon
                                    for w in [i for i in selected.items if type(i) == Weapon]:
                                        if selected.equipWeapon(w):
                                            break #if we can equip, loop breaks
                            else:
                                #equip option
                                selected.equipWeapon(selectedItem) #tries to equip
                            selectedItem = None #resets selectedItem
                            if selected.equip == None:
                                #if we have no equipped item we remove the attack option from menu
                                if "attack" in menu:
                                    menu.remove("attack")
                                #we also empty attackableSquares
                                self.attackableSquares = []
                        elif type(selectedItem) == Consumable:
                            #if a consumable is a selected, we check whehther uses or discards
                            #0 is use, 1 is discard
                            if self.optselected:
                                #discard option
                                selected.items.remove(selectedItem)#discards item
                            else:
                                #use option
                                if not selectedItem.use(selected):
                                    #uses consumable
                                    #if it breaks we remove it
                                    selected.items.remove(selectedItem)
                                moved.add(selected) #unit must wait after using a consumable
                                attacked.add(selected)
                                self.oldx,self.oldy = selected.x,selected.y #no moving back after using a consumable
                                self.moveableSquares,self.attackableSquares = [],[] #empties moveablesquares
                                mode = "optionmenu"
                                menuselect = 0
                            selectedItem = None #resets selectedItem
                        if len(selected.items) == 0:
                            #if we have no items left, we go back to option menu and remove items from the list
                            menu.remove("item")
                            mode = "optionmenu"
                            menuselect = 0
                #------X------#
                if e.unicode.lower() == "x":
                    #if the user pressed x
                    #handles backtracing
                    if mode == "move":
                        mode = "freemove"
                    elif mode == "optionmenu":
                        mode = "move"
                        selected.x,selected.y = self.oldx,self.oldy
                        if self.moveableSquares == []:
                            mode = "freemove" #we go back to freemove mode if we have no moveablesquares
                    elif mode == "itemattack":
                        mode = "optionmenu"
                        menuselect = 0
                    elif mode == "item":
                        if selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
                            mode = "item"
                            selectedItem = None
                        else:
                            mode = "optionmenu"
                            menuselect = 0
                    elif mode == "attack":
                        menuselect = 0
                        mode = "itemattack"

                if e.unicode == " ":
                    #restarts turn
                    #only temporary
                    startTurn()
        #-----END OF EVENT LOOP----#
        if mode == "gameover":
            return 0
        screen.blit(filler,(0,0)) #blits the filler
        if yoyo.hp == 0 and mode != "gameover":
            gameOver()
            mode = "gameover"
            return 0
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if framecounter - self.clickedFrame > 60 and mode in ["freemove","move"] and framecounter%15 == 0:
            #if framecounter is greater than 60 we move more
            #we only do it once every 15 frames or it'll be too fast
            moveSelect()
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
            fillSquares(screen,set([(x,y) for x,y,m in self.moveableSquares]+[(selected.x,selected.y)]),transBlue)
            if self.attackableSquares:
                fillSquares(screen,self.attackableSquares,transRed)
        #DRAWS PERSONS
        for a in allies:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            screen.blit(allyMapSprites[a.__class__.__name__][framecounter%240//60],(a.x*30,a.y*30))
        for e in enemies:
            screen.blit(enemyMapSprites[e.__class__.__name__][framecounter%240//60],(e.x*30,e.y*30))
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
            if selectedItem != None:
                #if we have a selected Item we draw the submenu
                if type(selectedItem) == Weapon:
                    if selected.canEquip(selectedItem):
                        col = GREEN #color to write "Equip" with
                        #green means can, grey means can't
                    else:
                        col = GREY
                    #options user can choose for the selected item
                    options = ["Equip","Discard"] #weapons can be equipped or discarded
                if type(selectedItem) == Consumable:
                    col = GREEN
                    options = ["Use","Discard"] #consumables can be used or discarded
                draw.rect(screen,BLUE,(22*30,8*30,120,len(options)*30)) #draws submenu backdrop for item
                screen.blit(sans.render(options[0],True,col),(22*30,8*30)) #draws first option
                screen.blit(sans.render(options[1],True,WHITE),(22*30,9*30)) #draws discard option
                draw.rect(screen,WHITE,(22*30,(8+self.optselected)*30,120,30),1) #selected option
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
        framecounter += 1 #increases frame counter
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
    mode.playMusic()
#----FINALIZES SCREEN----#
running = True
currmode = StartMenu() #sets current mode
currmode.draw(screen)
currmode.playMusic()
while running:
    currmode.run(screen) #runs current mode
    display.flip() #updates screen
quit()
