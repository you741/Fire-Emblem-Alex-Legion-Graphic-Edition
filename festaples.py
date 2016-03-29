#FE Staples keeps important functions and classes
#pretty much "staples" for my program
#mostly to make main.py easier to read...
from pygame import *
from random import *
from feweapons import *

#----COLORS----#
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)

#----FONT----#
font.init()
sans = font.SysFont("Comic Sans MS",20)
papyrus = font.SysFont("Papyrus",20)

#----String formatting----#
def stripNums(string):
    "strips all numbers from end of a string"
    while True:
        try:
            int(string[-1]) #tries to int last character
        except:
            break #if it failed we break the loop
        string = string[:-1] #removes last character of string
    return string

#----Map Calculations----#
def getMoves(person,x,y,movesleft,stage,allies,enemies,visited):
    "gets all moveable squares for a person"
    moveable = [] #moveable squares
    #NOTE: the dictionary "visited" stores the amount of moves left after travelling to a point
    #in order to make this value optimal, I reset everytime I find a lower movesleft value
    #this is only really useful for mounted units
    if movesleft >= 0 and 0 <= y < len(stage) and 0 <= x < len(stage[0]) and ((x,y) not in visited or visited.get((x,y)) < movesleft):           
        if (x,y) not in allies+enemies:
            moveable.append((x,y,movesleft))
        if (x,y) not in enemies:
            if person.canPass(stage[y][x]):
                #if the person can pass this terrain
                #we call the function in four directions
                visited[(x,y)] = movesleft #sets visited at (x,y) to movesleft
                moveable += getMoves(person,x-1,y,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x+1,y,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x,y-1,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
                moveable += getMoves(person,x,y+1,movesleft-stage[y][x].hind,stage,allies,enemies,visited)
    moveable = [(x,y,m) for x,y,m in moveable if visited[(x,y)] == m] #seeds out all non-optimal tuples (where m isn't as high as it could be)
    return moveable
def getAttackableEnemies(person,enemies,x=None,y=None,weapon=None):
    "returns attackable enemies by person (optional parameters for different (x,y))"
    atten = [] #attackble enemies
    for e in enemies:
        if canAttackTarget(person,e,x,y,weapon):
            atten.append(e)
    return atten
def getTargetableAllies(rnge,maxrnge,x,y,allies):
    "returns all allies that are targetable"
    return [a for a in allies if rnge <= getDistance(x,y,a.x,a.y) <= maxrnge]
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

#----Other Calculations----#
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
    killgain = max(7,killgain) if kill else 0 #we only gain from kills if we actually kill
    return int(min(100,hitgain + killgain))
def getAttackResults(person,enemy,stage):
    "performs an attack on enemy by person, returns if it hit or crit and total damage"
    hit,dam,crit = False,0,False #hit = did it hit?; dam = damage; crit = did it crit?
    if randint(0,99) < person.getHit(enemy,stage):
        hit = True
        dam = person.getDamage(enemy,stage)
        if randint(0,99) < person.getCritical(enemy):
            crit = True
            dam *= 3 #damage is tripled
    return (hit,dam,crit) #returns (hit,dam,crit)

#----Creation Functions----#
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

#----Drawing Functions----#
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
def drawLevelUp(screen,person):
    "draws the stat changes when a unit levels up"
    #the unit's individual stat attribute changes, but not the value in the dictionary "stats"
    #that's how we calculate which stats changed
    screenBuff = screen.copy() #screen buffer    
    draw.rect(screen,(0,0,255),(300,240,600,240))
    screen.blit(sans.render(person.name+" LV "+str(person.lv),True,WHITE),(300,240))
    statCoords = {"maxhp":(300,270),"stren":(300,300),"skl":(300,330),"spd":(300,360),"lck":(300,390),"defen":(300,420)} #dictionary of the coordinates of every stat
    for i,k in enumerate(person.growths):
        #draws a +1 next to every stat gained
        if person.stats[k] != eval("person."+k):
def drawHealthBar(screen,person,x,y):
    "draws a health bar"
    hpx,hpy = x,y #x,y for each health point line
    for i in range(person.maxhp):
        if i == 40:
            hpy += 30
            hpx -= 160
        if i == 80:
            hpy += 30
            hpx -= 160
        draw.line(screen,(0,120,0),(hpx+i*4,hpy),(hpx+i*4,hpy+30),3)
    hpx,hpy = x,y
    for i in range(person.hp):
        if i == 40:
            hpy += 30
            hpx -= 160
        if i == 80:
            hpy += 30
            hpx -= 160
        draw.line(screen,GREEN,(hpx+i*4,hpy),(hpx+i*4,hpy+30),3)
        
def drawHealthLoss(screen,person,dam,x,y,enemy=True):
    "draws a depleting health bar"
    for i in range(dam):
        #for every point of damage we loop and remove it
        if person.hp == 0:
            break
        person.hp -= 1
        if enemy:
            draw.rect(screen,RED,(0,600,500,100))
        else:
            draw.rect(screen,BLUE,(700,600,500,100))
        drawHealthBar(screen,person,x,y)
        screen.blit(sans.render(str(person.hp),True,WHITE),(x+160,y+5))
        display.flip()
        time.wait(50)
        

def singleAttack(screen,person,person2,x,y,hpx,hpy,isenemy,stage):
    "animates a single attack"
    hit,dam,crit = getAttackResults(person,person2,stage) #gets attack results
    #draws person 2's standing sprite
    screen.blit(person2.anims["stand"],(0,200))
    filler = screen.copy().subsurface(Rect(0,0,1200,600))
    if not crit or not hit:
        #sets to attack animation with weapon
        frames,hitFrame = person.anims[person.equip.typ]
    if crit and hit:
        #sets to critical attack animation
        frames,hitFrame = person.anims[person.equip.typ+"crit"]
    for i in range(hitFrame):
        #draws frames up to the hit frame
        screen.blit(filler,(0,0))
        screen.blit(frames[i],(0,200))
        time.wait(50)
        display.flip()
    if person.equip.anims != None:
        #if the person's weapon has an animation, we draw it
        weapFiller = screen.copy() #weapon filler - only for the weapon
        for f in person.equip.anims:
            screen.blit(weapFiller,(0,0))
            screen.blit(f,(0,200)) #draws all the frames of the equipped weapon's animation
            display.flip()
            time.wait(50)
        screen.blit(weapFiller,(0,0))
    if not hit:
        screen.blit(papyrus.render("MISS!",True,(0,0,0)),(x,y))
        display.flip()
        time.wait(500)
    elif dam == 0:
        screen.blit(papyrus.render("NO DAMAGE!",True,(0,0,0)),(x,y))
        display.flip()
        time.wait(500)
    else:
        drawHealthLoss(screen,person2,dam,hpx,hpy,isenemy)
    for i in range(hitFrame,len(frames)):
        #draws remaining frames for animation
        screen.blit(filler,(0,0))
        screen.blit(frames[i],(0,200))
        time.wait(50)
        display.flip()
    screen.blit(filler,(0,0))
    screen.blit(person.anims["stand"],(0,200)) #draws standing sprite
    display.flip()
    if hit or person.equip.mag:
        #reduces durability if person hits enemy
        #or if the weapon is magical (they lose durability whether
        #they hit or not)
        person.equip.dur -= 1
        if person.equip.dur == 0:
            person.items.remove(person.equip) #removes weapon if destroyed
            person.equip = None #sets equip to None
            for w in [item for item in person.items if type(item) == Weapon]:
                #tries to equip weapons
                if person.equipWeapon(w):
                    break
    time.wait(300)

def drawExpGain(ally,expgain,screen):
    "draws exp gain (a bar filling up with exp)"
    screenBuff = screen.copy()
    draw.rect(screen,BLUE,(420,330,360,60)) #backdrop for exp bar
    draw.rect(screen,BLACK,(450,345,300,30)) #draws exp bar black (non-filled exp)
    draw.rect(screen,YELLOW,(450,345,int(300*(ally.exp/100)),30)) #draws filled exp
    screen.blit(sans.render(str(ally.exp),True,WHITE),(422,335)) #writes exp
    display.flip()
    time.wait(200)
    appExp = ally.exp #apparent exp
    for i in range(expgain):
        appExp += 1
        if appExp >= 100:
            appExp = 0 #makes sure apparent Experience does not exceed 99
        draw.rect(screen,BLUE,(420,330,360,60)) #backdrop for exp bar
        draw.rect(screen,BLACK,(450,345,300,30))
        draw.rect(screen,YELLOW,(450,345,int(300*(appExp/100)),30)) #draws filled exp bar
        screen.blit(sans.render(str(appExp),True,WHITE),(420,340)) #writes exp
        time.wait(50)
        display.flip()
        
