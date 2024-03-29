#FE Staples keeps important functions and classes
#pretty much "staples" for my program
#mostly to make main.py easier to read...
from pygame import *
from random import *
from feweapons import *
from queue import *
from math import *
import winsound
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
smallsans = font.SysFont("Chomic Sans MS",15)
papyrus = font.SysFont("Papyrus",20)
superScript14 = font.Font("fonts/SUPERSCR.TTF",14)
superScript40 = font.Font("fonts/SUPERSCR.TTF",40)

fpsLimiter = time.Clock() #fps Limiting clock

#----SOUND EFFECTS----#
mixer.init()
hitSnd = mixer.Sound("music/snd_flameloop.ogg")
critSnd = mixer.Sound("music/snd_heavydamage.ogg")
healSnd = mixer.Sound("music/snd_fall2.ogg")
levelUpSnd = mixer.Sound("music/snd_ballchime.ogg")
missSnd = mixer.Sound("music/snd_bombfall.ogg")
nodamageSnd = mixer.Sound("music/snd_curtgunshot.ogg")

#IMAGES
infoBox = image.load('images/infoBox.png')
infoBoxNW = image.load('images/infoBoxNW.png')
storytextBG = transform.smoothscale(image.load("story/storytextbackground.png"),(1200,200))

#--battle images--#
battlestatblue = transform.smoothscale(image.load("images/battle/battlestatblue.png"),(50,50))
battlestatred = transform.smoothscale(image.load("images/battle/battlestatred.png"),(50,50))
healthbarblue = transform.smoothscale(image.load("images/battle/healthbarblue.png"),(500,120))
healthbarred = transform.smoothscale(image.load("images/battle/healthbarred.png"),(500,120))
nameblue = transform.smoothscale(image.load("images/battle/nameblue.png"),(300,50))
namered = transform.smoothscale(image.load("images/battle/namered.png"),(300,50))
weapontagr = transform.smoothscale(image.load("images/battle/weapontagr.png"),(450,50))
weapontagl = transform.flip(weapontagr,True,False)

#----Map Calculations----#

def getMoves(person,x,y,movesleft,stage,allies,enemies,visited):
    "returns all moveable squares with the pathing to it"
##    #NOTE: the dictionary "visited" stores the amount of moves left after travelling to a point
##    #in order to make this value optimal, I reset everytime I find a lower movesleft value
##    #this is only really useful for mounted units

    moveable = [(person.x,person.y,movesleft,[(person.x,person.y)])]

    q = Queue() #stored as (movesused,[paths]) 
    q.put((0,[(person.x,person.y)]))
    while not q.empty():
        node = q.get()
        place = node[-1][-1]
        if node[0] <= movesleft:
            if 0 <= place[0] < len(stage[0]) and 0 <= place[1] < len(stage) and (place not in visited or visited.get(place) < movesleft - node[0]):
                hind = stage[place[1]][place[0]].hind if not person.flying else 1
                if person.canPass(stage[place[1]][place[0]]) or place == (person.x,person.y):
                    if place not in allies+enemies:
                        #the path is already the shortest
                        moveable.append((place[0],place[1],movesleft-node[0],node[1]))
                    if place not in enemies:
                        #put  four directions in the queue
                        visited[place] = movesleft - node[0]
                        for k in [(0,1),(0,-1),(1,0),(-1,0)]:
                            q.put((node[0]+hind,node[1]+[(place[0]+k[0],place[1]+k[1])]))                        

    moveable = [(x,y,m,ali) for x,y,m,ali in moveable if visited[(x,y)] == m] #seeds out all non-optimal tuples (where m isn't as high as it could be)
    return moveable
        
def getAttackableEnemies(person,enemies,x=None,y=None,weapon=None):
    "returns attackable enemies by person (optional parameters for different (x,y))"
    atten = [] #attackble enemies
    for e in enemies:
        if canAttackTarget(person,e.x,e.y,x,y,weapon):
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
def getTargetableSquaresByMoving(moveablesquares,rnge,maxrnge):
    targetableSquares = set()
    for x,y in moveablesquares:
        for ax,ay in getAttackableSquares(rnge,maxrnge,x,y):
            targetableSquares.add((ax,ay))
    return targetableSquares
