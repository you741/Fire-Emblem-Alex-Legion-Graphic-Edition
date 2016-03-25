from pygame import *
from feclasses import *
from festaples import *
from feterrain import *
from feweapons import *
from fesprites import *
from copy import deepcopy
from random import *
screen = display.set_mode((1200,720))

screen.fill((0,255,0))
#FONTS
font.init()
smallsans = font.SysFont("Comic Sans MS",15)
sans = font.SysFont("Comic Sans MS",20)
papyrus = font.SysFont("Papyrus",20)
#TERRAIN
plain = Terrain("Plain",0,0,1)
#WEAPONS
real_knife = Weapon("Real Knife",99,1,1000,999,"Sword",600)
iron_bow = Weapon("Iron Bow",6,6,46,80,"Bow",100,0,2,46,False,[],2)
iron_lance = Weapon("Iron Lance",7,8,45,80,"Lance",100)
silver_lance = Weapon("Silver Lance",14,10,20,75,"Lance",100)
fire = Weapon("Fire",5,4,40,95,"Anima",100,0,1,40,True,"",2)
slim_sword = Weapon("Slim Sword",3,2,35,100,"Sword",200,5)
steel_sword = Weapon("Steel Sword",8,10,30,80,"Sword",200)
iron_sword = Weapon("Iron Sword",5,5,47,90,"Sword",100)
iron_axe = Weapon("Iron Axe",8,10,45,75,"Axe",100)
rapier = Weapon("Rapier",7,5,40,90,"Sword",700,10,1,40,False,["Cavalier","Paladin","Knight","General"],1,5,"Effective against knights, cavalry","Yoyo")
vulnerary = Item("Vulnerary",3,"Heals for 10 HP")

#TRANSLUCENT SQUARES
transBlue = Surface((30,30), SRCALPHA)
transBlue.fill((0,0,255,122))
transRed = Surface((30,30), SRCALPHA)
transRed.fill((255,0,0,122))
transBlack = Surface((1200,720), SRCALPHA)
transBlack.fill((0,0,0,122))
#PERSONS
yoyo = Lord("Yoyo",0,0,
               {"lv":1,"stren":5,"defen":4,"skl":7,"lck":7,
                "spd":5,"con":5,"move":5,"res":4,"hp":18,"maxhp":18},
               {"stren":40,"defen":30,"skl":70,"lck":70,
                "spd":40,"res":50,"maxhp":60},
               [rapier.getInstance(),iron_bow.getInstance(),vulnerary.getInstance()],{"Sword":200},
               {"attack":(yoyoAttackSprite,5),"stand":yoyoStandSprite,"crit":(yoyoCritSprite,29)}) #test person
allies = [yoyo] #allies
#ENEMIES
dummy = Brigand("Dummy",0,0,
                  {"stren":3,"defen":3,"skl":3,"lck":0,
                   "spd":3,"con":3,"move":3,"res":0,"hp":33,"maxhp":33},{},[iron_bow.getInstance()],{"Bow":600},{})
enemies = []
#CHAPTERS
#MAPS
chapter0 = [[plain for i in range(40)] for j in range(24)]
#CHAPTER DATA
#Stored in tuples
#(allyCoordinates,Enemies,Goal)
chapterData = [([(0,0)],createEnemyList([dummy],[3],[(3,3),(3,1),(4,2)]),"Defeat all enemies")] #chapter data, chapter is determined by index
oldAllies = [a.getInstance() for a in allies] #keeps track of allies before the fight
moved,attacked = set(),set() #sets of allies that already moved or attacked
selectx,selecty = 0,0 #select points
#GLOBAL FUNCTIONS
#LIKE TURN STARTING, GAME OVER SCREENS, SAVING
#PRETTY MUCH GLOBAL AFFECTORS (Sorry I'm really bad at naming things)
def startTurn():
    "starts the turn"
    global allies,enemies,moved,attacked
    screenBuff = screen.copy() #sets the screenBuffer to cover up the text
    screen.blit(transform.scale(transBlue,(1200,60)),(0,330)) #blits the text "PLAYER PHASE" on a translucent blue strip
    screen.blit(papyrus.render("PLAYER PHASE",True,(255,255,255)),(450,340))
    moved.clear() #empties moved and attacked
    attacked.clear()
    display.flip() #updates screen
    time.wait(1000)
    screen.blit(screenBuff,(0,0)) #covers up text
    display.flip()
