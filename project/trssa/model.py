class Species:
    def __init__(self, name):
        self.name = name
        self.isProductOnly = True
        self.affectReactions = set()

    def getName(self):
        return self.name

    def isProductOnly(self):
        return self.isProductOnly

    def setIsProductOnly(self, isProductOnly):
        self.isProductOnly = isProductOnly

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

class StateList:
    def __init__(self):
        self.speciesCollection = {}

    def getSpeciesList(self):
        speciesList = []
        for i in self.speciesCollection:
            speciesList.append(i)
        return speciesList

    def getSpecies(self, name):
        for i in self.speciesCollection:
            if i.name == name:
                return i

    def updateSpeciesPopulation(self, species, new_population):
        self.speciesCollection[species] = new_population

    def getPopulation(self, species):
        return self.speciesCollection[species]

class Reaction:
    def __init__(self, index, reactants, products, rate):
        self.reactionIndex = index
        self.reactants = reactants
        self.products = products
        self.rate = rate
        self.dependent = set()

    def getReactionIndex(self):
        return self.reactionIndex

    def getReactants(self):
        return self.reactants

    def getProducts(self):
        return self.products

    def getRate(self):
        return self.rate

    def reactantsContainSpecies(self, s):
        for i in self.reactants:
            if i.getSpecies().equals(s):
                return True
        return False

    def productsContainSpecies(self, s):
        for i in self.products:
            if i.getSpecies().equals(s):
                return True
        return False

    def affect(self, o):
        isAffect = False
        for r in self.reactants:
            if self.isCatalyst(r) == False and reactantsContainSpecies(r.getSpecies()):
                isAffect = True
                break

        for p in self.products:
            if self.isCatalyst(p) == False and reactantsContainSpecies(p.getSpecies()):
                isAffect = True
                break

        return isAffect

    def isCatalyst(self, t):
        result = False
        coffBackup = t.getCoff()
        t.setCoff(-coffBackup)
        if coffBackup < 0 and t in self.products:
            result = True
        elif coffBackup > 0 and t in self.reactants:
            result = True
        t.setCoff(coffBackup)
        return result

    def addDependentReaction(self, index):
        self.dependent.add(index)

    def getDependent(self):
        return self.dependent

    def toString(self):
        result = ""
        result += str(self.reactionIndex) + ":"

        if len(self.reactants) == 0:
            result += "_ "
        else:
            for t in self.reactants:
                result += t.toString() + " + "
            result = result[:len(result)-2]
        result += "->"
        if len(self.products) == 0:
            result += "_ "
        else:
            for t in self.products:
                result += t.toString() + " + "
            result = result[:len(result)-2]
        result += "\n with " + str(type(self.rate))

class ReactionList:
    def __init__(self):
        self.reactionCollection = {}

    def addReaction(self, r):
        self.reactionCollection[r.getReactionIndex()] = r

    def getLength(self):
        return len(self.reactionCollection)

    def getReaction(self, index):
        return self.reactionCollection[index]

    def getReactionList(self):
        list = []
        for i in self.reactionCollection.keys():
            list.append(self.reactionCollection[i])
        return list

    def toString(self):
        result = ""
        for i in self.reactionCollection.keys():
            result += "\n" + self.reactionCollection[i].toString()
        return result

    def toStringFull(self):
        result = ""
        for i in self.reactionCollection.keys():
            r = self.reactionCollection[i]
            result += "\n" + r.toString()
            dependent = r.getDependent()
            if not (len(dependent) == 0):
                result += "\n affected reaction: "
                for dependencyReaction in dependent:
                    result += str(dependencyReaction) + ", "
                result = result[:len(result)-2]
        return result

class Term:
    def __init__(self, species, stoichiometric):
        self.species = species
        self.stoichiometric = stoichiometric

    def setCoff(self, coff):
        self.stoichiometric = coff

    def getCoff(self):
        return self.stoichiometric

    def getSpecies(self):
        return self.species

    def setSpecies(self, species):
        self.species = species

    def toString(self):
        return "({})*{}".format(self.stoichiometric, self.species)

    def equals(self, o):
        if type(o) == type(self):
            if self.species.equals(o.species) and self.stoichiometric == o.species.stoichiometric:
                return true
        return false
