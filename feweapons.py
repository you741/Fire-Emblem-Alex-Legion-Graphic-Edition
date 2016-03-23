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
    def __init__(self,name,mt,wt,maxdur,acc,typ,mast,crit=0,rnge=1,dur=None,mag=False,sup_eff=[],maxrnge=1,wexp=3,desc="",prf=""):
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
    def getInstance(self):
        "gets instance of weapon"
        return Weapon(self.name,self.mt,self.wt,self.dur,self.acc,self.typ,self.mast,self.crit,self.rnge,self.dur,self.mag,self.sup_eff,self.maxrnge,self.wexp,self.desc,self.prf)
