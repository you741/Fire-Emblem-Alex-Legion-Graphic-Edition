#fesprites.py
#keeps all of the sprites
from pygame import *

yoyoStandSprite = image.load("images/Yoyo/YoyoAttackFrame1.png")
yoyoAttackSprite = [image.load("images/Yoyo/YoyoAttackFrame"+str(i+1)+".png")
                    for i in range(13)]
yoyoCritSprite = [image.load("images/Yoyo/YoyoCritFrame"+str(i+1)+".png")
                  for i in range(43)]
