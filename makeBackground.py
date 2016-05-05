from pygame import *
from math import *
screen = display.set_mode((1200,720))
img = image.load("images/faces/Yoyo.png")

def tileBackground(background,tilenum):
    "returns tiled background tilenum times, tilenum > 0"
    tiledbackground = Surface((background.get_width(),background.get_height()*tilenum))
    ##take top tier, bottom tier, place at top and bottom
    ##stretch the middle
    top = background.subsurface((0,0,int(background.get_width()),int(background.get_height()/3)))
    bottom = background.subsurface((0,int(2*(background.get_height()/3)),int(background.get_width()),int(background.get_height()/3)))
    middle = background.subsurface((0,int(background.get_height()/3),int(background.get_width()),int(background.get_width()/3)))
    ##for each tilenum-1(tilenum times, but the original is already there, and starts at 0), blit 3 of the middle
    for i in range (tilenum):
        tiledbackground.blit(middle,(0,i*int(background.get_height())+int((0)*background.get_height()/3)))
        tiledbackground.blit(middle,(0,i*int(background.get_height())+int((1)*background.get_height()/3)))
        tiledbackground.blit(middle,(0,i*int(background.get_height())+int((2)*background.get_height()/3)))
    tiledbackground.blit(top,(0,0))
    tiledbackground.blit(middle,(0,int(tiledbackground.get_height()/3)))
    tiledbackground.blit(bottom,(0,int(tiledbackground.get_height()-background.get_height()/3)))

    return tiledbackground


while True:
    for e in event.get():
        if e.type == QUIT:
            break
    screen.blit(makeBackground(img,8),(0,0))
    screen.blit(img,(500,500))
    display.flip()
quit()
