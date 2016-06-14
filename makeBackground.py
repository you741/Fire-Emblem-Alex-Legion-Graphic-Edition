from pygame import *
from math import *
screen = display.set_mode((1200,720))
img = transform.smoothscale(image.load("images/Menu/menubackground.png"),(100,60))
def tileBackground(background,width,height):
    "returns tiled background based on width and height, width and height > 2/3 original width and height"
    #----vertically----#
    vtilenum = height // background.get_height()
    vtiledbackground = Surface((background.get_width(),height))
    ##take top tier, bottom tier, place at top and bottom
    ##stretch the middle
    top = background.subsurface((0,0,int(background.get_width()),int(background.get_height()/3)))
    bottom = background.subsurface((0,int(2*(background.get_height()/3)),int(background.get_width()),int(background.get_height()/3)))
    middle = background.subsurface((0,int(background.get_height()/3),int(background.get_width()),int(background.get_height()/3)))
    ##for each tilenum-1(tilenum times, but the original is already there, and starts at 0), blit 3 of the middle
    for i in range (vtilenum):
        vtiledbackground.blit(middle,(0,i*int(background.get_height())+int((0)*background.get_height()/3)))
        vtiledbackground.blit(middle,(0,i*int(background.get_height())+int((1)*background.get_height()/3)))
        vtiledbackground.blit(middle,(0,i*int(background.get_height())+int((2)*background.get_height()/3)))
    vtiledbackground.blit(top,(0,0))
    vtiledbackground.blit(middle,(0,int(vtiledbackground.get_height()-(2)*background.get_height()/3)))
    vtiledbackground.blit(bottom,(0,int(vtiledbackground.get_height()-(1)*background.get_height()/3)))
    #----vertically----#

    #----horizontally----#
    htilenum = width // background.get_width()
    tiledbackground = Surface((width,height))
    left = vtiledbackground.subsurface((0,0,int(vtiledbackground.get_width()/3),int(vtiledbackground.get_height())))
    right = vtiledbackground.subsurface((int(2*(vtiledbackground.get_width()/3)),0,int(vtiledbackground.get_width()/3),int(vtiledbackground.get_height())))
    hmiddle = vtiledbackground.subsurface((int(vtiledbackground.get_width()/3),0,int(vtiledbackground.get_width()/3),int(vtiledbackground.get_height())))
    for i in range (htilenum):
        tiledbackground.blit(hmiddle,(i*int(vtiledbackground.get_width())+int((0)*vtiledbackground.get_width()/3),0))
        tiledbackground.blit(hmiddle,(i*int(vtiledbackground.get_width())+int((1)*vtiledbackground.get_width()/3),0))
        tiledbackground.blit(hmiddle,(i*int(vtiledbackground.get_width())+int((2)*vtiledbackground.get_width()/3),0))
    tiledbackground.blit(left,(0,0))
    tiledbackground.blit(hmiddle,(int(tiledbackground.get_width()-(2)*vtiledbackground.get_width()/3),0))
    tiledbackground.blit(right,(int(tiledbackground.get_width()-(1)*vtiledbackground.get_width()/3),0))
    #----horizontally----#
    
    return tiledbackground

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.fill((255,255,255))
    screen.blit(tileBackground(img,500,500),(0,0))
    screen.blit(img,(500,500))
    mp = mouse.get_pos()
    display.flip()
quit()
