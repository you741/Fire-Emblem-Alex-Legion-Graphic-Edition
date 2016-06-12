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
__author__ = "Yttrium Z (You Zhou) & AZhan (Albert Zhan)"
__date__ = "Incomplete"
__purpose__ = "Game for Grade 11 final project"
__name__ = "Fire Emblem Alex Legion"
__copyright__ = "Yttrium Z 2015-2016"
#----SETUP----#
os.environ['SDL_VIDEO_WINDOW_POS'] = '25,25'
screen = display.set_mode((1200,720))
display.set_caption("YTTRIUM Z AND AZHAN PRESENTS ~~~~~~~FIRE EMBLEM ALEX LEGION~~~~~~~","Fire Emblem Alex Legion")


#loading screen
loadingScreen = image.load("images/loading_screen.png")

#sets the progress bar - blits the progress as the images are loading
def LS(prog):
    "displays loading screen based on prog"
    screen.blit(loadingScreen,(0,0))
    draw.rect(screen,(230,240,90),(219,532,prog,82))                
    if handleEvents(event.get()):
        quit()
    display.flip()
    
LS(1)
#----GLOBAL VARIABLES----#
#----COLORS----#
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
GREY = (160,160,160,255)
LS(55)
#----FONTS----#
timesnr = font.SysFont("Times New Roman",15)
comicsans = font.SysFont("Comic Sans MS",25)
arial = font.SysFont("Arial",15)
monospace = font.SysFont("Monospace",30)
smallsans = font.SysFont("Comic Sans MS",15)
sans = font.SysFont("Comic Sans MS",20)
papyrus = font.SysFont("Papyrus",20)
superScript14 = font.Font("fonts/SUPERSCR.TTF",14)
superScript40 = font.Font("fonts/SUPERSCR.TTF",40)
LS(110)
#----MUSIC----#
bgMusic = mixer.Channel(0) #channel for background music
sndEffs = mixer.Channel(1) #channel for sound effects
#conquest = mixer.Sound("music/3-01-conquest.ogg")
LS(220)
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
#LOADING PLAYER
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

LS(255)
#LOADING YOYO
yoyoSwordSprite = ([image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)],5)
yoyoStandSprite = yoyoSwordSprite[0][0]
yoyoSwordcritSprite = ([image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)],29)
yoyoLightSprite = (yoyoSwordcritSprite[0][:6] + yoyoSwordcritSprite[0][:6][::-1],6)
yoyoLightcritSprite = (yoyoSwordcritSprite[0][:12] + yoyoSwordcritSprite[0][:6][::-1],12)
#LOADING ALBERT
albertLanceSprite = ([image.load("images/Albert/AlbertLanceFrame"+str(i+1)+".png")
                      for i in range(24)],7)
albertStandSprite = albertLanceSprite[0][0]
albertLancecritSprite = (albertLanceSprite[0][:4] + [image.load("images/Albert/AlbertLancecritFrame"+str(i+1)+".png")
                                                  for i in range(9)] + albertLanceSprite[0][5:],15)
albertSwordSprite = ([image.load('images/Albert/AlbertSwordFrame'+str(i+1)+'.png')
                      for i in range(18)],6)
albertSwordcritSprite = (albertSwordSprite[0][:3] + [image.load('images/Albert/AlbertSwordcritFrame'+str(i+1)+'.png')
                                                  for i in range(15)] + albertSwordSprite[0][3:],21)
LS(280)
#LOADING FRANNY
frannyLanceSprite = ([image.load("images/Franny/FrannyAttackFrame"+str(i+1)+".png")
                      for i in range(10)],5)
frannyStandSprite = frannyLanceSprite[0][0]
frannyLancecritSprite = (frannyLanceSprite[0][:2] + [image.load("images/Franny/FrannyCritFrame"+str(i+1)+".png")
                                                  for i in range(11)] + frannyLanceSprite[0][2:],16)
frannySwordSprite = ([image.load("images/Franny/FrannySwordFrame"+str(i+1)+".png")
                      for i in range(11)],4)
frannySwordcritSprite = ([frannySwordSprite[0][0]] + [image.load("images/Franny/FrannySwordcritFrame"+str(i+1)+".png")
                                                    for i in range(16)] + frannySwordSprite[0][1:],20)
#LOADING GARY
garyAxeSprite = ([image.load("images/Gary/GaryAttackFrame"+str(i+1)+".png")
                  for i in range(18)],10)
garyStandSprite = garyAxeSprite[0][0]
garyAxecritSprite = ([garyStandSprite] + [image.load("images/Gary/GaryCritFrame"+str(i+1)+".png")
                                          for i in range(12)] + garyAxeSprite[0][7:],16)
#LOADING HENNING
henningStandSprite = image.load("images/Henning/HenningStand.png")
LS(315)
#LOADING HENRY
henrySwordSprite = ([image.load("images/Henry/HenryAttackFrame"+str(i+1)+".png")
                     for i in range(17)],10)
henryStandSprite = henrySwordSprite[0][0]
henrySwordcritSprite = ([henryStandSprite] + [image.load("images/Henry/HenryCritFrame"+str(i+1)+".png")
                                              for i in list(range(2)) + list(range(12))] + henrySwordSprite[0][8:],17)
#LOADING ERIC
ericStaffSprite = ([image.load("images/Eric/EricHealFrame"+str(i+1)+".png")
                    for i in range(7)],3)
ericStandSprite = ericStaffSprite[0][0]
#LOADING BRANDON
brandonSwordSprite = ([image.load("images/Brandon/BrandonAttackFrame"+str(i+1)+".png")
                       for i in range(15)],5)
brandonStandSprite = brandonSwordSprite[0][0]
brandonSwordcritSprite = (brandonSwordSprite[0][:11] + brandonSwordSprite[0][3:],13)
LS(350)
#LOADING STEFANO
stefanoBowSprite = ([image.load("images/Stefano/StefanoBowFrame"+str(i+1)+".png")
                     for i in range(16)],14)
stefanoStandSprite = stefanoBowSprite[0][0]
stefanoBowcritSprite = ([stefanoStandSprite] + [image.load("images/Stefano/StefanoBowcritFrame"+str(i+1)+".png")
                                                for i in range(11)] + stefanoBowSprite[0][9:],18)
#LOADING KEVIN
kevinDarkSprite = ([image.load('images/Kevin/KevinAttackFrame'+str(i+1)+'.png')
                    for i in range(27)],24)
kevinStandSprite = kevinDarkSprite[0][0]
kevinDarkcritSprite = ([kevinStandSprite] + [image.load('images/Kevin/KevinCritFrame'+str(i+1)+'.png')
                                             for i in range(14)] + kevinDarkSprite[0][22:],18)
LS(375)
#ENEMIES' ANIMATIONS
#BRIGAND
brigandAxeSprite = ([image.load("images/Brigand/BrigandAttackFrame"+str(i+1)+".png")
                       for i in range(14)],9)
brigandStandSprite = brigandAxeSprite[0][0]
brigandAxecritSprite = ([image.load("images/Brigand/BrigandCritFrame"+str(i+1)+".png")
                     for i in range(2)] + brigandAxeSprite[0],11)
#MERCENARY
mercenarySwordSprite = ([image.load("images/Mercenary/MercenaryAttackFrame"+str(i+1)+".png")
                         for i in range(21)],12)
mercenaryStandSprite = mercenarySwordSprite[0][0]
mercenarySwordcritSprite = ([mercenaryStandSprite]+[image.load("images/Mercenary/MercenaryCritFrame"+str(i+1)+".png")
                                                     for i in range(18)] + mercenarySwordSprite[0][6:],25)
#KNIGHT
knightLanceSprite = ([image.load("images/Knight/KnightAttackFrame"+str(i+1)+".png")
                      for i in range(9)],5)
knightStandSprite = knightLanceSprite[0][0]
knightLancecritSprite = ([knightStandSprite] + [image.load("images/Knight/KnightCritFrame"+str(i+1)+".png")
                          for i in range(5)] + knightLanceSprite[0][1:],10)
#MAGIC ANIMATIONS
#--FIRE
fireSprite = [image.load("images/Magic/Fire/Fire"+str(i+1)+".png").convert_alpha()
              for i in range(17)]
#--LIGHTNING
lightningSprite = [image.load('images/Magic/Lightning/Lightning'+str(i+1)+'.png')
                   for i in range(6)]
#--FLUX
fluxSprite = [image.load("images/Magic/Flux/Flux"+str(i+1)+".png")
              for i in range(14)]
#--HEAL
healSprite = [image.load("images/Magic/Heal/HealFrame"+str(i+1)+".png").convert_alpha()
              for i in range(2)]*7
