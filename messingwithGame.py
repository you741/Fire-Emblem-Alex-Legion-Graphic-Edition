class Game():
    def __init__(self):
        "initializes game"
        self.selectx,self.selecty = 0,0 #select cursor starting point
        self.framecounter = 0
        self.clickedFrame = 0 #the frame user clicked (pressed z)
        self.fpsTracker = time.Clock() #fpsTracker
        self.mode = "freemove" #mode Game is in
        self.menuselect = 0 #option in menu selected
        self.menu = [] #menu for optionmenu mode
        self.selectedEnemy,self.selectedItem = 0,None #selected Enemy and selected Item
        self.selected = None #selected ally
        self.selected2 = None #2nd selected ally - only for trading option
        self.selectedAlly = 0 #2nd selected ally that user is hovering over - only for trading option and healing option
        self.targetableAllies = [] #targetable allies
        self.filler = screen.copy()
        self.moved,self.attacked = set(),set() #sets moved and attacked to be sets
        self.turn = 1 #turn that it is
        self.goal = ""
        self.stopped = False #we are not stopped
    def draw(self,screen):
        "draws game on screen - also starts game"
        self.start()
        self.filler = screen.copy() #filler
    def playMusic(self):
        "plays music for the chapter"
        #bgMusic.play(chapterMusic[chapter],-1)
        pass
    def gameVictory(self):
        "Victory, to continue the storyline"
        global oldAllies,allies,allAllies
        ##whatever animation/dialogue that needs to happen
        allAllies = [a for a in allAllies if a.name not in [al.name for al in allies]] #removes all of allies from allAllies
        allAllies += allies #adds allies to allAllies
        for a in allAllies:
            #brings all allies back to full health
            a.hp = a.maxhp
            a.stats["hp"] = a.maxhp
        draw.circle(screen,WHITE,(100,100),100) #NOTE TO ALBURITO!!!!!! !IJIOJOIASJFIOWJOIFWJFOIWJ!!!IJAOF! : th is this? got a circle fetish!? haha its a joke lol
        changemode(SaveGame())
    def drawPeople(self):
        "draws all people on the map"
        for a in allies:
            #draws one of four frames in the map sprite - changes sprites every 60 frames
            if a not in self.attacked or a not in self.moved:
                screen.blit(allyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
            else:
                #if the ally has moved already we draw it grey
                screen.blit(allyGreyMapSprites[a.__class__.__name__][self.framecounter%40//10],(a.x*30,a.y*30))
        for e in enemies:
            if e not in self.attacked or e not in self.moved:
                screen.blit(enemyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
            else:
                screen.blit(enemyGreyMapSprites[e.__class__.__name__][self.framecounter%40//10],(e.x*30,e.y*30))
    def start(self):
        "starts a chapter, also serves a restart"
        global allies,enemies,oldAllies
        self.selectx,self.selecty = 0,0
        newAllies,allyCoords,newenemies,self.goal,backgroundImage = chapterData[chapter]
        if chapter < 99:
            #the early chapters have no prefight screen to load oldAllies so allAllies are oldAllies
            oldAllies = [a.getInstance() for a in allAllies]
        enemies = [e.getInstance() for e in newenemies]
        allies = [a.getInstance() for a in oldAllies]
        allies += [a.getInstance() for a in newAllies] #adds all new allies to allies
        for i in range(len(allyCoords)):
            global player
            allies[i].x,allies[i].y = allyCoords[i] #sets all ally coords
            if allies[i].name.lower() not in usedNames:
                #player gets it's own variable, so it is special
                player = allies[i]
            else:
                #sets name representing ally to be the new instance
                exec("global "+allies[i].name.lower()+"\n"+allies[i].name.lower()+"=allies[i]")
        self.moved.clear()
        self.attacked.clear()
        screen.blit(backgroundImage,(0,0))#draws map background on the screen
        drawGrid(screen)
        self.startTurn()
    def startTurn(self):
        "starts the turn"
        global allies,enemies
        screenBuff = screen.copy() #sets the screenBuffer to cover up the text
        screen.blit(transform.scale(transBlue,(1200,60)),(0,330)) #blits the text "PLAYER PHASE" on a translucent blue strip
        screen.blit(papyrus.render("PLAYER PHASE",True,WHITE),(450,340))
        self.moved.clear() #empties moved and attacked
        self.attacked.clear()
        display.flip() #updates screen
        time.wait(1000)
        screen.blit(screenBuff,(0,0)) #covers up text
        display.flip()
        event.clear()#clears events so that it doesnt allow events to occur as soon as this ends
        self.mode = "freemove" #sets the mode back to freemove
    def endTurn(self):
        "ends the turn, starts the enemy turn"
        global running
        self.attacked.clear()
        self.moved.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        screenBuff = screen.copy()
        screen.blit(transform.scale(transRed,(1200,60)),(0,330)) #blits the text "ENEMY PHASE" on a translucent red strip
        screen.blit(papyrus.render("ENEMY PHASE",True,WHITE),(450,340))
        display.flip()
        time.wait(1000)
        screen.blit(screenBuff,(0,0))
        framelimiter = time.Clock()
        #ENEMY'S PHASE GOES HERE
        for i in range(len(enemies)-1,-1,-1):
            en = enemies[i]
            screen.blit(self.filler,(0,0)) #fills the screen
            for evnt in event.get():
                if evnt.type == QUIT:
                    running = False
                    return 0
            #DRAWS PEOPLE
            self.drawPeople()
            display.flip()
            time.wait(500)
            encoords = [(e.x,e.y) for e in enemies] #enemies' coordinates
            acoords = [(a.x,a.y) for a in allies] #allies' coordinates
            enMoves = getMoves(en,en.x,en.y,en.move,chapterMaps[chapter],encoords,acoords,{}) #enemy's moveableSquares
            enMoves = [(x,y) for x,y,m in enMoves]
            action = getEnemyAction(en,chapterMaps[chapter],allies,enMoves)
            if action == "attack":
                attackableSquares = getAttackableSquaresByMoving(enMoves,en) #attackableSquares by moving
                attackableAllies = [a for a in allies if (a.x,a.y) in attackableSquares]
                bestAlly,bestX,bestY = getOptimalAlly(en,chapterMaps[chapter],attackableAllies,enMoves)
                en.x,en.y = bestX,bestY
                screen.blit(self.filler,(0,0)) #fills the screen
                #DRAWS PEOPLE
                self.drawPeople()
                display.flip()
                time.wait(500)
                attack(en,bestAlly)
                if yoyo.hp == 0 or player.hp == 0:
                    return 0 #if yoyo or the player dies we leave the function, bounces to gameOver
            elif action == "move":
                pass
            self.turn += 1 #increases turn by 1
            self.moved.add(en)
            self.attacked.add(en)
            display.flip()
            framelimiter.tick(60)
        self.moved.clear()
        self.attacked.clear()
        screen.blit(self.filler,(0,0)) #fills the screen
        self.startTurn() #starts the turn      
    def gameOver(self):
        "draws game over screen"
        for i in range(50):
            screen.blit(transBlack,(0,0)) #fills the screen with black slowly over time - creates fadinge effect
            display.flip()
            time.wait(50)
        screen.blit(papyrus.render("GAME OVER",True,RED),(500,300))
        display.flip()
        changemode(StartMenu)
    def moveSelect(self):
        "moves selector"
        kp = key.get_pressed()
        if kp[K_UP]:
            self.selecty -= 1
        if kp[K_DOWN]:
            self.selecty += 1
        if kp[K_LEFT]:
            self.selectx -= 1
        if kp[K_RIGHT]:
            self.selectx += 1
        if self.mode in ["freemove","move"]:
            self.selectx = min(39,max(0,self.selectx))
            self.selecty = min(23,max(0,self.selecty))

    def run(self,screen):
        "runs the game in the running loop"
        global running,chapter
        #----EVENT LOOP----#
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if self.mode == "gameover":
                    self.start()
                    continue
                kp = key.get_pressed()

                
                #MOVEMENT OF SELECTION CURSOR OR MENU OPTION
                if self.mode in ["freemove","move"]:
                    #freemove moves freely; move picks a location
                    self.moveSelect() #handles movements by player
                    self.clickedFrame = self.framecounter #sets the clickedFrame to self
                if self.mode in ["optionmenu","itemattack","item","mainmenu"]:                    
                    #moves selected menu item
                    if self.mode in ["optionmenu","mainmenu"]:
                        self.menu.moveSelect()
                if self.mode == "attack":
                    #changes enemy selected
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        self.selectedEnemy += 1
                    if kp[K_LEFT] or kp[K_UP]:
                        self.selectedEnemy -= 1
                    if self.selectedEnemy == len(self.attackableEnemies):
                        self.selectedEnemy = 0
                    elif self.selectedEnemy == -1:
                        self.selectedEnemy = len(self.attackableEnemies)-1
                    self.selectx,self.selecty = self.attackableEnemies[self.selectedEnemy].x,self.attackableEnemies[self.selectedEnemy].y
                if self.mode in ["trade","heal"] and self.selected2 == None:
                    if kp[K_RIGHT] or kp[K_DOWN]:
                        self.selectedAlly += 1
                    if kp[K_LEFT] or kp[K_UP]:
                        self.selectedAlly -= 1
                    if self.selectedAlly == len(self.targetableAllies):
                        self.selectedAlly = 0
                    elif self.selectedAlly == -1:
                        self.selectedAlly = len(self.targetableAllies)-1
                elif self.mode == "trade":
                    #if we have a selected2 we move the item selector instead
                    #horizontal movement of item selector across two allies
                    if kp[K_RIGHT]:
                        self.menuselect[0] = 1
                    elif kp[K_LEFT]:
                        self.menuselect[0] = 0
                    #vertical movement within the item menu
                    selectedAllies = [self.selected,self.selected2] #the selected allies
                    self.menuselect[1] = self.moveMenuSelect(self.menuselect[1],5)
                #---------Z--------#
                if e.unicode.lower() == "z":
                    #if the user pressed z
                    #handles clicks
                    #FREE MOVE MODE
                    if self.mode == "freemove":
                        for p in allies+enemies:
                            #checks if ally or enemy is clicked
                            if self.selectx == p.x and self.selecty == p.y and p not in self.moved:
                                self.mode = "move"
                                self.selected = p
                                self.oldx,self.oldy = p.x,p.y #keeps track of ally's position before so that we can backtrace
                                acoords = [(a.x,a.y) for a in allies]
                                encoords = [(e.x,e.y) for e in enemies]
                                if p in allies:
                                    #we get movements below
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,chapterMaps[chapter],acoords,encoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackables squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in acoords]
                                elif p in enemies:
                                    self.moveableSquares = getMoves(p,p.x,p.y,p.move,chapterMaps[chapter],encoords,acoords,{})
                                    self.attackableSquares = getAttackableSquaresByMoving([(x,y) for x,y,m in self.moveableSquares]+[(p.x,p.y)],p)
                                    if self.attackableSquares:
                                        #we get all attackable squares that we cannot move to
                                        self.attackableSquares = [sq for sq in self.attackableSquares if sq not in [(x,y) for x,y,m in self.moveableSquares] and sq not in encoords]
                                break#if we are in move mode we constantly fill moveable and attackable squares
                        else:
                            #if the user presses a blank spot, we set the mode to main menu
                            self.mode = "mainmenu"
                            self.menu = ["end"] #menu has End turn
                            self.menuselect = 0

                            
                    #MOVE MODE
                    elif self.mode == "move":
                        #moves the unit if it is an ally and within the moveable squares
                        if (self.selectx,self.selecty) in [(x,y) for x,y,m in self.moveableSquares]+[(self.selected.x,self.selected.y)] and self.selected in allies:
                            self.selected.x,self.selected.y = self.selectx,self.selecty
                            self.mode = "optionmenu"
                            self.menu = []
                            self.menuselect = 0
                            #----Menu Creation
                            #ATTACK OPTION
                            if not (self.selected in self.attacked or self.selected.equip == None):
                                for w in [i for i in self.selected.items if type(i) == Weapon]:
                                    #checks every weapon if one yields in an attack we equip it and add attack
                                    if not self.selected.canEquip(w):
                                        continue
                                    if len(getAttackableEnemies(self.selected,enemies,weapon=w)) > 0:
                                        self.selected.equipWeapon(w)
                                        self.menu.append("attack")
                                        break
                            #ITEM OPTION
                            if len(self.selected.items) > 0:
                                self.menu.append("item")
                            #TRADE OPTION
                            if len(getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)) > 0:
                                self.menu.append("trade") #we can only trade if we have targetable allies within range 1
                            #WAIT OPTION
                            self.menu.append("wait") #a person can always wait
                    #MAIN MENU CLICK

                            
                    elif self.mode == "mainmenu":
                        #allows user to select options
                        if self.menu[self.menuselect] == "end":
                            self.mode = "enemyphase"
                            self.endTurn() #ends turn
                    #OPTION MENU CLICK
                    elif self.mode == "optionmenu":
                        #allows user to select options
                        if self.menu[self.menuselect] == "attack":
                            self.mode = "itemattack"
                            self.menuselect = 0
                        elif self.menu[self.menuselect] == "item":
                            self.mode = "item"
                            self.menuselect = 0
                        elif self.menu[self.menuselect] == "trade":
                            self.mode = "trade"
                            self.targetableAllies = getTargetableAllies(1,1,self.selected.x,self.selected.y,allies)
                            self.menuselect = [0,0] #menuselect becomes a list, first element is the selected person, second is the selected item
                        elif self.menu[self.menuselect] == "wait":
                            self.mode = "freemove"
                            self.moved.add(self.selected)
                            self.attacked.add(self.selected)
                    #ATTACK CLICKS
                    elif self.mode == "itemattack":
                        if self.menuselect < len(self.selected.items):
                            if type(self.selected.items[self.menuselect]) == Weapon:
                                if self.selected.canEquip(self.selected.items[self.menuselect]) and getAttackableEnemies(self.selected,enemies,weapon=self.selected.items[self.menuselect]):
                                    self.mode = "attack"
                                    self.selected.equipWeapon(self.selected.items[self.menuselect])
                                    self.attackableEnemies = getAttackableEnemies(self.selected,enemies)
                                    self.selectx,self.selecty = self.attackableEnemies[0].x,self.attackableEnemies[0].y
                                    self.selectedEnemy = 0
                    elif self.mode == "attack":
                        #does an attack
                        attack(self.selected,self.attackableEnemies[self.selectedEnemy])
                        self.attacked.add(self.selected)
                        self.moved.add(self.selected)
                        self.mode = "freemove"
                    #ITEM MODE CLICK
                    elif self.mode == "item":
                        #handles item selection
                        if self.selectedItem == None:
                            #selects an item and creates a submenu
                            self.optselected = 0 #option selected for the submenu
                            self.selectedItem = self.selected.items[self.menuselect]
                        elif type(self.selectedItem) == Weapon:
                            #if a weapon is selected, we check whether user equips or discards
                            #0 is equip, 1 is discard
                            if self.optselected:
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            else:
                                #equip option
                                self.selected.equipWeapon(self.selectedItem) #tries to equip
                            self.selectedItem = None #resets self.selectedItem
                            if self.selected.equip == None:
                                #if we have no equipped item we remove the attack option from menu
                                if "attack" in self.menu:
                                    self.menu.remove("attack")
                                #we also empty attackableSquares
                                self.attackableSquares = []
                        elif type(self.selectedItem) == Consumable:
                            #if a consumable is a selected, we check whehther uses or discards
                            #0 is use, 1 is discard
                            if self.optselected:
                                #discard option
                                self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                            else:
                                #use option
                                if not self.selectedItem.use(self.selected):
                                    #uses consumable
                                    #if it breaks we remove it
                                    self.selected.removeItem(self.selectedItem) #removes selectedItem from items
                                self.moved.add(self.selected) #unit must wait after using a consumable
                                self.attacked.add(self.selected)
                                self.oldx,self.oldy = self.selected.x,self.selected.y #no moving back after using a consumable
                                self.moveableSquares,self.attackableSquares = [],[] #empties moveablesquares
                                self.mode = "optionmenu"
                                self.menuselect = 0
                            self.selectedItem = None #resets selectedItem
                        if len(self.selected.items) == 0:
                            #if we have no items left, we go back to option menu and remove items from the list
                            self.menu.remove("item")
                            self.mode = "optionmenu"
                            self.menuselect = 0
                    #TRADE MODE CLICK
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            #if there is self.selected2, we set one
                            self.selected2 = self.targetableAllies[self.selectedAlly]
                        else:
                            #otherwise we select an item
                            if self.selectedItem == None:
                                #if we have no selectedItem we set one
                                self.selectedItem = self.menuselect[:]
                            else:
                                #if we have a selected item, we commence the trade
                                selectedAllies = [self.selected,self.selected2] #selected allies
                                selectedItem1 = selectedItem2 = None #the default selected Item is None
                                if self.selectedItem[1] < len(selectedAllies[self.selectedItem[0]].items):
                                    #1st item is in range and is not None, then we give it to the other selected ally
                                    selectedItem1 = selectedAllies[self.selectedItem[0]].items[self.selectedItem[1]] #first selected item
                                if self.menuselect[1] < len(selectedAllies[self.menuselect[0]].items):
                                    #2nd item is in range and is not None, then we give it to the other selected ally
                                    selectedItem2 = selectedAllies[self.menuselect[0]].items[self.menuselect[1]] #second selected item
                                if selectedItem1 != None:
                                    selectedAllies[self.selectedItem[0]].removeItem(selectedItem1) #removes first item
                                    selectedAllies[self.menuselect[0]].addItem(selectedItem1) #appends 1st item to second ally
                                if selectedItem2 != None:
                                    selectedAllies[self.menuselect[0]].removeItem(selectedItem2) #removes second item
                                    selectedAllies[self.selectedItem[0]].addItem(selectedItem2) #appends 2nd item to first ally
                                self.selectedItem = None #resets selectedItem

                #------X------#
                if e.unicode.lower() == "x":
                    #if the user pressed x
                    #handles backtracing
                    if self.mode == "move":
                        self.mode = "freemove"
                    elif self.mode == "mainmenu":
                        self.mode = "freemove"
                    elif self.mode == "optionmenu":
                        self.mode = "move"
                        self.selected.x,self.selected.y = self.oldx,self.oldy
                        if self.moveableSquares == []:
                            self.mode = "freemove" #we go back to freemove mode if we have no moveablesquares
                    elif self.mode == "itemattack":
                        self.mode = "optionmenu"
                        self.menuselect = 0
                    elif self.mode == "item":
                        if self.selectedItem != None:
                            #if we have a selected Item
                            #we have a submenu, so we close that instead
                            self.mode = "item"
                            self.selectedItem = None
                        else:
                            self.mode = "optionmenu"
                            self.menuselect = 0
                    elif self.mode == "trade":
                        if self.selected2 == None:
                            self.mode = "optionmenu"
                            self.menuselect = 0
                        else:
                            if self.selectedItem == None:
                                self.selected2 = None #if there exists selected2, that means the trade interface is open, so we close that
                            else:
                                #however if there is a selected item, we instead deselect it
                                self.selectedItem = None
                    elif self.mode == "attack":
                        self.menuselect = 0
                        self.mode = "itemattack"
                if e.unicode == "v":
                    #skips battle for now
                    self.gameVictory()
        if self.stopped:
            return 0 #ends the function if we stopped
        #-----END OF EVENT LOOP----#
        if self.mode == "gameVictory":
            return 0
        if self.mode == "gameover":
            return 0
        screen.blit(self.filler,(0,0)) #blits the filler
        if 0 in [player.hp,yoyo.hp] and self.mode != "gameover":
            self.gameOver()
            self.mode = "gameover"
            return 0
        kp = key.get_pressed()
        #HANDLES HOLDING ARROW KEYS
        if self.framecounter - self.clickedFrame > 20 and self.mode in ["freemove","move"] and not self.framecounter%6:
            #if we held for 20 frames or more we move more
            #we only do it once every 6 frames or it'll be too fast
            self.moveSelect()
        #--------------------HIGHLIGHTING A PERSON---------------#
        if self.mode == "freemove":
            for p in allies+enemies:
                if self.selectx == p.x and self.selecty == p.y:
                    #DRAWS PERSON MINI DATA BOX
                    pdbx,pdby = 0,0 #person data box x and y
                    if self.selectx < 20 and self.selecty <= 12:
                        pdby = 630
                    draw.rect(screen,BLUE,(pdbx,pdby,300,90)) #background box
                    screen.blit(sans.render(stripNums(p.name),True,WHITE),(pdbx+15,pdby+3)) #person's name
                    screen.blit(smallsans.render("HP: "+str(p.hp)+"/"+str(p.maxhp),True,WHITE),(pdbx+15,pdby+33)) #health
                    draw.line(screen,(80,60,30),(pdbx+90,pdby+48),(pdbx+270,pdby+48),30) #health bar
                    draw.line(screen,YELLOW,(pdbx+90,pdby+48),(pdbx+90+(p.hp/p.maxhp)*180,pdby+48),30)
                    break
        #---------------DIFFERENT MODE DISPLAYS------------------#
        #MOVE MODE DISPLAY
        if self.mode == "move":
            #fills moveable and attackable squares
            fillSquares(screen,set([(x,y) for x,y,m in self.moveableSquares]+[(self.selected.x,self.selected.y)]),transBlue)
            if self.attackableSquares and self.selected.equip != None:
                fillSquares(screen,self.attackableSquares,transRed)
        #DRAWS PEOPLE
        self.drawPeople()
        #MAIN MENU MODE DISPLAY
        if self.mode == "mainmenu":
            #if it is menu mode we draw the menu
            menux,menuy = 18,4
            drawMenu(self.menu,menux,menuy,120,480,self.menuselect) #draws the main menu
        #OPTION MENU MODE DISPLAY
        if self.mode == "optionmenu":
            menux,menuy = 36,2
            if self.selected.x >= 20:
                menux = 0
            drawMenu(self.menu,menux,menuy,120,len(self.menu)*30,self.menuselect)
        #ATTACK MODE DISPLAY
        if self.mode == "itemattack":
            #displays item selection menu for attack
            drawItemMenu(self.selected,self.selected.x+1,self.selected.y,self.menuselect)
        if self.mode == "attack":
            #highlights all attackable squares
            fillSquares(screen,getAttackableSquares(self.selected.equip.rnge,self.selected.equip.maxrnge,self.selected.x,self.selected.y),transRed)
            #displays battle stats (such as hit chance, damage, crit)
            x,y = 25,3
            if self.selected.x > 20:
                x = 0 #x goes to left if selected person is on the right
            #battle stats from ally's POV
            #battleStatsMenu has name, HP, hit chance, damage, crit chance, weapon of use and whether the weapon has an advantage or not
            enemy = self.attackableEnemies[self.selectedEnemy] #the selected enemy
            #gets battle stats for the selected ally
            battleStatsMenu = getBattleStats(self.selected,enemy,chapterMaps[chapter])
            drawMenu(battleStatsMenu,x,y,210,210,-20) #draws battle stats menu for ally

            #battle stats from enemy's POV
            battleStatsMenu = getBattleStats(enemy,self.selected,chapterMaps[chapter])
            drawMenu(battleStatsMenu,x+7,y,210,210,-20,RED) #draws battle stats menu for enemy
        #ITEM MODE DISPLAY
        if self.mode == "item":
            screen.blit(transBlack,(0,0))
            drawItemMenu(self.selected,14,8,self.menuselect)
            if self.selectedItem != None:
                #if we have a selected Item we draw the submenu
                if type(self.selectedItem) == Weapon:
                    if self.selected.canEquip(self.selectedItem):
                        col = GREEN #color to write "Equip" with
                        #green means can, grey means can't
                    else:
                        col = GREY
                    #options user can choose for the selected item
                    options = ["Equip","Discard"] #weapons can be equipped or discarded
                if type(self.selectedItem) == Consumable:
                    col = GREEN
                    options = ["Use","Discard"] #consumables can be used or discarded
                draw.rect(screen,BLUE,(22*30,8*30,120,len(options)*30)) #draws submenu backdrop for item
                screen.blit(sans.render(options[0],True,col),(22*30,8*30)) #draws first option
                screen.blit(sans.render(options[1],True,WHITE),(22*30,9*30)) #draws discard option
                draw.rect(screen,WHITE,(22*30,(8+self.optselected)*30,120,30),1) #selected option
        #TRADE MODE DISPLAY
        if self.mode == "trade":
            if self.selected2 == None:
                #if we have no 2nd selected ally, we draw the selector around the 2nd selected ally
                highlightedAlly = self.targetableAllies[self.selectedAlly] #highlighted ally
                draw.rect(screen,WHITE,(highlightedAlly.x*30,highlightedAlly.y*30,30,30),1) #draws selector around highlighted ally
            else:
                screen.fill(GREEN) #fills the screen with green
                #draws item menu for both allies
                #first we set which item selected out of the two menus
                #this is based on which ally the selector is on
                #which is determined by the first element of menuselect
                menuselect1 = -20 if self.menuselect[0] else self.menuselect[1]
                menuselect2 = -20 if not self.menuselect[0] else self.menuselect[1]
                                                                                
                drawItemMenu(self.selected,8,9,menuselect1)
                drawItemMenu(self.selected2,24,9,menuselect2)
                if self.selectedItem != None:
                    #if the selected Item isn't none, we draw the cursor
                    draw.rect(screen,WHITE,((8+self.selectedItem[0]*16)*30,(9+self.selectedItem[1])*30,240,30),1)
        #---------------INFO DISPLAY BOXES----------------------#
        #TERRAIN DATA BOX
        if self.mode == "freemove":
            tbx,tby = 1020,630 #terrain box x and y
            stage = chapterMaps[chapter]
            if self.selectx >= 20:
                tbx = 0
            draw.rect(screen,BLUE,(tbx,tby,180,90))
            screen.blit(sans.render(stage[self.selecty][self.selectx].name,True,WHITE),(tbx+15,tby+3))
            draw.rect(screen,(255,230,200),(tbx,tby+30,180,60))
            screen.blit(sans.render("DEFENSE: "+str(stage[self.selecty][self.selectx].adef),True,BLACK),(tbx+15,tby+33))
            screen.blit(sans.render("AVOID: "+str(stage[self.selecty][self.selectx].avo),True,BLACK),(tbx+15,tby+63))
        #GOAL DISPLAY BOX
            goalx,goaly = 1020,0
            if self.selecty <= 12 and self.selectx >= 20:
                goaly = 630
            draw.rect(screen,(50,50,180),(goalx,goaly,180,90))
            screen.blit(smallsans.render(self.goal,True,WHITE),(goalx+15,goaly+35))
        #---------------SELECTED SQUARE BOX----------------#
        if self.mode in ["freemove","move","attack"]:
            draw.rect(screen,WHITE,(self.selectx*30,self.selecty*30,30,30),1) #draws select box
        #----------------ENDING THE LOOP-------------------#
        display.flip()
        self.framecounter += 1 #increases frame counter
        self.fpsTracker.tick(60) #limits FPS to 60