def gameOver():
    "game over screen - might be a class later"
    for i in range(50):
        screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fadinge effect
        display.flip()
        time.wait(50)
    screen.blit(papyrus.render("GAME OVER",True,(255,0,0)),(500,300))
    display.flip()
def start():
    "starts a chapter, also serves a restart"
    global mode,allies,enemies,goal,selectx,selecty
    selectx,selecty = 0,0
    allyCoords,newenemies,goal = chapterData[chapter]
    enemies = [e.getInstance() for e in newenemies]
    allies = [a.getInstance() for a in oldAllies]
    for i in range(len(allyCoords)):
        allies[i].x,allies[i].y = allyCoords[i] #sets all ally coords
        exec("global "+allies[i].name.lower()+"\n"+allies[i].name.lower()+"=allies[i]")
    moved.clear()
    attacked.clear()
    mode = "freemove"
    screen.fill((0,255,0)) #replace this with map sprite later
    drawGrid(screen)
    startTurn()
#DRAWING FUNCTIONS
def drawHealthBar(person,x,y):
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
        draw.line(screen,(0,255,0),(hpx+i*4,hpy),(hpx+i*4,hpy+30),3)
def drawHealthLoss(person,dam,x,y,enemy=True):
    "draws a depleting health bar"
    for i in range(dam):
        #for every point of damage we loop and remove it
        if person.hp == 0:
            break
        person.hp -= 1
        if enemy:
            draw.rect(screen,(255,0,0),(0,600,500,100))
        else:
            draw.rect(screen,(0,0,255),(700,600,500,100))
        drawHealthBar(person,x,y)
        screen.blit(sans.render(str(person.hp),True,(255,255,255)),(x+160,y+5))
        display.flip()
        time.wait(50)
def drawItemMenu(person,x,y):
    "draws an item menu for a person"
    if x + 8 > 39:
        x -= 9
    if y + 5 > 24:
        y -= 4
    draw.rect(screen,(0,0,255),(x*30,y*30,240,150))
    for i in range(5):
        if i < len(person.items):
            col = (255,255,255)
            if type(person.items[i]) == Weapon:
                if not person.canEquip(person.items[i]):
                    #if the person cannot equip, the color goes grey
                    col = (160,160,160)
            screen.blit(sans.render(person.items[i].name,True,col),(x*30,(y+i)*30))
            screen.blit(sans.render(str(person.items[i].dur)+"/"+str(person.items[i].maxdur),True,col),((x+6)*30,(y+i)*30)) #blits durability
    draw.rect(screen,(255,255,255),(x*30,(y+menuselect)*30,240,30),1) #draws selected item
#USER INTERFACE FUNCTION
def moveSelect():
    "moves selector"
    global selectx,selecty
    kp = key.get_pressed()
    oldx,oldy = selectx,selecty #old coords for if user moves out of range
    if kp[K_UP]:
        selecty -= 1
    if kp[K_DOWN]:
        selecty += 1
    if kp[K_LEFT]:
        selectx -= 1
    if kp[K_RIGHT]:
        selectx += 1
    if mode in ["freemove","move"]:
        selectx = min(39,max(0,selectx))
        selecty = min(23,max(0,selecty))
#PERSON ACTIONS
#ATTACK FUNCTIONS
def getAttackResults(person,enemy):
    "performs an attack on enemy by person, returns if it hit or crit and total damage"
    hit,dam,crit = False,0,False #hit = did it hit?; dam = damage; crit = did it crit?
    if randint(0,99) < person.getHit(enemy,eval("chapter"+str(chapter))):
        hit = True
        dam = person.getDamage(enemy,eval("chapter"+str(chapter)))
        if randint(0,99) < person.getCritical(enemy):
            crit = True
            dam *= 3 #damage is tripled
    return (hit,dam,crit) #returns (hit,dam,crit)
