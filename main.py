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
superScript40 = font.Font("fonts/SUPERSCR.TTF",40)
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
#animations are stored (except for stand) in tuples: (list_of_surfaces_for_each_frame_of_the_animation,frame_enemy/ally_is_hit)
playerMageAnimaSprite = ([image.load("images/Player/Mage/MageAttackFrame"+str(i+1)+".png")
                          for i in range(16)],10)
playerMageStandSprite = playerMageAnimaSprite[0][0]
playerMageAnimacritSprite = ([image.load("images/Player/Mage/MageCritFrame"+str(i+1)+".png")
                        for i in range(12)] + playerMageAnimaSprite[0][1:],21)
playerKnightLanceSprite = ([image.load("images/Player/Knight/KnightAttackFrame"+str(i+1)+".png")
                            for i in range(11)],5)
playerKnightStandSprite = playerKnightLanceSprite[0][0]
playerKnightLancecritSprite = ([image.load("images/Player/Knight/KnightCritFrame"+str(i+1)+".png")
                                for i in range(8)] + playerKnightLanceSprite[0],13)


yoyoSwordSprite = ([image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)],5)
yoyoStandSprite = yoyoSwordSprite[0][0]
yoyoSwordcritSprite = ([image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)],29)

#change albert's later
albertStandSprite = playerMageStandSprite
albertAnimacritSprite = playerMageAnimacritSprite
albertAnimaSprite = playerMageAnimaSprite

frannyLanceSprite = ([image.load("images/Franny/FrannyAttackFrame"+str(i+1)+".png")
                      for i in range(10)],5)
frannyStandSprite = frannyLanceSprite[0][0]
frannyLancecritSprite = (frannyLanceSprite[0][:2] + [image.load("images/Franny/FrannyCritFrame"+str(i+1)+".png")
                                                  for i in range(11)] + frannyLanceSprite[0][2:],16)
frannySwordSprite = ([image.load("images/Franny/FrannySwordFrame"+str(i+1)+".png")
                      for i in range(11)],4)
frannySwordcritSprite = ([frannySwordSprite[0][0]] + [image.load("images/Franny/FrannySwordcritFrame"+str(i+1)+".png")
                                                    for i in range(16)] + frannySwordSprite[0][1:],20)
garyAxeSprite = ([image.load("images/Gary/GaryAttackFrame"+str(i+1)+".png")
                  for i in range(18)],10)
garyStandSprite = garyAxeSprite[0][0]
garyAxecritSprite = ([garyStandSprite] + [image.load("images/Gary/GaryCritFrame"+str(i+1)+".png")
                                          for i in range(12)] + garyAxeSprite[0][7:],16)
#ENEMIES' ANIMATIONS
brigandAxeSprite = ([image.load("images/Brigand/BrigandAttackFrame"+str(i+1)+".png")
                       for i in range(14)],9)
brigandStandSprite = brigandAxeSprite[0][0]
brigandAxecritSprite = ([image.load("images/Brigand/BrigandCritFrame"+str(i+1)+".png")
                     for i in range(2)] + brigandAxeSprite[0],11)
mercenarySwordSprite = ([image.load("images/Mercenary/MercenaryAttackFrame"+str(i+1)+".png")
                         for i in range(21)],12)
mercenaryStandSprite = mercenarySwordSprite[0][0]
mercenarySwordcritSprite = ([mercenaryStandSprite]+[image.load("images/Mercenary/MercenaryCritFrame"+str(i+1)+".png")
                                                     for i in range(18)] + mercenarySwordSprite[0][6:],25)
#MAGIC ANIMATIONS
fireSprite = [image.load("images/Magic/Fire/Fire"+str(i+1)+".png").convert_alpha()
              for i in range(17)]