LS(400)
#MAP SPRITES
#--allies
allyMapSprites = {"Mage":[transform.scale(image.load("images/MapSprites/Ally/Mage"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Lord":[transform.scale(image.load("images/MapSprites/Ally/Lord"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Knight":[transform.scale(image.load("images/MapSprites/Ally/Knight"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Cavalier":[transform.scale(image.load("images/MapSprites/Ally/Cavalier"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Paladin":[transform.scale(image.load('images/MapSprites/Ally/Paladin'+str(i+1)+'.png').convert_alpha(),(30,30)) for i in range(4)],
                  "Fighter":[transform.scale(image.load("images/MapSprites/Ally/Fighter"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Mercenary":[transform.scale(image.load("images/MapSprites/Ally/Mercenary"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Transporter":[transform.scale(image.load("images/MapSprites/Ally/Transporter"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                  "Thief":[transform.scale(image.load("images/MapSprites/Ally/Thief"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Priest":[transform.scale(image.load("images/MapSprites/Ally/Priest"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Archer":[transform.scale(image.load("images/MapSprites/Ally/Archer"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                  "Shaman":[transform.scale(image.load("images/MapSprites/Ally/Shaman"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)]}
#--enemies
enemyMapSprites = {"Brigand":[transform.scale(image.load("images/MapSprites/Enemy/Brigand"+str(i+1)+".gif").convert_alpha(),(30,30)) for i in range(4)],
                   "Mercenary":[transform.scale(image.load("images/MapSprites/Enemy/Mercenary"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)],
                   "Knight":[transform.scale(image.load("images/MapSprites/Enemy/Knight"+str(i+1)+".png").convert_alpha(),(30,30)) for i in range(4)]}
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
         "Henry":image.load("images/faces/Henry.png"),
         "Brandon":image.load("images/faces/Brandon.png"),
         "Stefano":image.load("images/faces/Stefano.png"),
         "Eric":image.load('images/faces/Eric.png'),
         "Kevin":image.load('images/faces/Kevin.png'),
        "Bandit":image.load("images/faces/Bandit.png"),
        "Mercenary":image.load("images/faces/Bandit.png"),
         "Villager":image.load("images/faces/Villager.png")} #dictionary of all faces of characters

#ARROW SPRITES
arrowHead = image.load("images/Arrow/arrowHead.png")
arrowBent = image.load("images/Arrow/arrowBent.png")
arrowStraight = image.load("images/Arrow/arrowStraight.png")

#TERRAIN IMAGES
forestImg = image.load('images/terrain/forest.png')
mountainImg = image.load('images/terrain/mountain.png')
peakImg = image.load("images/terrain/peak.png")
vendImg = image.load("images/terrain/vendor.png")
armImg = image.load("images/terrain/armory.png")
vilImg = image.load("images/terrain/village.png")
castleImg = image.load("images/terrain/castle.png")
fortImg = image.load("images/terrain/fort.png")
#BACKGROUND IMAGES
plainsBackground = image.load("images/Maps/prologue.png")

#battle background
battlePlains = image.load("images/backgrounds/battlePlains.png")

#UI Images
menuBG = image.load("images/backgrounds/menuBackground.png")
trnsferBG = image.load("images/backgrounds/transferscreen.png")
statsBG = image.load('images/backgrounds/statsMenu.png')
itemsInfoBG = image.load('images/backgrounds/itemMenu.png')
mastBG = image.load("images/backgrounds/masteryMenu.png")
armorySelect,armorySelect2,vendorSelect,vendorSelect2 = [image.load("images/backgrounds/"+imgName+".png") for imgName in ["armorySelect","armorySelect2","vendorSelect",
                                                                                                                          "vendorSelect2"]]
pointer = image.load('images/pointer.png')
infoBox = image.load('images/infoBox.png')
infoBoxNW = image.load('images/infoBoxNW.png')
LS(440)
#----END OF IMAGE LOAD----#
#TERRAIN
plain = Terrain("Plain",0,0,1)
forest = Terrain("Forest",1,20,2,forestImg)
mountain = Terrain("Mountain",2,30,3,mountainImg)
peak = Terrain("Peak",3,40,4,peakImg)
vendor = Vendor("Vendor",0,10,1,vendImg)
armory = Armory("Armory",0,10,1,armImg)
village = Village("Village",0,10,1,vilImg)
castle = Terrain("Castle",0,0,1,castleImg)
castlePiece = Terrain("Castle",0,0,1)
gate = Terrain("Gate",2,20,2,heal=6)
fort = Terrain("Fort",2,20,2,fortImg,heal=6)
throne = Terrain("Throne",30,3,3) #needs img
water = Terrain("Water",10,0,3) #needs img
#ITEMS
#Troll weapons
real_knife = Weapon("Real Knife",99,1,1000,999,"Sword",600,9999)
#Bows
iron_bow = Weapon("Iron Bow",6,5,45,85,"Bow",100,540,0,2,46,False,[],2)
steel_bow = Weapon("Steel Bow",9,9,30,70,"Bow",200,720,0,2,30,False,[],2)
#Lances
iron_lance = Weapon("Iron Lance",7,8,45,80,"Lance",100,360)
steel_lance = Weapon("Steel Lance",10,13,30,70,"Lance",200,480)
silver_lance = Weapon("Silver Lance",14,10,20,75,"Lance",500,1200)
long_lance = Weapon("Long Lance",8,12,20,65,"Lance",200,900,maxrnge=2)
#Anima Magic
fire = Weapon("Fire",5,4,40,90,"Anima",100,560,0,1,40,True,maxrnge=2,anims=fireSprite)
#Light Magic
lightning = Weapon("Lightning",4,6,35,95,"Light",100,630,5,1,35,True,maxrnge=2,anims=lightningSprite)
#Dark Magic
flux = Weapon("Flux",7,8,45,80,"Dark",100,900,0,1,45,True,maxrnge=2,anims=fluxSprite)
#Staves
heal = Staff("Heal",30,100,600,10,"Heals an injured ally",anims=healSprite)
#Swords
slim_sword = Weapon("Slim Sword",3,2,30,100,"Sword",100,480,5)
steel_sword = Weapon("Steel Sword",8,10,30,80,"Sword",200,600)
iron_sword = Weapon("Iron Sword",5,5,47,90,"Sword",100,460)
killing_edge = Weapon("Killing Edge",9,7,20,75,"Sword",300,1300,30)
rapier = Weapon("Rapier",7,5,40,95,"Sword",700,6000,10,1,40,False,["Cavalier","Paladin","Knight","General"],1,5,"Effective against knights, cavalry","Yoyo")
#Axes
iron_axe = Weapon("Iron Axe",8,10,45,75,"Axe",100,270)
steel_axe = Weapon("Steel Axe",11,15,30,65,"Axe",100,360)
#Consumables
vulnerary = Consumable("Vulnerary",10,3,300,"Heals for 10 HP")
#Misc.
lock_pick = Item("Lock Pick",45,500,"Opens doors and chests")
red_gem = Item("Red Gem",1,4000,"Sells for 2000G")
blue_gem = Item("Blue Gem",1,10000,"Sells for 5000G")
white_gem = Item("White Gem",1,20000,"Sells for 10000G")
#TRANSLUCENT SQUARES
transBlue = Surface((30,30), SRCALPHA)
transBlue.fill((0,0,255,122))
transRed = Surface((30,30), SRCALPHA)
transRed.fill((255,0,0,122))
transBlack = Surface((1200,720), SRCALPHA)
transBlack.fill((0,0,0,122))
transGreen = Surface((30,30), SRCALPHA)
transGreen.fill((0,255,0,122))
LS(550)
#----PERSONS----#
#ALLIES
name = "" #name of player
usedNames = ["yoyo","albert","franny","gary","stefano","henry","henning","brandon","eric","alex","villager","kevin"] #names the player cannot use
player = None #player is defined in NewGame or LoadGame
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":3,"skl":7,"lck":7,
                "spd":6,"con":5,"move":5,"res":4,"hp":21,"maxhp":21},
               {"stren":40,"defen":20,"skl":70,"lck":70,
                "spd":40,"res":40,"maxhp":60},
               [rapier.getInstance(),lightning.getInstance(),vulnerary.getInstance()],{"Sword":200,"Light":100},
               {"Sword":yoyoSwordSprite,"Swordcrit":yoyoSwordcritSprite,"stand":yoyoStandSprite,
                "Light":yoyoLightSprite,"Lightcrit":yoyoLightcritSprite},faces["Yoyo"],deathQuote="Sorry everyone... I'm nothing but a failure...")
albert = Paladin("Albert",0,0,
              {"lv":1,"stren":12,"defen":10,"skl":19,"lck":6,
                "spd":15,"con":10,"move":8,"res":8,"hp":38,"maxhp":38},
               {"stren":25,"defen":20,"skl":35,"lck":35,
                "spd":25,"res":10,"maxhp":40},
              [silver_lance.getInstance(),steel_sword.getInstance(),iron_sword.getInstance(),vulnerary.getInstance()],{'Sword':300,'Lance':500},
              {'stand':albertStandSprite,'Lance':albertLanceSprite,'Lancecrit':albertLancecritSprite,
               'Sword':albertSwordSprite,'Swordcrit':albertSwordcritSprite},faces["Albert"],
                 deathQuote="Sigh... I don't even understand how I died... I'm OP. If someone were controlling me I'd call them a n00b...")
franny = Cavalier("Franny",0,0,
                  {"lv":3,"stren":7,"defen":5,"skl":9,"lck":4,
                   "spd":8,"con":10,"move":7,"res":1,"hp":24,"maxhp":24},
                  {"stren":35,"defen":25,"skl":50,"spd":55,"lck":45,"res":15,"maxhp":70},
                  [iron_lance.getInstance(),iron_sword.getInstance(),vulnerary.getInstance()],{'Lance':200,'Sword':200},
                  {'stand':frannyStandSprite,'Lance':frannyLanceSprite,'Lancecrit':frannyLancecritSprite,
                   'Sword':frannySwordSprite,'Swordcrit':frannySwordcritSprite},faces["Franny"],
                  deathQuote="Lo siento amigos mío... Señor Albert... protegéis Señor You Zhou...")
gary = Fighter("Gary",0,0,
               {"lv":3,"stren":9,"defen":6,"skl":6,"lck":4,
                "spd":6,"con":13,"move":5,"res":0,"hp":32,"maxhp":32},
               {"stren":55,"defen":40,"skl":40,"spd":30,"lck":45,"res":10,"maxhp":85},
               [iron_axe.getInstance(),vulnerary.getInstance()],{"Axe":200},
               {"stand":garyStandSprite,"Axe":garyAxeSprite,"Axecrit":garyAxecritSprite},faces["Gary"],
               deathQuote="Rip... Welp. It's 'bout time I got shut down... *kek*... GG... WP...")
henning = Transporter("Henning",0,0,
               {"lv":1,"stren":2,"defen":10,"skl":18,"lck":5,
                "spd":15,"con":25,"move":6,"res":7,"hp":28,"maxhp":28},
               {"stren":5,"defen":100,"skl":100,"spd":100,"lck":100,"res":75,"maxhp":100},
               [red_gem.getInstance()],{},
               {"stand":henningStandSprite},faces["Henning"],[vulnerary.getInstance(),white_gem.getInstance(),red_gem.getInstance(),blue_gem.getInstance()],
                deathQuote="lel I'm ded. jk m8. I'll be back next chapter, but like, i gotta scram or our stuff will get stolen.")
henry = Mercenary("Henry",0,0,
               {"lv":5,"stren":9,"defen":5,"skl":10,"lck":9,
                "spd":10,"con":10,"move":5,"res":2,"hp":27,"maxhp":27},
               {"stren":50,"defen":25,"skl":45,"spd":55,"lck":40,"res":10,"maxhp":75},
               [killing_edge.getInstance(),iron_sword.getInstance(),steel_sword.getInstance(),red_gem.getInstance(),vulnerary.getInstance()],{"Sword":300},
               {"stand":henryStandSprite,"Sword":henrySwordSprite,"Swordcrit":henrySwordcritSprite},faces["Henry"],
                deathQuote="I've been bested. So be it...")
eric = Priest("Eric",0,0,
               {"lv":5,"stren":6,"defen":2,"skl":8,"lck":8,
                "spd":10,"con":6,"move":5,"res":8,"hp":24,"maxhp":24},
               {"stren":35,"defen":10,"skl":50,"spd":50,"lck":45,"res":35,"maxhp":60},
               [heal.getInstance(),vulnerary.getInstance()],{"Staff":200},
               {"stand":ericStandSprite,"Staff":ericStaffSprite},faces["Eric"],
              deathQuote="...Why... Why now? Please fight on everyone!")
brandon = Thief("Brandon",0,0,
                {"lv":4,"stren":5,"defen":3,"skl":7,"lck":5,
                "spd":13,"con":5,"move":6,"res":3,"hp":22,"maxhp":22},
               {"stren":25,"defen":20,"skl":45,"spd":70,"lck":30,"res":15,"maxhp":60},
               [iron_sword.getInstance(),blue_gem.getInstance(),lock_pick.getInstance(),vulnerary.getInstance()],{"Sword":100},
               {"stand":brandonStandSprite,"Sword":brandonSwordSprite,"Swordcrit":brandonSwordcritSprite},faces["Brandon"],
                deathQuote="Ouch! That really... hurt...........")
stefano = Archer("Stefano",0,0,
                {"lv":4,"stren":7,"defen":5,"skl":9,"lck":7,
                "spd":9,"con":5,"move":5,"res":3,"hp":25,"maxhp":25},
               {"stren":40,"defen":25,"skl":50,"spd":45,"lck":35,"res":10,"maxhp":65},
               [iron_bow.getInstance(),white_gem.getInstance(),vulnerary.getInstance()],{"Bow":200},
               {"stand":stefanoStandSprite,"Bow":stefanoBowSprite,"Bowcrit":stefanoBowcritSprite},faces["Stefano"],
                 deathQuote="$!@#! I KNEW I shouldn't have joined this group. I swear I'm going to $@!# whoever let me die like a $!@# piece of !@#$!!!")
kevin = Shaman("Kevin",0,0,
               {"lv":5,"stren":9,"defen":4,"skl":10,"lck":3,
                "spd":8,"con":6,"move":5,"res":7,"hp":26,"maxhp":26},
               {"stren":55,"defen":15,"skl":45,"spd":40,"lck":20,"res":50,"maxhp":70},
               [flux.getInstance(),vulnerary.getInstance()],{"Dark":200},
               {"stand":kevinStandSprite,"Dark":kevinDarkSprite,"Darkcrit":kevinDarkcritSprite},faces["Kevin"],
               deathQuote="我觉得谁控制我是哑巴。Dang it pygame no support my chinese...") 
allies = [] #allies
#ENEMIES
#--Brigands
bandit0 = Brigand("Bandit",0,0,
                  {"lv":1,"stren":5,"defen":2,"skl":3,"lck":0,
                   "spd":3,"con":8,"move":5,"res":0,"hp":20,"maxhp":20},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
bandit1 = Brigand("Bandit",0,0,
                  {"lv":3,"stren":6,"defen":3,"skl":4,"lck":0,
                   "spd":3,"con":9,"move":5,"res":0,"hp":22,"maxhp":22},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
alexTheBandit = Brigand("Alex the Bandit",0,0,
                        {"lv":5,"stren":8,"defen":5,"skl":4,"lck":3,
                         "spd":3,"con":13,"move":5,"res":0,"hp":25,"maxhp":25},{},[iron_axe.getInstance()],{"Axe":200},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],70,guard=True,
                fightQuote="How dare you kill all my friends! You're seriously going to pay!",
                deathQuote="Ugh... how could I die to a pampered lordling... and some hobo...")
bandit2 = Brigand("Bandit",0,0,
                {"lv":5,"stren":7,"defen":4,"skl":4,"lck":0,
                "spd":4,"con":9,"move":5,"res":0,"hp":23,"maxhp":23},{},[iron_axe.getInstance()],{"Axe":300},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
bandit2_v = Brigand("Bandit",0,0,
                {"lv":5,"stren":7,"defen":4,"skl":4,"lck":0,
                "spd":4,"con":9,"move":5,"res":0,"hp":23,"maxhp":23},{},[iron_axe.getInstance(),vulnerary.getInstance()],{"Axe":300},
                {"Axe":brigandAxeSprite,"Axecrit":brigandAxecritSprite,"stand":brigandStandSprite},faces["Bandit"],20)
#--Mercenaries
merc1 = Mercenary("Mercenary",0,0,
                {"lv":3,"stren":5,"defen":2,"skl":8,"lck":2,
                "spd":8,"con":6,"move":5,"res":0,"hp":18,"maxhp":18},{},[iron_sword.getInstance()],{"Sword":200},
                {"Sword":mercenarySwordSprite,"Swordcrit":mercenarySwordcritSprite,"stand":mercenaryStandSprite},faces["Bandit"],20)
merc2 = Mercenary("Mercenary",0,0,
                {"lv":5,"stren":6,"defen":3,"skl":9,"lck":2,
                "spd":9,"con":6,"move":5,"res":0,"hp":19,"maxhp":19},{},[iron_sword.getInstance()],{"Sword":200},
                {"Sword":mercenarySwordSprite,"Swordcrit":mercenarySwordcritSprite,"stand":mercenaryStandSprite},faces["Bandit"],20)
alexTheMerc = Mercenary("Alex the Merc",0,0,
                {"lv":7,"stren":7,"defen":4,"skl":10,"lck":2,
                "spd":9,"con":10,"move":5,"res":0,"hp":27,"maxhp":27},{},[steel_sword.getInstance()],{"Sword":300},
                 {"Sword":mercenarySwordSprite,"Swordcrit":mercenarySwordcritSprite,"stand":mercenaryStandSprite},faces["Bandit"],100,guard=True,
                fightQuote="You think you can stand up to LEX REAPER!? Ha! Try me",
                deathQuote="Watch out King Alex... these men are strong... After all, they even bested me!")
#--Knights
knight2 = Knight("Knight",0,0,
                {"lv":5,"stren":8,"defen":6,"skl":3,"lck":0,
                "spd":1,"con":12,"move":4,"res":0,"hp":20,"maxhp":20},{},[iron_lance.getInstance()],{"Lance":100},
                {"Lance":knightLanceSprite,"Lancecrit":knightLancecritSprite,"stand":knightStandSprite},faces["Bandit"],20,guard=True)
alexTheKnight = Knight("Knight Alex",0,0,
                {"lv":10,"stren":10,"defen":8,"skl":5,"lck":1,
                "spd":4,"con":15,"move":4,"res":0,"hp":30,"maxhp":30},{},[steel_lance.getInstance(),long_lance.getInstance()],{"Lance":300},
                {"Lance":knightLanceSprite,"Lancecrit":knightLancecritSprite,"stand":knightStandSprite},faces["Bandit"],100,throne=True)

enemies = []
LS(660)
#----CHAPTERS----#
numChaps = 3 #number of chapters - including prologue
chapterShops = [[],
                [vendor.setItems([vulnerary.getInstance()]),
                 armory.setItems([iron_sword.getInstance(),
                                  iron_lance.getInstance(),
                                  iron_axe.getInstance(),
                                  iron_bow.getInstance()])],
                [armory.setItems([steel_sword.getInstance(),
                                  steel_lance.getInstance(),
                                  steel_axe.getInstance(),
                                  steel_bow.getInstance()]),

                 vendor.setItems([vulnerary.getInstance(),fire.getInstance(),heal.getInstance(),lightning.getInstance()])]]
chapterVillages = [[],
                   [village.setItems(vulnerary.getInstance(),"story/chapter1village1.txt")],
                   [village.setItems(silver_lance.getInstance(),"story/chapter2village1.txt"),
                    village.setItems(vulnerary.getInstance(),"story/chapter2village2.txt"),
                    village.setItems(white_gem.getInstance(),"story/chapter2village3.txt")]]
#MAPS
def createMap(width,height,terrains=[]):
    "creates a map (2d list)"
    newMap = [[plain for i in range(width)] for j in range(height)]
    for t,coords in terrains:
        for x,y in coords:
            newMap[y][x] = t
    return newMap
terrDict = {".":plain,
            "|":forest,
            "^":mountain,
            "&":peak,
            "S":vendor,
            "R":armory,
            "V":village,
            "$":castle,
            "%":castlePiece,
            "T":throne,
            "G":gate,
            "@":fort,
            "-":water} #translates string into terrain
def createMapFromFile(chapterNum):
    "creates map from file"
    newMap = []
    mapFile = open("maps/chapter"+str(chapterNum)+".txt")
    shopNum = 0
    villageNum = 0
    for line in mapFile.read().strip().split("\n"):
        newLine = []
        for c in line:
            terr = terrDict[c]
            if c in ["S","R"]:
                terr = chapterShops[chapterNum][shopNum]
                shopNum += 1
            if c == "V":
                terr = chapterVillages[chapterNum][villageNum].getInstance()
                villageNum += 1
            newLine.append(terr)
        newMap.append(newLine)
    return newMap
def getEcoords(chapterNum):
    "gets Enemy coordinates in a specific chapter"
    coords = []
    mapFile = open("maps/chapter"+str(chapterNum)+"C.txt")
    map2D = mapFile.read().strip().split("\n")
    for y in range(len(map2D)):
        line = map2D[y]
        for x in range(len(line)):
            c = line[x]
            if isInt(c):
                coords.append((int(c),x,y))
    coords.sort()
    return [(x,y) for c,x,y in coords] #returns coordinates for enemies
def getAcoords(chapterNum):
    "gets ally coordinates in a specific chapter"
    coords = []
    mapFile = open("maps/chapter"+str(chapterNum)+"C.txt")
    map2D = mapFile.read().strip().split("\n")
    for y in range(len(map2D)):
        line = map2D[y]
        for x in range(len(line)):
            c = line[x]
            if c in "abcdefghijklmnopqrstuvwxyz":
                coords.append((c,x,y))
    coords.sort()
    return [(x,y) for c,x,y in coords] #returns coordinates for enemies
def getNumEnList(chapterNum):
    "gets list of number of enemies in specified chapter"
    numEnList = [0 for i in range(10)]#the result
    map2D = open("maps/chapter"+str(chapterNum)+"C.txt").read().strip().split("\n")
    for y in range(len(map2D)):
        line = map2D[y]
        for x in range(len(line)):
            c = line[x]
            if isInt(c):
                numEnList[int(c)] += 1
    return [i for i in numEnList if i != 0] #returns all non-zeros
def drawMap(maptodraw):
    "draws a map"
    for y in range(len(maptodraw)):
        for x in range(len(maptodraw[y])):
            if maptodraw[y][x].img != None:
                screen.blit(maptodraw[y][x].img,(x*30,y*30))
#chapter0 = createMapFromFile(0)
#chapter1 = createMap(40,24,[(peak,[(7,10),(10,7),(11,11),(8,10),(7,11),(8,11),(9,11),(10,11),(9,10),(10,10),(11,10),(10,9),(10,8)])])
chapterMaps = [createMapFromFile(i) for i in range(numChaps)]
#CHAPTER DATA
#Stored in tuples
#(gainedAllies,allyCoordinates,Enemies,Goal,BackgroundImage)
#chapter data, chapter is determined by index
chapterData = [([yoyo],getAcoords(0),createEnemyList([bandit0,alexTheBandit],[5,1],getEcoords(0)),
                "Defeat all enemies",plainsBackground),
               ([albert,franny,gary,henning],getAcoords(1),createEnemyList([bandit1,merc1,alexTheMerc],[6,6,1],getEcoords(1)),
                "Defeat all enemies",plainsBackground),
               ([henry,eric,kevin,stefano,brandon],getAcoords(2),createEnemyList([bandit2,merc2,bandit2_v,knight2,alexTheKnight],getNumEnList(2),getEcoords(2)),
                "Seize gate",plainsBackground)]
chapterBattleBackgrounds = [battlePlains,battlePlains,battlePlains]
oldAllies = [] #keeps track of allies before the fight
allAllies = [] #all allies that exist

#----MUSIC----#
#add at the end because Albert's mac is funny
#each index represents what music is played in the chapter of that index
#chapterMusic = [conquest]

#miscellaneous
chapter = 0 #changes when load new/old game, so stays global
fpsLimiter = time.Clock()
gold = 0 #gold the player has
LS(766)
screen.fill(BLACK)
#----GLOBAL FUNCTIONS----#
def addAlly(ally):
    "adds an ally to the allies list - updates allAllies too"
    allies.append(ally) #adds ally to allies
    allAllies.append(ally) #adds ally to allAllies
def load(file):
    "loads the file into the game, and returning 0 if it is empty"
    global chapter,allAllies,player,gold
    if "chapter" not in file:
        file.close()
        changemode(NewGame())#goes to new game
    else:
        #sets the chapter we are about to start and allAllies
        chapter = file["chapter"]
        allAllies = file["allAllies"]
        gold = file["gold"]
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
    file["gold"] = gold
    file.close()
    changemode(getStory(chapter))
def getSavedChapter(file):
    "gets the chapter saved file #"
    try:
        return "Chapter: "+str(file["chapter"])
    except:
        return "--NO DATA--"
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
            if type(person.items[i]) in [Weapon,Staff]:
                if not person.canEquip(person.items[i]):
                    #if the person cannot equip, the color goes grey
                    col = GREY
            screen.blit(sans.render(person.items[i].name,True,col),(x*30,(y+i)*30))
            screen.blit(sans.render(str(person.items[i].dur)+"/"+str(person.items[i].maxdur),True,col),((x+6)*30,(y+i)*30)) #blits durability
    draw.rect(screen,WHITE,(x*30,(y+menuselect)*30,240,30),1) #draws selected item
def drawItem(person,item,x,y,diff=180,fnt=sans):
    "draws an item"
    col = WHITE
    if type(item) in [Weapon,Staff]:
        if not person.canEquip(item):
            #if the person cannot equip, the color goes grey
            col = GREY
    screen.blit(fnt.render(item.name,True,col),(x,y))
    screen.blit(fnt.render(str(item.dur)+"/"+str(item.maxdur),True,col),(x+diff,y)) #blits durability
#----PERSON ACTIONS----#
#ATTACK FUNCTIONS
def checkDead(ally,enemy):
    "checks if an ally or an enemy is dead; also removes ally or enemy from list"
    if ally.hp == 0:
        allies.remove(ally)
        if ally.deathQuote == "":
            return True
        if not writeDialogue(screen,ally.deathQuote,name=ally.name,face=ally.face):
            quit()
        waiting = True #waiting for user to press a key in order to move on
        arrowflashcounter = 0
        while waiting:
            for e in event.get():
                if e.type == QUIT:
                    quit()
                    return 0
                if e.type == KEYDOWN:
                    if e.key in [K_z,K_x,K_RETURN]:
                        waiting = False
            draw.rect(screen,BLUE,(0,690,1200,30)) #might have to be subsurface
            botinstruct = sans.render("Z to continue, X or Enter to Skip",True,WHITE) if int(arrowflashcounter)%2 else sans.render("Z to continue, X or Enter to Skip V",True,WHITE)
            screen.blit(botinstruct,(0,690))
            arrowflashcounter += 0.15
            display.flip()
        return True
    if enemy.hp == 0:
        enemies.remove(enemy)
        if enemy.deathQuote == "":
            return True
        if not writeDialogue(screen,enemy.deathQuote,900,name=enemy.name,face=enemy.face):
            quit()
        waiting = True #waiting for user to press a key in order to move on
        arrowflashcounter = 0
        while waiting:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    return 0
                if e.type == KEYDOWN:
                    if e.key in [K_z,K_x,K_RETURN]:
                        waiting = False
            draw.rect(screen,BLUE,(0,690,1200,30)) #might have to be subsurface
            botinstruct = sans.render("Z to continue, X or Enter to Skip",True,WHITE) if int(arrowflashcounter)%2 else sans.render("Z to continue, X or Enter to Skip V",True,WHITE)
            screen.blit(botinstruct,(0,690))
            arrowflashcounter += 0.15
            display.flip()
        return True
    return False
def attack(person,person2):
    "attack animation of person to person2"
    #sets who is the ally and who is the enemy
    global running
    if person in allies:
        ally = person
        enemy = person2
    else:
        ally = person2
        enemy = person
    if enemy.fightQuote != "" and not enemy.fought:
        if not writeDialogue(screen,enemy.fightQuote,900,530,enemy.name,enemy.face):
            quit()
        enemy.fought = True #only enemy has a fightquote
        waiting = True #waiting for user to press a key in order to move on
        arrowflashcounter = 0
        while waiting:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    return 0
                if e.type == KEYDOWN:
                    if e.key in [K_z,K_x,K_RETURN]:
                        waiting = False
            draw.rect(screen,BLUE,(0,690,1200,30)) #might have to be subsurface
            botinstruct = sans.render("Z to continue, X or Enter to Skip",True,WHITE) if int(arrowflashcounter)%2 else sans.render("Z to continue, X or Enter to Skip V",True,WHITE)
            screen.blit(botinstruct,(0,690))
            arrowflashcounter += 0.15
            display.flip()
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
    equipped = ally.equip
    broke = False
    enBroke = False
    if not singleAttack(screen,person,person2,isenemy,chapterMaps[chapter]):
        if person == ally:
            broke = True
        else:
            enBroke = True
    wexpGain = 0
    if person == ally:
        wexpGain = equipped.wexp
    if handleEvents(event.get()):
        quit()
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
            if equipped != None:
                if ally.gainWExp(wexpGain,equipped.typ):
                    dispTempMsg(screen,equipped.typ.title() + " mastery level increased.",0,0,centerX=True,centerY=True)
            if broke:
                dispTempMsg(screen,equipped.name+" broke!",centerX=True,centerY=True)
        display.flip()
        time.wait(500)
        return False #ends the function if either ally or enemy is dead
    #Draws damage for attack 2
    person2hit = False #did person2 hit? (person 1 hits no matter what, so I don't need that)
    if canAttackTarget(person2,person.x,person.y):
        #if person2 can attack
        screen.blit(actionFiller,(0,0)) #covers both persons
        if not singleAttack(screen,person2,person,not isenemy,chapterMaps[chapter]):
            if person2 == ally:
                broke = True
            else:
                enBroke = True
        person2hit = True
        if ally == person2:
            wexpGain += equipped.wexp
    if handleEvents(event.get()):
        quit()
    if checkDead(ally,enemy):
        #gains exp if enemy died
        if enemy.hp == 0:
            expgain = getExpGain(ally,enemy,True) #gains exp on a kill
            drawChangingBar(screen,ally.exp,ally.exp+expgain,100,420,330,360,60,"Exp")
            needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
            if needLevelUp:
                #level up
                ally.levelUp()
                drawLevelUp(screen,ally)
            if ally.gainWExp(wexpGain,equipped.typ):
                dispTempMsg(screen,equipped.typ.title() + " mastery level increased.",0,0,centerX=True,centerY=True)                    
            if broke:
                dispTempMsg(screen,equipped.name+" broke!",centerX=True,centerY=True)
        display.flip()
        time.wait(500)
        if handleEvents(event.get()):
            quit()
        return False
    #Draws damage for attack 3
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy.x,enemy.y) and not broke:
        screen.blit(actionFiller,(0,0)) #covers both persons
        if not singleAttack(screen,ally,enemy,False,chapterMaps[chapter]):
            broke = True
        person2hit = ally == person2 #person2hit becomes true if ally was person2
        wexpGain += equipped.wexp
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally.x,ally.y) and not enBroke:
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(screen,enemy,ally,True,chapterMaps[chapter])
    if handleEvents(event.get()):
        quit()
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
    if handleEvents(event.get()):
        quit()
    needLevelUp = ally.gainExp(expgain) #sets a boolean from the result of our exp gain
    if needLevelUp:
        #level up
        ally.levelUp()
        drawLevelUp(screen,ally)
    if equipped != None:
        if ally.gainWExp(wexpGain,equipped.typ):
            dispTempMsg(screen,equipped.typ.title() + " mastery level increased.",0,0,centerX=True,centerY=True)
    if broke:
        dispTempMsg(screen,equipped.name+" broke!",centerX=True,centerY=True)
    time.wait(1000)
    if handleEvents(event.get()):
        quit()
def heal(person,person2,stf):
    "draws healing animation"
    screen.blit(chapterBattleBackgrounds[chapter],(0,0))
    display.flip()
    time.wait(200)
    drawBattleInfo(screen,person,person2,chapterMaps[chapter],True,stf)
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    if person.equip == None:
        screen.blit(person.anims["stand"],(0,0))
    else:
        screen.blit(person.anims[person.equip.typ][0][0],(0,0))
    if person2.equip == None:
        screen.blit(transform.flip(person2.anims["stand"],True,False),(0,0))
    else:
        screen.blit(transform.flip(person2.anims[person2.equip.typ][0][0],True,False),(0,0))
    display.flip()
    time.wait(200)
    if handleEvents(event.get()):
        quit()
    screen.blit(actionFiller,(0,0))
    if not singleAttack(screen,person,person2,False,chapterMaps[chapter],True,stf):
        dispTempMsg(screen,stf.name+" Broke!",centerX=True,centerY=True)
    expgain = 20 + person.stren + stf.heal
    drawChangingBar(screen,person.exp,person.exp+expgain,100,420,330,360,60,"Exp")
    if person.gainExp(expgain):
        #level up
        person.levelUp()
        drawLevelUp(screen,person)
    if person.gainWExp(stf.wexp,"Staff"):
        dispTempMsg(screen,stf.typ.title() + " mastery level increased.",centerX=True,centerY=True)
    time.wait(1000)
    event.clear()
#-------ITEM OVERFLOW---------#
#This is so items don't overflow - we can send to henning if he has space, otherwise we delete
def itemOverflow(p,item):
    "handles item overflow"
    global running
    buffer = screen.copy()
    selecting = True
    selItem = 0 #selected item
    draw.rect(screen,BLUE,(200,200,600,360))
    for i in range(len(p.items)):
        drawItem(p,p.items[i],200,200+60*i,460,superScript40) #draws all items
    drawItem(p,item,200,500,460,superScript40)
    draw.rect(screen,BLUE,(0,0,1200,60))
    if len(henning.supply) < 100:
        #henning has space
        screen.blit(superScript40.render("Select an item to send to Henning",True,WHITE),(0,0))
        henningSpace = True
    else:
        #henning has no space
        screen.blit(superScript40.render("Select an item to send to discard",True,WHITE),(0,0))
        henningSpace = False
    allItems = p.items + [item]
    filler = screen.copy()
    framecounter = 0
    clickedFrame = -1
    while selecting:
        screen.blit(filler,(0,0))
        for e in event.get():
            if e.type == QUIT:
                running = False
                return 0
            if e.type == KEYDOWN:
                if e.key == K_DOWN:
                    selItem += 1
                if e.key == K_UP:
                    selItem -= 1
                if e.key == K_z:
                    msg = "Sent to Henning" if henningSpace else "Discarded"
                    dispTempMsg(screen,allItems[selItem].name + " " + msg,centerX=True,centerY=True)
                    if henningSpace:
                        henning.supply.append(allItems[selItem])
                    if selItem < 5:
                        p.removeItem(p.items[selItem])
                        p.addItem(item)
                    selecting = False
                selItem = min(5,max(selItem,0))
                clickedFrame = framecounter
            if e.type == KEYUP:
                clickedFrame = -1
        if framecounter - clickedFrame > 20 and framecounter%6 and clickedFrame > 0:
            kp = key.get_pressed()
            if kp[K_UP]:
                selItem -= 1
            if kp[K_DOWN]:
                selItem += 1
            selItem = min(5,max(selItem,0))
        draw.rect(screen,WHITE,(200,200+60*selItem,600,60),1)
        screen.blit(pointer,(150,200+60*selItem)) #blits pointer of selected item
        display.flip()
        framecounter += 1
        fpsLimiter.tick(60) #LIMITS TO 60 FPS
    screen.blit(buffer,(0,0))
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
    for w in [i for i in ally.items if type(i) in [Weapon,Staff]]:
        #goes through all weapons and imagifies them
        if w.anims != None:
            #changes all weapons with an animation to be stringified
            w.anims = w.name.lower()+"Sprite"
def imagifyStrings(ally):
    "imagifies all strings in ally - opposite of stringifyImages"
    for i,k in enumerate(ally.anims):
        ally.anims[k] = eval(ally.anims[k]) #creates an image from the string using eval
    for w in [i for i in ally.items if type(i) in [Weapon,Staff]]:
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

            if self.background.get_at((x-self.x,y-self.y)) != (0,0,0,255):
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
        self.info = False
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
        draw.rect(screen,BLUE,(self.x*30,self.y*30,self.width,self.height)) #this is the menu background
        screen.blit(self.background,(self.x*30,self.y*30)) #blits the background (nothing atm)
        x = self.x*30
        for i in range(len(self.items)):
            #draws the item
            opt = self.items[i] #option to draw
            y = (self.y+i)*30
            if type(opt) == str:
                screen.blit(sans.render(opt.title(),True,WHITE),(x,y))
            elif type(opt) == Item or issubclass(type(opt),Item):
                drawItem(person,opt,x,y)
                if self.info and self.selected == i:
                    ix = x+250
                    drawInfoBox(screen,ix,y,opt)
        screen.blit(pointer,(x-30,(self.y+self.selected)*30,self.width,30))
        draw.rect(screen,WHITE,(x,(self.y+self.selected)*30,self.width,30),1)
        if self.subMenu != None:
            self.subMenu.draw(person)#draws the subMenu
    def getOption(self):
        "returns the option that is selected"
        if self.subMenu == None:
            return self.items[self.selected]
        else:
            #if we have a sub menu we instead get the option from that
            return self.subMenu.getOption()
    def onS(self):
        "sets to info mode"
        self.info = not self.info
class TradeMenu(Menu):
    "Trade Menu class - allows for trade"
    def __init__(self, x=0,y=0,width=0,height=0,background=Surface((1,1)),selected=0,items=[]):
        "initialize trade menu"
        super(TradeMenu,self).__init__(x,y,width,height,background,selected,items)
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
                drawItem(people[p],opt,self.x*30+p*(self.width+30),(self.y+i)*30)
        if self.firstSelection != None:
            screen.blit(pointer,(self.x*30+self.firstSelection[0]*(self.width+30)-30,(self.y+self.firstSelection[1])*30))
            draw.rect(screen,WHITE,(self.x*30+self.firstSelection[0]*(self.width+30),(self.y+self.firstSelection[1])*30,self.width,30),1) #draws a border around the first option
        screen.blit(pointer,(self.x*30+self.selectedPerson*(self.width+30)-30,(self.y+self.selected)*30))
        draw.rect(screen,WHITE,(self.x*30+self.selectedPerson*(self.width+30),(self.y+self.selected)*30,self.width,30),1) #draws border around selected option
        if self.info:
            ix = self.x*30+self.selectedPerson*(self.width+30)+250
            y = (self.y+self.selected)*30
            drawInfoBox(screen,ix,y,self.items[self.selectedPerson][self.selected])
categories = ["Sword","Lance","Axe","Bow","Staff","Anima","Light","Dark","Others"]
class TransferScreen():
    "screen where user transfers items from Henning"
    def __init__(self,p):
        self.p = p #the person selected
        self.selAct = 0 #selected action (Give or Take)
        self.selItem = 0 #index of selected item
        self.selCat = 0 #selected category (swords,lances,axes,bows,staves,anima,light,dark,others)
        self.shownItems = [i for i in henning.supply if i.typ == "Sword"] #shown items start off as non weapons
        self.startPoint = 0 #starting point for items to display
        self.mode = "select" #mode of transfer screen(select,give,take)
        self.info = False
    def changeCat(self,diff):
        "changes category - also updates shownItems"
        self.selCat += diff
        #wraps around
        if self.selCat >= 9:
            self.selCat = 0
        elif self.selCat < 0:
            self.selCat = 8
        self.setShownItems()
        self.startPoint = 0
        self.selItem = 0
    def setShownItems(self):
        "sets shown items"
        self.shownItems = [i for i in henning.supply if i.typ == categories[self.selCat] or (categories[self.selCat] == "Others" and i.typ not in categories)]
    def moveSelItem(self,diff):
        "changes the selected item (for take mode only)"
        if len(self.shownItems) == 0:
            return 0
        self.selItem += diff
        self.selItem = min(max(self.selItem,0),len(self.shownItems)-1) #limits selected item
        if self.selItem >= self.startPoint + 10:
            self.startPoint += self.selItem - self.startPoint - 9 #moves startpoint if the selected item is too much bigger than the startpoint it goes up
        if self.selItem < self.startPoint:
            self.startPoint = self.selItem #moves startpoint up
    def draw(self):
        "draws the transfer screen"
        screen.blit(trnsferBG,(0,0))
        screen.blit(superScript40.render(str(len(henning.supply)),True,WHITE),(960,60))
        draw.rect(screen,YELLOW,(632+61*self.selCat,120,60,60),2) #draws yellow around selected category
        for i in range(len(self.p.items)):
            #draws the item
            item = self.p.items[i]
            drawItem(self.p,item,80,330+60*i,350)
        for i in range(self.startPoint,min(len(self.shownItems),self.startPoint+10)):
            #draws all items in supply from startPoint to 10 more
            drawItem(self.p,self.shownItems[i],640,190+(i-self.startPoint)*30)
        drawTransRect(screen,BLACK,0,680,1200,40)
        if self.mode == "select":
            screen.blit(pointer,(300,165+75*self.selAct))
            draw.rect(screen,WHITE,(330,165+75*self.selAct,216,75),1)
            screen.blit(sans.render("Z to select an option; X to cancel; Arrow keys to change option",True,WHITE),(0,680))
        if self.mode == "give":
            draw.rect(screen,RED,(330,165,216,75),1)
            if len(self.p.items) != 0:
                screen.blit(pointer,(50,330+60*self.selItem))
                draw.rect(screen,WHITE,(80,330+60*self.selItem,480,30),1)
                if self.info:
                    ix = 80
                    y = 330+60*self.selItem+60
                    opt = self.p.items[self.selItem]
                    drawInfoBox(screen,ix,y,opt)
            screen.blit(sans.render("Z to give an item; X to cancel; Arrow keys to change item",True,WHITE),(0,680))
        if self.mode == "take":
            draw.rect(screen,RED,(330,240,216,75),1)
            if len(self.shownItems) != 0:
                screen.blit(pointer,(610,190+(self.selItem-self.startPoint)*30))
                draw.rect(screen,WHITE,(640,190+(self.selItem-self.startPoint)*30,530,30),1)
                if self.info:
                    opt = self.shownItems[self.selItem]
                    ix = 640
                    y = 190+(self.selItem-self.startPoint)*30+30
                    drawInfoBox(screen,ix,y,opt)
            screen.blit(sans.render("Z to take an item; X to cancel; Arrow keys to change item",True,WHITE),(0,680))
        
    def onZ(self):
        "handles clicks"
        if self.mode == "select":
            opts = ["give","take"]
            self.selItem = 0
            self.mode = opts[self.selAct]
        elif self.mode == "give":
            if len(self.p.items) == 0:
                return 0 #can't do anything if no person has no items
            if len(henning.supply) >= 100:
                return 0 #can't do anything if henning has too many items
            item = self.p.items[self.selItem]
            self.p.removeItem(item)
            henning.supply.append(item)
        elif self.mode == "take":
            if len(self.shownItems) == 0:
                return 0 #can't do anything if no shown items
            if len(self.p.items) >= 5:
                dispTempMsg(screen,"Inventory Full",centerX=True,centerY=True)
                return 0 #can't take anything if inventory full
            item = self.shownItems[self.selItem]
            self.p.addItem(item)
            henning.supply.remove(item)
            self.selItem -= 1
            if self.selItem < 0:
                self.startPoint -= 1
            self.startPoint = max(0,self.startPoint)
            self.selItem = max(0,self.selItem)
        self.setShownItems() #resets shown Items
    def onX(self):
        "handles back tracing"
        if self.mode in ["give",'take']:
            self.mode = "select"
            self.info = False
            return True
        return False #returns false to exit transfer screen
    def handleMove(self):
        "handles keyboard moves"
        kp = key.get_pressed()
        if self.mode == "select":
            if kp[K_UP]:
                self.selAct -= 1
            if kp[K_DOWN]:
                self.selAct += 1
            if self.selAct < 0:
                self.selAct = 1
            if self.selAct > 1:
                self.selAct = 0
        elif self.mode == "give":
            if kp[K_UP]:
                self.selItem -= 1
            if kp[K_DOWN]:
                self.selItem += 1
            if self.selItem >= len(self.p.items):
                self.selItem = 0
            elif self.selItem < 0:
                self.selItem = len(self.p.items)-1
        elif self.mode == "take":
            if kp[K_UP]:
                self.moveSelItem(-1)
            if kp[K_DOWN]:
                self.moveSelItem(1)
            if kp[K_RIGHT]:
                self.changeCat(1)
            if kp[K_LEFT]:
                self.changeCat(-1)
    def onS(self):
        "handles s clicks"
        self.info = not self.info #reverses self.info
class VillageScreen():
    "village screen class"
    def __init__(self,visitor,village):
        "dialogue is a string telling where to search for the story"
        self.visitor = visitor
        self.item = village.item
        self.dialogue = open(village.story).read().strip().replace("*Visitor*",self.visitor.name).split("\n")[1:]
        self.limit = len(self.dialogue)
        self.background = image.load(open(village.story).readline().strip())
        self.currDial = 0
        self.cond = False
    def draw(self):
        "draws the dialogue"
        pass
    def run(self,screen):
        "runs the story dialogue"
        global running
        visiting = True
        while visiting:
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
            cM = False #boolean: to break or not

            ##blitting the text across the screen 1 by 1
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
                visiting = False
                preposition = "a " if self.item.name[0].lower() not in "aeiou" else "an "
                dispTempMsg(screen,"Received "+preposition+self.item.name,centerX=True,centerY=True)
                if len(self.visitor.items) < 5:
                    self.visitor.addItem(self.item)
                else:
                    itemOverflow(self.visitor,self.item) #handles the overflow
                break

class ShopScreen():
    "shop screen class"
    def __init__(self,p,items,vendor=False):
        self.p = p
        self.items = items
        if vendor:
            self.typ = "vendor"
        else:
            self.typ = "armory"
        self.mode = "select" #different modes - select, sell or buy
        self.selAct = 0 #selected action (buy or sell)
        self.selItem = 0 #selected item
        self.info = False
    def handleMove(self):
        "handles arrow keys"
        kp = key.get_pressed()
        if self.mode == "select":
            if kp[K_LEFT]:
                self.selAct -= 1
            if kp[K_RIGHT]:
                self.selAct += 1
            if self.selAct < 0:
                self.selAct = 1
            elif self.selAct > 1:
                self.selAct = 0 #wraps around
        if self.mode in ["buy","sell"]:
            limit = len(self.items) if self.mode == "buy" else len(self.p.items)
            if kp[K_UP]:
                self.selItem -= 1
            if kp[K_DOWN]:
                self.selItem += 1
            self.selItem = min(limit-1,max(0,self.selItem))
    def onS(self):
        "handles s clicks"
        self.info = not self.info #reverses self.info
    def draw(self):
        "draws the screen"
        bgs = [armorySelect,armorySelect2] if self.typ == "armory" else [vendorSelect,vendorSelect2] #backgrounds
        itms = [] #items to write
        if self.mode == "select":
            if self.selAct:
                #sell mode
                screen.blit(bgs[1],(0,0))
            else:
                #buy mode
                screen.blit(bgs[0],(0,0))        
        if self.mode == "buy":
            screen.blit(bgs[0],(0,0))
            itms = self.items
        if self.mode == "sell":
            screen.blit(bgs[1],(0,0))
            itms = self.p.items
        for i in range(len(itms)):
            drawItem(self.p,itms[i],290,330+60*i,320,superScript40)
            cst = itms[i].getCost()
            cst = cst//2 if self.mode == "sell" else cst
            screen.blit(superScript40.render(str(cst)+"G",True,WHITE),(840,330+60*i))
        if self.mode in ["buy","sell"]:
            screen.blit(pointer,(260,330+60*self.selItem))
            draw.rect(screen,WHITE,(290,330+60*self.selItem,720,60),1)
            if self.info and len(itms) > self.selItem:
                drawInfoBox(screen,290,390+60*self.selItem,itms[self.selItem])
        screen.blit(superScript40.render(str(gold),True,WHITE),(885,230)) #blits gold
        drawTransRect(screen,BLACK,0,680,1200,40)
        if self.mode == "select":
            screen.blit(sans.render("Z to select an option; X to cancel; Arrow keys to change option",True,WHITE),(0,680))
        elif self.mode == "buy":
            screen.blit(sans.render("Z to buy item; X to cancel; Arrow keys to change item",True,WHITE),(0,680))
        elif self.mode == "sell":
            screen.blit(sans.render("Z to sell item; X to cancel; Arrow keys to change item",True,WHITE),(0,680))
    def onZ(self):
        "handles z click"
        global gold
        if self.mode == "select":
            self.mode = ["buy","sell"][self.selAct]
            if self.mode == "sell" and len(self.p.items) == 0:
                self.onX()
                dispTempMsg(screen,"No items to sell",centerX=True,centerY=True,fnt=superScript40)
        elif self.mode == "buy":
            if gold >= self.items[self.selItem].getCost():
                #can buy
                if len(self.p.items) < 5:
                    self.p.addItem(self.items[self.selItem])
                gold -= self.items[self.selItem].getCost()
            else:
                dispTempMsg(screen,"Can't buy - no money",centerX=True,centerY=True,fnt=superScript40)
            if len(self.p.items) >= 5:
                itemOverflow(self.p,self.items[self.selItem]) #handles the overflow
        elif self.mode == "sell":
            gold += self.p.items[self.selItem].getCost()//2
            self.p.removeItem(self.p.items[self.selItem]) #removes the item
            if self.selItem >= len(self.p.items):
                self.selItem -= 1
                self.selItem = max(0,self.selItem)
            if len(self.p.items) == 0:
                self.onX() #goes back to select if no items to sell
    def onX(self):
        "handles x clicks - returns False if need to change mode"
        if self.mode in ["buy","sell"]:
            self.mode = "select"
            self.selItem = 0
            return True
        return False
    def onS(self):
        "handles s clicks"
        self.info = not self.info #reverses self.info
class InfoScreen():
    "mode that displays information about a character"
    def __init__(self,p):
        self.p = p #person info is about
        self.mode = "stats" #different mods of info: stats, items, mastery
        self.info = False #if the info display is on
        self.sel = 0 #selected piece of data - for info mode display
    def handleMove(self):
        "handles movements with arrow keys and the keyboard in general"
        kp = key.get_pressed()
        if self.info:
            if kp[K_UP]:
                self.sel -= 1
            if kp[K_DOWN]:
                self.sel += 1
            self.sel = max(0,min(len(self.p.items)-1,self.sel))
            return 0
        if kp[K_UP] or kp[K_DOWN]:
            #changes selected person
            cm = currmode
            pList = allies if self.p in allies else enemies
            ind = pList.index(self.p)
            ind += 1 if kp[K_DOWN] else -1
            if ind < 0:
                ind = len(pList)-1
            if ind >= len(pList):
                ind = 0
            self.p = pList[ind]
            cm.selectx,cm.selecty = self.p.x,self.p.y
        elif kp[K_RIGHT] or kp[K_LEFT]:
            #changes mode
            modes = ["stats","items","mastery"]
            ind = modes.index(self.mode)
            ind += 1 if kp[K_RIGHT] else -1
            if ind > 2:
                ind = 0
            if ind < 0:
                ind = 2
            self.mode = modes[ind]
    def onS(self):
        "handles s clicks"
        if self.mode == "items":
            self.info = not self.info
            self.sel = 0
    def draw(self):
        "draws the screen"
        a = self.p #selected ally
        if self.mode == "stats":
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
            
        if self.mode == "items":
            screen.blit(itemsInfoBG,(0,0)) #blits items background
            for i in range(len(a.items)):
                drawItem(a,a.items[i],540,115+i*60,360,superScript40)
            if self.info:
                drawInfoBox(screen,540,115+60*self.sel+60,a.items[self.sel])
                screen.blit(pointer,(490,115+60*self.sel))
            atk=hit=rng=crit="--"
            avo = str(a.getAtkSpd()*2 + a.lck)
            if a.equip != None:
                atk = str(a.stren + a.equip.mt)
                hit = str(a.skl*2 + a.lck//2 + a.equip.acc)
                rng = str(a.equip.rnge)
                if a.equip.maxrnge != a.equip.rnge:
                    rng += "-"+str(a.equip.maxrnge)
                crit = str(a.skl//2 + a.equip.crit)
            coords = [(690,560),(690,630),(1010,490),(1010,560),(1010,630)]
            stats = [atk,hit,rng,crit,avo]
            for i in range(5):
                x,y = coords[i]
                screen.blit(superScript40.render(stats[i],True,WHITE),(x,y))
        if self.mode == "mastery":
            screen.blit(mastBG,(0,0))
            coords = {"Sword":(620,120),"Lance":(620,190),"Anima":(620,300),"Light":(620,370),"Axe":(940,120),"Bow":(940,190),
                      "Dark":(940,300),"Staff":(940,370)}
            for i,k in enumerate(a.mast):
                x,y = coords[k]
                screen.blit(superScript40.render("FEDCBAS"[a.mast[k]//100],True,WHITE),(x,y))
        screen.blit(transform.scale(a.face,(360,320)),(75,32))
        screen.blit(superScript40.render(a.name,True,BLACK),(144,381)) #blits name of the selected unit
        screen.blit(superScript40.render(a.__class__.__name__,True,WHITE),(15,485))
        screen.blit(superScript40.render("LV "+str(a.lv)+" EXP "+str(a.exp),True,WHITE),(15,555))
        screen.blit(superScript40.render("HP "+str(a.hp)+"/"+str(a.maxhp),True,WHITE),(15,610))
        drawTransRect(screen,BLACK,0,680,1200,40)
        msg = "Side arrow keys to change page; Up and down arrow key to change character; X to return"
        if self.mode == "items":
            msg += "; S to check item info"
        if self.info:
            msg = "Up and down arrow keys to view different item; S to exit info mode; X to return"
        screen.blit(sans.render(msg,True,WHITE),(0,680))
#----MODE CLASSES----#
#these classes are the different modes for the scren - must be in the main
class StartMenu():
    "start menu mode"
    def __init__(self):
        "sets button list of mode"
        self.stopped = False
        #BUTTON SPRITES
        self.buttonnormal = transform.smoothscale(image.load("images/Buttons/button.png").convert_alpha(),(200,50))
        self.buttonnormalstretch = transform.smoothscale(self.buttonnormal,(300,50))
        self.buttonhl = transform.smoothscale(image.load("images/Buttons/buttonhl.png").convert_alpha(),(200,50))
        self.buttonhlstretch = transform.smoothscale(self.buttonhl,(300,50))
        self.buttons = [Button(500,420,200,50,
                               FilledSurface((200,50),self.buttonnormal,"START",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),self.buttonhl,"START",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),self.buttonhl,"START",WHITE,monospace,(30,10)),
                               ["changemode(LoadGame())"]),
                        Button(450,490,300,50,
                               FilledSurface((300,50),self.buttonnormalstretch,"INSTRUCTIONS",BLACK,monospace,(30,10)),
                               FilledSurface((300,50),self.buttonhlstretch,"INSTRUCTIONS",BLACK,monospace,(30,10)),
                               FilledSurface((300,50),self.buttonhlstretch,"INSTRUCTIONS",WHITE,monospace,(30,10)),
                               ["changemode(InstructionScreen())"])] #Start button and Instruction button

    def draw(self,screen):
        "draws mode on screen"
        screen.blit(transform.smoothscale(image.load("images/backgrounds/StartMenu.jpeg"),(1200,720)),(0,0))
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
class InstructionScreen():
    "instruction screen"
    def __init__(self):
        self.stopped = False
        self.currDial = 0
        #buttons are BACK, SKIP, MENU
        #the func will be changing currmode.background
        #running loop will continuously blit background
 #       self.backgrounds = [image.load("instructions/backgrounds/instructionscreen"+str(i)+".png")for i in range (2)]
        self.buttons = [Button(500,420,200,50,
                               FilledSurface((200,50),RED,"Menu",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"Menu",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),GREEN,"Menu",BLACK,monospace,(30,10)),
                               ["changemode(StartMenu())"]),
                        Button(710,420,200,50,
                               FilledSurface((200,50),RED,"Skip",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"Skip",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),GREEN,"Skip",BLACK,monospace,(30,10)),
                               ["currmode.currDial += 1"]),
                        Button(920,420,200,50,
                               FilledSurface((200,50),RED,"Back",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),YELLOW,"Back",BLACK,monospace,(30,10)),
                               FilledSurface((200,50),GREEN,"Back",BLACK,monospace,(30,10)),
                               ["currmode.currDial -= 1"])
                               ]
        #dialogue is in form of either:
        #image (the background)
        #:text to display
        self.dialogue = open("instructions/instructiontext.txt").read().strip().split("\n")
        self.limit = len(self.dialogue)
        
        pass
    def draw(self,screen):
        "draws the initial screen"
        #pass since display and dialogue format handles this
        pass
    def playMusic(self):
        "plays instruction music"
        pass
    def run(self,screen):
        "runs the mode as if it were in the running loop"
        global running
        for e in event.get():
            if e.type == QUIT:
                running = False #quits
            if e.type == MOUSEBUTTONDOWN:
                #checks if user clicked any buttons
                for b in self.buttons:
                    if b.istouch():
                        b.click()
        if self.currDial <=  len(self.dialogue):
            self.display(screen)
        if self.stopped:
                return 0 #stops the method once stopped
        for b in self.buttons:
            b.draw(screen)

    def display(self,screen):
        "displays the instructions, based on which line the self.currdial is on"
        global running
        sentence = self.dialogue[self.currDial] #sentence to display
        cM = False #boolean: change mode?
        if sentence[0] != ":":
            screen.blit(image.load(sentence),(0,0))
            self.currDial += 1
        if sentence[0] == ":":
            sentence = sentence[1:]
            breakLoop = False
            #checking if the user is skipping through text
            kp = key.get_pressed()
            if not writeDialogue(screen,sentence):
                return 0
            arrowflashcounter = 0
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
                    if e.type == MOUSEBUTTONDOWN:
                        #checks if user clicked any buttons
                        for b in self.buttons:
                            if b.istouch():
                                b.click()
                                return 0
                            
                #tiny instructions with flashing arrow
                draw.rect(screen,BLUE,(0,690,1200,30)) #might have to be subsurface
                botinstruct = sans.render("Z to continue, X or Enter to Skip",True,WHITE) if int(arrowflashcounter)%2 else sans.render("Z to continue, X or Enter to Skip V",True,WHITE)
                screen.blit(botinstruct,(0,690))
                arrowflashcounter += 0.15
                for b in self.buttons:
                    b.draw(screen)
                display.flip()
                fpsLimiter.tick(60) #limits to 60 FPS
        if self.currDial >= self.limit or cM:
            changemode(StartMenu())
            

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
        #sets the button text based on which files have data
        button1Text = getSavedChapter(self.file1)
        button2Text = getSavedChapter(self.file2)
        button3Text = getSavedChapter(self.file3)
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

        button1Text = getSavedChapter(self.file1)
        button2Text = getSavedChapter(self.file2)
        button3Text = getSavedChapter(self.file3)

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
{'stand':playerMageStandSprite,'Anima':playerMageAnimaSprite,'Animacrit':playerMageAnimacritSprite},faces['Player'],deathQuote='Tactical error... time to restart.')
addAlly(player)
""",
                                "changemode(getStory(chapter))"]),
                         
                         Button(600,300,200,50,
                                FilledSurface((200,50),BLUE,"KNIGHT",WHITE,monospace,(40,10)),
                                FilledSurface((200,50),YELLOW,"KNIGHT",BLACK,monospace,(40,10)),
                                FilledSurface((200,50),GREEN,"KNIGHT",BLACK,monospace,(40,10)),
                                ["global player",
                                 """player = Knight(name,0,0,{"lv":1,"hp":26,"maxhp":26,"stren":7,"defen":8,"spd":5,"res":0,"skl":6,"lck":4,"con":12,"move":4},
{"stren":55,"defen":50,"skl":45,"lck":40,"spd":30,"res":15,"maxhp":65},
[iron_lance.getInstance(),vulnerary.getInstance()],
{"Lance":200},
{"Lance":playerKnightLanceSprite,"Lancecrit":playerKnightLancecritSprite,"stand":playerKnightStandSprite},faces['Player'],deathQuote='Tactical error... time to restart.')
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
                    if kp[K_RETURN] and len(name) > 0 and name.lower() in usedNames:
                        dispTempMsg(screen,"Name is unavailable",centerX=True,centerY=True)
                    
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
    def run(self,screen):
        "runs the story dialogue"
        global running
        event.clear()
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
        arrowflashcounter = 0
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
                        
            #tiny instructions with flashing arrow
            draw.rect(screen,BLUE,(0,690,1200,30)) #might have to be subsurface
            botinstruct = sans.render("Z to continue, X or Enter to Skip",True,WHITE) if int(arrowflashcounter)%2 else sans.render("Z to continue, X or Enter to Skip V",True,WHITE)
            screen.blit(botinstruct,(0,690))
            arrowflashcounter += 0.15
            
            display.flip()
            fpsLimiter.tick(60) #limits to 60 FPS
        if self.currDial >= self.limit or cM:
            if self.end:
                changemode(SaveGame()) #we change to savegame if it's the end
            else:
                #once we hit the limit we transition to the game mode
                changemode(Game())
class VillageStory(Story):
    def __init__(self,dialogue,background,music=None,end=False):
        super(VillageStory,self).__init__(self,dialogue,background,music=None,end=False)
    
class Game():
    def __init__(self):
        "initializes game"
        self.selectx,self.selecty = 0,0 #select cursor starting point
        self.framecounter = 0
        self.clickedFrame = -1 #the frame user clicked (pressed z)
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
        self.transferScreen = None #transfer screen
        self.infoScreen = None #info screen
        self.shopScreen = None #shop screen
        self.stopped = False #we are not stopped
        self.currAlly = 0 #for cycling
        self.staffableSquares = []
        self.attackableSquares = []
        self.moveableSquares = []
        self.oldGold=gold
    def draw(self,screen):
        "draws game on screen - also starts game"
        self.start()
        self.filler = screen.copy() #filler
    def getPath(self,ms,endx,endy):
        "Gets path"
        coords = [(x,y) for x,y,m,ali in ms]
        spot = -1
        for i in range(len(coords)):
            if coords[i] == (endx,endy):
                spot = i
        if spot == -1:
            return [] #return nothing
        steps = [ali for x,y,m,ali in ms][spot] #steps = the coords to get to the steps
        if len(steps) == 1:
            return [] #returns nothing for own spot
        return steps
    def animWalk(self,p,ms,x,y):
        "uses ms for moveablesquares and x and y for end point"
        #WIP!!!
 #       draw.rect(screen,GREEN,(self.selected.x*30,self.selected.y*30,30,30)) #coverup to cover the character when animated
        screen.blit(self.filler,(0,0))
        self.drawPeople([a for a in allies if a != p],[e for e in enemies if e != p])
        snap = screen.copy()
        num = 0 #number of frame to show
        for cord in self.getPath(ms,x,y):
            screen.blit(snap,(0,0))
            if p in allies:
                screen.blit(allyMapSprites[p.__class__.__name__][num%4],(cord[0]*30,cord[1]*30))
            else:
                screen.blit(enemyMapSprites[p.__class__.__name__][num%4],(cord[0]*30,cord[1]*30)) 
            display.flip()                
            if handleEvents(event.get()):
                quit()
            time.wait(100)
            num += 1
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
    def drawArrow(self,ms,x,y):
        "draws an arrow from self.selected.x,y to self.selectx,y"
        #WIP - find smart way to figure out which one to draw using indices of 2x2 array
        steps = [(self.selected.x,self.selected.y)]+self.getPath(ms,x,y)
        if len(steps) == 1:
            return 0

        #steps includes the self character x&y
        
        #loop through each, check the next one and previous one to see which one of the three to draw
        for i in range (2,len(steps)-1):
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
        if henning not in allAllies and chapter > 0:
            allAllies.append(henning)
        for a in allAllies:
            #brings all allies back to full health
            a.hp = a.maxhp
            a.stats["hp"] = a.maxhp
        changemode(getStory(chapter,True))
    def drawPeople(self,alliesToDraw=None,enemiesToDraw=None):
        "draws all people on the map"
        alliesToDraw = allies if alliesToDraw==None else alliesToDraw
        enemiesToDraw = enemies if enemiesToDraw==None else enemiesToDraw
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
        global allies,enemies,oldAllies,gold
        self.currAlly = 0
        gold = self.oldGold
        newAllies,allyCoords,newenemies,self.goal,backgroundImage = chapterData[chapter]
        if chapter < 99:
            #the early chapters have no prefight screen to load oldAllies so allAllies are oldAllies
            oldAllies = [a.getInstance() for a in allAllies]
        enemies = [e.getInstance() for e in newenemies]
        allies = [a.getInstance() for a in oldAllies]
        allies += [a.getInstance() for a in newAllies] #adds all new allies to allies
        for i in range(len(allyCoords)):
            global player
            if i >= len(allies):
                break #we stop have too many coordinates
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
        for y in range(len(chapterMaps[chapter])):
            for x in range(len(chapterMaps[chapter])):
                if type(chapterMaps[chapter][y][x]) == Village:
                    chapterMaps[chapter][y][x].visited = False
        drawMap(chapterMaps[chapter])#draws all terrain
        drawGrid(screen)
        self.selectx,self.selecty = yoyo.x,yoyo.y
        self.startTurn()
    def startTurn(self):
        "starts the turn"
        global allies,enemies
        screenBuff = screen.copy() #sets the screenBuffer to cover up the text
        self.moved.clear() #empties moved and attacked
        self.attacked.clear()
        self.drawPeople()
        screen.blit(transform.scale(transBlue,(1200,60)),(0,330)) #blits the text "PLAYER PHASE" on a translucent blue strip
        screen.blit(papyrus.render("PLAYER PHASE",True,WHITE),(450,340))
        screen.blit(screenBuff,(0,0)) #covers up text
        display.flip() #updates screen
        time.wait(1000)
        for a in allies:
            aterr = a.getTerrain(chapterMaps[chapter])
            a.movesLeft = a.move
            if aterr.heal != 0 and a.hp < a.maxhp:
                screen.blit(screenBuff,(0,0))
                draw.rect(screen,YELLOW,(a.x*30,a.y*30,30,30),2)
                display.flip()
                time.wait(500)
                if handleEvents(event.get()):
                    quit()
                drawChangingBar(screen,a.hp,a.hp+aterr.heal,a.maxhp,420,330,390,60,"Hp",False)
                a.hp = min(a.hp+aterr.heal,a.maxhp)
        for e in enemies:
            e.movesLeft = e.move
        screen.blit(screenBuff,(0,0)) #covers up text
        display.flip()
        if handleEvents(event.get()):
            quit()
        self.mode = "freemove" #sets the mode back to freemove
    def endTurn(self):
        "ends the turn, starts the enemy turn"
        global running
        self.turn += 1 #increases turn by 1
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
            draw.rect(screen,YELLOW,(en.x*30,en.y*30,30,30),2)
            eterr = en.getTerrain(chapterMaps[chapter])
            if eterr.heal != 0 and en.hp < en.maxhp:
                display.flip()
                time.wait(500)
                if handleEvents(event.get()):
                    quit()
                drawChangingBar(screen,en.hp,en.hp+eterr.heal,en.maxhp,420,330,390,60,"Hp",False,RED)
                en.hp = min(en.hp+eterr.heal,en.maxhp)
            display.flip()
            time.wait(200)
            encoords = [(e.x,e.y) for e in enemies] #enemies' coordinates
            acoords = [(a.x,a.y) for a in allies] #allies' coordinates
            enemyMoves = getMoves(en,en.x,en.y,en.movesLeft,chapterMaps[chapter],encoords,acoords,{}) #enemy's moveableSquares
            if en.throne:
                enemyMoves = [(en.x,en.y,en.move,[(en.x,en.y)])] #throne guard can't move
            enMoves = [(x,y) for x,y,m,ali in enemyMoves]
            action = getEnemyAction(en,chapterMaps[chapter],allies,enMoves)
            if action == "attack":
                attackableSquares = getAttackableSquaresByMoving(enMoves,en) #attackableSquares by moving
                attackableAllies = [a for a in allies if (a.x,a.y) in attackableSquares]
                bestAlly,bestX,bestY = getOptimalAlly(en,chapterMaps[chapter],attackableAllies,enMoves)
                self.animWalk(en,enemyMoves,bestX,bestY)
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
                bestPath = pathtoAlly(en,chapterMaps[chapter],allies,enemies)
                if bestPath != -1:
                    bestSquare = enMoves[0]
                    for i in range(len(bestPath)-1,-1,-1):
                        x,y = bestPath[i]
                        if (x,y) in enMoves:
                            bestSquare = (x,y)
                            break #go as far along the path as we are able to, in order to get best spot
                    (bestX,bestY) = bestSquare
                    self.animWalk(en,enemyMoves,bestX,bestY)
                    en.x,en.y = bestX,bestY
            elif action == "stay":
                pass
            display.flip()
            time.wait(500)
            self.moved.add(en)
            self.attacked.add(en)
            fpsLimiter.tick(60)
        self.moved.clear()
        self.attacked.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        event.clear()
        if len(enemies) == 0 and self.goal.lower() == "defeat all enemies":
            #no more enemies means the player won
            self.mode = "gameVictory"
            self.gameVictory()
            return 0
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
        if self.selected not in self.attacked:
            #SEIZE OPTION
            if self.selected == yoyo:
                #only yoyo can seize
                terr = self.selected.getTerrain(chapterMaps[chapter])
                if terr.name.lower() == "gate" and self.goal.lower() == "seize gate":
                    self.menu.items.append("seize")
                elif terr.name.lower() == "throne" and self.goal.lower() == "seize throne":
                    self.menu.items.append("seize")
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
            #STAFF OPTION
            if not self.selected in self.attacked:
                for stf in [i for i in self.selected.items if type(i) == Staff]:
                    #checks every staff and sees if we can equip it
                    if not self.selected.canEquip(stf):
                        continue
                    if len(getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)) > 0 and stf.heal != 0:
                        self.menu.items.append("staff")
                        break
            #STEAL OPTION
            if type(self.selected) == Thief and len(self.selected.items) < 5:
                units = getUnitsWithinRange(self.selected.x,self.selected.y,1,1,enemies)
                for u in units:
                    if u.spd <= self.selected.spd and len([i for i in u.items if type(i) != Weapon]) > 0:
                        self.menu.items.append("steal")
                        break
            #VENDOR/ARMORY OPTION
            if self.selected.getTerrain(chapterMaps[chapter]).name.lower() in ["vendor","armory"]:
                opt = "vendor" if self.selected.getTerrain(chapterMaps[chapter]).name.lower() == "vendor" else "armory"
                self.menu.items.append(opt)
            #VILLAGE OPTION
            if self.selected.getTerrain(chapterMaps[chapter]).name.lower() == "village":
                if not self.selected.getTerrain(chapterMaps[chapter]).visited:
                    self.menu.items.append("visit")
        #ITEM OPTION
        if len(self.selected.items) > 0:
            self.menu.items.append("item")
        #TRADE OPTION
        if len(getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)) > 0:
            self.menu.items.append("trade") #we can only trade if we have targetable allies within range 1
        #TRANSFER OPTION
        if getDistance(self.selected.x,self.selected.y,henning.x,henning.y) <= 1:
            #allows for access to supply with proximity to henning
            self.menu.items.append("transfer")
        #VILLAGE OPTION
        if 0 == 0:
            pass
        #WAIT OPTION
        self.menu.items.append("wait") #a person can always wait
    def setMoveableSquares(self,p,isally):
        "gets ally moves"      
        acoords = [(a.x,a.y) for a in allies]
        encoords = [(e.x,e.y) for e in enemies]
        self.staffableSquares = []
        if isally:
            self.moveableSquares = getMoves(p,p.x,p.y,p.movesLeft,chapterMaps[chapter],acoords,encoords,{})
            self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],p)
            if self.attackableSquares:
                #we get all attackable squares that we cannot move to
                self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m,ali in self.moveableSquares] and sq not in acoords]
            if not self.attackableSquares and len([i for i in p.items if type(i) == Staff and p.canEquip(i)]) > 0:
                self.staffableSquares = [sq for sq in getTargetableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],1,1) if sq not in encoords]
        else:
            self.moveableSquares = getMoves(p,p.x,p.y,p.movesLeft,chapterMaps[chapter],encoords,acoords,{})
            self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],p)
            if self.attackableSquares:
                #we get all attackable squares that we cannot move to
                self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m,ali in self.moveableSquares] and sq not in encoords]
            if not self.attackableSquares and len([i for i in p.items if type(i) == Staff and p.canEquip(i)]) > 0:
                self.staffableSquares = [sq for sq in getTargetableSquaresByMoving([(x,y) for x,y,m,ali in self.moveableSquares],1,1) if sq not in acoords]
        if p in self.attacked:
            self.attackableSquares = []
            self.staffableSquares = []
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
                    self.selectx,self.selecty = self.targetableAllies[self.selectedAlly].x,self.targetableAllies[self.selectedAlly].y
                elif self.mode == "trade":
                    #if we have a selected2 we move the item selector instead
                    self.menu.moveSelect()
                #----STEAL MODE
                elif self.mode == "steal1":
                    if kp[K_UP] or kp[K_LEFT]:
                        self.selectedEnemy -= 1
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        self.selectedEnemy += 1
                    if self.selectedEnemy >= len(self.targetableEnemies):
                        self.selectedEnemy = 0
                    if self.selectedEnemy < 0:
                        self.selectedEnemy = len(self.targetableEnemies)-1
                    self.selectx,self.selecty = self.targetableEnemies[self.selectedEnemy].x,self.targetableEnemies[self.selectedEnemy].y
                elif self.mode == "steal2":
                    self.menu.moveSelect()
                #----TRANSFER MODE
                elif self.mode == "transfer":
                    self.transferScreen.handleMove()
                    if 1 in kp:
                        self.clickedFrame = self.framecounter
                #----INFO MODE
                elif self.mode == "info":
                    self.infoScreen.handleMove()
                #----VENDOR/ARMORY MODE
                elif self.mode in ["vendor","armory"]:
                    self.shopScreen.handleMove()
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
                                self.oldM = p.movesLeft #old moves left
                                if p in allies:
                                    #we get movements below
                                    self.setMoveableSquares(p,True)
                                elif p in enemies:
                                    self.setMoveableSquares(p,False)
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
                            self.animWalk(self.selected,self.moveableSquares,self.selectx,self.selecty)
                            self.selected.x,self.selected.y = self.selectx,self.selecty
                            if self.selected.mounted:
                                self.selected.movesLeft = [m for x,y,m,ali in self.moveableSquares if (x,y) == (self.selected.x,self.selected.y)][0]
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
                        if self.menu.getOption().lower() == "seize":
                            self.gameVictory()
                            return 0
                        if self.menu.getOption().lower() == "attack":
                            self.mode = "itemattack"
                            self.menu.selected = 0
                            self.menu.items = [i for i in self.selected.items if type(i) == Weapon]
                            self.menu.height = 30*len(self.menu.items)
                        elif self.menu.getOption().lower() == "item":
                            self.mode = "item"
                            self.menu.selected = 0
                            self.menu.items = self.selected.items
                            self.selectedItem = None
                        elif self.menu.getOption().lower() == "staff":
                            self.mode = "itemstaff"
                            self.menu.selected = 0
                            self.menu.items = [i for i in self.selected.items if type(i) == Staff]
                        elif self.menu.getOption().lower() == "trade":
                            self.mode = "trade"
                            self.selectedAlly = 0
                            self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                            self.selectx,self.selecty = self.targetableAllies[self.selectedAlly].x,self.targetableAllies[self.selectedAlly].y
                        elif self.menu.getOption().lower() == "transfer":
                            self.mode = "transfer"
                            self.transferScreen = TransferScreen(self.selected)
                        elif self.menu.getOption().lower() in ["vendor","armory","visit"]:
                            self.mode = self.menu.getOption().lower()
                            isvendor = self.mode == "vendor" #is it a vendor?
                            isvillage = self.mode == "visit" #is it a village?
                            if not isvillage:
                                self.shopScreen = ShopScreen(self.selected,chapterMaps[chapter][self.selected.y][self.selected.x].items,isvendor)
                            else:
                                vill = self.selected.getTerrain(chapterMaps[chapter])
                                vill.visited = True
                                villageScreen = VillageScreen(self.selected,vill) #creates the dialogue
                                villageScreen.run(screen) #runs the dialogue
                                self.mode = "move" #resets everything
                                self.attacked.add(self.selected)
                                self.oldX,self.oldY = self.selected.x,self.selected.y
                                self.oldM = self.selected.movesLeft
                                if not self.selected.mounted or self.selected.movesLeft == 0:
                                    self.moved.add(self.selected)
                                    self.mode = "freemove"
                                self.setMoveableSquares(self.selected,True)
                        elif self.menu.getOption().lower() == "steal":
                            self.mode = "steal1"
                            self.targetableEnemies = [u for u in getUnitsWithinRange(self.selected.x,self.selected.y,1,1,enemies) if u.spd <= self.selected.spd]
                            self.targetableEnemies = [u for u in self.targetableEnemies if len([i for i in u.items if type(i) != Weapon]) > 0]
                            self.selectx,self.selecty = self.targetableEnemies[0].x,self.targetableEnemies[0].y
                            self.selectedEnemy = 0
                        elif self.menu.getOption().lower() == "wait":
                            self.mode = "freemove"
                            self.moved.add(self.selected)
                            self.attacked.add(self.selected)
                    #ATTACK CLICKS
                    elif self.mode == "itemattack":
                        if self.menu.selected < len(self.selected.items):
                            if self.selected.canEquip(self.selected.items[self.menu.selected]) and getAttackableEnemies(self.selected,enemies,weapon=self.selected.items[self.menu.selected]):
                                self.mode = "attack"
                                self.selected.equipWeapon(self.selected.items[self.menu.selected])
                                self.attackableEnemies = getAttackableEnemies(self.selected,enemies)
                                self.selectx,self.selecty = self.attackableEnemies[0].x,self.attackableEnemies[0].y
                                self.selectedEnemy = 0
                            else:
                                if not self.selected.canEquip(self.selected.items[self.menu.selected]):
                                    dispTempMsg(screen,"You have not enough mastery to equip that weapon",centerX=True,centerY=True)
                                else:
                                    dispTempMsg(screen,"No enemies in range of that weapon",centerX=True,centerY=True)
                    elif self.mode == "attack":
                        #does an attack
                        attack(self.selected,self.attackableEnemies[self.selectedEnemy])
                        self.attacked.add(self.selected)
                        self.moved.add(self.selected)
                        self.mode = "freemove"
                    #STAFF CLICKS
                    elif self.mode == "itemstaff":
                        if self.menu.selected < len(self.selected.items):
                            if self.selected.canEquip(self.menu.getOption()):
                                if self.menu.getOption().heal != 0:
                                    self.mode = "heal"
                                    self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                                    self.selectx,self.selecty = self.targetableAllies[0].x,self.targetableAllies[0].y
                                    self.selectedAlly = 0
                    elif self.mode == "heal":
                        #does a heal
                        heal(self.selected,self.targetableAllies[self.selectedAlly],self.menu.getOption())
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
                                    #if it breaks we remove it
                                    self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                                self.mode = "move"
                                if not self.selected.mounted and self.selected.movesLeft > 0:
                                    self.moved.add(self.selected)
                                    self.mode = "freemove"
                                self.attacked.add(self.selected) #guy who used consumable can't move - treated like an attack
                                self.oldx,self.oldy = self.selected.x,self.selected.y
                                self.oldM = self.selected.movesLeft
                                self.setMoveableSquares(self.selected,True)
                            elif optselected.lower() == "equip":
                                #equip option
                                self.selected.equipWeapon(self.selectedItem) #tries to equip
                            elif optselected.lower() == "discard":
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            self.selectedItem = None #resets self.selectedItem
                            self.menu.subMenu = None
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
                                self.menu.items = [firstItemList,secondItemList] #trade menu items reset
                                self.menu.firstSelection = None
                                if not self.selected.mounted and self.selected.movesLeft > 0:
                                    self.moved.add(self.selected)
                                self.oldx,self.oldy = self.selected.x,self.selected.y
                                self.oldM = self.selected.movesLeft
                    #STEAL MODE CLICKS
                    elif "steal" in self.mode:
                        if self.mode == "steal1":
                            self.mode = "steal2"
                            self.menu = Menu(3,3,500,150,items=self.targetableEnemies[self.selectedEnemy].items)
                            self.selectedItem = 0
                        elif self.mode == "steal2":
                            item = self.menu.getOption()
                            if type(item) != Weapon:
                                self.selected.addItem(item)
                                self.targetableEnemies[self.selectedEnemy].removeItem(item)
                                self.mode = "freemove"
                                self.attacked.add(self.selected)
                                self.moved.add(self.selected)
                                dispTempMsg(screen,("A " if item.name[0].lower() not in "aeiou" else "An ")+item.name+" was stolen!",centerX=True,centerY=True)
                                drawChangingBar(screen,self.selected.exp,self.selected.exp+25,100,420,330,360,60,"Exp") #draws exp gain
                                if self.selected.gainExp(25):
                                    self.selected.levelUp()
                                    drawLevelUp(screen,self.selected)
                            else:
                                dispTempMsg(screen,"Weapons cannot be stolen",centerX=True,centerY=True)
                    #TRANSFER MODE CLICK
                    elif self.mode == "transfer":
                        self.transferScreen.onZ()                
                        if not self.selected.mounted and self.selected.movesLeft > 0:
                            self.moved.add(self.selected)
                        self.oldx,self.oldy = self.selected.x,self.selected.y
                        self.oldM = self.selected.movesLeft
                    #SHOPSCREEN CLICK
                    elif self.mode in ["armory","vendor"]:
                        self.shopScreen.onZ()
                        if not self.selected.mounted and self.selected.movesLeft > 0:
                            self.moved.add(self.selected)
                        self.oldx,self.oldy = self.selectx,self.selecty
                        self.oldM = self.selected.movesLeft
                #------X------#
                if e.key == K_x:
                    #if the user pressed x
                    #handles backtracing
                    if self.mode == "move":
                        self.mode = "freemove"
                        self.selectx = self.selected.x
                        self.selecty = self.selected.y
                        if self.selected in self.attacked:
                            self.moved.add(self.selected)
                    elif self.mode == "mainmenu":
                        self.mode = "freemove"
                    elif self.mode == "optionmenu":
                        self.mode = "move"
                        self.selected.x,self.selected.y = self.oldx,self.oldy
                        self.selected.movesLeft = self.oldM
                        if self.moveableSquares == [] or self.selected in self.moved:
                            self.mode = "freemove" #we go back to freemove mode if we have no moveablesquares
                            self.attacked.add(self.selected)
                        self.setMoveableSquares(self.selected,True)
                    elif self.mode == "itemattack":
                        self.mode = "optionmenu"
                        self.createOptionMenu() #creates the option menu and sets the menu to it
                    elif self.mode == "itemstaff":
                        self.mode = "optionmenu"
                        self.createOptionMenu() #creates the option menu
                    elif self.mode == "item":
                        if self.selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
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
                            if self.menu.firstSelection == None:
                                self.selected2 = None #if there exists selected2, that means the trade interface is open, so we close that
                            else:
                                #however if there is a selected item, we instead deselect it
                                self.menu.firstSelection = None
                    elif self.mode == "attack":
                        self.menu.selected = 0
                        self.mode = "itemattack"
                    elif self.mode == "heal":
                        self.menu.selected = 0
                        self.mode = "itemstaff"
                    elif self.mode == "transfer":
                        if not self.transferScreen.onX():
                            self.mode = "optionmenu"
                            self.createOptionMenu()
                    elif self.mode == "steal1":
                        self.mode = "optionmenu"
                        self.createOptionMenu()
                    elif self.mode == "steal2":
                        self.mode = "steal1"
                    elif self.mode in ["vendor","armory"]:
                        if not self.shopScreen.onX():
                            self.mode = "optionmenu"
                            self.createOptionMenu()
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
                                self.infoScreen = InfoScreen(self.selected)
                                break
                    elif self.mode in ["item","trade"]:
                        self.menu.onS()
                    elif self.mode == "transfer":
                        self.transferScreen.onS()
                    elif self.mode in ["vendor","armory"]:
                        self.shopScreen.onS()
                    elif self.mode == "info":
                        self.infoScreen.onS()
                #------A------#
                if e.key == K_a:
                    #cycles through allies
                    self.currAlly += 1
                    if self.currAlly >= len(allies):
                        self.currAlly = 0
                    self.selectx,self.selecty = allies[self.currAlly].x,allies[self.currAlly].y
                #-------##temporary##-------#
                #WIP(this symbol is used to represent all things to delete at the end)
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
        if len(enemies) == 0 and self.goal.lower() == "defeat all enemies":
            #no more enemies means the player won
            self.mode = "gameVictory"
            self.gameVictory()
            return 0
        screen.blit(self.filler,(0,0)) #blits the filler
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if self.framecounter - self.clickedFrame > 20 and self.mode in ["freemove","move"] and not self.framecounter%5 and self.clickedFrame > 0:
            #if we held for 20 frames or more we move more
            #we only do it once every 5 frames or it'll be too fast
            self.moveSelect()
        if self.framecounter - self.clickedFrame > 10 and self.mode == "transfer" and not self.framecounter%2 and self.clickedFrame > 0:
            self.transferScreen.handleMove()
        #---------------DIFFERENT MODE DISPLAYS------------------#
        #DRAWS PEOPLE
        self.drawPeople()
        #MOVE MODE DISPLAY
        if self.mode == "move":
            #fills moveable and attackable squares
            fillSquares(screen,set([(x,y) for x,y,m,ali in self.moveableSquares]),transBlue)
            if self.attackableSquares and self.selected.equip != None:
                fillSquares(screen,self.attackableSquares,transRed)
            if self.staffableSquares:
                fillSquares(screen,set([sq for sq in self.staffableSquares if sq not in [(x,y) for x,y,m,ali in self.moveableSquares]]),transGreen)
            if self.selected in allies:
                self.drawArrow(self.moveableSquares,self.selectx,self.selecty)
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Click Z on a blue square to move there (you can click on character to stay put); Click X to go back; Arrow keys to move cursor",True,WHITE),(0,y))
        #MAIN MENU MODE DISPLAY
        if self.mode == "mainmenu":
            #if it is menu mode we draw the menu
            self.menu.x,self.menu.y = 18,4
            self.menu.width,self.menu.height = 120,480
            self.menu.draw()
            drawTransRect(screen,BLACK,0,680,1200,40)
            screen.blit(sans.render("Z to select an option; X to cancel; Up and down keys to change option",True,WHITE),(0,680))
 #          drawMenu(self.menu,menux,menuy,120,480,self.menu.selected) #draws the main menu
        #OPTION MENU MODE DISPLAY
        if self.mode == "optionmenu":
            self.menu.x,self.menu.y = 32,2
            if self.selected.x >= 20:
                self.menu.x = 0
            self.menu.width=270
            self.menu.height=30*len(self.menu.items)
            self.menu.draw()
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to select an option; X to cancel; Up and down keys to change option",True,WHITE),(0,y))
#            drawMenu(self.menu,menux,menuy,120,len(self.menu.items)*30,self.menu.selected)
        #ATTACK MODE DISPLAY
        if self.mode == "itemattack":
            #displays item selection menu for attack
            self.menu.draw(self.selected)
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to select item to attack; X to cancel; Arrow keys to change selected weapon",True,WHITE),(0,y))
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
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to attack selected enemy; X to cancel; Arrow keys to change enemy",True,WHITE),(0,y))
        #STAFF MODE DISPLAYS
        if self.mode == "itemstaff":
            #displays item menu
            self.menu.draw(self.selected)
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to select staff; X to cancel; Arrow keys to change selected staff",True,WHITE),(0,y))
        if self.mode == "heal":
            #highlights all healable squares
            fillSquares(screen,getAttackableSquares(1,1,self.selected.x,self.selected.y),transGreen)
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to heal; X to cancel; Arrow keys to change selected ally",True,WHITE),(0,y))
        #ITEM MODE DISPLAY
        if self.mode == "item":
            screen.blit(transBlack,(0,0))
            self.menu.x,self.menu.y = 16,8
            self.menu.width = 240
            self.menu.height = 150
            self.menu.draw(self.selected)
            drawTransRect(screen,BLACK,0,680,1200,40)
            if self.menu.subMenu == None:
                screen.blit(sans.render("Z to select an item; X to cancel; Arrow keys to change item selected; S to toggle info mode",True,WHITE),(0,680))
            else:
                screen.blit(sans.render("Z to select option; X to cancel; Arrow keys to change option selected",True,WHITE),(0,680))
        #TRADE MODE DISPLAY
        if self.mode == "trade":
            if self.selected2 == None:
                #if we have no 2nd selected ally, we draw the selector around the 2nd selected ally
                highlightedAlly = self.targetableAllies[self.selectedAlly] #highlighted ally
                y = 0 if self.selected.y > 12 else 680
                drawTransRect(screen,BLACK,0,y,1200,40)
                screen.blit(sans.render("Z to trade with selected ally; X to cancel; Arrow keys to change ally",True,WHITE),(0,y))
            else:
                screen.blit(menuBG,(0,0)) #blits menu background
                #draws item menu for both allies
                #first we set which item selected out of the two menus
                #this is based on which ally the selector is on
                #which is determined by the first element of menuselect
                screen.blit(self.selected.face,(240,190))
                screen.blit(self.selected2.face,(630,190))
                self.menu.draw(self.selected,self.selected2)
                drawTransRect(screen,BLACK,0,680,1200,40)
                if self.menu.firstSelection == None:
                    screen.blit(sans.render("Z to select an item; X to cancel; Arrow keys to change item; S to toggle info mode",True,WHITE),(0,680))
                else:
                    screen.blit(sans.render("Z to trade selected item with current item; X to cancel; Arrow keys to change item",True,WHITE),(0,680))
        #STEAL MODE DISPLAY
        if self.mode == "steal1":
            fillSquares(screen,[(u.x,u.y) for u in self.targetableEnemies],transRed)
            y = 0 if self.selected.y > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z to select an enemy to steal from; X to cancel; Arrow keys to change selected enemy",True,WHITE),(0,y))
        if self.mode == "steal2":
            self.menu.draw(self.targetableEnemies[self.selectedEnemy])
            draw.rect(screen,BLUE,(700,0,500,30))
            screen.blit(sans.render("Choose an item to steal",True,WHITE),(700,0))
            drawTransRect(screen,BLACK,0,680,1200,40)
            screen.blit(sans.render("Z to steal item; X to cancel; Arrow keys to change selected item",True,WHITE),(0,680))
        #TRANSFER MODE DISPLAY
        if self.mode == "transfer":
            self.transferScreen.draw()
        #INFO MODE DISPLAY
        #displays character info screen
        if self.mode == "info":
            self.infoScreen.draw()
        #VENDOR/ARMORY MODE DISPLAY
        if self.mode in ["armory","vendor"]:
            self.shopScreen.draw()
        #--------------------HIGHLIGHTING A PERSON---------------#
        if self.mode == "freemove":
            for p in allies+enemies:
                if self.selectx == p.x and self.selecty == p.y:
                    #DRAWS PERSON MINI DATA BOX
                    pdbx,pdby = 0,40 #person data box x and y
                    if self.selectx < 20 and self.selecty <= 12:
                        pdby = 590
                    draw.rect(screen,BLUE,(pdbx,pdby,300,90)) #background box
                    screen.blit(sans.render(p.name,True,WHITE),(pdbx+15,pdby+3)) #person's name
                    screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,WHITE),(pdbx+15,pdby+33)) #health
                    draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                    draw.line(screen,YELLOW,(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                    break
            y = 0 if self.selecty > 12 else 680
            drawTransRect(screen,BLACK,0,y,1200,40)
            screen.blit(sans.render("Z on an active character to select; Z on ground for menu; S: view profile; Arrow keys: move cursor; A: cycle through allies",True,WHITE),(0,y))

        #---------------INFO DISPLAY BOXES----------------------#
        #TERRAIN DATA BOX
        if self.mode == "freemove":
            tbx,tby = 1020,590 #terrain box x and y
            stage = chapterMaps[chapter]
            if self.selectx >= 20:
                tbx = 0
            draw.rect(screen,BLUE,(tbx,tby,180,90))
            screen.blit(sans.render(stage[self.selecty][self.selectx].name,True,WHITE),(tbx+15,tby+3))
            draw.rect(screen,(255,230,200),(tbx,tby+30,180,60))
            screen.blit(sans.render("DEFENSE: "+str(stage[self.selecty][self.selectx].adef),True,BLACK),(tbx+15,tby+33))
            screen.blit(sans.render("AVOID: "+str(stage[self.selecty][self.selectx].avo),True,BLACK),(tbx+15,tby+63))
        #GOAL DISPLAY BOX
            goalx,goaly = 1020,40
            if self.selecty <= 12 and self.selectx >= 20:
                goaly = 590
            draw.rect(screen,(50,50,180),(goalx,goaly,180,90))
            screen.blit(smallsans.render(self.goal,True,WHITE),(goalx+15,goaly+35))
        #---------------SELECTED SQUARE BOX----------------#

        if self.mode in ["freemove","move","attack","heal","trade","steal1"]:
            if self.mode == "trade" and self.selected2 != None:
                pass
            else:
                draw.rect(screen,YELLOW,(self.selectx*30,self.selecty*30,30,30),2) #draws select box
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
