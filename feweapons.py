#FE Weapons keeps weapons and item classes
class Item():
    def __init__(self,name,maxdur,cost,desc="",dur=None):
        self.maxdur = maxdur
        self.dur = dur if dur != None else maxdur
        self.name = name
        self.desc = desc
        self.cost = cost
        self.typ = ""
        self.intact=True
    def getCost(self):
        return int(self.dur/self.maxdur*self.cost)
    def getInstance(self):
        "returns an intance of the item"
        return Item(self.name,self.maxdur,self.cost,self.desc,self.dur)
class Weapon(Item):
    def __init__(self,name,mt,wt,maxdur,acc,typ,mast,cost,crit=0,rnge=1,dur=None,mag=False,sup_eff=[],maxrnge=1,wexp=3,desc="",prf=""):
        super(Weapon,self).__init__(name,maxdur,cost,desc,dur)
        self.mt = mt
        self.wt = wt
        self.wexp = wexp
        self.acc = acc
        self.crit = crit
        self.rnge = rnge
        self.mag = mag
        self.typ = typ
        self.mast = mast
        self.sup_eff = sup_eff
        self.maxrnge = maxrnge
        self.prf = prf
    def getInstance(self):
        "gets instance of weapon"
        return Weapon(self.name,self.mt,self.wt,self.maxdur,self.acc,self.typ,self.mast,self.cost,self.crit,self.rnge,self.dur,self.mag,self.sup_eff,self.maxrnge,self.wexp,self.desc,self.prf)
class Staff(Item):
    def __init__(self,name,maxdur,mast,cost,heal=0,desc="",dur=None,wexp=3):
        super(Staff,self).__init__(name,maxdur,cost,desc,dur)
        self.typ = "Staff"
        self.heal = heal
        self.wexp = wexp
        self.mast = mast
    def getInstance(self):
        "gets instance of staff"
        return Staff(self.name,self.maxdur,self.mast,self.cost,self.heal,self.desc,self.dur,self.wexp)
class Consumable(Item):
    def __init__(self,name,hpGain,maxdur,cost,desc="",dur=None):
        super(Consumable,self).__init__(name,maxdur,cost,desc,dur)
        self.hpGain = hpGain
        self.typ = "Consumable"
    def getInstance(self):
        "gets instance of Consumable"
        return Consumable(self.name,self.hpGain,self.maxdur,self.cost,self.desc,self.dur)
    def use(self,person):
        "uses consumable on person"
        #returns False if item breaks
        person.hp += self.hpGain
        person.hp = min(person.maxhp,person.hp)
        self.dur -= 1
        if self.dur <= 0:
            return False
        return True
class Booster(Item):
    "Boosts a stat"
    def __init__(self,name,maxdur,cost,stat,amnt,desc="",dur=None):
        super(Booster,self).__init__(name,maxdur,cost,desc,dur)
        self.stat = stat
        self.amnt = amnt
    def getInstance(self):
        return Booster(self.name,self.maxdur,self.cost,self.stat,self.amnt,self.desc,self.dur)
class Promotional(Item):
    "promotes a unit"
    def __init__(self,name,maxdur,cost,clss,desc="",dur=None):
        super(Promotional,self).__init__(name,maxdur,cost,desc,dur)
        self.clss = clss #classes that can be promoted
    def canUse(self,p):
        "can the person use it?"
        if p.__class__.__name__.lower() in self.clss and p.lv >= 10:
            return True
        return False
    def getInstance(self):
        return Promotional(self.name,self.maxdur,self.cost,self.clss,self.desc,self.dur)
