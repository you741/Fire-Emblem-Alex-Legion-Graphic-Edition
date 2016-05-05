from pygame import *
from copy import *
screen = display.set_mode((1200,720))
img = image.load("images/logo.png")

def makeBackground(background,tilenum):
    ##background should be all set width and height
    background = transform.smoothscale(background,(300,30))
    tiledbackground = Surface((300,int(30*tilenum)))
    ##take top quarter, bottom quarter, place at top and bottom
    ##stretch the middle
    top = copy(background.subsurface((0,0,300,30//4)))
    bottom = copy(background.subsurface((0,90//4,300,30//4)))
    middle = copy(background.subsurface((0,90//4,300,30//4)))
    tiledbackground.blit(top,(0,0))
    tiledbackground.blit(bottom,(0,tiledbackground.get_height()-30//4))
    for i in range (tilenum-1):
        tiledbackground.blit(middle,(0,i*30//2+30//4))
    return tiledbackground
while True:
    for e in event.get():
        if e.type == QUIT:
            break
    screen.blit(makeBackground(img,5),(0,0))
    display.flip()
quit()
