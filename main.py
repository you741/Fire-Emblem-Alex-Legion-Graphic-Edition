#Fire Emblem Alex Legion
#This game is a Fire Emblem Spin-off featuring my own unique characters named after my classmates
#The user controls an army that fights off the enemy's army for multiple levels to win
#There is also a great story line

#----BUILT-IN MODULE IMPORTS
import os
from pygame import *
import time as time2
from math import *
from random import *
import shelve
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
#----GLOBAL VARIABLES----#
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
#------------------------------------------------------TESTING STUFF------------------------------------------------------#
##file1 = shelve.open("saves/file1")
##if not file1.get('display'):
##    file1['display'] = "NEW gAME"
file1 = shelve.open("saves/file1")
file2 = shelve.open("saves/file2")
file3 = shelve.open("saves/file3")

##file1['allAllies'] = []
##file2['allAllies'] = []
##file3['allAllies'] = None
##file1.close()
##file2.close()
##file3.close()
#------------------------------------------------------TESTING STUFF------------------------------------------------------#

#TRANSLUCENT SQUARES
transBlue = Surface((30,30), SRCALPHA)
transBlue.fill((0,0,255,122))
transRed = Surface((30,30), SRCALPHA)
transRed.fill((255,0,0,122))
transBlack = Surface((1200,720), SRCALPHA)
transBlack.fill((0,0,0,122))
#----PERSONS----#
#ALLIES
name = "" #name of player
usedNames = ["yoyo"] #names the player cannot use
player = None #player is defined in NewGame or LoadGame
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
               [rapier.getInstance(),vulnerary.getInstance()],{"Sword":200},
               {"Sword":(yoyoAttackSprite,5),"Swordcrit":(yoyoCritSprite,29),"stand":yoyoStandSprite})
