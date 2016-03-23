#FE Classes keeps all the classes for classes in the game
#*by classes I mean like "Knight" and "Mage" and etc.
from pygame import *
from feweapons import *
from random import *
class Person():
    "person class - root of all classes"
    def __init__(self,name,x,y,stats,growth,items,mast,gift=0):
        "initializes person"
        #takes in stats and growth - dictionaries
        self.name = name
        self.x,self.y = x,y
        self.stats = stats #stats
        self.growth = growth #growth percentage
        self.items = items #items
        self.mast = mast #mastery of weapons
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
        self.exp = 0
    def getDamage(self,enemy,stage=None):
        "returns damage dealt to enemy"
        #does not account for critical hit
        if self.equip == None:
            return 0
        eterr = enemy.getTerrain(stage) #enemy's terrain
        if eterr == None:
            adef = 0
        else:
            adef = eterr.adef
        edefen = enemy.defen if not self.equip.mag else enemy.res
        return max(0,self.stren - edefen - adef + self.equip.mt)
    def getTerrain(self,stage):
        "returns type of terrain unit is standing on"
        if stage == None:
            return None
        return stage[self.y][self.x]
    def getCritical(self,enemy):
        "returns critical chance against enemy in percent"
        if self.equip == None:
            return 0
        return max(0,self.skl-enemy.lck+self.equip.crit)
    def getHit(self,enemy,stage=None):
        "returns hit chance on enemy in percent"
        if self.equip == None:
            return 0
        eterr = enemy.getTerrain(stage)
        if eterr == None:
            avo = 0
        else:
            avo = eterr.avo
        return max(0,self.skl*2-enemy.getAtkSpd()*2+self.lck//2-enemy.lck+self.equip.acc-avo)
    def getAtkSpd(self):
        "returns attack speed"
        if self.equip == None:
            return self.spd
        return self.spd - max(0,self.equip.wt - self.con)
    def canPass(self,terrain):
        "returns whether person can pass terrain"
        if terrain.name.lower() == "wall":
            return False #nothing can pass walls
        if self.flying:
            return True #there ain't nothing flying dudes can't pass
        if terrain.name.lower() == "mountain":
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
        if weapon not in self.items:
            return False
        if weapon.typ not in self.mast:
            return False
        if self.mast[weapon.typ] >= weapon.mast:
            return True
        return False
    def gainExp(self,exp):
        "gains exp, returns whether should level up or not"
        self.exp += exp
        if self.exp > 100:
            return True #returns True if we should level up
        else:
            return False
    def levelUp(self,screen):
        "levels up until exp < 100"
        for lvup in range(0,self.exp,100):
            if self.lv == 20:
                break
            self.lv += 1
            for i,k in self.growths:
                if randint(0,99) < self.growths[k]:
                    exec("self."+k+"+=1")
        self.exp = 0 if self.lv == 20 else self.exp
    def getInstance(self):
        "gets instance of person"
        return Person(self.name,self.x,self.y,self.stats,self.growth,
                      [i.getInstance() for i in self.items],
                      self.mast,self.gift)
    def getMinRange(self):
        "returns minimum range of weapons, returns False if no weapons"
        if len([i for i in self.items if type(i) == Weapon]) > 0:
            return min([i.rnge for i in self.items if type(i) == Weapon])
        return False
    def getMaxRange(self):
        "returns maximum range of weapons, returns False if no weapons"
        if len([i for i in self.items if type(i) == Weapon]) > 0:
            return max([i.maxrnge for i in self.items if type(i) == Weapon])
        return False
    def getInternalLevel(self):
        "returns internal level of person, not displayed level"
        internalLV = self.lv
        if not issubclass(type(self),Person):
            #if the unit is a promoted unit, the internal LV is higher
            internalLV += 20
        return internalLV
class Mage(Person):
    "mage class"
    def __init__(self,name,x,y,stats,growth,items,mast,gift=0):
        super(Mage,self).__init__(name,x,y,stats,growth,items,mast,gift)
        self.magical = True
class Knight(Person):
    "knight class"
    pass
class Myrmidon(Person):
    "myrmidon class"
    pass
