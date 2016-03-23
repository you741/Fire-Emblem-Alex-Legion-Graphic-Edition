#Fire Emblem Alex Legion
#This game is a Fire Emblem Spin-off featuring my own unique characters named after my classmates
#The user controls an army that fights off the enemy's army for multiple levels to win
#There is also a great story line

#----DEFAULT MODULE IMPORTS
import os
from pygame import *
import time as time2
from math import *
from random import *
#----CUSTOM MODULE IMPORTS
from feclasses import *
from feweapons import *
from feterrain import *
from festaples import *
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
#----COLORS----#
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
#----FONTS----#
timesnr = font.SysFont("Times New Roman",15)
comicsans = font.SysFont("Comic Sans MS",25)
arial = font.SysFont("Arial",15)
monospace = font.SysFont("Monospace",15)
#----IMAGE LOAD----#
logo = image.load("images/logo.png")

#----HELPFUL CLASSES----#
#any classes that help me code
class FilledSurface(Surface):
    "a surface we can make filled on declaration"
    #aids in my drawing efforts as I am too lazy to make a new surface everytime I want a filled one
    def __init__(self,dimensions,background=None,text=None,fontColor=None,fontFamily=None,tpos=None):
        super(FilledSurface,self).__init__(dimensions) #calls super
        if background != None:
            if type(background) in [Color,tuple]:
                self.fill(background) #fills the surface if the background is a color
            else:
                self.blit(background,(0,0))
        if text != None:
            #blits text if it isn't None
            if fontFamily == None:
                fontFamily = timesnr #sets default font
            if fontColor == None:
                fontColor = BLACK #sets default color
            if tpos == None:
                tpos = (0,0) #sets default text position
            self.blit(fontFamily.render(text,True,fontColor),tpos)
            
#----UI CLASSES----#
#these classes are the user interface classes - any classes that help user interaction are here
class Button():
    def __init__(self,x=0,y=0,width=0,height=0,background=Surface((1,1)),hlbackground=Surface((1,1)),func=[]):
        "sets all the class's members"
        self.x = x #co-ordinates
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = background #background of button
        self.hlbackground = hlbackground #background of button when highlighted
        self.func = func #func is a list of strings that contains commands to be executed
    def istouch(self,x=None,y=None):
        "checks if co-ordinates are touching Button"
        #default is mouse co-ordinates
        mx,my = mouse.get_pos()
        if x == None:
            x = mx
        if y == None:
            y = my
        return Rect(self.x,self.y,self.width,self.height).collidepoint(x,y) #returns boolean
    def draw(self,screen):
        "draws button on screen"
        if self.istouch():
            screen.blit(self.hlbackground,(self.x,self.y)) #if it's highlighted we draw the highlighted background
        else:
            screen.blit(self.background,(self.x,self.y))
    def click(self):
        "runs button's func"
        exec("\n".join(self.func))
        
#----MODE CLASSES----#
#these classes are the different modes for the scren - must be in the main
class StartMenu():
    #start menu mode
    def __init__(self,screen):
        "sets button list of mode"
        self.stopped = False
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"NEW GAME",BLACK,font.SysFont("Monospace",30),(30,10)),
                               FilledSurface((200,50),YELLOW,"NEW GAME",WHITE,font.SysFont("Monospace",30),(30,10)),
                               ["changemode(NewGame(screen))"])] #START BUTTON
    def draw(self,screen):
        #draws mode on screen
        screen.blit(logo,(300,50))
    def run(self,screen):
        global running
        #runs the mode as if it were in the running loop
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
class NewGame():
    "this class let's user choose his name and class"
    def __init__(self,screen):
        self.selectingname = True #is the user choosing his name?
        self.selectingclass = False #is the user selecting his class?
        self.typing = False #is the user typing his name?
        self.tbrect = Rect(400,300,500,50)
        self.name = "" #name user chosen
        self.ipos = 0 #insertion point position
        #name select buttons
        self.buttons1 = [Button(900,300,200,50,FilledSurface((200,50),BLUE,"SUBMIT",BLACK,font.SysFont("Monospace",30),(30,10)),
                               FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,font.SysFont("Monospace",30),(30,10)),
                               ["currmode.selectingname = False","currmode.selectingclass = True","screen.fill(BLACK)"])]
        #class select buttons
        self.buttons2 = [Button(300,300,200,50,FilledSurface((200,50),BLUE,"MAGE",BLACK,font.SysFont("Monospace",30),(30,10)),
                                FilledSurface((200,50),YELLOW,"SUBMIT",BLACK,font.SysFont("Monospace",30),(30,10)),
                                ["global player",
                                 "player = Mage(self.name,0,0,{'stren':5,'defen':3,'spd':7,'res':5,'lck':5,'skl':6,'con':5,'move':5},{},[],{})"])]
    def draw(self,screen):
        #draws newgame screen
        screen.fill(BLACK)
        screen.blit(comicsans.render("ENTER NAME: ",True,WHITE),(self.tbrect[0]-250,self.tbrect[1]+10))
        draw.rect(screen,WHITE,self.tbrect)
    def run(self,screen):
        global running
        #runs new game screen
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                if self.selectingname:
                    #if the user is selecting his name
                    if self.tbrect.collidepoint(e.pos):
                        #if we are touching the textbox
                        self.typing = True
                    else:
                        self.typing = False
                if self.selectingname and len(self.name) > 0:
                    for b in self.buttons1:
                        if b.istouch():
                            b.click()
            if e.type == KEYDOWN:
                if self.typing:
                    if key.get_pressed()[K_BACKSPACE]:
                        self.name = self.name[:self.ipos-1] + self.name[self.ipos:]#deletes last character behind ipos in name if user backspaced
                        self.ipos -= 1
                    elif len(self.name) < 16:
                        self.name += e.unicode #Otherwise it adds what they typed to name
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
                    draw.line(screen,BLACK,(self.tbrect[0]+comicsans.render(self.name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]),
                              (self.tbrect[0]+comicsans.render(self.name[:self.ipos],True,BLACK).get_width(),self.tbrect[1]+self.tbrect[3]))
            screen.blit(comicsans.render(self.name,True,BLACK),self.tbrect) #blits text on
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
#----GLOBAL VARIABLES----#
name = "" #name of player
player = None
#----FINALIZES SCREEN----#
running = True
currmode = StartMenu(screen) #sets current mode
currmode.draw(screen)
while running:
    currmode.run(screen) #runs current mode
    display.flip() #updates screen
quit()