def getUnitsWithinRange(x,y,rnge,maxrnge,persons):
    "gets all units in persons within the range"
    units = []
    for p in persons:
        if rnge <= getDistance(x,y,p.x,p.y) <= maxrnge:
            units.append(p)
    return units
#----Other Calculations----#
def canAttackTarget(person,tx,ty,x=None,y=None,weapon=None):
    "returns whether person can target square (tx,ty)"
    if person.equip == None:
        return False
    if x == None:
        x = person.x
    if y == None:
        y = person.y
    weapon = person.equip if weapon == None else weapon
    return weapon.rnge <= getDistance(x,y,tx,ty) <= weapon.maxrnge
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
def getBattleStats(person,person2,stage):
    "returns a list of battle stats based on person and person2"
    if canAttackTarget(person,person2.x,person2.y):
        #only sets stats if ally can hit enemy, otherwise it sets them to "--"
        hit,dam,crit = person.getHit(person2,stage),person.getDamage(person2,stage),person.getCritical(person2)
        if person.getAtkSpd() >= person2.getAtkSpd()+4:
            dam = str(dam)
            dam += " x 2" #if we are fast enough to attack twice, we let the player know
    else:
        hit=dam=crit = "--"
    return [person.name,"HP: "+str(person.hp)+"/"+str(person.maxhp),
                   "Hit: "+str(hit),"Dmg: "+str(dam),"Crt: "+str(crit),"" if not person.equip else person.equip.name,
                   "" if person.getAdv(person2) == -1 else ("Advantage" if person.getAdv(person2) else "Disadvantage")]
#----Creation Functions----#
def createEnemyList(enemies,amounts,coords):
    "takes in a list of enemies, a corresponding list of amounts and a list of coordinates"
    enemyList = []
    enemyat = 0
    for i in range(len(enemies)):
        for j in range(amounts[i]):
            newEnemy = enemies[i].getInstance()
            newEnemy.x,newEnemy.y = coords[enemyat]
            enemyat += 1
            enemyList.append(newEnemy)
    return enemyList

#----Drawing Functions----#
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

def drawTransRect(screen,color,x,y,width,height):
    "draws a transparent rectangle"
    surf = Surface((width,height),SRCALPHA)
    surf.fill((color[0],color[1],color[2],140))
    screen.blit(surf,(x,y))
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
    levelUpSnd.play()
    screenBuff = screen.copy() #screen buffer
    screen.blit(tileBackground(transform.smoothscale(image.load("images/Menu/menubackground.png"),(100,60)),600,240),(300,240))
    person.stats["lv"] += 1 #increases stats level member by one (should be same as person's lv member after the increase)
    screen.blit(sans.render(person.name+" LV "+str(person.lv),True,WHITE),(300,240))
    statCoords = {"maxhp":(300,270),"stren":(300,300),"skl":(300,330),"spd":(300,360),"lck":(300,390),"defen":(300,420),
                  "res":(300,450)} #dictionary of the coordinates of every stat
    for i,k in enumerate(statCoords):
        screen.blit(sans.render(k.title()+": "+str(person.stats[k]),True,WHITE),statCoords[k])
    display.flip()
    time.wait(200)
    waitTime = 300
    for i,k in enumerate(statCoords):
        #draws a +1 next to every stat gained
        if person.stats[k] != eval("person."+k):
            er = handleEvents(event.get())
            if er == 1:
                quit()
            elif er == -1:
                waitTime = 1
            newStatValue = eval("person."+k)
            screen.blit(sans.render("+1 = "+str(newStatValue),True,WHITE),(statCoords[k][0]+150,statCoords[k][1])) #new stat 150 more to the right
            person.stats[k] = newStatValue
            display.flip()
            time.wait(waitTime)
    time.wait(1500)
    screen.blit(screenBuff,(0,0))