#MAP SPRITES
allyMapSprites = {"Mage":[transform.scale(image.load("images/MapSprites/Ally/Mage"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Lord":[transform.scale(image.load("images/MapSprites/Ally/Lord"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Knight":[transform.scale(image.load("images/MapSprites/Ally/Knight"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Cavalier":[transform.scale(image.load("images/MapSprites/Ally/Cavalier"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Fighter":[transform.scale(image.load("images/MapSprites/Ally/Fighter"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)]}
enemyMapSprites = {"Brigand":[transform.scale(image.load("images/MapSprites/Enemy/Brigand"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                   "Mercenary":[transform.scale(image.load("images/MapSprites/Enemy/Mercenary"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)]}
allyGreyMapSprites = {}
for i,k in enumerate(allyMapSprites):
    allyGreyMapSprites[k] = [greyScale(img) for img in allyMapSprites[k]]
enemyGreyMapSprites = {}
for i,k in enumerate(enemyMapSprites):
    enemyGreyMapSprites[k] = [greyScale(img) for img in enemyMapSprites[k]]
faces = {"Yoyo":image.load("images/faces/Yoyo.png"),
        "Player":image.load("images/faces/player.png"),
        "Franny":image.load("images/faces/Franny.png"),
        "Albert":image.load("images/faces/Albert.png"),
        "Gary":image.load("images/faces/Gary.png"),
        "Henning":image.load("images/faces/Henning.png"),
        "Bandit":image.load("images/faces/Bandit.png"),
        "Mercenary":image.load("images/faces/Bandit.png")} #dictionary of all faces of characters
#ARROW SPRITES
arrowHead = image.load("images/Arrow/arrowHead.png")
arrowBent = image.load("images/Arrow/arrowBent.png")
arrowStraight = image.load("images/Arrow/arrowStraight.png")

#TERRAIN IMAGES
peakImg = image.load("images/terrain/peak.png")

#BACKGROUND IMAGES
plainsBackground = image.load("images/Maps/prologue.png")
#battle background
battlePlains = image.load("images/backgrounds/battlePlains.png")

#UI Backgrounds
menuBG = image.load("images/backgrounds/menuBackground.png")
statsBG = image.load('images/backgrounds/statsMenu.png')
#----END OF IMAGE LOAD----#
#TERRAIN
plain = Terrain("Plain",0,0,1)
peak = Terrain("Peak",4,40,4,peakImg)
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
              {'stand':playerMageStandSprite,'Anima':playerMageAnimaSprite,'Animacrit':playerMageAnimacritSprite},faces["Albert"])#test person for chapter 1
franny = Cavalier("Franny",0,0,
                  {"lv":3,"stren":7,"defen":5,"skl":9,"lck":4,
                   "spd":8,"con":10,"move":7,"res":1,"hp":24,"maxhp":24},
                  {"stren":35,"defen":25,"skl":50,"spd":55,"lck":45,"res":15,"maxhp":70},
                  [iron_lance.getInstance(),iron_sword.getInstance(),vulnerary.getInstance()],{'Lance':200,'Sword':200},
                  {'stand':frannyStandSprite,'Lance':frannyLanceSprite,'Lancecrit':frannyLancecritSprite,
                   'Sword':frannySwordSprite,'Swordcrit':frannySwordcritSprite},faces["Franny"])
gary = Fighter("Gary",0,0,
               {"lv":3,"stren":9,"defen":5,"skl":6,"lck":4,
                "spd":5,"con":13,"move":5,"res":0,"hp":32,"maxhp":32},
               {"stren":55,"defen":40,"skl":40,"spd":30,"lck":45,"res":10,"maxhp":85},
               [iron_axe.getInstance(),vulnerary.getInstance()],{"Axe":200},
               {"stand":garyStandSprite,"Axe":garyAxeSprite,"Axecrit":garyAxecritSprite},faces["Gary"])

allies = [] #allies
#ENEMIES
#--Brigands
bandit0 = Brigand("Bandit",0,0,
                  {"lv":1,"stren":6,"defen":3,"skl":3,"lck":0,
                   "spd":3,"con":8,"move":5,"res":0,"hp":20,"maxhp":20},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
bandit1 = Brigand("Bandit",0,0,
                  {"lv":3,"stren":8,"defen":4,"skl":4,"lck":1,
                   "spd":4,"con":9,"move":5,"res":0,"hp":24,"maxhp":24},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
alexTheBandit = Brigand("Alex the Bandit",0,0,
                        {"lv":3,"stren":8,"defen":4,"skl":4,"lck":3,
                         "spd":4,"con":10,"move":5,"res":0,"hp":24,"maxhp":24},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],70)
#--Mercenaries
merc1 = Mercenary("Mercenary",0,0,
                {"lv":3,"stren":6,"defen":3,"skl":8,"lck":2,
                "spd":8,"con":6,"move":5,"res":0,"hp":18,"maxhp":18},{},[iron_sword.getInstance()],{"Sword":200},
                {"Sword":mercenarySwordSprite,"Swordcrit":mercenarySwordcritSprite,"stand":mercenaryStandSprite},faces["Bandit"],20)
enemies = []
#----CHAPTERS----#
#MAPS
def createMap(width,height,terrains=[]):
    "creates a map (2d list)"
    newMap = [[plain for i in range(width)] for j in range(height)]
    for t,coords in terrains:
        for x,y in coords:
            newMap[y][x] = t
    return newMap
def drawMap(maptodraw):
    for y in range(len(maptodraw)):
        for x in range(len(maptodraw[y])):
            if maptodraw[y][x].img != None:
                screen.blit(maptodraw[y][x].img,(x*30,y*30))
chapter0 = createMap(40,24)
chapter1 = createMap(40,24,[(peak,[(7,10),(10,7),(11,11),(8,10),(7,11),(8,11),(9,11),(10,11),(9,10),(10,10),(11,10),(10,9),(10,8)])])
chapterMaps = [chapter0,chapter1]
#CHAPTER DATA
#Stored in tuples
#(gainedAllies,allyCoordinates,Enemies,Goal,BackgroundImage)
#chapter data, chapter is determined by index
chapterData = [([yoyo],[(0,1),(0,0)],createEnemyList([bandit0,alexTheBandit],[3,1],[(3,3),(3,1),(4,2),(8,9)]),
                "Defeat all enemies",plainsBackground),
               ([albert,franny,gary],[(0,1),(0,0),(1,1),(1,0),(2,0)],createEnemyList([bandit1,merc1],[3,2],[(7,7),(7,6),(8,3),(7,8),(8,7)]),
                "Defeat all enemies",plainsBackground)]
chapterBattleBackgrounds = [battlePlains,battlePlains]
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
    global chapter,allAllies,player
    if "chapter" not in file:
        file.close()
        changemode(NewGame())#goes to new game
    else:
        #sets the chapter we are about to start and allAllies
        chapter = file["chapter"]
        allAllies = file["allAllies"]
        for a in allAllies:
            imagifyStrings(a) #imagify all images as they were strings while data of allies
            if a.name.lower() not in usedNames:
                player = a
        file.close()
        changemode(getStory(chapter))
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
    changemode(getStory(chapter))
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
    draw.rect(screen,BLUE,(x*30,y*30,240,150)) #########CANCEEEEEEEEERRRRRRRRRR
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
    screen.blit(chapterBattleBackgrounds[chapter],(0,0))
    display.flip()
    time.wait(200)
    drawBattleInfo(screen,ally,enemy,chapterMaps[chapter])
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for ally and enemy
    if ally.equip == None:
        screen.blit(ally.anims["stand"],(0,0))
    else:
        screen.blit(ally.anims[ally.equip.typ][0][0],(0,0))
    if enemy.equip == None:
        screen.blit(enemy.anims["stand"],(0,0))
    else:
        screen.blit(enemy.anims[enemy.equip.typ][0][0],(0,0))
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
    #resets the faces
    if ally.name.lower() not in usedNames:
        #if it's the player we set to player face
        ally.face = faces["Player"]
    else:
        ally.face = faces[ally.name]
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
        self.subMenu = None #allows for menus inside menus
    def moveSelect(self):
        "moves menu selector and returns new value"
        #moves self.selected up and down
        if self.subMenu != None:
            #this is menu object that scrolls through there.
            self.subMenu.moveSelect()
        else:
            kp = key.get_pressed()
            if kp[K_UP]:
                self.selected -= 1
            elif kp[K_DOWN]:
                self.selected += 1
            #wrapping around selected
            if self.selected < 0:
                self.selected = len(self.items) - 1
            elif self.selected >= len(self.items):
                self.selected = 0
    def makeBackground(self):
        "transforms the background based on how many items are in it"
        #WIP
        pass
    def draw(self,person=None):
        "draws a list of strings as a vertical menu at positions x and y"
        draw.rect(screen,BLUE,(self.x*30,self.y*30,self.width,self.height))
        screen.blit(self.background,(self.x*30,self.y*30)) #blits the background
        for i in range(len(self.items)):
            opt = self.items[i] #option to draw
            if type(opt) == str:
                screen.blit(sans.render(opt.title(),True,WHITE),(self.x*30,(self.y+i)*30))
            elif type(opt) == Item or issubclass(type(opt),Item):
                #draws the item
                col = GREY if not person.canEquip(opt) and type(opt) == Weapon else WHITE #color is Grey if it's a weapon user cannot equip - else it's white
                screen.blit(sans.render(opt.name,True,col),(self.x*30,(self.y+i)*30))
                screen.blit(sans.render(str(opt.dur)+"/"+str(opt.maxdur),True,col),((self.x+6)*30,(self.y+i)*30)) #blits durability
        draw.rect(screen,WHITE,(self.x*30,(self.y+self.selected)*30,self.width,30),1) #draws a border around the selected option
        if self.subMenu != None:
            self.subMenu.draw(person)#draws the subMenu
    def getOption(self):
        "returns the option that is selected"
        if self.subMenu == None:
            return self.items[self.selected]
        else:
            #if we have a sub menu we instead get the option from that
            return self.subMenu.getOption()
        
class TradeMenu(Menu):
    "Trade Menu class - allows for trade"
    def __init__(self, x=0,y=0,width=0,height=0,background=Surface((1,1)),selected=0,items=[]):
        "initialize trade menu"
        super().__init__(x,y,width,height,background,selected,items)
        self.selectedPerson = 0 #selected person
        self.firstSelection = None #first selection - player makes two to perform a trade
    def moveSelect(self):
        "moves the selected option in the menu"
        if self.subMenu != None:
            #this is menu object that scrolls through there.
            self.subMenu.moveSelect()
        kp = key.get_pressed()
        if kp[K_UP]:
            self.selected -= 1
        elif kp[K_DOWN]:
            self.selected += 1
        #wrapping around if exceeding length of item list in selectedPerson or if less than 0
        if self.selected < 0:
            self.selected = len(self.items[self.selectedPerson]) - 1
        elif self.selected >= len(self.items[self.selectedPerson]):
            self.selected = 0
        if kp[K_LEFT]:
            self.selectedPerson -= 1
        elif kp[K_RIGHT]:
            self.selectedPerson += 1
        self.selectedPerson = min(max(self.selectedPerson,0),1) #limits selectedPerson between two people
    def getOption(self):
        "gets the option that is selected"
        if self.subMenu == None:
            return (self.selectedPerson,self.selected) #returns position of item
        else:
            #returns submenu's option if we have one
            return self.subMenu.getOption()
    def onClick(self):
        "handles clicks within the trade menu - returns the items to be switched in a list of tuples (person,item)"
        if self.firstSelection == None:
            #if there is no first selection we select one
            self.firstSelection = (self.selectedPerson,self.selected)
            return False #no need to do anything if we're just setting the first option
        else:
            #returns the list of tuples
            return [self.firstSelection,self.getOption()]
    def draw(self,person=None,person2=None):
        "draws the trade menu"
        draw.rect(screen,BLUE,(self.x*30,self.y*30,self.width,self.height))
        draw.rect(screen,BLUE,((self.x+1)*30+self.width,self.y*30,self.width,self.height)) #draws two rectangles
        screen.blit(self.background,(self.x*30,self.y*30)) #blits the background
        screen.blit(self.background,((self.x+1)*30+self.width,self.y*30))
        people = [person,person2] #list of people
        for p in range(len(self.items)):
            #loops through persons
            for i in range(len(self.items[p])):
                #loops through items of each person
                opt = self.items[p][i] #selected item
                if opt == None:
                    continue #we don't draw blanks
                #draws the item
                col = GREY if not people[p].canEquip(opt) and type(opt) == Weapon else WHITE #color is Grey if it's a weapon user cannot equip - else it's white
                screen.blit(sans.render(opt.name,True,col),(self.x*30+p*(self.width+30),(self.y+i)*30))
                screen.blit(sans.render(str(opt.dur)+"/"+str(opt.maxdur),True,col),((self.x+6)*30+p*(self.width+30),(self.y+i)*30)) #blits durability
        if self.firstSelection != None:
            draw.rect(screen,WHITE,(self.x*30+self.firstSelection[0]*(self.width+30),(self.y+self.firstSelection[1])*30,self.width,30),1) #draws a border around the first option
        draw.rect(screen,WHITE,(self.x*30+self.selectedPerson*(self.width+30),(self.y+self.selected)*30,self.width,30),1) #draws border around selected option

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
    fileName = "chapters/chapter"+str(chapter)
    fileName = fileName + "end" if end else fileName #adds end to the file name if it's the end
    fileName += ".txt"
    storyFile = open(fileName)
    story = storyFile.read().strip().replace("*Player*",player.name).split("\n") #story
    background = story[0].strip() #background image source
    story = story[1:] #actual story
    return Story(story,image.load(background),end=end)

class Story():
    "screen mode for user to see the story"
    def __init__(self,dialogue,background,music=None,end=False):
        "initialize the Story class contains all dialogue (which also includes which picture to put)"
        self.dialogue = dialogue
        self.background = background
        self.music=None
        self.currDial = 0 #current dialogue we are on
        self.limit = len(dialogue) #limit of the dialogue - once reached the story ends
        self.end = end #is it an ending story?
        self.cond = False
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
                    if e.key == K_z or e.key == K_x or e.key == K_RETURN:
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

        kp = key.get_pressed()
        
        if func == "CONDITION":
            if sentence == "*End*":
                self.cond = False
            else:
                alive,dead = sentence.split(";")
                alive = alive.lower().split(",")
                dead = dead.lower().split(",")
                names = [a.name.lower() for a in allAllies]
                if alive != ['']:
                    if len([n for n in alive if n in names]) == len(alive):
                        self.cond = False
                    else:
                        self.cond = True
                if dead != ['']:
                    if len([n for n in dead if n not in names]) == len(dead):
                        self.cond = False
                    else:
                        self.cond = True
            self.currDial += 1
        elif self.cond:
            #self.cond == True indicates we did not meet the condition, so we skip over
            self.currDial += 1
        else:
            if func == "":
                #displays narration
                if not writeDialogue(screen,sentence):
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
                    x = 900 #changes the x to other side of the screen if it's not an ally
                if func.lower() == player.name.lower():
                    img = faces["Player"] #player's face
                else:
                    img = faces[func] #anyone else's face
                if not writeDialogue(screen,sentence,x,530,func,img):
                    #writes dialogue
                    return 0 #if it returns false it means the user quit, so we quit as well
        breakLoop = False if func != "CONDITION" and not self.cond else True
        cM = False #boolean: change mode?
        while not breakLoop:
            #loops until user hits z or x to move on
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    breakLoop = True
                if e.type == KEYDOWN:
                    if e.key == K_z:
                        self.currDial += 1
                        breakLoop = True
                    if e.key == K_RETURN or e.key == K_x:
                        #enter or x skips entirely
                        cM = True
                        breakLoop = True
                    
            display.flip()
            fpsLimiter.tick(60) #limits to 60 FPS
        if self.currDial >= self.limit or cM:
            if self.end:
                changemode(SaveGame()) #we change to savegame if it's the end
            else:
                #once we hit the limit we transition to the game mode
                changemode(Game())
        
class Game():
    def __init__(self):
        "initializes game"
        self.selectx,self.selecty = 0,0 #select cursor starting point
        self.framecounter = 0
        self.clickedFrame = 0 #the frame user clicked (pressed z)
        self.mode = "freemove" #mode Game is in
        self.menu = Menu(0,0,0,0,FilledSurface((1,1),BLUE),0,[]) #menu for optionmenu mode
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
    def getPath(self):
        "Gets path"
        coords = [(x,y) for x,y,m,ali in self.moveableSquares]
        spot = -1
        for i in range(len(coords)):
            if coords[i] == (self.selectx,self.selecty):
                spot = i
        if spot == -1:
            return [(self.selected.x,self.selected.y)] #return the spot the character is on
        steps = [ali for x,y,m,ali in self.moveableSquares][spot] #steps = the coords to get to the steps
        return steps
    def animWalk(self):
        "uses self.selected.x,y and self.selectx,y"
        #WIP!!!
 #       draw.rect(screen,GREEN,(self.selected.x*30,self.selected.y*30,30,30)) #coverup to cover the character when animated
        snap = screen.copy()
        for cord in self.getPath():
            screen.blit(snap,(0,0))
            draw.rect(screen,BLACK,(cord[0]*30,cord[1]*30,30,30))##need sprite?
            display.flip()
            time.wait(100)
            event.pump() #pumps events so we don't lock down
        event.clear()
    def getArrow(self,coord,coord1,coord2,head=False):
        "takes in two coordinates and returns an image that represents the proper arrowpiece"
        dx1 = coord[0] - coord1[0] #change in x and y for the first coordinate
        dy1 = coord[1] - coord1[1]
        if head:
            #returns proper arrow head
            if dx1 == 0:
                #vertical arrowhead
                if dy1 == -1:
                    #from downwards
                    return transform.rotate(arrowHead,90)
                else:
                    #from upwards
                    return transform.rotate(arrowHead,-90)
            else:
                #horizontal arrowhead
                if dx1 == -1:
                    #from right
                    return transform.flip(arrowHead,1,0)
                else:
                    #from left
                    return arrowHead
                    
        dx2 = coord[0] - coord2[0] #change in x and y for second coordinate
        dy2 = coord[1] - coord2[1]
        if abs(dx1 - dx2) == 1:
            #handles bent arrowpieces
            if (dx1,dy2) == (-1,1) or (dx2,dy1) == (-1,1):
                #top-right
                return transform.flip(arrowBent,1,1)
            elif (dx1,dy2) == (-1,-1) or (dx2,dy1) == (-1,-1):
                #bottom-right
                return transform.flip(arrowBent,1,0)
            elif (dx1,dy2) == (1,-1) or (dx2,dy1) == (1,-1):
                #bottom-left
                return arrowBent
            else:
                #top-left
                return transform.flip(arrowBent,0,1)
        else:
            #handles straight arrowpieces
            if abs(dx1 - dx2) == 2:
                #horizontal
                return arrowStraight
            else:
                #vertical
                return transform.rotate(arrowStraight,90)
        return 1
    def drawArrow(self):
        "draws an arrow from self.selected.x,y  to self.selectx,y"
        #WIP - find smart way to figure out which one to draw using indices of 2x2 array
        steps = [(self.selected.x,self.selected.y)]+self.getPath()

        #steps includes the self character x&y
        
        #loop through each, check the next one and previous one to see which one of the three to draw
        for i in range (1,len(steps)-1):
            coord1 = steps[i-1] #previous coord
            coord = steps[i] #current coord
            coord2 = steps[i+1] #subsequent coord
            screen.blit(self.getArrow(coord,coord1,coord2),(coord[0]*30,coord[1]*30)) #blits proper arrow piece
        if len(steps) > 1:
            screen.blit(self.getArrow(steps[-1],steps[-2],steps[0],True),(steps[-1][0]*30,steps[-1][1]*30)) #Blits arrowhead
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
        changemode(getStory(chapter,True))
    def drawPeople(self,alliesToDraw=False,enemiesToDraw=False):
        "draws all people on the map"
        alliesToDraw = allies if not alliesToDraw else alliesToDraw
        enemiesToDraw = enemies if not enemiesToDraw else enemiesToDraw
        for a in alliesToDraw:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            if a not in self.attacked or a not in self.moved:
                screen.blit(allyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
            else:
                #if the ally has moved already we draw it grey
                screen.blit(allyGreyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
        for e in enemiesToDraw:
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
        drawMap(chapterMaps[chapter])#draws all terrain
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
        #ENEMY'S PHASE GOES HERE, AI use
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
            enemyMoves = getMoves(en,en.x,en.y,en.move,chapterMaps[chapter],encoords,acoords,{})+[(en.x,en.y,en.move,[(en.x,en.y)])] #enemy's moveableSquares

            enMoves = [(x,y) for x,y,m,ali in enemyMoves]
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
 #               (bestX,bestY) = getOptimalSquare(en,chapterMaps[chapter],allies,enemyMoves)
#                en.x,en.y = bestX,bestY
                pass
            self.turn += 1 #increases turn by 1
            self.moved.add(en)
            self.attacked.add(en)
            display.flip()
            fpsLimiter.tick(60)
        self.moved.clear()
        self.attacked.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        event.clear()
        self.startTurn() #starts the turn      
    def gameOver(self):
        "draws game over screen"
        for i in range(50):
            screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fading effect
            display.flip()
            time.wait(50)
        screen.blit(papyrus.render("GAME OVER",True,RED),(500,300))
        display.flip()
        self.mode = "gameOver"
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

    def createOptionMenu(self):
        "sets a menu's items to an option menu for selected person"
        self.menu = Menu(32,2,270,30,FilledSurface((1,1),BLUE),0,[]) #menu for optionmenu mode
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
    def run(self,screen):
        "runs the game in the running loop"
        global running,chapter
        #----EVENT LOOP----#
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if self.mode == "gameOver":
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
                    #if we have a selected2 we move the item selector inste
                    self.menu.moveSelect()
                #---------Z--------#
                if e.key == K_z:
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
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],p)
                                    if self.attackableSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m,ali in self.moveableSquares] and sq not in acoords]
                                elif p in enemies:
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,chapterMaps[chapter],encoords,acoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],p)
                                    if self.attackableSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m,ali in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we constantly fill moveable and attackable squares
                        else:
                            #if the user presses a blank spot, we set the mode to main menu
                            self.mode = "mainmenu"
                            self.menu.items = ["End"] #menu has End turn
                            self.menu.selected = 0
                            
                    #MOVE MODE
                    elif self.mode == "move":
                        #moves the unit if it is an ally and within the moveable squares or it's own square
                        if (self.selectx,self.selecty) in [(x,y) for x,y,m,ali in self.moveableSquares] and self.selected in allies:
                            self.animWalk()
                            self.selected.x,self.selected.y = self.selectx,self.selecty
                            self.mode = "optionmenu"
                            self.createOptionMenu() #creates the option menu and sets the menu to it
                    #MAIN MENU CLICK
                    elif self.mode == "mainmenu":
                        #allows user to select options
                        if self.menu.getOption().lower() == "end":
                            self.mode = "enemyphase"
                            self.endTurn() #ends turn
                    #OPTION MENU CLICK
                    elif self.mode == "optionmenu":
                        #allows user to select options
                        if self.menu.getOption().lower() == "attack":
                            self.mode = "itemattack"
                            self.menu.selected = 0
                            self.menu.items = [i for i in self.selected.items if type(i) == Weapon]
                        elif self.menu.getOption().lower() == "item":
                            self.mode = "item"
                            self.menu.selected = 0
                            self.menu.items = self.selected.items
                        elif self.menu.getOption().lower() == "trade":
                            self.mode = "trade"
                            self.selectedAlly = 0
                            self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                        elif self.menu.getOption().lower() == "wait":
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
                            self.selectedItem = self.menu.getOption()
                            firOp = "Equip" if type(self.selectedItem) == Weapon else "" #first option
                            firOp = "Use" if type(self.selectedItem) == Consumable else firOp
                            self.menu.subMenu = Menu(24,8,120,60,items=[firOp,"Discard"])
                        else:
                            #if a weapon is selected, we check whether user equips or discards
                            optselected = self.menu.getOption()
                            if optselected.lower() == "use":
                                #use option
                                drawChangingBar(screen,self.selected.hp,self.selected.hp+self.selectedItem.hpGain,self.selected.maxhp,420,330,360,60,"Hp",False)
                                if not self.selectedItem.use(self.selected):
                                    #uses consumable
                                    #if it breaks we remove it
                                    self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                                self.moved.add(self.selected)
                                self.attacked.add(self.selected) #guy who used consumable can't move - treated like attack
                                self.mode = "freemove"
                            elif optselected.lower() == "equip":
                                #equip option
                                self.selected.equipWeapon(self.selectedItem) #tries to equip
                            elif optselected.lower() == "discard":
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            self.selectedItem = None #resets self.selectedItem
                            self.menu.subMenu = None
                            if self.selected.equip == None:
                                #if we have no equipped item we remove the attack option from menu
                                if "attack" in self.menu.items:
                                    self.menu.items.remove("attack")
                                #we also empty attackableSquares
                                self.attackableSquares = []
                        if len(self.selected.items) == 0:
                            #if we have no items left, we go back to option menu
                            self.mode = "optionmenu"
                            self.createOptionMenu() #creates the option menu and sets the menu to it
                    #TRADE MODE CLICK
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            #if there is no self.selected2, we set one and set a menu
                            self.selected2 = self.targetableAllies[self.selectedAlly]
                            firstItemList = self.selected.items + [None]*(5-len(self.selected.items)) #list of items with Nonetypes filling up to 5
                            secondItemList = self.selected2.items + [None]*(5-len(self.selected2.items))
                            self.menu = TradeMenu(8,9,360,150,items=[firstItemList,secondItemList]) #trade menu
                        else:
                            #otherwise we select an item
                            if self.menu.onClick():
                                #if the click returns a list of tuples, we perform the trade
                                selectedAllies = [self.selected,self.selected2] #selected allies
                                selectedItem1 = selectedItem2 = None #the default selected Item is None
                                firstSel,secSel = self.menu.onClick() #gets the two selections made by user
                                if firstSel[1] < len(selectedAllies[firstSel[0]].items):
                                    #1st item is in range and is not None, then we give it to the other selected ally
                                    selectedItem1 = selectedAllies[firstSel[0]].items[firstSel[1]] #first selected item
                                if secSel[1] < len(selectedAllies[secSel[0]].items):
                                    #2nd item is in range and is not None, then we give it to the other selected ally
                                    selectedItem2 = selectedAllies[secSel[0]].items[secSel[1]] #second selected item
                                if selectedItem1 != None:
                                    selectedAllies[firstSel[0]].removeItem(selectedItem1) #removes first item
                                    selectedAllies[secSel[0]].addItem(selectedItem1) #appends 1st item to second ally
                                if selectedItem2 != None:
                                    selectedAllies[secSel[0]].removeItem(selectedItem2) #removes second item
                                    selectedAllies[firstSel[0]].addItem(selectedItem2) #appends 2nd item to first ally
                                firstItemList = self.selected.items + [None]*(5-len(self.selected.items)) #list of items with Nonetypes filling up to 5
                                secondItemList = self.selected2.items + [None]*(5-len(self.selected2.items))
                                self.menu = TradeMenu(8,9,360,150,items=[firstItemList,secondItemList]) #trade menu
                                self.menu.firstSelection = None

                #------X------#
                if e.key == K_x:
                    #if the user pressed x
                    #handles backtracing
                    if self.mode == "move":
                        self.mode = "freemove"
                        self.selectx = self.selected.x
                        self.selecty = self.selected.y
                    elif self.mode == "mainmenu":
                        self.mode = "freemove"
                    elif self.mode == "optionmenu":
                        self.mode = "move"
                        self.selected.x,self.selected.y = self.oldx,self.oldy
                        if self.moveableSquares == []:
                            self.mode = "freemove" #we go back to freemove mode if we have no moveablesquares
                    elif self.mode == "itemattack":
                        self.mode = "optionmenu"
                        self.createOptionMenu() #creates the option menu and sets the menu to it
                    elif self.mode == "item":
                        if self.selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
                            self.mode = "item"
                            self.selectedItem = None
                            self.menu.subMenu = None
                        else:
                            self.mode = "optionmenu"
                            self.createOptionMenu() #creates the option menu and sets the menu to it
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            self.mode = "optionmenu"
                            self.createOptionMenu() #creates the option menu and sets the menu to it
                        else:
                            if self.selectedItem == None:
                                self.selected2 = None #if there exists selected2, that means the trade interface is open, so we close that
                            else:
                                #however if there is a selected item, we instead deselect it
                                self.selectedItem = None
                    elif self.mode == "attack":
                        self.menu.selected = 0
                        self.mode = "itemattack"
                    elif self.mode == "info":
                        self.mode = "freemove"
                        self.selected = None
                #------S------#
                if e.key == K_s:
                    #info mode on
                    if self.mode == "freemove":
                        for p in allies+enemies:
                            if self.selectx == p.x and self.selecty == p.y:
                                #highlighting an ally
                                self.selected = p
                                self.mode = "info" #sets to info mode
                                break
                #-------##temporary##-------#
                if e.key == K_v:
                    self.gameVictory()
                    return 0
        if self.stopped:
            return 0 #ends the function if we stopped
        #-----END OF EVENT LOOP----#
        if 0 in [player.hp,yoyo.hp] and self.mode != "gameOver":
            self.gameOver()
            return 0
        if self.mode in ["gameVictory","gameOver"]:
            display.flip()
            return 0#we quit the function if it is gameVictory or game over
        if len(self.moved) == len(self.attacked) == len(allies) and self.mode != "enemyphase":
            #if all allies have moved and attacked, we end the turn by default
            self.mode = "enemyphase"
            self.endTurn() #ends turn
        if len(enemies) == 0:
            #no more enemies means the player won
            self.mode = "gameVictory"
            self.gameVictory()
            return 0
        screen.blit(self.filler,(0,0)) #blits the filler
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if self.framecounter - self.clickedFrame > 20 and self.mode in ["freemove","move"] and not self.framecounter%5:
            #if we held for 20 frames or more we move more
            #we only do it once every 6 frames or it'll be too fast
            self.moveSelect()
        #---------------DIFFERENT MODE DISPLAYS------------------#
        #MOVE MODE DISPLAY
        if self.mode == "move":
            #fills moveable and attackable squares
            fillSquares(screen,set([(x,y) for x,y,m,ali in self.moveableSquares]),transBlue)
            if self.attackableSquares and self.selected.equip != None:
                fillSquares(screen,self.attackableSquares,transRed)
            if self.selected in allies:
                self.drawArrow()
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
            self.menu.x,self.menu.y = 32,2
            if self.selected.x >= 20:
                self.menu.x = 0
            self.menu.width=270
            self.menu.height=30*len(self.menu.items)
            self.menu.draw()
#            drawMenu(self.menu,menux,menuy,120,len(self.menu.items)*30,self.menu.selected)
        #ATTACK MODE DISPLAY
        if self.mode == "itemattack":
            #displays item selection menu for attack
            self.menu.draw(self.selected)
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
            self.menu.x,self.menu.y = 16,8
            self.menu.width = 240
            self.menu.height = 150
            self.menu.draw(self.selected)
        #TRADE MODE DISPLAY
        if self.mode == "trade":
            if self.selected2 == None:
                #if we have no 2nd selected ally, we draw the selector around the 2nd selected ally
                highlightedAlly = self.targetableAllies[self.selectedAlly] #highlighted ally
                draw.rect(screen,WHITE,(highlightedAlly.x*30,highlightedAlly.y*30,30,30),1) #draws selector around highlighted ally
            else:
                screen.blit(menuBG,(0,0)) #blits menu background
                #draws item menu for both allies
                #first we set which item selected out of the two menus
                #this is based on which ally the selector is on
                #which is determined by the first element of menuselect
                self.menu.draw(self.selected,self.selected2)
        #INFO MODE DISPLAY
        #displays character info screen
        if self.mode == "info":
            a = self.selected #selected ally
##            draw.rect(screen,BLUE,(600,100,600,520)) #blits background for stats
##            draw.rect(screen,BLUE,(610,20,580,60))
##            screen.blit(sans.render("PERSONAL DATA",True,WHITE),(610,30))
            screen.blit(statsBG,(0,0)) #blits stats background
            displayList = [[str(a.stren),str(a.move)],
                           [str(a.skl),str(a.con)],
                           [str(a.spd),""],
                           [str(a.lck),""],
                           [str(a.defen),""],
                           [str(a.res),""]]
            for i in range(len(displayList)):
                #blits all the things in displayList
                #all the items are lists representing a row
                cell1,cell2 = displayList[i] #cell1 and cell2 in the row
                screen.blit(superScript40.render(cell1,True,WHITE),(640,130+i*72))
                screen.blit(superScript40.render(cell2,True,WHITE),(980,130+i*72))
##            draw.rect(screen,(230,240,233),(30,30,540,520)) #background for face
            screen.blit(transform.scale(self.selected.face,(360,320)),(75,32))
            screen.blit(superScript40.render(a.name,True,BLACK),(144,381)) #blits name of the selected unit
##            screen.blit(transform.scale(transBlack,(570,150)),(0,560))
            screen.blit(superScript40.render(a.__class__.__name__,True,WHITE),(15,485))
            screen.blit(superScript40.render("LV "+str(a.lv)+" EXP "+str(a.exp),True,WHITE),(15,555))
            screen.blit(superScript40.render("HP "+str(a.hp)+"/"+str(a.maxhp),True,WHITE),(15,610))
        #--------------------HIGHLIGHTING A PERSON---------------#
        if self.mode == "freemove":
            for p in allies+enemies:
                if self.selectx == p.x and self.selecty == p.y:
                    #DRAWS PERSON MINI DATA BOX
                    pdbx,pdby = 0,0 #person data box x and y
                    if self.selectx < 20 and self.selecty <= 12:
                        pdby = 630
                    draw.rect(screen,BLUE,(pdbx,pdby,300,90)) #background box
                    screen.blit(sans.render(p.name,True,WHITE),(pdbx+15,pdby+3)) #person's name
                    screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,WHITE),(pdbx+15,pdby+33)) #health
                    draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                    draw.line(screen,YELLOW,(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                    break
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
