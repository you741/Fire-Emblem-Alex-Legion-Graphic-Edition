#fesprites.py
#keeps all of the sprites
from pygame import *
def greyScale(img):
    "returns a grey version of img"
    new_img = Surface((img.get_width(),img.get_height()),SRCALPHA)
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r,g,b,a = img.get_at((x,y))
            grey = (r+g+b)//3
            new_color = Color(grey,grey,grey,a)
            new_img.set_at((x,y),new_color)
    return new_img
#ALLIES
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

yoyoStandSprite = image.load("images/Yoyo/YoyoAttackFrame1.png")
yoyoSwordSprite = ([image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)],5)
yoyoSwordcritSprite = ([image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)],29)

albertStandSprite = playerMageStandSprite
albertAnimacritSprite = playerMageAnimacritSprite
albertAnimaSprite = playerMageAnimaSprite
#ENEMIES
brigandStandSprite = image.load("images/Brigand/BrigandAttackFrame1.png")
brigandAxeSprite = ([image.load("images/Brigand/BrigandAttackFrame"+str(i+1)+".png")
                       for i in range(14)],9)
brigandAxecritSprite = ([image.load("images/Brigand/BrigandCritFrame"+str(i+1)+".png")
                     for i in range(2)] + brigandAxeSprite[0],11)

#MAGIC
fireSprite = [image.load("images/Magic/Fire/Fire"+str(i+1)+".png")
              for i in range(17)]

#MAP SPRITES
allyMapSprites = {"Mage":[transform.scale(image.load("images/MapSprites/Ally/Mage"+str(i+1)+".gif"),(30,30)) for i in range(4)],
                  "Lord":[transform.scale(image.load("images/MapSprites/Ally/Lord"+str(i+1)+".png"),(30,30)) for i in range(4)],
                  "Knight":[transform.scale(image.load("images/MapSprites/Ally/Knight"+str(i+1)+".gif"),(30,30)) for i in range(4)]}
enemyMapSprites = {"Brigand":[transform.scale(image.load("images/MapSprites/Enemy/Brigand"+str(i+1)+".gif"),(30,30)) for i in range(4)]}
allyGreyMapSprites = {}
for i,k in enumerate(allyMapSprites):
    allyGreyMapSprites[k] = [greyScale(img) for img in allyMapSprites[k]]
enemyGreyMapSprites = {}
for i,k in enumerate(enemyMapSprites):
    enemyGreyMapSprites[k] = [greyScale(img) for img in enemyMapSprites[k]]
