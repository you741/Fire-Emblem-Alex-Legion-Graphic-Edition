#Fire Emblem Alex Legion
#This game is a Fire Emblem Spin-off featuring my own unique characters named after my classmates
#The user controls an army that fights off the enemy's army for multiple levels to win
#There is also a great story line

#----DEFAULT MODULE IMPORTS
import os
from pygame import *
from pygame import time as pytime
from time import *
from math import *
from random import *
#----CUSTOM MODULE IMPORTS

font.init()
#----METADATA----#
__author__ = "Yttrium Z (You Zhou)"
__date__ = "Incomplete"
__purpose__ = "Game for Grade 11 final project"
__name__ = "Fire Emblem Alex Legion"
__copyright__ = "Yttrium Z 2015-2016"
#----SETUP----#
os.environ['SDL_VIDEO_WINDOW_POS'] = '25,25'
display.set_caption("YTTRIUM Z PRESENTS ~~~~~~~FIRE EMBLEM ALEX LEGION~~~~~~~","Fire Emblem Alex Legion")
screen = display.set_mode((1200,736))
#----COLORS----#
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
#----FONTS----#
timesnr = font.SysFont("Times New Roman",15)
comicsans = font.SysFont("Comic Sans MS",15)
arial = font.SysFont("Arial",15)
monospace = font.SysFont("Monospace",15)
#----IMAGE LOAD----#
logo = image.load("images/logo.png")

#----HELPFUL CLASSES----#
#any classes that help me code
class FilledSurface(Surface):
    #a surface we can make filled on declaration
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
        #sets all the class's members
        self.x = x #co-ordinates
        self.y = y
        self.width = width #dimensions
        self.height = height
        self.background = background #background of button
        self.hlbackground = hlbackground #background of button when highlighted
        self.func = func #func is a list of strings that contains commands to be executed
    def istouch(self,x=None,y=None):
        #checks if co-ordinates are touching Button
        #default is mouse co-ordinates
        mx,my = mouse.get_pos()
        if x == None:
            x = mx
        if y == None:
            y = my
        return Rect(self.x,self.y,self.width,self.height).collidepoint(x,y) #returns boolean
    def draw(self,screen):
        #draws button on screen
        if self.istouch():
            screen.blit(self.hlbackground,(self.x,self.y)) #if it's highlighted we draw the highlighted background
        else:
            screen.blit(self.background,(self.x,self.y))
    def click(self):
        #runs button's func
        exec("\n".join(self.func))
        
#----MODE CLASSES----#
#these classes are the different modes for the scren - must be in the main
class StartMenu():
    #start menu mode
    def __init__(self,screen):
        #draws screen when defined
        screen.blit(logo,(300,50))
        #sets button list of mode
        self.buttons = [Button(500,420,200,50,FilledSurface((200,50),BLUE,"START",BLACK,font.SysFont("Monospace",30),(50,10)),
                               FilledSurface((200,50),YELLOW,"START",WHITE,font.SysFont("Monospace",30),(50,10)),
                               ["global running","running = False"])] #START BUTTON
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
        #draws buttons
        for b in self.buttons:
            b.draw(screen)
        
#----FINALIZES SCREEN----#
running = True
currmode = StartMenu(screen) #sets current mode
while running:
    currmode.run(screen) #runs current mode
    display.flip() #updates screen
quit()