albert = Mage("Albert",0,0,
              {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
              [fire.getInstance(),vulnerary.getInstance()],{'Anima':200},
              {'stand':playerMageStandSprite,'Anima':(playerMageAttackSprite,10),'Animacrit':(playerMageCritSprite,21)})#test person for chapter 1
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
chapter1 = [[plain for i in range(40)] for j in range(24)]
#CHAPTER DATA
#Stored in tuples
#(gainedAllies,allyCoordinates,Enemies,Goal,BackgroundImage)
#chapter data, chapter is determined by index
chapterData = [([yoyo],[(0,1),(0,0)],createEnemyList([bandit0],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies",image.load("images/Maps/prologue.png")),
               ([albert],[(0,1),(0,0),(1,1)],createEnemyList([bandit0],[3],[(3,3),(3,1),(4,2)]),"IS THIS LOADED PROPERLY",image.load("images/Maps/prologue.png"))]
oldAllies = [] #keeps track of allies before the fight
allAllies = [] #all allies that exist
#CHAPTER MUSIC
#each index represents what music is played in the chapter of that index
#chapterMusic = [conquest]

#important variables for the Game class
chapter = 0 #changes when load new/old game, so stays global

#----GLOBAL FUNCTIONS----#
def addAlly(ally):
    "adds an ally to the allies list - updates allAllies and oldAllies too"
    global oldAllies
    allies.append(ally) #adds ally to allies
    oldAllies.append(ally.getInstance())
    allAllies.append(ally) #adds ally to allAllies
def load(file):
    "loads the file into the game, and returning 0 if it is empty"
    global chapter
    if file.get("chapter") == None:
        changemode(NewGame())#goes to new game
    else:
        #sets the chapter we are about to start and allAllies
        chapter = file["chapter"]
        allAllies = file["allAllies"]
        changemode(Game())
    file.close()
def save(file):
    "saves game into file"
    global chapter, allAllies
    print("i entered")
    file["chapter"] = chapter + 1
    chapter += 1
    ##this will need more work here when we need to modify ally list based on chapter
    file["allAllies"] = allAllies
    file.close()
    changemode(Game())
#----DRAWING FUNCTIONS----#
def drawMenu(menu,x,y,width,height,menuselect,col=BLUE):
    "draws a list of strings as a vertical menu at positions x and y"
    draw.rect(screen,col,(x*30,y*30,width,height))
    for i in range(len(menu)):
        opt = menu[i].title() #option to draw
        screen.blit(sans.render(opt,True,WHITE),(x*30,(y+i)*30))
    draw.rect(screen,WHITE,(x*30,(y+menuselect)*30,width,30),1) #draws a border around the selected option
def drawItemMenu(person,x,y,menuselect):
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
#----PERSON ACTIONS----#
#ATTACK FUNCTIONS
def checkDead(ally,enemy):
    "checks if an ally or an enemy is dead; also removes ally or enemy from list"
    if ally.hp == 0:
        allies.remove(ally)
        return True
    if enemy.hp == 0:
        enemies.remove(enemy)
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
    drawBattleInfo(screen,ally,enemy)
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for ally and enemy
    screen.blit(ally.anims["stand"],(0,200))
    screen.blit(enemy.anims["stand"],(0,200))
    display.flip()
    time.wait(200)
    isenemy = person in enemies #is person an enemy? (boolean)
    #Draws damage for attack 1
    screen.blit(actionFiller,(0,0)) #covers both persons
    singleAttack(screen,person,person2,isenemy,eval("chapter"+str(chapter)))
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
        singleAttack(screen,person2,person,not isenemy,eval("chapter"+str(chapter)))
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
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy):
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,ally,enemy,False,eval("chapter"+str(chapter)))
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally):
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,enemy,ally,True,eval("chapter"+str(chapter)))
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
                               ["changemode(LoadGame())"])] #START BUTTON

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
class SaveGame():
    def __init__(self):
        self.stopped = False
        #Loads files
        self.file1 = shelve.open("saves/file1")
        self.file2 = shelve.open("saves/file2")
        self.file3 = shelve.open("saves/file3")
        #sets the button text based on which files have data
        button1Text = "--NO DATA--" if self.file1.get("chapter") == None else "Chapter: "+str(self.file1.get("chapter"))
        button2Text = "--NO DATA--" if self.file2.get("chapter") == None else "Chapter: "+str(self.file2.get("chapter"))
        button3Text = "--NO DATA--" if self.file3.get("chapter") == None else "Chapter: "+str(self.file3.get("chapter"))
        #creates buttons
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,button1Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button1Text,BLACK,monospace,(0,10)),
                                       ["save(currmode.file1)"]),
                                Button(500,480,200,50,FilledSurface((200,50),BLUE,button2Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button2Text,BLACK,monospace,(0,10)),
                                       ["save(currmode.file2)"]),
                                Button(500,540,200,50,FilledSurface((200,50),BLUE,button3Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button3Text,BLACK,monospace,(0,10)),
                                       ["save(currmode.file3)"])]
    def draw(self,screen):
        "draws mode on screen"
        pass
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
            