def drawPromotion(screen,person,oldPerson):
    "draws a promotion - very similar to drawLevelUp"
    screenBuff = screen.copy() #screen buffer    
    screen.blit(tileBackground(transform.smoothscale(image.load("images/Menu/menubackground.png"),(100,60)),600,240),(300,240))
    screen.blit(sans.render(oldPerson.name+" LV "+str(person.lv),True,WHITE),(300,240))
    statCoords = {"maxhp":(300,270),"stren":(300,300),"skl":(300,330),"spd":(300,360),"lck":(300,390),"defen":(300,420),
                  "res":(300,450)} #dictionary of the coordinates of every stat
    for i,k in enumerate(statCoords):
        screen.blit(sans.render(k.title()+": "+str(oldPerson.stats[k]),True,WHITE),statCoords[k])
    screen.blit(sans.render(oldPerson.__class__.__name__,True,WHITE),(500,240))
    display.flip()
    time.wait(300)                            
    if handleEvents(event.get()):
        quit()
    screen.blit(tileBackground(transform.smoothscale(image.load("images/Menu/menubackground.png"),(100,60)),600,240).subsurface(0,0,600,30),(300,240))
    screen.blit(sans.render(person.__class__.__name__,True,WHITE),(500,240))
    screen.blit(sans.render(person.name+" LV "+str(person.lv),True,WHITE),(300,240))
    display.flip()
    time.wait(500)
    if handleEvents(event.get()) == 1:
        quit()
    for i,k in enumerate(statCoords):
        #draws a +1 next to every stat gained
        if oldPerson.stats[k] != person.stats[k]:                            
            if handleEvents(event.get()) == 1:
                quit()
            newStatValue = person.stats[k]
            screen.blit(sans.render("+"+str(person.stats[k]-oldPerson.stats[k])+" = "+str(newStatValue),True,WHITE),(statCoords[k][0]+150,statCoords[k][1])) #new stat 150 more to the right
            display.flip()
            time.wait(500)
    for i,k in enumerate(person.mast):
        if k not in oldPerson.mast:
            dispTempMsg(screen,"You can now use "+k+" weapons",centerX=True,centerY=True)
        if handleEvents(event.get()) == 1:
            quit()
    time.wait(1500)                            
    if handleEvents(event.get()) == 1:
        quit()
    screen.blit(screenBuff,(0,0))
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
        
def drawStatBox(screen,person1,person2,stage,x,y,color):
    "draws a little stat box to show hit,dam and crit within a fight"
    hit,dam,crit = person1.getHit(person2,stage),person1.getDamage(person2,stage),person1.getCritical(person2)
    if color == BLUE:
        screen.blit(battlestatblue,(x,y-5))
    elif color == RED:
        screen.blit(battlestatred,(x,y-5))    #draws text
    screen.blit(smallsans.render("Hit "+str(hit),True,WHITE),(x,y))
    screen.blit(smallsans.render("Dmg "+str(dam),True,WHITE),(x,y+17))
    screen.blit(smallsans.render("Crt "+str(crit),True,WHITE),(x,y+34))