def singleAttack(person,person2,x,y,hpx,hpy,isenemy):
    "animates a single attack"
    hit,dam,crit = getAttackResults(person,person2) #gets attack results
    if "stand" in person2.anims:
        #draws person 2's standing animation
        screen.blit(person2.anims["stand"],(0,200))
    filler = screen.copy().subsurface(Rect(0,0,1200,600))
    if "attack" in person.anims and (not crit or not hit):
        #draws non-crit attack animation
        frames,hitFrame = person.anims["attack"]
    if "crit" in person.anims and crit and hit:
        #draws crit attack animation
        frames,hitFrame = person.anims["crit"]
    if ("crit" in person.anims and crit and hit) or ("attack" in person.anims and (not crit or not hit)):
        #once everyone has an animation we won't need this if statement
        #all it does is make sure we have the proper animation for the required action
        for i in range(hitFrame):
            screen.blit(filler,(0,0))
            screen.blit(frames[i],(0,200))
            time.wait(50)
            display.flip()
    if not hit:
        screen.blit(papyrus.render("MISS!",True,(0,0,0)),(x,y))
        display.flip()
        time.wait(500)
    elif dam == 0:
        screen.blit(papyrus.render("NO DAMAGE!",True,(0,0,0)),(x,y))
        display.flip()
        time.wait(500)
    else:
        drawHealthLoss(person2,dam,hpx,hpy,isenemy)
    if ("crit" in person.anims and crit and hit) or ("attack" in person.anims and (not crit or not hit)):
        #can remove if statement once there is an animation for everyone
        for i in range(hitFrame,len(frames)):
            screen.blit(filler,(0,0))
            screen.blit(frames[i],(0,200))
            time.wait(50)
            display.flip()
        screen.blit(filler,(0,0))
        screen.blit(frames[0],(0,200)) #draws first frame again
        display.flip()
    display.flip()
    person.equip.dur -= 1
    if person.equip.dur == 0:
        person.items.remove(person.equip)
        person.equip = None
        for w in [item for item in person.items if type(item) == Weapon]:
            if person.equipWeapon(w):
                break
    time.wait(300)
def checkDead(ally,enemy):
    "checks if an ally or an enemy is dead; also removes ally or enemy from list"
    if ally.hp == 0:
        allies.remove(ally)
        if ally in moved:
            moved.remove(ally)
        return True
    if enemy.hp == 0:
        enemies.remove(enemy)
        if ally in moved:
            moved.remove(enemy)
        return True
    return False
def attack(person,person2):
    "attack animation of person to person2"
    #sets who is the ally and who is the enemy
    if person in allies:
        ally = person
        enemy = person2
    else:
        ally = person2
        enemy = person
    filler = screen.copy()
    screen.fill((0,0,0)) #blackens screen
    display.flip()
    time.wait(200)
    draw.rect(screen,(0,255,0),(0,0,1200,600))
    draw.rect(screen,(0,0,255),(900,220,300,50)) #ally name rectangle
    draw.rect(screen,(255,0,0),(0,220,300,50)) #enemy name rectangle
    #draws ally and enemy's names
    screen.blit(sans.render(stripNums(ally.name),True,(255,255,255)),(920,220))
    screen.blit(sans.render(stripNums(enemy.name),True,(255,255,255)),(50,220))
    actionFiller = screen.copy().subsurface(Rect(0,0,1200,600)) #filler for the action
    #blits standing sprites for Person 1 and 2
    if "stand" in person.anims:
        screen.blit(person.anims["stand"],(0,200))
    if "stand" in person2.anims:
        screen.blit(person2.anims["stand"],(0,200))
    draw.rect(screen,(0,0,255),(700,600,500,120)) #draws ally health background
    draw.rect(screen,(255,0,0),(0,600,500,120)) #draws enemy health background
    drawHealthBar(ally,870,615)
    drawHealthBar(enemy,170,615)
    screen.blit(sans.render(str(ally.hp),True,(255,255,255)),(1032,620))
    screen.blit(sans.render(str(enemy.hp),True,(255,255,255)),(332,620))
    display.flip()
    time.wait(200)
    #sets variables for person drawing
    #differs based on which is enemy and which is ally
    if person2 == enemy:
        x,y = 725,300
        hpx,hpy = 870,615
        isenemy = False
        x2,y2 = 25,300
        hpx2,hpy2 = 170,615
    else:
        x,y = 25,300
        hpx,hpy = 170,615
        isenemy = True
        x2,y2 = 725,300
        hpx2,hpy2 = 870,615
    #Draws damage for attack 1
    screen.blit(actionFiller,(0,0)) #covers both persons
    singleAttack(person,person2,x2,y2,hpx2,hpy2,not isenemy)
    if checkDead(ally,enemy):
        return False #ends the function if either ally or enemy is dead
    #Draws damage for attack 2
    if canAttackTarget(person2,person):
        #if person2 can attack
        screen.blit(actionFiller,(0,0)) #covers both persons
        singleAttack(person2,person,x,y,hpx,hpy,isenemy)
    if checkDead(ally,enemy):
        return False
    #Draws damage for attack 3
    screen.blit(actionFiller,(0,0)) #covers both persons
    if ally.getAtkSpd() - 4 >= enemy.getAtkSpd() and canAttackTarget(ally,enemy):
        singleAttack(ally,enemy,25,300,170,615,True)
    if ally.getAtkSpd() + 4 <= enemy.getAtkSpd() and canAttackTarget(enemy,ally):
        singleAttack(enemy,ally,725,300,870,615,False)
    display.flip()
    time.wait(1000)
    screen.blit(filler,(0,0))
    checkDead(ally,enemy)
