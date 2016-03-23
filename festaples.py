#FE Staples keeps important functions and classes
from pygame import *
from copy import deepcopy
def getMoves(person,x,y,movesleft,stage,allies,enemies,visited):
    "gets all moveable squares for a person"
    moveable = [] #moveable squares
    if movesleft >= 0 and 0 <= y < len(stage) and 0 <= x < len(stage[0]) and ((x,y) not in visited or visited.get((x,y)) < movesleft):           
        if (x,y) not in allies+enemies:
            moveable.append((x,y,movesleft))
        if (x,y) not in enemies:
            if person.canPass(stage[y][x]):
                #if the person can pass this terrain
                #we call the function in four directions
                visited[(x,y)] = movesleft #sets visited (x,y) to movesleft
                moveable += getMoves(person,x-1,y,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x+1,y,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x,y-1,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x,y+1,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                
    return moveable
def getAttackableEnemies(person,enemies,x=None,y=None,weapon=None):
    "returns attackable enemies by person (optional parameters for different (x,y))"
    atten = [] #attackble enemies
    for e in enemies:
        if canAttackTarget(person,e,x,y,weapon):
            atten.append(e)
    return atten
def getAttackableSquares(rnge,maxrnge,x,y):
    "returns all attackable squares from (x,y)"
    asq = [] #attackable squares
    for i in range(rnge,maxrnge+1):
        for dx in range(-i,i+1):
            for dy in range(-i,i+1):
                if abs(dx) + abs(dy) == i and 0<=x+dx<=39 and 0<=y+dy<=23:
                    asq.append((x+dx,y+dy))
    return asq
def getAttackableSquaresByMoving(moveablesquares,person):
    attackableSquares = set() #attackable squares
    if person.equip == None:
        return False #if we have no weapon, we can't attack so we return False
    for x,y in moveablesquares:
        for ax,ay in getAttackableSquares(person.getMinRange(),person.getMaxRange(),x,y):
            attackableSquares.add((ax,ay))
    return attackableSquares
def canAttackTarget(person,enemy,x=None,y=None,weapon=None):
    "returns whether person can attack enemy"
    if person.equip == None:
        return False
    if x == None:
        x = person.x
    if y == None:
        y = person.y
    weapon = person.equip if weapon == None else weapon
    return weapon.rnge <= getDistance(x,y,enemy.x,enemy.y) <= weapon.maxrnge
def getDistance(x,y,x2,y2):
    "returns distance between 2 points"
    return abs(x-x2) + abs(y-y2)
def drawPerson(screen,person):
    "draws a person on the grid"
    #no sprite so will use rectangles for now
    draw.rect(screen,(0,0,0),(person.x*30,person.y*30,30,30))
def drawGrid(screen,width=1200,height=720):
    "draws a grid on the screen"
    for x in range(0,width,30):
        draw.line(screen,(0,0,0),(x,0),(x,720))
    for y in range(0,height,30):
        draw.line(screen,(0,0,0),(0,y),(1200,y))
def fillSquares(screen,coords,filler):
    "fills squares at coords with filler"
    for x,y in coords:
        screen.blit(filler,(x*30,y*30))
def createEnemyList(enemies,amounts,coords):
    "takes in a list of enemies, a corresponding list of amounts and a list of coordinates"
    enemyList = []
    enemyat = 0
    for i in range(len(enemies)):
        for j in range(amounts[i]):
            newEnemy = enemies[i].getInstance()
            newEnemy.x,newEnemy.y = coords[enemyat]
            newEnemy.name = newEnemy.name + str(enemyat)
            enemyat += 1
            enemyList.append(newEnemy)
    return enemyList
def stripNums(string):
    "strips all numbers from end of a string"
    while True:
        try:
            int(string[-1]) #tries to int last character
        except:
            break #if it failed we break the loop
        string = string[:-1] #removes last character of string
    return string
def getExpGain(ally,enemy,kill=False):
    "returns amount of exp that should be gained"
    LD = enemy.getInternalLevel() - ally.getInternalLevel() #level difference
    #the following formula is a copy of Fire Emblem Awakening (with small tweaks)
    if LD >= 0:
        hitgain = (31+LD)/3 #exp gained from hit
        killgain = 20 + LD*3 + enemy.gift #exp gained from kill
    elif LD == -1:
        hitgain = (33+LD)/3
        killgain = 23 + LD*3 + enemy.gift
    else:
        hitgain = (33+LD)/3
        killgain = 26 + LD*3 + enemy.gift
    hitgain = max(1,hitgain)
    killgain = max(7,killgain)
    return min(100,hitgain + killgain)