def drawBattleInfo(screen,ally,enemy,stage,heal=False,stf=False):
    "draws all the battle info on the screen"
    screen.blit(nameblue,(900,0))
    screen.blit(namered if not heal else nameblue,(0,0))
    screen.blit(weapontagr,(50,550))
    screen.blit(weapontagl,(700,550))
    drawStatBox(screen,ally,enemy,stage,1150,550,BLUE) #draws two little boxes
    drawStatBox(screen,enemy,ally,stage,0,550,RED if not heal else BLUE) #each shows the hit, dam and crit
    #draws ally and enemy's names
    screen.blit(sans.render(ally.name,True,WHITE),(960,10))
    screen.blit(sans.render(enemy.name,True,WHITE),(50,10))
    if ally.equip != None:
        screen.blit(sans.render(ally.equip.name,True,BLACK),(720,560))
    if heal:
        screen.blit(sans.render(stf.name,True,BLACK),(720,560))
    if enemy.equip != None:
        screen.blit(sans.render(enemy.equip.name,True,BLACK),(70,560))
    screen.blit(healthbarblue,(700,600))
    screen.blit(healthbarred if not heal else healthbarblue,(0,600))
    #draws ally and enemy's health bar
    drawHealthBar(screen,ally,870,615)
    drawHealthBar(screen,enemy,170,615)
    #writes the hp down
    screen.blit(sans.render(str(ally.hp),True,WHITE),(1032,620))
    screen.blit(sans.render(str(enemy.hp),True,WHITE),(332,620))
        
def drawHealthLoss(screen,person,dam,enemy=True):
    "draws a depleting health bar lowering at 20 FPS"
    for i in range(dam):
        er = handleEvents(event.get())
        if er == 1:
            quit()
        elif er == -1:
            person.hp -= dam - i
            person.hp = max(0, person.hp)
            #cover up the health bar so that it doesn't blit on top of itself
            if enemy:
                screen.blit(healthbarred,(0,600))
                x,y = 170,615 #sets enemy's health bar coordinates
            else:
                screen.blit(healthbarblue,(700,600)) #ally's covering
                x,y = 870,615
            drawHealthBar(screen,person,x,y)
            screen.blit(sans.render(str(person.hp),True,WHITE),(x+160,y+5))
            display.flip()
            fpsLimiter.tick(20) #lowers health at 20 FPS
            return
        #for every point of damage we loop and remove it
        if person.hp == 0:
            break
        person.hp -= 1
        #cover up the health bar so that it doesn't blit on top of itself
        if enemy:
            screen.blit(healthbarred,(0,600))
            x,y = 170,615 #sets enemy's health bar coordinates
        else:
            screen.blit(healthbarblue,(700,600)) #ally's covering
            x,y = 870,615
        #draw health bar and amount of health
        drawHealthBar(screen,person,x,y)
        screen.blit(sans.render(str(person.hp),True,WHITE),(x+160,y+5))
        display.flip()
        fpsLimiter.tick(20) #lowers health at 20 FPS
def drawHealthGain(screen,person,dam,enemy=True):
    "draws a increasing health bar lowering at 20 FPS"
    for i in range(dam):
        er = handleEvents(event.get())
        if er == 1:
            quit()
        elif er == -1:
            person.hp += dam - i
            person.hp = min(person.maxhp, person.hp)
            #cover up the health bar so that it doesn't blit on top of itself
            if enemy:
                screen.blit(healthbarblue,(0,600))
                x,y = 170,615 #sets enemy's health bar coordinates
            else:
                screen.blit(healthbarblue,(700,600))
                x,y = 870,615                
            drawHealthBar(screen,person,x,y)
            screen.blit(sans.render(str(person.hp),True,WHITE),(x+160,y+5))
            display.flip()
            fpsLimiter.tick(20) #lowers health at 20 FPS
            return
        #for every point of damage we loop and remove it
        if person.hp == person.maxhp:
            break
        person.hp += 1
        #cover up the health bar so that it doesn't blit on top of itself
        if enemy:
            screen.blit(healthbarblue,(0,600))
            x,y = 170,615 #sets enemy's health bar coordinates
        else:
            screen.blit(healthbarblue,(700,600))
            x,y = 870,615
        #draw health bar and amount of health
        drawHealthBar(screen,person,x,y)
        screen.blit(sans.render(str(person.hp),True,WHITE),(x+160,y+5))
        display.flip()
        fpsLimiter.tick(20) #lowers health at 20 FPS