#important variables
chapter = 0
mode = "freemove"
goal = ""
selected = None #selected Person
selectedItem = None #selected Item
attackableEnemies = [] #attackable enemies of the selected person
selectedEnemy = 0 #selected Enemy
menu = None #options in menu
menuselect = 0 #option selected in the menu
running = True
framecounter = 0
#starts chapter
start()
filler = screen.copy() #filler
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if mode == "gameover":
                start()
                continue
            kp = key.get_pressed()
            
            if mode in ["freemove","move"]:
                #freemove moves freely; move picks a location
                moveSelect() #handles movements by player
                framecounter = 0
            
            if mode in ["optionmenu","itemattack"] or (mode == "item" and selectedItem == None):                    
                #moves menu option
                if kp[K_UP]:
                    menuselect -= 1
                elif kp[K_DOWN]:
                    menuselect += 1
                if mode == "optionmenu":
                    limit = len(menu)
                elif mode == "item":
                    limit = len(selected.items)
                else:
                    limit = 5
                if menuselect < 0:
                    menuselect = limit - 1
                elif menuselect >= limit:
                    menuselect = 0

            if mode == "attack":
                #changes enemy selected
                if kp[K_RIGHT] or kp[K_DOWN]:
                    selectedEnemy += 1
                if kp[K_LEFT] or kp[K_UP]:
                    selectedEnemy -= 1
                if selectedEnemy == len(attackableEnemies):
                    selectedEnemy = 0
                elif selectedEnemy == -1:
                    selectedEnemy = len(attackableEnemies)-1
                selectx,selecty = attackableEnemies[selectedEnemy].x,attackableEnemies[selectedEnemy].y
            
            if e.unicode.lower() == "z":
                #if the user pressed z
                #handles clicks
                if mode == "freemove":
                    for p in allies+enemies:
                        #checks if ally or enemy is clicked
                        if selectx == p.x and selecty == p.y and p not in moved:
                            mode = "move"
                            selected = p
                            oldx,oldy = p.x,p.y #keeps track of ally's position before so that we can backtrace
                            acoords = [(a.x,a.y) for a in allies]
                            encoords = [(e.x,e.y) for e in enemies]
                            if selected in allies:
                                #we get movements below
                                moveableSquares = getMoves(selected,selected.x,selected.y,selected.move,eval("chapter"+str(chapter)),acoords,encoords,{})
                                attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in moveableSquares]+[(p.x,p.y)],p)
                                if attackableSquares:
                                    #we get all attackables squares that we cannot move to
                                    attackableSquares = [sq for sq in attackableSquares if sq not in [(x,y) for x,y,m in moveableSquares] and sq not in acoords]
                            elif selected in enemies:
                                moveableSquares = getMoves(selected,selected.x,selected.y,selected.move,eval("chapter"+str(chapter)),encoords,acoords,{})
                                attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in moveableSquares]+[(p.x,p.y)],p)
                                if attackableSquares:
                                    #we get all attackable squares that we cannot move to
                                    attackableSquares = [sq for sq in attackableSquares if sq not in [(x,y) for x,y,m in moveableSquares] and sq not in encoords]
                            break#if we are in move mode we consistently fill moveable and attackable squares
                
                elif mode == "move":
                    #moves the unit if it is an ally
                    if (selectx,selecty) in [(x,y) for x,y,m in moveableSquares]+[(selected.x,selected.y)] and selected in allies:
                        selected.x,selected.y = selectx,selecty
                        mode = "optionmenu"
                        menu = []
                        menuselect = 0
                        #----Menu Creation
                        #ATTACK OPTION
                        if not (selected in attacked or selected.equip == None):
                            for w in [i for i in selected.items if type(i) == Weapon]:
                                #checks every weapon if one yields in an attack we equip it and add attack
                                if not selected.canEquip(w):
                                    continue
                                if len(getAttackableEnemies(selected,enemies,weapon=w)) > 0:
                                    selected.equipWeapon(w)
                                    menu.append("attack")
                                    break
                        #ITEM OPTION
                        if len(selected.items) > 0:
                            menu.append("item")
                        #WAIT OPTION
                        menu.append("wait") #person can always wait

                elif mode == "optionmenu":
                    #allows user to select options
                    if menu[menuselect] == "attack":
                        mode = "itemattack"
                        menuselect = 0
                    if menu[menuselect] == "item":
                        mode = "item"
                        menuselect = 0
                    if menu[menuselect] == "wait":
                        mode = "freemove"
                        moved.add(selected)
                        attacked.add(selected)

                elif mode == "itemattack":
                    if menuselect < len(selected.items):
                        if type(selected.items[menuselect]) == Weapon:
                            if selected.canEquip(selected.items[menuselect]) and getAttackableEnemies(selected,enemies,weapon=selected.items[menuselect]):
                                mode = "attack"
                                selected.equipWeapon(selected.items[menuselect])
                                attackableEnemies = getAttackableEnemies(selected,enemies)
                                selectx,selecty = attackableEnemies[0].x,attackableEnemies[0].y
                                selectedEnemy = 0

                elif mode == "attack":
                    #does an attack
                    attack(selected,attackableEnemies[selectedEnemy])
                    attacked.add(selected)
                    moved.add(selected)
                    mode = "freemove"

                elif mode == "item":
                    #handles item selection
                    selectedItem = selected.items[menuselect]
                    if type(selectedItem) == Weapon:
                        pass

