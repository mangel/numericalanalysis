class Species:
    def __init__(self, name):
        self.name = name
        self.isProductOnly = True
        self.affectReactions = set()

    def getName(self):
        return self.name

    def isProductOnly(self):
        return self.isProductOnly

    def addAffectReaction(self, reaction_index):
        self.affectReactions.add(reaction_index)

    def getAffectReaction(self):
        return self.affectReactions

    def toString(self):
        return self.name

    def equals(self, other):
        if type(self) == type(other):
            return other.name == self.name
        return false
        
    def hashcode(self):
        return hash(self.name)