def drawFrames(screen,frames):
    "draws all frames with an FPS of 20"
    filler = screen.copy().subsurface(Rect(0,0,1200,600))
    for f in frames:      
        if handleEvents(event.get()) == 1:
            quit()
        elif handleEvents(event.get()) == -1:
            screen.blit(filler,(0,0))
            screen.blit(frames[-1],(0,0)) #blits all frames
            fpsLimiter.tick(20)
            display.flip()
            return
        screen.blit(filler,(0,0))
        screen.blit(f,(0,0)) #blits all frames
        fpsLimiter.tick(20)
        display.flip()
        
def singleAttack(screen,person,person2,personAnims,person2Anims,isenemy,stage,weapanim=None,heal=False,stf=None):
    "animates a single attack"
    waitTime = 500
    if heal:
        equip=stf
        dam = person.getHeal(stf) #damage is negative for the heals
        hit = True
        crit = False
        if person2.equip == None:
            screen.blit(transform.flip(person2Anims["stand"],True,False),(0,0))
        else:
            screen.blit(transform.flip(person2Anims[person2.equip.typ][0][0],True,False),(0,0))
        filler = screen.copy().subsurface(Rect(0,0,1200,600))
        x = 25
        y = 300
        frames,hitFrame = personAnims["Staff"]
    else:
        equip = person.equip
        hit,dam,crit = getAttackResults(person,person2,stage) #gets attack results
        #draws person 2's standing sprite
        if person2.equip == None:
            screen.blit(person2Anims["stand"],(0,0))
        else:
            screen.blit(person2Anims[person2.equip.typ][0][0],(0,0))
        filler = screen.copy().subsurface(Rect(0,0,1200,600))
        #sets x and y for the text "MISS" and "NO DAMAGE"
        x = 725 if isenemy else 25
        y = 300
        if not crit or not hit:
            #sets to attack animation with weapon
            frames,hitFrame = personAnims[person.equip.typ]
        if crit and hit:
            #sets to critical attack animation
            frames,hitFrame = personAnims[person.equip.typ+"crit"]
    drawFrames(screen,frames[:hitFrame]) #draws frames up to the hit frame
    if weapanim != None:
        #if the person's weapon has an animation, we draw it
        weapAnims = weapanim
        if isenemy:
            weapAnims = [transform.flip(img,True,False) for img in weapAnims]
        weapFiller = screen.copy() #weapon filler - only for the weapon
        drawFrames(screen,weapAnims) #draws all weapon's animation
        screen.blit(weapFiller,(0,0)) #covers the weapon's final frame
    if handleEvents(event.get()) == 1:
        quit()
    elif handleEvents(event.get()) == -1:
        waitTime = 1
    if heal:
        healSnd.play()
        drawHealthGain(screen,person2,dam)
        display.flip()
        time.wait(waitTime)
    elif not hit:
        missSnd.play()
        screen.blit(papyrus.render("MISS!",True,WHITE,BLUE),(x,y)) #writes MISS
        display.flip()
        time.wait(waitTime)
    elif dam == 0:
        nodamageSnd.play()
        screen.blit(papyrus.render("NO DAMAGE!",True,WHITE,BLUE),(x,y)) #writes NO DAMAGE
        display.flip()
        time.wait(waitTime)
    else:
        if crit:
            critSnd.play()
        elif hit:
            hitSnd.play()
        drawHealthLoss(screen,person2,dam,not isenemy) #draws the health bar losing health for person2
    screen.blit(filler,(0,0)) #covers the screen
    drawFrames(screen,frames[hitFrame:]+[frames[0]]) #draws all frames with standing frame at the end
    if hit or equip.mag:
        #reduces durability if person hits enemy
        #or if the weapon is magical (they lose durability whether they hit or not)
        equip.dur -= 1
        if equip.dur == 0:
            #the weapon broke!
            person.removeItem(equip) #removes the weapon
            return False
    time.wait(waitTime)
    return True