##                    mode = "freemove"
##                    moved.add(selected) #unit gets appended to moved
##                    if selected.mounted:
##                        #handle this later NOTEITHOIESHFOIAWHFIOAWEHIOFHNAWGHISEHFUIGWAHOIFEK
##                        #N O T I C E   M E   Y O U - S E N P A I ! ! !   H A N D L E   M O U N T E D   U N I T S ! ! ! ! ! ! ! ! ! ! !
##                        movesMem[selected.name] = getMoves(selected,selected.x,selected.y,selected.move,
##                                                           eval("chapter"+str(chapter)),[(a.x,a.y) for a in allies],[(e.x,e.y) for e in enemies],{})
##                        if selected not in attacked:
##                            attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in movesMem[selected.name]],selected)
##                            if attackableSquares:
##                                #we memorize all attackables squares that we cannot move to
##                                attacksMem[selected.name] = [sq for sq in attackableSquares if sq not in [(x,y) for x,y,m in movesMem[selected.name]] and sq != (selected.x,selected.y)]
            
            if e.unicode.lower() == "x":
                #if the user pressed x
                #handles backtracing
                if mode == "move":
                    mode = "freemove"
                elif mode == "optionmenu":
                    mode = "move"
                    selected.x,selected.y = oldx,oldy
                elif mode == "itemattack":
                    mode = "optionmenu"
                    menuselect = 0
                elif mode == "item":
                    mode = "optionmenu"
                    menuselect = 0
                elif mode == "attack":
                    menuselect = 0
                    mode = "itemattack"

            if e.unicode == " ":
                #restarts turn
                #only temporary
                startTurn()
    if mode == "gameover":
        continue
    screen.blit(filler,(0,0)) #blits the filler
    if yoyo.hp == 0 and mode != "gameover":
        gameOver()
        mode = "gameover"
        continue
    kp = key.get_pressed()
    #HANDLES HOLDING ARROW KEYS
    if kp[K_LEFT] or kp[K_RIGHT] or kp[K_UP] or kp[K_DOWN] and mode in ["freemove","move"]:
        #increases frame counter if we're holding something
        framecounter += 1
    if framecounter > 100 and mode in ["freemove","move"]:
        #if framecounter is greater than 60 we move more
        moveSelect()
        time.wait(50)
    #DRAWS PERSONS
    for p in allies+enemies:
        drawPerson(screen,p) #draws persons
    #--------------------HIGHLIGHTING A PERSON---------------#
    if mode == "freemove":
        for p in allies+enemies:
            if selectx == p.x and selecty == p.y:
                #DRAWS PERSON MINI DATA BOX
                pdbx,pdby = 0,0 #person data box x and y
                if selectx < 20 and selecty <= 12:
                    pdby = 630
                draw.rect(screen,(0,0,255),(pdbx,pdby,300,90)) #background box
                screen.blit(sans.render(stripNums(p.name),True,(255,255,255)),(pdbx+15,pdby+3)) #person's name
                screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,(255,255,255)),(pdbx+15,pdby+33)) #health
                draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                draw.line(screen,(255,255,0),(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                break
    #-------------DIFFERENT MODE DISPLAYS------------------#
    #MOVE MODE DISPLAY
    if mode == "move":
        #fills moveable and attackable squares
        fillSquares(screen,set([(x,y) for x,y,m in moveableSquares]),transBlue)
        if attackableSquares:
            fillSquares(screen,attackableSquares,transRed)
    #OPTION MENU MODE DISPLAY
    if mode == "optionmenu":
        #if it is menu mode we draw the menu
        menux,menuy = 36,2
        if selected.x >= 20:
            menux = 0
        draw.rect(screen,(0,0,255),(menux*30,menuy*30,120,len(menu)*30))
        for i in range(len(menu)):
            #for every option in menu, we write the text
            opt = menu[i].title()
            screen.blit(sans.render(opt,True,(255,255,255)),(menux*30,(menuy+i)*30))
        draw.rect(screen,(255,255,255),(menux*30,(menuy+menuselect)*30,120,30),1) #draws selected option
    #ATTACK MODE DISPLAY
    if mode == "itemattack":
        #displays item selection menu for attack
        drawItemMenu(selected,selected.x+1,selected.y)
    if mode == "attack":
        fillSquares(screen,getAttackableSquares(selected.equip.rnge,selected.equip.maxrnge,selected.x,selected.y),transRed) #highlights all attackable squares
    #ITEM MODE DISPLAY
    if mode == "item":
        screen.blit(transBlack,(0,0))
        drawItemMenu(selected,14,8)
    #---------------INFO DISPLAY BOXES----------------------#
    #TERRAIN DATA
    if mode == "freemove":
        tbx,tby = 1020,630 #terrain box x and y
        stage = eval("chapter"+str(chapter))
        if selectx >= 20:
            tbx = 0
        draw.rect(screen,(0,0,255),(tbx,tby,180,90))
        screen.blit(sans.render(stage[selecty][selectx].name,True,(255,255,255)),(tbx+15,tby+3))
        draw.rect(screen,(255,230,200),(tbx,tby+30,180,60))
        screen.blit(sans.render("DEFENSE: "+str(stage[selecty][selectx].adef),True,(0,0,0)),(tbx+15,tby+33))
        screen.blit(sans.render("AVOID: "+str(stage[selecty][selectx].avo),True,(0,0,0)),(tbx+15,tby+63))
    #GOAL BOX
    if mode == "freemove":
        goalx,goaly = 1020,0
        if selecty <= 12 and selectx >= 20:
            goaly = 630
        draw.rect(screen,(50,50,180),(goalx,goaly,180,90))
        screen.blit(smallsans.render(goal,True,(255,255,255)),(goalx+15,goaly+35))
    #---------------SELECTED SQUARE BOX----------------#
    if mode in ["freemove","move","attack"]:
        draw.rect(screen,(255,255,255),(selectx*30,selecty*30,30,30),1) #draws select box
    display.flip()
quit()
