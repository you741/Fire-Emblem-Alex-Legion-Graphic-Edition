#fesprites.py
#keeps all of the sprites
from pygame import *
#ALLIES
playerMageStandSprite = image.load('images/Player/Mage/MageAttackFrame1.png')
playerMageAttackSprite = [image.load("images/Player/Mage/MageAttackFrame"+str(i+1)+".png")
                          for i in range(16)]
playerMageCritSprite = [image.load("images/Player/Mage/MageCritFrame"+str(i+1)+".png")
                        for i in range(12)] + playerMageAttackSprite[1:]
yoyoStandSprite = image.load("images/Yoyo/YoyoAttackFrame1.png")
yoyoAttackSprite = [image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)]
yoyoCritSprite = [image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)]


#ENEMIES
brigandStandSprite = image.load("images/Brigand/BrigandAttackFrame1.png")
brigandAttackSprite = [image.load("images/Brigand/BrigandAttackFrame"+str(i+1)+".png")
                       for i in range(14)]
brigandCritSprite = [image.load("images/Brigand/BrigandCritFrame"+str(i+1)+".png")
                     for i in range(2)] + brigandAttackSprite

#MAGIC
fireSprite = [image.load("images/Magic/Fire/Fire"+str(i+1)+".png")
              for i in range(17)]
