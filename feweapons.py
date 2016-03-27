#FE Weapons keeps weapons and item classes
class Item():
    def __init__(self,name,maxdur,desc="",dur=None):
        self.maxdur = maxdur
        self.dur = dur if dur != None else maxdur
        self.name = name
        self.desc = desc
        self.intact=True
    def getInstance(self):
        "returns an intance of the item"
        return Item(self.name,self.maxdur,self.desc,self.dur)
class Weapon(Item):
    def __init__(self,name,mt,wt,maxdur,acc,typ,mast,crit=0,rnge=1,dur=None,mag=False,sup_eff=[],maxrnge=1,wexp=3,desc="",prf="",anims=None):
        super(Weapon,self).__init__(name,maxdur,desc,dur)
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
        self.anims = anims
    def getInstance(self):
        "gets instance of weapon"
        return Weapon(self.name,self.mt,self.wt,self.maxdur,self.acc,self.typ,self.mast,self.crit,self.rnge,self.dur,self.mag,self.sup_eff,self.maxrnge,self.wexp,self.desc,self.prf,self.anims)
class Consumable(Item):
    def __init__(self,name,hpGain,maxdur,desc="",dur=None):
        super(Consumable,self).__init__(name,maxdur,desc,dur)
        self.hpGain = hpGain
        
    def getInstance(self):
        "gets instance of Consumable"
        return Consumable(self.name,self.hpGain,self.maxdur,self.desc,self.dur)

    def use(self,person):
        "uses consumable on person"
        #returns False if item breaks
        person.hp += self.hpGain
        person.hp = min(person.maxhp,person.hp)
        self.dur -= 1
        if self.dur <= 0:
            return False
        return True
