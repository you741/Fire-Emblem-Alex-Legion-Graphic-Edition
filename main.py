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
def greyScale(img):
    "returns a grey version of img"
    new_img = Surface((img.get_width(),img.get_height()),SRCALPHA)
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r,g,b,a = img.get_at((x,y))
            grey = (r+g+b)//3
            new_color = Color(grey,grey,grey,a) #greyscale version of pixel
            new_img.set_at((x,y),new_color)
    return new_img
#ALLIES' ANIMATIONS
playerMageStandSprite = image.load('images/Player/Mage/MageAttackFrame1.png')
playerMageAnimaSprite = ([image.load("images/Player/Mage/MageAttackFrame"+str(i+1)+".png")
                          for i in range(16)],10)
playerMageAnimacritSprite = ([image.load("images/Player/Mage/MageCritFrame"+str(i+1)+".png")
                        for i in range(12)] + playerMageAnimaSprite[0][1:],21)
playerKnightStandSprite = image.load('images/Player/Knight/KnightAttackFrame1.png')
playerKnightLanceSprite = ([image.load("images/Player/Knight/KnightAttackFrame"+str(i+1)+".png")
                            for i in range(11)],5)
playerKnightLancecritSprite = ([image.load("images/Player/Knight/KnightCritFrame"+str(i+1)+".png")
                                for i in range(8)] + playerKnightLanceSprite[0],13)

yoyoStandSprite = image.load("images/Yoyo/YoyoAttackFrame1.png").convert_alpha()
yoyoSwordSprite = ([image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)],5)
yoyoSwordcritSprite = ([image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)],29)

albertStandSprite = playerMageStandSprite
albertAnimacritSprite = playerMageAnimacritSprite
albertAnimaSprite = playerMageAnimaSprite
#ENEMIES' ANIMATIONS
brigandStandSprite = image.load("images/Brigand/BrigandAttackFrame1.png")
brigandAxeSprite = ([image.load("images/Brigand/BrigandAttackFrame"+str(i+1)+".png")
                       for i in range(14)],9)
brigandAxecritSprite = ([image.load("images/Brigand/BrigandCritFrame"+str(i+1)+".png")
                     for i in range(2)] + brigandAxeSprite[0],11)

#MAGIC ANIMATIONS
fireSprite = [image.load("images/Magic/Fire/Fire"+str(i+1)+".png").convert_alpha()
              for i in range(17)]

