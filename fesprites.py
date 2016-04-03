#fesprites.py
#keeps all of the sprites
from pygame import *
#ALLIES
playerMageStandSprite = image.load('images/Player/Mage/MageAttackFrame1.png')
playerMageAnimaSprite = ([image.load("images/Player/Mage/MageAttackFrame"+str(i+1)+".png")
                          for i in range(16)],10)
playerMageAnimacritSprite = ([image.load("images/Player/Mage/MageCritFrame"+str(i+1)+".png")
                        for i in range(12)] + playerMageAnimaSprite[0][1:],21)
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
                  "Lord":[Surface((30,30))]*4}
enemyMapSprites = {"Brigand":[Surface((30,30))]*4}
