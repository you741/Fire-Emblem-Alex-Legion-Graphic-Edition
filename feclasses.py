#FE Classes keeps all the classes for classes in the game
#*by classes I mean like "Knight" and "Mage" and etc.
from pygame import *
from feweapons import *
from random import *
from copy import deepcopy

weaponTriangle = {"Sword":"Axe",
                  "Axe":"Lance",
                  "Lance":"Sword",
                  "Anima":"Light",
                  "Light":"Dark",
                  "Dark":"Anima"} #weapon triangle of weapon types
#in the format advantageous:disadvantageous
class Person():
    "person class - root of all classes"
    def __init__(self,name,x,y,stats,growths,items,mast,anims,face,gift=0,exp=0):
        "initializes person"
        #takes in stats and growth - dictionaries
        self.name = name
        self.x,self.y = x,y
        self.stats = stats #stats
        self.growths = growths #growth percentage
        self.items = items #items
        self.mast = mast #mastery of weapons
        self.anims = anims #animations
        self.face = face #face
        #the way animations are stored is through a dictionary
        #each key points to a list of frames
        #some items will be a tuple that represents
        #(listOfFrames,frameWherePersonHitTarget)
        self.equip = None
        for w in [i for i in items if type(i) == Weapon]:
            if self.equipWeapon(w):
                break #loops until we can equip a weapon, then we break
        for i,key in enumerate(stats):
            exec("self."+key+"=stats[key]") #sets self.stat to be the stat
        self.flying = False
        self.mounted = False
        self.magical = False
        self.mountainous = False
        self.waterproof = False
        self.gift = gift #gift for killing unit; only applies to enemies
        self.exp = exp
        self.caps = {"maxhp":60,
                     "stren":20,
                     "skl":20,
                     "spd":20,
                     "lck":20,
                     "defen":20,
                     "res":20} #caps for stats
    def getAdv(self,enemy):
        "returns whether weapon is advantageous or disadvantageous"
        #0 is disadvantageous, 1 is advantageous, -1 is neutral
        if self.equip == None or enemy.equip == None:
            return -1 #no advantage for armless units
        if weaponTriangle[self.equip.typ] == enemy.equip.typ:
            return 1 #we are advantageous
        if weaponTriangle[enemy.equip.typ] == self.equip.typ:
            return 0 #we are disadvantageous
        return -1 #no advantage or disadvantage if no cases were passed
    def getDamage(self,enemy,stage):
        "returns damage dealt to enemy"
        #does not account for critical hit
        if self.equip == None:
            return 0 #cannot attack if unit has no weapon
        eterr = enemy.getTerrain(stage) #enemy's terrain
        adef = eterr.adef #additional defense
        edefen = enemy.defen if not self.equip.mag else enemy.res
        dam = self.stren - edefen - adef + self.equip.mt
        if self.getAdv(enemy) != -1:
            #if there is an advantage or a disadvantage we handle extra damage
            if self.getAdv(enemy):
                dam += 1 #we have advantage so damage goes up by 1
            else:
                dam -= 1 #we have a disadvantage so damage goes down by 1
        return max(0,dam) #returns dam limited to 0 (no negative damage)
    def getCritical(self,enemy):
        "returns critical chance against enemy in percent"
        if self.equip == None:
            return 0
        return min(100,max(0,self.skl-enemy.lck+self.equip.crit))
    def getHit(self,enemy,stage):
        "returns hit chance on enemy in percent"
        if self.equip == None:
            return 0
        #enemy's avoid lowers hit chance, ally's skill, half of luck and weapon accuracy increases
        hit = self.skl*2-enemy.getAvo(stage)+self.lck//2+self.equip.acc #hit chance
        if self.getAdv(enemy) != -1:
            #if there is an advantage or a disadvantage we handle extra hit chance
            if self.getAdv(enemy):
                hit += 20 #advantage gives 20% more hit chance
            else:
                hit -= 20 #disadvantage makes us lose 20% hit chance
        return min(100,max(0,hit)) #limits hit chance between 0 and 100
    def getAtkSpd(self):
        "returns attack speed"
        if self.equip == None:
            return self.spd #If there is no equipped weapon the attackspeed is no different
        #attack speed is determined by speed subtracted the difference of weight and consitution
        #it only goes down if the equipped weapon is heavier
        return max(0,self.spd - max(0,self.equip.wt - self.con))
    def getAvo(self,stage):
        "returns avoid of Person"
        terr = self.getTerrain(stage) #terrain we're standing on
        avo = self.getAtkSpd()*2 + self.lck #avoid is double attack speed + luck
        if terr != None:
            avo += terr.avo #increases avoid by terrain advantage
        return avo
    def getTerrain(self,stage):
        "returns type of terrain unit is standing on"
        return stage[self.y][self.x]
    def canPass(self,terrain):
        "returns whether person can pass terrain"
        if terrain.name.lower() == "wall":
            return False #nothing can pass walls
        if self.flying:
            return True #there ain't nothing flying dudes can't pass
        if terrain.name.lower() == "peak":
            #only mountainous dudes can pass this
            return True if self.mountainous else False
        if terrain.name.lower() == "water":
            #only waterproof dudes can pass this
            return True if self.waterproof else False
        return True #it's always true otherwise
    def addItem(self,item):
        "adds an item to person"
        if len(self.items) > 5:
            return False
        else:
            self.items.append(item)
            if self.equip == None and type(item) == Weapon:
                self.equipWeapon(item)
    def equipWeapon(self,weapon):
        "equips a weapon to the Person"
        #has to check if the person can equip or not
        if self.canEquip(weapon):
            #if we can equip, we equip
            self.equip = weapon
            wepindx = self.items.index(weapon)
            self.items[0],self.items[wepindx] = weapon,self.items[0] #makes equipped weapon first
            return True
        return False
    def canEquip(self,weapon):
        "returns if person can equip weapon"
        if weapon not in self.items or type(weapon) != Weapon:
            return False #if we do not have the item we can't equip; if the weapon isn't a weapon we cannot equip either
        if weapon.prf.lower() == self.name.lower():
            return True #if the weapon has a preference to self, we can equip
        if weapon.typ not in self.mast:
            return False #if we have no mastery we can't equip
        if self.mast[weapon.typ] >= weapon.mast:
            return True #if we have enough mastery we can equip
        return False #if we do not have enough mastery we cannot equip
    def removeItem(self,item):
        "removes an item from the person's item list"
        if item not in self.items:
            return False #we cannot remove an item we don't have
        self.items.remove(item) #remove item
        if item == self.equip:
            #if we removed our equipped weapon
            #we equip a new one
            self.equip = None
            for w in [i for i in self.items if type(i) == Weapon]:
                #tries to equip weapons
                if self.equipWeapon(w):
                    break
    def gainExp(self,exp):
        "gains exp, returns whether should level up or not"
        self.exp += exp
        if self.exp >= 100:
            return True #returns True if we should level up
        else:
            return False
    def levelUp(self):
        "levels up"
        if self.exp < 100:
            #if we are less than 100 exp we cannot level up
            return False
        self.lv += 1
        for i,k in enumerate(self.growths):
            if randint(0,99) < self.growths[k]:
                #increases stats based on luck
                if eval("self."+k) >= self.caps[k]:
                    continue #if we are at maximum, we don't increase this stat
                exec("self."+k+"+=1")
                
        self.exp = self.exp%100 #exp goes down to exp modulus 100
        self.exp = 0 if self.lv == 20 else self.exp #if we are level 20 exp goes to 0
        return True
    def getMinRange(self):
        "returns minimum range of weapons, returns False if no weapons"
        if len([i for i in self.items if type(i) == Weapon and self.canEquip(i)]) > 0:
            return min([i.rnge for i in self.items if type(i) == Weapon and self.canEquip(i)])
        return False
    def getMaxRange(self):
        "returns maximum range of weapons, returns False if no weapons"
        if len([i for i in self.items if type(i) == Weapon and self.canEquip(i)]) > 0:
            return max([i.maxrnge for i in self.items if type(i) == Weapon and self.canEquip(i)])
        return False
    def getInternalLevel(self):
        "returns internal level of person, not displayed level"
        internalLV = self.lv
        if not issubclass(type(self),Person):
            #if the unit is a promoted unit, the internal LV is higher
            internalLV += 20
        return internalLV
    def getInstance(self):
        "gets instance of person"
        return eval(self.__class__.__name__+"(self.name,self.x,self.y,deepcopy(self.stats),self.growths,[i.getInstance() for i in self.items],deepcopy(self.mast),self.anims,self.face,self.gift,self.exp)")
class Mage(Person):
    "mage class"
    def __init__(self,name,x,y,stats,growths,items,mast,anims,face,gift=0,exp=0):
        super(Mage,self).__init__(name,x,y,stats,growths,items,mast,anims,face,gift,exp)
        self.magical = True
class Knight(Person):
    "knight class"
    pass
class Myrmidon(Person):
    "myrmidon class"
    pass
class Lord(Person):
    "lord class"
    pass
class Brigand(Person):
    "brigand class"
    def __init__(self,name,x,y,stats,growths,items,mast,anims,face,gift=0,exp=0):
        super(Brigand,self).__init__(name,x,y,stats,growths,items,mast,anims,face,gift,exp)
        self.mountainous = True
class Cavalier(Person):
    "cavalier class"
    def __init__(self,name,x,y,stats,growths,items,mast,anims,face,gift=0,exp=0):
        super(Cavalier,self).__init__(name,x,y,stats,growths,items,mast,anims,face,gift,exp)
        self.mounted = True    

class Fighter(Person):
    "fighter class"
    def __init__(self,name,x,y,stats,growths,items,mast,anims,face,gift=0,exp=0):
        super(Fighter,self).__init__(name,x,y,stats,growths,items,mast,anims,face,gift,exp)