#MAP SPRITES
allyMapSprites = {"Mage":[transform.scale(image.load("images/MapSprites/Ally/Mage"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Lord":[transform.scale(image.load("images/MapSprites/Ally/Lord"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Knight":[transform.scale(image.load("images/MapSprites/Ally/Knight"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)]}
enemyMapSprites = {"Brigand":[transform.scale(image.load("images/MapSprites/Enemy/Brigand"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)]}
allyGreyMapSprites = {}
for i,k in enumerate(allyMapSprites):
    allyGreyMapSprites[k] = [greyScale(img) for img in allyMapSprites[k]]
enemyGreyMapSprites = {}
for i,k in enumerate(enemyMapSprites):
    enemyGreyMapSprites[k] = [greyScale(img) for img in enemyMapSprites[k]]
faces = {"Yoyo":image.load("images/faces/Yoyo.png"),
                      "Player":image.load("images/faces/player.png"),
                      "Bandit":image.load("images/faces/Bandit.png")} #dictionary of all faces of characters
#----END OF IMAGE LOAD----#
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
#ALLIES
name = "" #name of player
usedNames = ["yoyo","albert","franny","gary","stefano","henry","henning","brandon","eric","alex"] #names the player cannot use
player = None #player is defined in NewGame or LoadGame
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
               [rapier.getInstance(),vulnerary.getInstance()],{"Sword":200},
               {"Sword":yoyoSwordSprite,"Swordcrit":yoyoSwordcritSprite,"stand":yoyoStandSprite},faces["Yoyo"])
albert = Mage("Albert",0,0,
              {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
              [fire.getInstance(),vulnerary.getInstance()],{'Anima':200},
              {'stand':playerMageStandSprite,'Anima':playerMageAnimaSprite,'Animacrit':playerMageAnimacritSprite},faces["Player"])#test person for chapter 1
allies = [] #allies
#ENEMIES
bandit0 = Brigand("Bandit",0,0,
                  {"lv":1,"stren":5,"defen":4,"skl":3,"lck":0,
                   "spd":3,"con":8,"move":5,"res":0,"hp":20,"maxhp":20},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
enemies = []
#----CHAPTERS----#
#MAPS
chapter0 = [[plain for i in range(40)] for j in range(24)]
chapter1 = [[plain for i in range(40)] for j in range(24)]
chapterMaps = [chapter0,chapter1]
#CHAPTER DATA
#Stored in tuples
#(gainedAllies,allyCoordinates,Enemies,Goal,BackgroundImage)
#chapter data, chapter is determined by index
chapterData = [([yoyo],[(0,1),(0,0)],createEnemyList([bandit0],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies",image.load("images/Maps/prologue.png")),
               ([albert],[(0,1),(0,0),(1,1)],createEnemyList([bandit0],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies",image.load("images/Maps/prologue.png"))]
oldAllies = [] #keeps track of allies before the fight
allAllies = [] #all allies that exist

#----MUSIC----#
#add at the end because Albert's mac is funny
#each index represents what music is played in the chapter of that index
#chapterMusic = [conquest]

#miscellaneous
chapter = 0 #changes when load new/old game, so stays global
fpsLimiter = time.Clock()

#----GLOBAL FUNCTIONS----#
def addAlly(ally):
    "adds an ally to the allies list - updates allAllies too"
    allies.append(ally) #adds ally to allies
    allAllies.append(ally) #adds ally to allAllies
def load(file):
    "loads the file into the game, and returning 0 if it is empty"
    global chapter,allAllies
    if "chapter" not in file:
        file.close()
        changemode(NewGame())#goes to new game
    else:
        #sets the chapter we are about to start and allAllies
        chapter = file["chapter"]
        allAllies = file["allAllies"]
        for a in allAllies:
            imagifyStrings(a) #imagify all images as they were strings while data of allies
        file.close()
        changemode(Game())
def save(file):
    "saves game into file"
    global chapter, allAllies
    file["chapter"] = chapter + 1
    chapter += 1
    ##this will need more work here when we need to modify ally list based on chapter
    for a in allAllies:
        stringifyImages(a) #stringify all images of allies
    file["allAllies"] = allAllies #save allAllies
    for a in allAllies:
        imagifyStrings(a) #imagify all images of allies
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
    drawBattleInfo(screen,ally,enemy,chapterMaps[chapter])
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for ally and enemy
    screen.blit(ally.anims["stand"],(0,0))
    screen.blit(enemy.anims["stand"],(0,0))
    display.flip()
    time.wait(200)
    isenemy = person in enemies #is person an enemy? (boolean)
    #Draws damage for attack 1
    screen.blit(actionFiller,(0,0)) #covers both persons
    singleAttack(screen,person,person2,isenemy,chapterMaps[chapter])
    event.pump() #handles events so we don't get locked down
    if checkDead(ally,enemy):
        #gains exp
        if enemy.hp == 0:
            expgain = getExpGain(ally,enemy,True) #gains exp on a kill
            drawChangingBar(screen,ally.exp,ally.exp+expgain,100,420,330,360,60,"Exp")
            needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
            if needLevelUp:
                #level up
                ally.levelUp()
                drawLevelUp(screen,ally)
        display.flip()
        time.wait(500)
        return False #ends the function if either ally or enemy is dead
    #Draws damage for attack 2
    person2hit = False #did person2 hit? (person 1 hits no matter what, so I don't need that)
    if canAttackTarget(person2,person.x,person.y):
        #if person2 can attack
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,person2,person,not isenemy,chapterMaps[chapter])
        person2hit = True
    event.pump() #handles events so we don't get locked down
    if checkDead(ally,enemy):#gains exp
        if enemy.hp == 0:
            expgain = getExpGain(ally,enemy,True) #gains exp on a kill
            drawChangingBar(screen,ally.exp,ally.exp+expgain,100,420,330,360,60,"Exp")
            needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
            if needLevelUp:
                #level up
                ally.levelUp()
                drawLevelUp(screen,ally)
        display.flip()
        time.wait(500)
        return False
    #Draws damage for attack 3
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy.x,enemy.y):
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,ally,enemy,False,chapterMaps[chapter])
        person2hit = ally == person2 #person2hit becomes true if ally was person2
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally.x,ally.y):
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,enemy,ally,True,chapterMaps[chapter])
    event.pump() #handles events so we don't get locked down
    kill = False
    if checkDead(ally,enemy):
        if ally.hp == 0:
            return False #we exit function if ally is dead
        kill = True
    expgain = getExpGain(ally,enemy,kill) #experience points to gain
    expgain = min(100,expgain) #experience gain cannot exceed 100
    if ally == person2 and not person2hit:
        #if person2 did not hit and that was the ally, we only gain 1 exp
        expgain = 1
    drawChangingBar(screen,ally.exp,ally.exp+expgain,100,420,330,360,60,"Exp")
    event.pump() #handles events so we don't get locked down
    needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
    if needLevelUp:
        #level up
        ally.levelUp()
        drawLevelUp(screen,ally)
    time.wait(1000)
    event.pump() #handles events so we don't get locked down
    event.clear()
#-------MANAGEMENT FUNCTIONS--------#
#this is to help me manage image saving
def stringifyImages(ally):
    "stringifies all images in ally - I need to do this in order to save them into a file, as Python can't save surfaces"
    #NOTE: to stringify means to change an image into a string representing the variable name that points to the image
    name = ally.name.lower()
    if ally.name.lower() not in usedNames:
        #if ally's name isn't in used names, then it is the player
        name = "player"+ally.__class__.__name__ #we add the class for the player
    for i,k in enumerate(ally.anims):
        ally.anims[k] = name+k.title()+"Sprite"
    for w in [i for i in ally.items if type(i) == Weapon]:
        #goes through all weapons and imagifies them
        if w.anims != None:
            #changes all weapons with an animation to be stringified
            w.anims = w.name.lower()+"Sprite"
def imagifyStrings(ally):
    "imagifies all strings in ally - opposite of stringifyImages"
    for i,k in enumerate(ally.anims):
        ally.anims[k] = eval(ally.anims[k]) #creates an image from the string using eval
    for w in [i for i in ally.items if type(i) == Weapon]:
        #goes through all weapons and imagifies them
        if w.anims != None:
            w.anims = eval(w.anims)
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
    "Allows user to perform an action by clicking on a button"
    def __init__(self,x=0,y=0,width=0,height=0,background=Surface((1,1)),hlbackground=Surface((1,1)),cbackground=Surface((1,1)),func=[]):
        "sets all the class's members"
        self.x = x #co-ordinates
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = background #background of button
        self.hlbackground = hlbackground #background of button when highlighted
        self.cbackground = cbackground #background when clicked
        self.func = func #func is a list of strings that contains commands to be executed
    def istouch(self,x=None,y=None):
        "checks if co-ordinates are touching Button"
        #default is mouse co-ordinates
        mx,my = mouse.get_pos()
        if x == None:
            x = mx
        if y == None:
            y = my
#        return Rect(self.x,self.y,self.width,self.height).collidepoint(x,y) #returns boolean
        if Rect(self.x,self.y,self.width,self.height).collidepoint(x,y):
            if self.background.get_at((x-self.x,y-self.y)) != (255,255,255):
                return True
        return False
    def draw(self,screen):
        "draws button on screen"
        if self.istouch():
            screen.blit(self.hlbackground,(self.x,self.y)) #if it's highlighted we draw the highlighted background
        else:
            screen.blit(self.background,(self.x,self.y))
    def click(self):
        screen.blit(self.cbackground,(self.x,self.y))
        "runs button's func"
        exec("\n".join(self.func))


class Menu():
    "menu so the user can select from a list of buttons"
    def __init__(self, x=0,y=0,width=0,height=0,background=Surface((1,1)),selected=0,items=[]):
        self.x = x #co-rds
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = background #background of the menu, will most likely be a rectangle that we stretch (<> -> <==========>)
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
            self.selected = len(self.items) - 1
        elif self.selected >= len(self.items):
            self.selected = 0
    def draw(self):
        "draws a list of strings as a vertical menu at positions x and y"
        draw.rect(screen,BLUE,(self.x*30,self.y*30,self.width,self.height))
        for i in range(len(self.items)):
            opt = self.items[i].title() #option to draw
            screen.blit(sans.render(opt,True,WHITE),(self.x*30,(self.y+i)*30))
        draw.rect(screen,WHITE,(self.x*30,(self.y+self.selected)*30,self.width,30),1) #draws a border around the selected option

    
       
#----MODE CLASSES----#
#these classes are the different modes for the scren - must be in the main
class StartMenu():
    "start menu mode"
    def __init__(self):
        "sets button list of mode"
        self.stopped = False
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"START",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"START",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),GREEN,"START",BLACK,monospace,(30,10)),
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
    "Screen mode for saving the game"
    def __init__(self):

        self.background = Surface((1200,720))
        self.background.fill(BLACK)
        
        self.stopped = False
        
        self.savingfile = False #is he choosing what file to save into?
        self.filenum = 1
        #Loads files
        self.file1 = shelve.open("saves/file1")
        self.file2 = shelve.open("saves/file2")
        self.file3 = shelve.open("saves/file3")
        print(self.file1.get("chapter")) #this fixes the code for some odd reason - I should probably discuss with Mr. Mckenzie later
        #sets the button text based on which files have data
        button1Text = "--NO DATA--" if "chapter" not in self.file1 else "Chapter: "+str(self.file1["chapter"])
        button2Text = "--NO DATA--" if "chapter" not in self.file2 else "Chapter: "+str(self.file2["chapter"])
        button3Text = "--NO DATA--" if "chapter" not in self.file3 else "Chapter: "+str(self.file3["chapter"])
        #creates buttons
        self.buttons1 = [Button(500,420,200,50,
                                       FilledSurface((200,50),BLUE,button1Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button1Text,BLACK,monospace,(0,10)),
                                       FilledSurface((200,50),GREEN,button1Text,BLACK,monospace,(0,10)),
                                       ["currmode.savingfile = True","currmode.filenum=1"]),
                                Button(500,480,200,50,
                                       FilledSurface((200,50),BLUE,button2Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button2Text,BLACK,monospace,(0,10)),
                                       FilledSurface((200,50),GREEN,button2Text,BLACK,monospace,(0,10)),
                                       ["currmode.savingfile = True","currmode.filenum=2"]),
                                Button(500,540,200,50,
                                       FilledSurface((200,50),BLUE,button3Text,WHITE,monospace,(0,10)),
                                       FilledSurface((200,50),YELLOW,button3Text,BLACK,monospace,(0,10)),
                                       FilledSurface((200,50),GREEN,button2Text,BLACK,monospace,(0,10)),
                                       ["currmode.savingfile = True","currmode.filenum=3"])]
        self.buttons2 = [Button(500,600,80,50,
                                FilledSurface((80,50),BLUE,"SAVE",WHITE,monospace,(0,10)),
                                FilledSurface((80,50),YELLOW,"SAVE",BLACK,monospace,(0,10)),
                                FilledSurface((80,50),GREEN,"SAVE",BLACK,monospace,(0,10)),
                                ["save([currmode.file1,currmode.file2,currmode.file3][currmode.filenum-1])"]),
                         Button(600,600,80,50,
                                FilledSurface((80,50),BLUE,"QUIT",WHITE,monospace,(0,10)),
                                FilledSurface((80,50),YELLOW,"QUIT",BLACK,monospace,(0,10)),
                                FilledSurface((80,50),GREEN,"QUIT",BLACK,monospace,(0,10)),
                                ["quit()"])]
                         
    def draw(self,screen):
        "draws mode on screen"
        screen.fill(BLACK)
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
                for b in self.buttons1:
                    if b.istouch() and currmode == self:
                        b.click()
                if self.savingfile: 
                    for b in self.buttons2:
                        if b.istouch() and currmode == self:
                            b.click()
            screen.blit(self.background,(0,0))
            kp = key.get_pressed()
            if kp[K_x]:
                self.savingfile = False
        if currmode != self:
            return 0 #if we have stopped, we return to stop the method
        #draws buttons
        for b in self.buttons1:
            b.draw(screen)
        if self.savingfile:
            for b in self.buttons2:
                b.draw(screen)
            ##this is temporary to show which one is selected, probably these'll all change to images
            draw.rect(screen,YELLOW,(500,420-60+self.filenum*60,200,50),5)
            
class LoadGame():
    "screen for loading game files"
    def __init__(self):
        self.stopped = False

        #Loads files
        #sets the button text based on which files have data
        self.file1 = shelve.open("saves/file1")
        self.file2 = shelve.open("saves/file2")
        self.file3 = shelve.open("saves/file3")

        button1Text = "--NO DATA--" if "chapter" not in self.file1 else "Chapter: "+str(self.file1["chapter"])
        button2Text = "--NO DATA--" if "chapter" not in self.file2 else "Chapter: "+str(self.file2["chapter"])
        button3Text = "--NO DATA--" if "chapter" not in self.file3 else "Chapter: "+str(self.file3["chapter"])


        #creates buttons
        self.buttons1 = [Button(500,420,200,50,
                               FilledSurface((200,50),BLUE,button1Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button1Text,BLACK,monospace,(0,10)),
                               FilledSurface((200,50),GREEN,button1Text,BLACK,monospace,(0,10)),
                               ["load(currmode.file1)"]),
                        Button(500,480,200,50,
                               FilledSurface((200,50),BLUE,button2Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button2Text,BLACK,monospace,(0,10)),
                               FilledSurface((200,50),GREEN,button2Text,BLACK,monospace,(0,10)),
                               ["load(currmode.file2)"]),
                        Button(500,540,200,50,
                               FilledSurface((200,50),BLUE,button3Text,WHITE,monospace,(0,10)),
                               FilledSurface((200,50),YELLOW,button3Text,BLACK,monospace,(0,10)),
                               FilledSurface((200,50),GREEN,button3Text,BLACK,monospace,(0,10)),
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
                for b in self.buttons1:
                    if b.istouch() and currmode == self:
                        b.click()
            kp = key.get_pressed()
            if kp[K_x]:
                changemode(StartMenu())
        if currmode != self:
            return 0 #if we have stopped, we return to stop the method
        #draws buttons
        for b in self.buttons1:
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
        self.buttons1 = [Button(900,300,200,50,
                               FilledSurface((200,50),BLUE,"SUBMIT",WHITE,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),GREEN,"SUBMIT",BLACK,monospace,(30,10)),
                               ["currmode.selectingname = False","currmode.selectingclass = True","screen.fill(BLACK)"])]
        #class select buttons
        self.buttons2 = [Button(300,300,200,50,
                                FilledSurface((200,50),BLUE,"MAGE",WHITE,monospace,(40,10)),
                                FilledSurface((200,50),YELLOW,"MAGE",BLACK,monospace,(40,10)),
                                FilledSurface((200,50),GREEN,"MAGE",BLACK,monospace,(40,10)),
                                ["global player",
                                 """player = Mage(name,0,0,{'lv':1,'hp':17,'maxhp':17,'stren':5,'defen':1,'spd':7,'res':5,'lck':5,'skl':6,'con':5,'move':5},
{'maxhp':55,'defen':10,'res':50,'stren':35,'spd':100,'skl':50,'lck':55},
[fire.getInstance()],
{'Anima':200},
{'stand':playerMageStandSprite,'Anima':playerMageAnimaSprite,'Animacrit':playerMageAnimacritSprite},faces['Player'])
addAlly(player)
""",
                                "changemode(getStory(chapter))"]),
                         
                         Button(600,300,200,50,
                                FilledSurface((200,50),BLUE,"KNIGHT",WHITE,monospace,(40,10)),
                                FilledSurface((200,50),YELLOW,"KNIGHT",BLACK,monospace,(40,10)),
                                FilledSurface((200,50),GREEN,"KNIGHT",BLACK,monospace,(40,10)),
                                ["global player",
                                 """player = Knight(name,0,0,{"lv":1,"hp":25,"maxhp":25,"stren":7,"defen":7,"spd":4,"res":0,"skl":5,"lck":4,"con":5,"move":4},
{"stren":55,"defen":50,"skl":45,"lck":40,"spd":30,"res":15,"maxhp":65},
[iron_lance.getInstance(),vulnerary.getInstance()],
{"Lance":200},
{"Lance":playerKnightLanceSprite,"Lancecrit":playerKnightLancecritSprite,"stand":playerKnightStandSprite},faces['Player'])
addAlly(player)
""",
                                 "changemode(getStory(chapter))"])]
        
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
                    elif len(name) > 0 and name.lower() in usedNames:
                        ##put a sound here
                        ##blit an image here
                        draw.rect(screen,WHITE,(100,100,100,100))
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

def getStory(chapter,end=False):
    "gets story based on the chapter number"
    storyFile = open("chapters/chapter"+str(chapter)+".txt")
    story = storyFile.read().strip().replace("*Player*",player.name).split("\n") #story
    background = story[0].strip() #background image source
    story = story[1:] #actual story
    return Story(story,image.load(background))

class Story():
    "screen mode for user to see the story"
    def __init__(self,dialogue,background,music=None):
        "initialize the Story class contains all dialogue (which also includes which picture to put)"
        self.dialogue = dialogue
        self.background = background
        self.music=None
        self.currDial = 0 #current dialogue we are on
        self.limit = len(dialogue) #limit of the dialogue - once reached the story ends
    def draw(self,screen):
        "draws screen on - starts on title screen"
        screen.blit(self.background,(0,0))
    def playMusic(self):
        "Plays music"
        #WIP
        pass
    def writeDialogue(self,sentence):
        "writes the sentence on the screen character by character"
        global running
        character = 1 #up to which character we display
        while character <= len(sentence):
            #loops to draw all the characters one by one
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    return 0
                if e.type == KEYDOWN:
                    if e.key == K_z:
                        character = len(sentence)
            drawSentence(screen,sentence[:character]) #draws the sentence up to character
            character += 1 #prepares to draw one more character
            display.flip()
            fpsLimiter.tick(30) #limits it to 30 FPS
        return 1
    def run(self,screen):
        "runs the story dialogue"
        global running
        screen.blit(self.background,(0,0))
        func,sentence = self.dialogue[self.currDial].split(":") #function and sentence to display
        
        if func == "":

            #displays narration
            if not self.writeDialogue(sentence):
                #writes narration
                return 0 #if it returns false it means the user quit, so we quit as well
        elif func == "TITLE":
            #display the title
            screen.fill(BLACK)
            draw.rect(screen,BLUE,(0,330,1200,60))
            img = sans.render(sentence,True,WHITE) #img of string to blit
            screen.blit(img,(600-img.get_width()//2,360-img.get_height()//2)) #draws title in the center
        else:
            #displays a character talking (func = name of character in this case)
            allynames = [a.name.lower() for a in allAllies] #names of all allies
            x=0
            if func.lower() not in allynames:
                x = 900 #changes the x to other side of the screen
            if func.lower() == player.name.lower():
                img = faces["Player"] #player's face
            else:
                img = faces[func] #anyone else's face
            screen.blit(img,(x,410)) #blits face of character speaking
            draw.rect(screen,YELLOW,(x,490,300,30)) #draws background box for name
            draw.rect(screen,BLUE,(x+2,492,294,26))
            screen.blit(sans.render(func,True,WHITE),(x+2,490)) #draws the name
            if not self.writeDialogue(sentence):
                #writes dialogue
                return 0 #if it returns false it means the user quit, so we quit as well
        breakLoop = False
        while not breakLoop:
            #loops until user hits z or x to move on
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    breakLoop = True
                if e.type == KEYDOWN:
                    if e.key == K_z or e.key == K_x or e.key == K_RETURN:
                        self.currDial += 1
                        breakLoop = True
            display.flip()
            fpsLimiter.tick(60) #limits to 60 FPS
        if self.currDial >= self.limit:
            #once we hit the limit we transition to the game mode
            changemode(Game())
class Game():
    def __init__(self):
        "initializes game"
        self.selectx,self.selecty = 0,0 #select cursor starting point
        self.framecounter = 0
        self.clickedFrame = 0 #the frame user clicked (pressed z)
        self.mode = "freemove" #mode Game is in
        self.menu = Menu(0,0,0,0,FilledSurface((200,50),BLUE,"",WHITE,monospace,(40,10)),0,[]) #menu for optionmenu mode
        self.selectedEnemy,self.selectedItem = 0,None #selected Enemy and selected Item
        self.selected = None #selected ally
        self.selected2 = None #2nd selected ally - only for trading option
        self.selectedAlly = 0 #2nd selected ally that user is hovering over - only for trading option and healing option
        self.targetableAllies = [] #targetable allies
        self.filler = screen.copy()
        self.moved,self.attacked = set(),set() #sets moved and attacked to be sets
        self.turn = 1 #turn that it is
        self.goal = ""
        self.stopped = False #we are not stopped
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
        global oldAllies,allies,allAllies
        ##whatever animation/dialogue that needs to happen
        allAllies = [a for a in allAllies if a.name not in [al.name for al in allies]] #removes all of allies from allAllies
        allAllies += allies #adds allies to allAllies
        for a in allAllies:
            #brings all allies back to full health
            a.hp = a.maxhp
            a.stats["hp"] = a.maxhp
        draw.circle(screen,WHITE,(100,100),100) #NOTE TO ALBURITO!!!!!! !IJIOJOIASJFIOWJOIFWJFOIWJ!!!IJAOF! : th is this? got a circle fetish!? haha its a joke lol
        changemode(SaveGame())
    def drawPeople(self):
        "draws all people on the map"
        for a in allies:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            if a not in self.attacked or a not in self.moved:
                screen.blit(allyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
            else:
                #if the ally has moved already we draw it grey
                screen.blit(allyGreyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
        for e in enemies:
            if e not in self.attacked or e not in self.moved:
                screen.blit(enemyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
            else:
                screen.blit(enemyGreyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
    def start(self):
        "starts a chapter, also serves a restart"
        global allies,enemies,oldAllies
        self.selectx,self.selecty = 0,0
        newAllies,allyCoords,newenemies,self.goal,backgroundImage = chapterData[chapter]
        if chapter < 99:
            #the early chapters have no prefight screen to load oldAllies so allAllies are oldAllies
            oldAllies = [a.getInstance() for a in allAllies]
        enemies = [e.getInstance() for e in newenemies]
        allies = [a.getInstance() for a in oldAllies]
        allies += [a.getInstance() for a in newAllies] #adds all new allies to allies
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
        event.clear()#clears events so that it doesnt allow events to occur as soon as this ends
        self.mode = "freemove" #sets the mode back to freemove
    def endTurn(self):
        "ends the turn, starts the enemy turn"
        global running
        self.attacked.clear()
        self.moved.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        self.drawPeople()
        screenBuff = screen.copy()
        screen.blit(transform.scale(transRed,(1200,60)),(0,330)) #blits the text "ENEMY PHASE" on a translucent red strip
        screen.blit(papyrus.render("ENEMY PHASE",True,WHITE),(450,340))
        display.flip()
        time.wait(1000)
        screen.blit(screenBuff,(0,0))
        framelimiter = time.Clock()

        #ENEMY'S PHASE GOES HERE
        for i in range(len(enemies)-1,-1,-1):
            en = enemies[i]
            screen.blit(self.filler,(0,0)) #fills the screen
            for evnt in event.get():
                if evnt.type == QUIT:
                    running = False
                    return 0
            #DRAWS PEOPLE
            self.drawPeople()
            display.flip()
            time.wait(500)
            encoords = [(e.x,e.y) for e in enemies] #enemies' coordinates
            acoords = [(a.x,a.y) for a in allies] #allies' coordinates
            enMoves = getMoves(en,en.x,en.y,en.move,chapterMaps[chapter],encoords,acoords,{}) #enemy's moveableSquares
            enMoves = [(x,y) for x,y,m in enMoves]
            action = getEnemyAction(en,chapterMaps[chapter],allies,enMoves)
            if action == "attack":
                attackableSquares = getAttackableSquaresByMoving(enMoves,en) #attackableSquares by moving
                attackableAllies = [a for a in allies if (a.x,a.y) in attackableSquares]
                bestAlly,bestX,bestY = getOptimalAlly(en,chapterMaps[chapter],attackableAllies,enMoves)
                en.x,en.y = bestX,bestY
                screen.blit(self.filler,(0,0)) #fills the screen
                #DRAWS PEOPLE
                self.drawPeople()
                display.flip()
                time.wait(500)
                attack(en,bestAlly)
                if yoyo.hp == 0 or player.hp == 0:
                    return 0 #if yoyo or the player dies we leave the function, bounces to gameOver
            elif action == "move":
                pass
            self.turn += 1 #increases turn by 1
            self.moved.add(en)
            self.attacked.add(en)
            display.flip()
            fpsLimiter.tick(60)
        self.moved.clear()
        self.attacked.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        self.startTurn() #starts the turn      
    def gameOver(self):
        "draws game over screen"
        for i in range(50):
            screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fading effect
            display.flip()
            time.wait(50)
        screen.blit(papyrus.render("GAME OVER",True,RED),(500,300))
        display.flip()
        changemode(StartMenu)
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
                #HANDLES ARROW KEYS
                #----MOVE MODE
                if self.mode in ["freemove","move"]:
                    #freemove moves freely; move picks a location
                    self.moveSelect() #handles movements by player
                    self.clickedFrame = self.framecounter #sets the clickedFrame to self
                #----MENU MODE
                if self.mode in ["optionmenu","itemattack","item","mainmenu"]:                    
                    #moves selected menu item
                    self.menu.moveSelect()

                #----ATTACK MODE
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
                #----TRADE/HEAL MODE
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
                        self.menu.selected[0] = 1
                    elif kp[K_LEFT]:
                        self.menu.selected[0] = 0
                    #vertical movement within the item menu
                    selectedAllies = [self.selected,self.selected2] #the selected allies
                    self.menu.selected[1] = self.menu.moveSelect(self.menu.selected[1],5)
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
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,chapterMaps[chapter],acoords,encoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in acoords]
                                elif p in enemies:
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,chapterMaps[chapter],encoords,acoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we constantly fill moveable and attackable squares
                        else:
                            #if the user presses a blank spot, we set the mode to main menu
                            self.mode = "mainmenu"
                            self.menu.items = ["End"] #menu has End turn
                            self.menu.selected = 0

                            
                    #MOVE MODE
                    elif self.mode == "move":
                        #moves the unit if it is an ally and within the moveable squares
                        if (self.selectx,self.selecty) in [(x,y) for x,y,m in self.moveableSquares]+[(self.selected.x,self.selected.y)] and self.selected in allies:
                            self.selected.x,self.selected.y = self.selectx,self.selecty
                            self.mode = "optionmenu"
                            self.menu.items = []
                            self.menu.selected = 0
                            #----Menu Creation
                            #ATTACK OPTION
                            if not (self.selected in self.attacked or self.selected.equip == None):
                                for w in [i for i in self.selected.items if type(i) == Weapon]:
                                    #checks every weapon if one yields in an attack we equip it and add attack
                                    if not self.selected.canEquip(w):
                                        continue
                                    if len(getAttackableEnemies(self.selected,enemies,weapon=w)) > 0:
                                        self.selected.equipWeapon(w)
                                        self.menu.items.append("attack")
                                        break
                            #ITEM OPTION
                            if len(self.selected.items) > 0:
                                self.menu.items.append("item")
                            #TRADE OPTION
                            if len(getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)) > 0:
                                self.menu.items.append("trade") #we can only trade if we have targetable allies within range 1
                            #WAIT OPTION
                            self.menu.items.append("wait") #a person can always wait
                    #MAIN MENU CLICK

                            
                    elif self.mode == "mainmenu":
                        #allows user to select options
                        if self.menu.items[self.menu.selected] == "end":
                            self.mode = "enemyphase"
                            self.endTurn() #ends turn
                    #OPTION MENU CLICK
                    elif self.mode == "optionmenu":
                        #allows user to select options
                        if self.menu.items[self.menu.selected] == "attack":
                            self.mode = "itemattack"
                            self.menu.selected = 0
                        elif self.menu.items[self.menu.selected] == "item":
                            self.mode = "item"
                            self.menu.selected = 0
                        elif self.menu.items[self.menu.selected] == "trade":
                            self.mode = "trade"
                            self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                            self.menu.selected = [0,0] #menuselect becomes a list, first element is the selected person, second is the selected item
                        elif self.menu.items[self.menu.selected] == "wait":
                            self.mode = "freemove"
                            self.moved.add(self.selected)
                            self.attacked.add(self.selected)
                    #ATTACK CLICKS
                    elif self.mode == "itemattack":
                        if self.menu.selected < len(self.selected.items):
                            if type(self.selected.items[self.menu.selected]) == Weapon:
                                if self.selected.canEquip(self.selected.items[self.menu.selected]) and getAttackableEnemies(self.selected,enemies,weapon=self.selected.items[self.menu.selected]):
                                    self.mode = "attack"
                                    self.selected.equipWeapon(self.selected.items[self.menu.selected])
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
                            self.selectedItem = self.selected.items[self.menu.selected]
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
                                if "attack" in self.menu.items:
                                    self.menu.items.remove("attack")
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
                                self.menu.selected = 0
                            self.selectedItem = None #resets selectedItem
                        if len(self.selected.items) == 0:
                            #if we have no items left, we go back to option menu and remove items from the list
                            self.menu.items.remove("item")
                            self.mode = "optionmenu"
                            self.menu.selected = 0
                    #TRADE MODE CLICK
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            #if there is self.selected2, we set one
                            self.selected2 = self.targetableAllies[self.selectedAlly]
                        else:
                            #otherwise we select an item
                            if self.selectedItem == None:
                                #if we have no selectedItem we set one
                                self.selectedItem = self.menu.selected[:]
                            else:
                                #if we have a selected item, we commence the trade
                                selectedAllies = [self.selected,self.selected2] #selected allies
                                selectedItem1 = selectedItem2 = None #the default selected Item is None
                                if self.selectedItem[1] < len(selectedAllies[self.selectedItem[0]].items):
                                    #1st item is in range and is not None, then we give it to the other selected ally
                                    selectedItem1 = selectedAllies[self.selectedItem[0]].items[self.selectedItem[1]] #first selected item
                                if self.menu.selected[1] < len(selectedAllies[self.menu.selected[0]].items):
                                    #2nd item is in range and is not None, then we give it to the other selected ally
                                    selectedItem2 = selectedAllies[self.menu.selected[0]].items[self.menu.selected[1]] #second selected item
                                if selectedItem1 != None:
                                    selectedAllies[self.selectedItem[0]].removeItem(selectedItem1) #removes first item
                                    selectedAllies[self.menu.selected[0]].addItem(selectedItem1) #appends 1st item to second ally
                                if selectedItem2 != None:
                                    selectedAllies[self.menu.selected[0]].removeItem(selectedItem2) #removes second item
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
                        self.menu.selected = 0
                    elif self.mode == "item":
                        if self.selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
                            self.mode = "item"
                            self.selectedItem = None
                        else:
                            self.mode = "optionmenu"
                            self.menu.selected = 0
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            self.mode = "optionmenu"
                            self.menu.selected = 0
                        else:
                            if self.selectedItem == None:
                                self.selected2 = None #if there exists selected2, that means the trade interface is open, so we close that
                            else:
                                #however if there is a selected item, we instead deselect it
                                self.selectedItem = None
                    elif self.mode == "attack":
                        self.menu.selected = 0
                        self.mode = "itemattack"
                if e.unicode == "v":
                    #skips battle for now
                    self.gameVictory()
        if self.stopped:
            return 0 #ends the function if we stopped
        #-----END OF EVENT LOOP----#

        if len(self.moved) == len(self.attacked) == len(allies) and self.mode != "enemyphase":
            #if all allies have moved and attacked, we end the turn by default
            self.mode = "enemyphase"
            self.endTurn() #ends turn
        if len(enemies) == 0:
            #no more enemies means the player won
            self.mode = "gameVictory"
            self.gameVictory()
        if self.mode in ["gameVictory","gameover"]:
            return 0#we quit the function if it is gameVictory or game over
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
        #DRAWS PEOPLE
        self.drawPeople()
        #MAIN MENU MODE DISPLAY
        if self.mode == "mainmenu":
            #if it is menu mode we draw the menu
            self.menu.x,self.menu.y = 18,4
            self.menu.width,self.menu.height = 120,480
            self.menu.draw()
 #          drawMenu(self.menu,menux,menuy,120,480,self.menu.selected) #draws the main menu
        #OPTION MENU MODE DISPLAY
        if self.mode == "optionmenu":
            self.menu.x,self.menu.y = 36,2
            if self.selected.x >= 20:
                self.menu.x = 0
            self.menu.draw()
#            drawMenu(self.menu,menux,menuy,120,len(self.menu.items)*30,self.menu.selected)
        #ATTACK MODE DISPLAY
        if self.mode == "itemattack":
            #displays item selection menu for attack
            drawItemMenu(self.selected,self.selected.x+1,self.selected.y,self.menu.selected)
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
            battleStatsMenu = getBattleStats(self.selected,enemy,chapterMaps[chapter])
            drawMenu(battleStatsMenu,x,y,210,210,-20) #draws battle stats menu for ally

            #battle stats from enemy's POV
            battleStatsMenu = getBattleStats(enemy,self.selected,chapterMaps[chapter])
            drawMenu(battleStatsMenu,x+7,y,210,210,-20,RED) #draws battle stats menu for enemy
        #ITEM MODE DISPLAY
        if self.mode == "item":
            screen.blit(transBlack,(0,0))
            drawItemMenu(self.selected,14,8,self.menu.selected)
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
                draw.rect(screen,WHITE,(highlightedAlly.x*30,highlightedAlly.y*30,30,30),1) #draws selector around highlighted ally
            else:
                screen.fill(GREEN) #fills the screen with green
                #draws item menu for both allies
                #first we set which item selected out of the two menus
                #this is based on which ally the selector is on
                #which is determined by the first element of menuselect
                menuselect1 = -20 if self.menu.selected[0] else self.menu.selected[1]
                menuselect2 = -20 if not self.menu.selected[0] else self.menu.selected[1]
                                                                                
                drawItemMenu(self.selected,8,9,menuselect1)
                drawItemMenu(self.selected2,24,9,menuselect2)
                if self.selectedItem != None:
                    #if the selected Item isn't none, we draw the cursor
                    draw.rect(screen,WHITE,((8+self.selectedItem[0]*16)*30,(9+self.selectedItem[1])*30,240,30),1)
        #INFO MODE DISPLAY
        #displays character info screen
        if self.mode == "info":
            screen.fill(RED)
            draw.rect(screen,BLUE,(600,0,600,360)) #blits background for stats
        #---------------INFO DISPLAY BOXES----------------------#
        #TERRAIN DATA BOX
        if self.mode == "freemove":
            tbx,tby = 1020,630 #terrain box x and y
            stage = chapterMaps[chapter]
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
        fpsLimiter.tick(60) #limits FPS to 60
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