def drawChangingBar(screen,amount,newAmount,total,x,y,width,height,label,wrap=True,col=BLUE):
    "draws a changing bar"
    screenBuff = screen.copy()
    direction = 1 if amount < newAmount else -1 #direction of change
    draw.rect(screen,col,(x,y,width,height))#draws outside rect
    draw.rect(screen,BLACK,(x+30,y+15,width-60,height-30))#draws full bar black
    draw.rect(screen,YELLOW,(x+30,y+15,int((width-60)*amount/total),height-30)) #draws filled part yellow
    draw.rect(screen,col,(x,y-25,50,25)) #draws a background for the label
    screen.blit(sans.render(label,True,WHITE),(x,y-25)) #blits label
    screen.blit(sans.render(str(amount),True,WHITE),(x+2,y+5)) #writes amount
    display.flip()
    time.wait(200) #updates screen so user can see original for a bit
    appAmount = amount #apparent amount
    for i in range(abs(newAmount-amount)):
        #loops through each unit of change
        appAmount += direction #changes apparent amount
        if wrap and appAmount >= total:
            appAmount = 0
        elif appAmount >= total:
            appAmount = total #if we do not wrap the apparent amout becomes max
        draw.rect(screen,col,(x,y,width,height))#draws outside rect
        draw.rect(screen,BLACK,(x+30,y+15,width-60,height-30))#draws full bar black
        draw.rect(screen,YELLOW,(x+30,y+15,int((width-60)*appAmount/total),height-30)) #draws filled part yellow
        draw.rect(screen,col,(x,y-25,50,25)) #draws a background for the label
        screen.blit(sans.render(label,True,WHITE),(x,y-25)) #blits label
        screen.blit(sans.render(str(appAmount),True,WHITE),(x+2,y+5)) #writes amount
        display.flip()
        time.wait(50)      
        if handleEvents(event.get()) == 1:
            quit()
        elif handleEvents(event.get()) == -1:
            display.flip()
            break
    screen.blit(screenBuff,(0,0))
def dispTempMsg(screen,msg,x=0,y=0,width=0,height=30,tim=750,centerX=False,centerY=False,fnt=sans):
    "displays message temporarily"
    buffer = screen.copy()
    img = fnt.render(msg,True,WHITE)
    width = img.get_width()+10 if width == 0 else width
    if centerX:
        x = (1200 - width)//2
    if centerY:
        y = (720 - height)//2
    draw.rect(screen,BLUE,(x-5,y,width,height))
    screen.blit(img,(x,y))
    display.flip()
    time.wait(tim)
    screen.blit(buffer,(0,0))
    event.clear()