class LoadGame():
    def __init__(self):
        self.stopped = False
        #Loads files
        #sets the button text based on which files have data
        self.file1 = shelve.open("saves/file1")
        self.file2 = shelve.open("saves/file2")
        self.file3 = shelve.open("saves/file3")
        button1Text = "--NO DATA--" if self.file1.get("chapter") == None else "Chapter: "+str(self.file1.get("chapter"))
        button2Text = "--NO DATA--" if self.file2.get("chapter") == None else "Chapter: "+str(self.file2.get("chapter"))
        button3Text = "--NO DATA--" if self.file3.get("chapter") == None else "Chapter: "+str(self.file3.get("chapter"))

        #creates buttons
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,button1Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button1Text,BLACK,monospace,(0,10)),
                               ["load(currmode.file1)"]),
                        Button(500,480,200,50,FilledSurface((200,50),BLUE,button2Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button2Text,BLACK,monospace,(0,10)),
                               ["load(currmode.file2)"]),
                        Button(500,540,200,50,FilledSurface((200,50),BLUE,button3Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button3Text,BLACK,monospace,(0,10)),
                               ["load(currmode.file3)"])]
    def draw(self,screen):
        "draws mode on screen"
        screen.fill(WHITE)
        pass
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
                                ["global player",
                                 """player = Mage(name,0,0,{'lv':1,'hp':17,'maxhp':17,'stren':5,'defen':1,'spd':7,'res':5,'lck':5,'skl':6,'con':5,'move':5},
{'maxhp':55,'defen':10,'res':50,'stren':35,'spd':50,'skl':50,'lck':55},
[fire.getInstance()],
{'Anima':200},
{'stand':playerMageStandSprite,'Anima':(playerMageAttackSprite,10),'Animacrit':(playerMageCritSprite,21)})
addAlly(player)
""",
                                "changemode(Game())"]),
                         Button(300,500,200,50,FilledSurface((200,50),BLUE,"LORD",WHITE,monospace,(40,10)),
                                FilledSurface((200,50),YELLOW,"LORD",BLACK,monospace,(40,10)),
                                ["global player",
                                 """player = Lord(name,0,0,{"lv":1,"hp":18,"maxhp":18,"stren":5,"defen":3,"spd":5,"res":4,"skl":7,"lck":7,"con":5,"move":5},
{"stren":40,"defen":20,"skl":70,"lck":70,"spd":40,"res":40,"maxhp":60},
[iron_sword.getInstance(),vulnerary.getInstance()],
{"Sword":200},
{"Sword":(yoyoAttackSprite,5),"Swordcrit":(yoyoCritSprite,29),"stand":yoyoStandSprite})
addAlly(player)
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
    #----this is all for text box----#
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
        self.selectx,self.selecty = 0,0 #select cursor starting point
        self.framecounter = 0
        self.clickedFrame = 0 #the frame user clicked (pressed z)
        self.fpsTracker = time.Clock() #fpsTracker
        self.mode = "freemove" #mode Game is in
        self.menuselect = 0 #option in menu selected
        self.menu = [] #menu for optionmenu mode
        self.selectedEnemy,self.selectedItem = 0,None #selected Enemy and selected Item
        self.selected = None #selected ally
        self.selected2 = None #2nd selected ally - only for trading option
        self.selectedAlly = 0 #2nd selected ally that user is hovering over - only for trading option and healing option
        self.targetableAllies = [] #targetable allies
        self.filler = screen.copy()
        self.moved,self.attacked = set(),set() #sets moved and attacked to be sets
        self.turn = 1 #turn that it is
        self.goal = ""
    def draw(self,screen):
        "draws game on screen - also starts game"
        self.start()
        self.filler = screen.copy() #filler
    def playMusic(self):
        "plays music for the chapter"
        #bgMusic.play(chapterMusic[chapter],-1)
        pass
    def gameVictory(self):
        "Victory, to continue the storyline"
        ##whatever animation/dialogue that needs to happen
        draw.circle(screen,WHITE,(100,100),100)
        changemode(SaveGame())
    def start(self):
        "starts a chapter, also serves a restart"
        global allies,enemies
        self.selectx,self.selecty = 0,0
        newAllies,allyCoords,newenemies,self.goal,backgroundImage = chapterData[chapter]
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
        self.moved.clear()
        self.attacked.clear()
        screen.blit(backgroundImage,(0,0))#draws map background on the screen
        drawGrid(screen)
        self.startTurn()
    def startTurn(self):
        "starts the turn"
        global allies,enemies
        screenBuff = screen.copy() #sets the screenBuffer to cover up the text
        screen.blit(transform.scale(transBlue,(1200,60)),(0,330)) #blits the text "PLAYER PHASE" on a translucent blue strip
        screen.blit(papyrus.render("PLAYER PHASE",True,WHITE),(450,340))
        self.moved.clear() #empties moved and attacked
        self.attacked.clear()
        display.flip() #updates screen
        time.wait(1000)
        screen.blit(screenBuff,(0,0)) #covers up text
        display.flip()
        self.mode = "freemove" #sets the mode back to freemove
    def endTurn(self):
        "ends the turn"
        screen.blit(self.filler,(0,0)) #fills the screen
        #DRAWS PERSONS
        for a in allies:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            screen.blit(allyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
        for e in enemies:
            screen.blit(enemyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
        display.flip()
        time.wait(500)
        screenBuff = screen.copy()
        screen.blit(transform.scale(transRed,(1200,60)),(0,330)) #blits the text "ENEMY PHASE" on a translucent red strip
        screen.blit(papyrus.render("ENEMY PHASE",True,WHITE),(450,340))
        display.flip()
        time.wait(1000)
        screen.blit(screenBuff,(0,0))
        #ENEMY'S PHASE GOES HERE - REQUIRES AI
        self.turn += 1 #increases turn by 1
        self.startTurn() #starts the turn
    def gameOver(self):
        "draws game over screen"
        for i in range(50):
            screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fadinge effect
            display.flip()
            time.wait(50)
        screen.blit(papyrus.render("GAME OVER",True,RED),(500,300))
        display.flip()
    def moveSelect(self):
        "moves selector"
        kp = key.get_pressed()
        if kp[K_UP]:
            self.selecty -= 1
        if kp[K_DOWN]:
            self.selecty += 1
        if kp[K_LEFT]:
            self.selectx -= 1
        if kp[K_RIGHT]:
            self.selectx += 1
        if self.mode in ["freemove","move"]:
            self.selectx = min(39,max(0,self.selectx))
            self.selecty = min(23,max(0,self.selecty))
    def moveMenuSelect(self,menuselect,limit):
        "moves a menu selector and returns new value"
        #moves self.menuselect up or down
        kp = key.get_pressed()
        if kp[K_UP]:
            menuselect -= 1
        elif kp[K_DOWN]:
            menuselect += 1
        #wraps around if too large or too small
        if menuselect < 0:
            menuselect = limit - 1
        elif menuselect >= limit:
            menuselect = 0
        return menuselect
    def run(self,screen):
        "runs the game in the running loop"
        global running,chapter
        #----EVENT LOOP----#
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if self.mode == "gameover":
                    self.start()
                    continue
                kp = key.get_pressed()
                #MOVEMENT OF SELECTION CURSOR OR MENU OPTION
                if self.mode in ["freemove","move"]:
                    #freemove moves freely; move picks a location
                    self.moveSelect() #handles movements by player
                    self.clickedFrame = self.framecounter #sets the clickedFrame to self
                if self.mode in ["optionmenu","itemattack","item","mainmenu"]:                    
                    #moves selected menu item
                    if self.mode in ["optionmenu","mainmenu"]:
                        self.menuselect = self.moveMenuSelect(self.menuselect,len(self.menu))
                    elif self.mode == "item":
                        if self.selectedItem == None:
                            self.menuselect = self.moveMenuSelect(self.menuselect,len(self.selected.items))
                        else:
                            self.optselected = self.moveMenuSelect(self.optselected,2) #item submenu has a limit 2
                    else:
                        self.menuselect = self.moveMenuSelect(self.menuselect,5)
                if self.mode == "attack":
                    #changes enemy selected
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        self.selectedEnemy += 1
                    if kp[K_LEFT] or kp[K_UP]:
                        self.selectedEnemy -= 1
                    if self.selectedEnemy == len(self.attackableEnemies):
                        self.selectedEnemy = 0
                    elif self.selectedEnemy == -1:
                        self.selectedEnemy = len(self.attackableEnemies)-1
                    self.selectx,self.selecty = self.attackableEnemies[self.selectedEnemy].x,self.attackableEnemies[self.selectedEnemy].y
                if self.mode in ["trade","heal"] and self.selected2 == None:
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        self.selectedAlly += 1
                    if kp[K_LEFT] or kp[K_UP]:
                        self.selectedAlly -= 1
                    if self.selectedAlly == len(self.targetableAllies):
                        self.selectedAlly = 0
                    elif self.selectedAlly == -1:
                        self.selectedAlly = len(self.targetableAllies)-1
                elif self.mode == "trade":
                    #if we have a selected2 we move the item selector instead
                    #horizontal movement of item selector across two allies
                    if kp[K_RIGHT]:
                        self.menuselect[0] = 1
                    elif kp[K_LEFT]:
                        self.menuselect[0] = 0
                    #vertical movement within the item menu
                    selectedAllies = [self.selected,self.selected2] #the selected allies
                    self.menuselect[1] = self.moveMenuSelect(self.menuselect[1],5)
                #---------Z--------#
                if e.unicode.lower() == "z":
                    #if the user pressed z
                    #handles clicks
                    #FREE MOVE MODE
                    if self.mode == "freemove":
                        for p in allies+enemies:
                            #checks if ally or enemy is clicked
                            if self.selectx == p.x and self.selecty == p.y and p not in self.moved:
                                self.mode = "move"
                                self.selected = p
                                self.oldx,self.oldy = p.x,p.y #keeps track of ally's position before so that we can backtrace
                                acoords = [(a.x,a.y) for a in allies]
                                encoords = [(e.x,e.y) for e in enemies]
                                if p in allies:
                                    #we get movements below
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,eval("chapter"+str(chapter)),acoords,encoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in acoords]
                                elif p in enemies:
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,eval("chapter"+str(chapter)),encoords,acoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we constantly fill moveable and attackable squares
                        else:
                            #if the user presses a blank spot, we set the mode to main menu
                            self.mode = "mainmenu"
                            self.menu = ["end"] #menu has End turn
                            self.menuselect = 0
                    #MOVE MODE
                    elif self.mode == "move":
                        #moves the unit if it is an ally and within the moveable squares
                        if (self.selectx,self.selecty) in [(x,y) for x,y,m in self.moveableSquares]+[(self.selected.x,self.selected.y)] and self.selected in allies:
                            self.selected.x,self.selected.y = self.selectx,self.selecty
                            self.mode = "optionmenu"
                            self.menu = []
                            self.menuselect = 0
                            #----Menu Creation
                            #ATTACK OPTION
                            if not (self.selected in self.attacked or self.selected.equip == None):
                                for w in [i for i in self.selected.items if type(i) == Weapon]:
                                    #checks every weapon if one yields in an attack we equip it and add attack
                                    if not self.selected.canEquip(w):
                                        continue
                                    if len(getAttackableEnemies(self.selected,enemies,weapon=w)) > 0:
                                        self.selected.equipWeapon(w)
                                        self.menu.append("attack")
                                        break
                            #ITEM OPTION
                            if len(self.selected.items) > 0:
                                self.menu.append("item")
                            #TRADE OPTION
                            if len(getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)) > 0:
                                self.menu.append("trade") #we can only trade if we have targetable allies within range 1
                            #WAIT OPTION
                            self.menu.append("wait") #a person can always wait
                    #MAIN MENU CLICK
                    elif self.mode == "mainmenu":
                        #allows user to select options
                        if self.menu[self.menuselect] == "end":
                            self.mode = "freemove"
                            self.endTurn() #ends turn
                    #OPTION MENU CLICK
                    elif self.mode == "optionmenu":
                        #allows user to select options
                        if self.menu[self.menuselect] == "attack":
                            self.mode = "itemattack"
                            self.menuselect = 0
                        elif self.menu[self.menuselect] == "item":
                            self.mode = "item"
                            self.menuselect = 0
                        elif self.menu[self.menuselect] == "trade":
                            self.mode = "trade"
                            self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                            self.menuselect = [0,0] #menuselect becomes a list, first element is the selected person, second is the selected item
                        elif self.menu[self.menuselect] == "wait":
                            self.mode = "freemove"
                            self.moved.add(self.selected)
                            self.attacked.add(self.selected)
                    #ATTACK CLICKS
                    elif self.mode == "itemattack":
                        if self.menuselect < len(self.selected.items):
                            if type(self.selected.items[self.menuselect]) == Weapon:
                                if self.selected.canEquip(self.selected.items[self.menuselect]) and getAttackableEnemies(self.selected,enemies,weapon=self.selected.items[self.menuselect]):
                                    self.mode = "attack"
                                    self.selected.equipWeapon(self.selected.items[self.menuselect])
                                    self.attackableEnemies = getAttackableEnemies(self.selected,enemies)
                                    self.selectx,self.selecty = self.attackableEnemies[0].x,self.attackableEnemies[0].y
                                    self.selectedEnemy = 0
                    elif self.mode == "attack":
                        #does an attack
                        attack(self.selected,self.attackableEnemies[self.selectedEnemy])
                        self.attacked.add(self.selected)
                        self.moved.add(self.selected)
                        self.mode = "freemove"
                    #ITEM MODE CLICK
                    elif self.mode == "item":
                        #handles item selection
                        if self.selectedItem == None:
                            #selects an item and creates a submenu
                            self.optselected = 0 #option selected for the submenu
                            self.selectedItem = self.selected.items[self.menuselect]
                        elif type(self.selectedItem) == Weapon:
                            #if a weapon is selected, we check whether user equips or discards
                            #0 is equip, 1 is discard
                            if self.optselected:
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            else:
                                #equip option
                                self.selected.equipWeapon(self.selectedItem) #tries to equip
                            self.selectedItem = None #resets self.selectedItem
                            if self.selected.equip == None:
                                #if we have no equipped item we remove the attack option from menu
                                if "attack" in self.menu:
                                    self.menu.remove("attack")
                                #we also empty attackableSquares
                                self.attackableSquares = []
                        elif type(self.selectedItem) == Consumable:
                            #if a consumable is a selected, we check whehther uses or discards
                            #0 is use, 1 is discard
                            if self.optselected:
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            else:
                                #use option
                                if not self.selectedItem.use(self.selected):
                                    #uses consumable
                                    #if it breaks we remove it
                                    self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                                self.moved.add(self.selected) #unit must wait after using a consumable
                                self.attacked.add(self.selected)
                                self.oldx,self.oldy = self.selected.x,self.selected.y #no moving back after using a consumable
                                self.moveableSquares,self.attackableSquares = [],[] #empties moveablesquares
                                self.mode = "optionmenu"
                                self.menuselect = 0
                            self.selectedItem = None #resets selectedItem
                        if len(self.selected.items) == 0:
                            #if we have no items left, we go back to option menu and remove items from the list
                            self.menu.remove("item")
                            self.mode = "optionmenu"
                            self.menuselect = 0
                    #TRADE MODE CLICK
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            #if there is self.selected2, we set one
                            self.selected2 = self.targetableAllies[self.selectedAlly]
                        else:
                            #otherwise we select an item
                            if self.selectedItem == None:
                                #if we have no selectedItem we set one
                                self.selectedItem = self.menuselect[:]
                            else:
                                #if we have a selected item, we commence the trade
                                selectedAllies = [self.selected,self.selected2] #selected allies
                                selectedItem1 = selectedItem2 = None #the default selected Item is None
                                if self.selectedItem[1] < len(selectedAllies[self.selectedItem[0]].items):
                                    #1st item is in range and is not None, then we give it to the other selected ally
                                    selectedItem1 = selectedAllies[self.selectedItem[0]].items[self.selectedItem[1]] #first selected item
                                if self.menuselect[1] < len(selectedAllies[self.menuselect[0]].items):
                                    #2nd item is in range and is not None, then we give it to the other selected ally
                                    selectedItem2 = selectedAllies[self.menuselect[0]].items[self.menuselect[1]] #second selected item
                                if selectedItem1 != None:
                                    selectedAllies[self.selectedItem[0]].removeItem(selectedItem1) #removes first item
                                    selectedAllies[self.menuselect[0]].addItem(selectedItem1) #appends 1st item to second ally
                                if selectedItem2 != None:
                                    selectedAllies[self.menuselect[0]].removeItem(selectedItem2) #removes second item
                                    selectedAllies[self.selectedItem[0]].addItem(selectedItem2) #appends 2nd item to first ally
                                self.selectedItem = None #resets selectedItem

                #------X------#
                if e.unicode.lower() == "x":
                    #if the user pressed x
                    #handles backtracing
                    if self.mode == "move":
                        self.mode = "freemove"
                    elif self.mode == "mainmenu":
                        self.mode = "freemove"
                    elif self.mode == "optionmenu":
                        self.mode = "move"
                        self.selected.x,self.selected.y = self.oldx,self.oldy
                        if self.moveableSquares == []:
                            self.mode = "freemove" #we go back to freemove mode if we have no moveablesquares
                    elif self.mode == "itemattack":
                        self.mode = "optionmenu"
                        self.menuselect = 0
                    elif self.mode == "item":
                        if self.selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
                            self.mode = "item"
                            self.selectedItem = None
                        else:
                            self.mode = "optionmenu"
                            self.menuselect = 0
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            self.mode = "optionmenu"
                            self.menuselect = 0
                        else:
                            if self.selectedItem == None:
                                self.selected2 = None #if there exists selected2, that means the trade interface is open, so we close that
                            else:
                                #however if there is a selected item, we instead deselect it
                                self.selectedItem = None
                    elif self.mode == "attack":
                        self.menuselect = 0
                        self.mode = "itemattack"
                if e.unicode == "v":
                    #skips battle for now
                    self.gameVictory()
        #-----END OF EVENT LOOP----#
        if self.mode == "gameVictory":
            return 0
        if self.mode == "gameover":
            return 0
        screen.blit(self.filler,(0,0)) #blits the filler
        if 0 in [player.hp,yoyo.hp] and self.mode != "gameover":
            self.gameOver()
            self.mode = "gameover"
            return 0
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if self.framecounter - self.clickedFrame > 20 and self.mode in ["freemove","move"] and not self.framecounter%6:
            #if we held for 20 frames or more we move more
            #we only do it once every 6 frames or it'll be too fast
            self.moveSelect()
        #--------------------HIGHLIGHTING A PERSON---------------#
        if self.mode == "freemove":
            for p in allies+enemies:
                if self.selectx == p.x and self.selecty == p.y:
                    #DRAWS PERSON MINI DATA BOX
                    pdbx,pdby = 0,0 #person data box x and y
                    if self.selectx < 20 and self.selecty <= 12:
                        pdby = 630
                    draw.rect(screen,BLUE,(pdbx,pdby,300,90)) #background box
                    screen.blit(sans.render(stripNums(p.name),True,WHITE),(pdbx+15,pdby+3)) #person's name
                    screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,WHITE),(pdbx+15,pdby+33)) #health
                    draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                    draw.line(screen,YELLOW,(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                    break
        #---------------DIFFERENT MODE DISPLAYS------------------#
        #MOVE MODE DISPLAY
        if self.mode == "move":
            #fills moveable and attackable squares
            fillSquares(screen,set([(x,y) for x,y,m in self.moveableSquares]+[(self.selected.x,self.selected.y)]),transBlue)
            if self.attackableSquares and self.selected.equip != None:
                fillSquares(screen,self.attackableSquares,transRed)
        #DRAWS PERSONS
        for a in allies:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            screen.blit(allyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
        for e in enemies:
            screen.blit(enemyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
        #MAIN MENU MODE DISPLAY
        if self.mode == "mainmenu":
            #if it is menu mode we draw the menu
            menux,menuy = 18,4
            drawMenu(self.menu,menux,menuy,120,480,self.menuselect) #draws the main menu
        #OPTION MENU MODE DISPLAY
        if self.mode == "optionmenu":
            menux,menuy = 36,2
            if self.selected.x >= 20:
                menux = 0
            drawMenu(self.menu,menux,menuy,120,len(self.menu)*30,self.menuselect)
        #ATTACK MODE DISPLAY
        if self.mode == "itemattack":
            #displays item selection menu for attack
            drawItemMenu(self.selected,self.selected.x+1,self.selected.y,self.menuselect)
        if self.mode == "attack":
            #highlights all attackable squares
            fillSquares(screen,getAttackableSquares(self.selected.equip.rnge,self.selected.equip.maxrnge,self.selected.x,self.selected.y),transRed)
            #displays battle stats (such as hit chance, damage, crit)
            x,y = 25,3
            if self.selected.x > 20:
                x = 0 #x goes to left if selected person is on the right
            #battle stats from ally's POV
            #battleStatsMenu has name, HP, hit chance, damage, crit chance, weapon of use and whether the weapon has an advantage or not
            enemy = self.attackableEnemies[self.selectedEnemy] #the selected enemy
            #gets battle stats for the selected ally
            battleStatsMenu = getBattleStats(self.selected,enemy,eval("chapter"+str(chapter)))
            drawMenu(battleStatsMenu,x,y,210,210,-20) #draws battle stats menu for ally

            #battle stats from enemy's POV
            battleStatsMenu = getBattleStats(enemy,self.selected,eval("chapter"+str(chapter)))
            drawMenu(battleStatsMenu,x+7,y,210,210,-20,RED) #draws battle stats menu for enemy
        #ITEM MODE DISPLAY
        if self.mode == "item":
            screen.blit(transBlack,(0,0))
            drawItemMenu(self.selected,14,8,self.menuselect)
            if self.selectedItem != None:
                #if we have a selected Item we draw the submenu
                if type(self.selectedItem) == Weapon:
                    if self.selected.canEquip(self.selectedItem):
                        col = GREEN #color to write "Equip" with
                        #green means can, grey means can't
                    else:
                        col = GREY
                    #options user can choose for the selected item
                    options = ["Equip","Discard"] #weapons can be equipped or discarded
                if type(self.selectedItem) == Consumable:
                    col = GREEN
                    options = ["Use","Discard"] #consumables can be used or discarded
                draw.rect(screen,BLUE,(22*30,8*30,120,len(options)*30)) #draws submenu backdrop for item
                screen.blit(sans.render(options[0],True,col),(22*30,8*30)) #draws first option
                screen.blit(sans.render(options[1],True,WHITE),(22*30,9*30)) #draws discard option
                draw.rect(screen,WHITE,(22*30,(8+self.optselected)*30,120,30),1) #selected option
        #TRADE MODE DISPLAY
        if self.mode == "trade":
            if self.selected2 == None:
                #if we have no 2nd selected ally, we draw the selector around the 2nd selected ally
                highlightedAlly = self.targetableAllies[self.selectedAlly] #highlighted ally
                draw.rect(screen,WHITE,(highlightedAlly.x,highlightedAlly.y,30,30),1) #draws selector around highlighted ally
            else:
                screen.fill(GREEN) #fills the screen with green
                #draws item menu for both allies
                #first we set which item selected out of the two menus
                #this is based on which ally the selector is on
                #which is determined by the first element of menuselect
                menuselect1 = -20 if self.menuselect[0] else self.menuselect[1]
                menuselect2 = -20 if not self.menuselect[0] else self.menuselect[1]
                                                                                
                drawItemMenu(self.selected,8,9,menuselect1)
                drawItemMenu(self.selected2,24,9,menuselect2)
                if self.selectedItem != None:
                    #if the selected Item isn't none, we draw the cursor
                    draw.rect(screen,WHITE,((8+self.selectedItem[0]*16)*30,(9+self.selectedItem[1])*30,240,30),1)
        #---------------INFO DISPLAY BOXES----------------------#
        #TERRAIN DATA BOX
        if self.mode == "freemove":
            tbx,tby = 1020,630 #terrain box x and y
            stage = eval("chapter"+str(chapter))
            if self.selectx >= 20:
                tbx = 0
            draw.rect(screen,BLUE,(tbx,tby,180,90))
            screen.blit(sans.render(stage[self.selecty][self.selectx].name,True,WHITE),(tbx+15,tby+3))
            draw.rect(screen,(255,230,200),(tbx,tby+30,180,60))
            screen.blit(sans.render("DEFENSE: "+str(stage[self.selecty][self.selectx].adef),True,BLACK),(tbx+15,tby+33))
            screen.blit(sans.render("AVOID: "+str(stage[self.selecty][self.selectx].avo),True,BLACK),(tbx+15,tby+63))
        #GOAL DISPLAY BOX
            goalx,goaly = 1020,0
            if self.selecty <= 12 and self.selectx >= 20:
                goaly = 630
            draw.rect(screen,(50,50,180),(goalx,goaly,180,90))
            screen.blit(smallsans.render(self.goal,True,WHITE),(goalx+15,goaly+35))
        #---------------SELECTED SQUARE BOX----------------#
        if self.mode in ["freemove","move","attack"]:
            draw.rect(screen,WHITE,(self.selectx*30,self.selecty*30,30,30),1) #draws select box
        #----------------ENDING THE LOOP-------------------#
        display.flip()
        self.framecounter += 1 #increases frame counter
        self.fpsTracker.tick(60) #limits FPS to 60
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