def drawInfoBox(screen,ix,y,opt):
    "draws an info box"
    if opt == None:
        return 0
    if type(opt) == Weapon:
        screen.blit(infoBox,(ix,y))
        typ,mt,rnge,hit,wt,crit = str(opt.typ),str(opt.mt),str(opt.rnge),str(opt.acc),str(opt.wt),str(opt.crit)
        if rnge != str(opt.maxrnge):
            rnge = rnge + "-" + str(opt.maxrnge)
        typ += " " + ["F","E","D","C","B","A","S","Prf"][opt.mast//100]
        infos = [typ,mt,rnge,hit,wt,crit]
        coords = [(15,30),(45,60),(150,30),(150,60),(260,30),(260,60)]
        for i in range(6):
            screen.blit(superScript14.render(infos[i],True,BLACK),(coords[i][0]+ix,coords[i][1]+y))
        if opt.desc != "":
            draw.rect(screen,WHITE,(ix,y+100,334,20))
            screen.blit(superScript14.render(opt.desc,True,BLACK),(ix+15,y+100))
    else:
        screen.blit(infoBoxNW,(ix,y))
        screen.blit(superScript14.render(opt.desc,True,BLACK),(ix+15,y+30))
#------ENEMY AI-------#
def optimalValue(square,stage,allies):
    "returns how optimal the moving to that square is largest=good"
    #returns weighted:
    #if there are more allies to attack, if enemies can reach etc.
#    getOptimalAlly(enemy,stage,allies,moveableSquares)
    return 10

def pathtoAlly(enemy,stage,allies,enemies):
    "returns list of shortest path to an ally"
    #hypot does not work as it does not take into consideration of terrain (we need taxi-cab distance)
    #uses a priority direction, order of BFS goes in order with the direction the enemy needs to travel
    #simple Djikstra in a priorityQueue in order to get path to closest ally
    visited = [[0 for i in range (40)]for j in range (24)] #visited array the size of the map
    #(0,0) are placeholders, to allow [1] and [-1] to point at different values, also if the change is 0 then it doesn't move it, to no longer search
    acoords = [(a.x,a.y) for a in allies] #ally coordinates
    ecoords = [(e.x,e.y) for e in enemies] #enemy coordinates
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    q = PriorityQueue()
    enemycord = (enemy.x,enemy.y)
    q.put((stage[enemy.y][enemy.x].hind,enemycord,[enemycord]))
    while not q.empty():
        node = q.get()
        cost = node[0]
        spot = node[1]
        x,y = spot
        terr = stage[y][x]
        if not enemy.canPass(terr):
            continue #if we can't pass we move on
        if spot in ecoords:
            cost += 2 #increases cost for walking through enemies
        for w in [i for i in enemy.items if enemy.canEquip(i) and type(i) == Weapon]:
            for ax,ay in acoords:
                if canAttackTarget(enemy,ax,ay,x,y,w):
                    return node[2] #if we can attack an ally we're good
        if spot in acoords:
            return node[2] #stop when we find an ally - always closest due to PriorityQueue
        if 0 <= y < len(stage) and 0 <= x < len(stage[0]) and not visited[y][x] and enemy.canPass(terr):
            #deltas calculated by spot - target
            visited[y][x] = 1
            for d in directions:
                if 0 <= y+d[1] < len(stage) and 0 <= x+d[0] < len(stage[0]):
                    nterr = stage[y+d[1]][x+d[0]] #terrain
                    q.put((cost+nterr.hind,(x+d[0],y+d[1]),node[2] + [(x + d[0], y + d[1])]))
        if handleEvents(event.get()) == 1:
            quit()
    return -1

##def distAlly(enemycord,stage,allies):
##    "returns the length of the path to the nearest ally"
##    smallest = 1000000
##    for a in allies:
##        tmp = len(pathtoAlly(enemycord,stage,a))
##        if tmp < smallest:
##            smallest = tmp
##    return smallest
##
##def getOptimalSquare(enemy,stage,allies,moveableSquares):
##    "returns optimal square to move to, assuming enemy can't attack"
##    best = -9999
##    point = (enemy.x,enemy.y)
##    for i in moveableSquares:
##        ##optimize such that the square that is moved to is the one where the next move will hit the best ally
##        #weight will be optimal value - movesleft (to go furthest possible) + distance to closest ally (to close distance)
##        #optimal value is maximum damage with multiplier?
##        #i is in form x,y,m,ali
##        tmp = optimalValue((i[0],i[1]),stage,allies) + i[2]*2 - distAlly((i[0],i[1]),stage,allies)*3
##        if tmp > best:
##            point = (i[0],i[1])
##            best = tmp
##    #returns best coord to move to
##    return point

def getEnemyAction(enemy,stage,allies,moveableSquares):
    "returns whether enemy should attack or move"
    if enemy.throne:
        moveableSquares = [(enemy.x,enemy.y)] #throne guard can't move
    if enemy.equip == None:
        if enemy.guard or enemy.throne:
            return "stay"
        return "move"
    attackableSquares = getAttackableSquaresByMoving(moveableSquares,enemy)
    attackableAllies = [(a.x,a.y) for a in allies if (a.x,a.y) in attackableSquares]
    if len(attackableAllies) > 0:
        return "attack" #enemy attacks if enemy can
    elif enemy.guard or enemy.throne:
        return "stay"
    return "move" #if enemy can't attack they just move

def getOptimalAlly(enemy,stage,attackableAllies,moveableSquares):
    "returns optimal ally out of attackableAllies, as well as which weapon to use and where to move"
    #returns a tuple (ally,x,y)
    
    bestdam = -1 #best damage
    bestAlly = attackableAllies[0]
    bestWeapon = enemy.equip
    bestx,besty = 0,0
    #(percentage of health damage against ally,hit chance against ally,damage against enemy,hit chance of ally against enemy)
    for a in attackableAllies:
        for w in [i for i in enemy.items if type(i) == Weapon]:
            #goes through all weapons, equips them, and checks damage
            if enemy.equipWeapon(w):
                #equip sucess
                for x,y in moveableSquares:
                    if canAttackTarget(enemy,a.x,a.y,x,y):
                        break
                else:
                    #if we could not attack any allies with the current weapon, we move on
                    continue
                perdam = 100*enemy.getDamage(a,stage)/a.hp #percentage of health damage
                if perdam > bestdam:
                    bestdam = perdam
                    bestAlly = a
                    bestWeapon = w #sets the best stuff
    enemy.equipWeapon(bestWeapon) #equips best weapon
    allCoords = [(x,y) for x,y in getAttackableSquares(enemy.equip.rnge,enemy.equip.maxrnge,bestAlly.x,bestAlly.y)
                 if (x,y) in moveableSquares] #all coordinates where enemy can attack ally
    bestx,besty = allCoords[0] #best place to move and attack ally
    for x,y in allCoords:
        if not canAttackTarget(bestAlly,x,y):
            #checks if ally can attack the enemy at position (x,y)
            #if they cannot, we set the bestx and besty to this value and break
            bestx,besty = x,y
            break
    return (bestAlly,bestx,besty)


#----STORY FUNCTIONS----#
def drawSentence(screen,sentence,x=10,y=530,fnt=sans):
    "draws the sentence as a dialogue box"
    winsound.Beep(500,33)
    screen.blit(storytextBG,(0,520))    
    words = sentence.split()
    for i in range(len(words)):
        word = words[i] #current word
        nextWord = None
        if i < len(words)-1:
            nextWord = words[i+1]
        img = fnt.render(word+" ",True,WHITE) #img of blitted word
        width = img.get_width()
        if width + x > 1200:
            x = 10
            y += 25 #moves on to next line if we go over
        screen.blit(img,(x,y))
        x += width

def writeDialogue(screen,sentence,x=0,y=530,name=None,face=None,fnt=sans):
    "writes the sentence on the screen character by character, char by char"
    character = 1 #up to which character we display
    while character <= len(sentence):
        #loops to draw all the characters one by one
        for e in event.get():
            if e.type == QUIT:
                return 0
            
            #blitting all the text if they choose to skip
            if e.type == KEYDOWN:
                if e.key == K_z or e.key == K_x or e.key == K_RETURN:
                    character = len(sentence)
            elif e.type == MOUSEBUTTONDOWN:
                character = len(sentence)
                
        if name != None:
            screen.blit(face,(x,y-120)) #blits face of character speaking
            draw.rect(screen,YELLOW,(x,y-40,300,30)) #draws background box for name
            draw.rect(screen,BLUE,(x+2,y-38,294,26))
            screen.blit(sans.render(name,True,WHITE),(x+2,y-38))
        drawSentence(screen,sentence[:character],10,y,fnt) #draws the sentence up to character
        character += 1 #prepares to draw one more character
        display.flip()
        fpsLimiter.tick(30) #limits it to 30 FPS
    return 1

#----USEFUL FUNCTIONS----#
def isInt(string):
    "checks if a string represents an Int"
    try:
        int(string)
        return True
    except ValueError:
        return False
def handleEvents(events):
    "handles events and checks for quit"
    for e in events:
        if e.type == QUIT:
            return 1 #checks if user quits
        if e.type == KEYDOWN:
            if e.key in [K_RETURN]:
                return -1
    return 0
