from model import Species, StateList

class ComputingMachine:
    @staticmethod
    def buildPopulationList(population_list):
        states = SateList()
        for i in population_list:
            tokens = i.split("=")
            s = Species(tokens[0])
            states.updateSpeciesPopulation(s, int(tokens[1]))
        return states

    @staticmethod
    def buildReactionList(reactionList, rates, states):
        reactions = ReactionList()
        r = None
        for i in range(0, len(reactionList)):
            r = buildReaction(reactionList[i].trim(), rates[i], i, states)
            reactions.addReaction(r)
        return reactions

    @staticmethod
    def buildReaction(reactionInfo, rate, reactionIndex, states):
        tokens = reactionInfo.split("->")
        reactants = buildPart(states, tokens[0], -1)
        products = buildPart(states, tokens[1], 1)
        for t in reactants:
            t.getSpecies().setIsProductOnly(False)
        return Reaction(reactionIndex, reactants, products, rate)

    @staticmethod
    def buildPart(states, part, mul):
        partTerm = []
        if part.trim() == "_":
            return partTerm
        tokens = part.split("+")

        for token in tokens:
            piece = token.trim()
            i = 0
            for c in piece:
                if c.isalpha():
                    break
                i = i + 1
            name = piece[i:]
            coff = mul
            if not (piece[0:i] == ""):
                coff = coff * int(piece[0:i])
            partTerm.append(Term(states.getSpecies(name), coff))
        return partTerm

    @staticmethod
    def buildBipartieDependency(reactions, states):
        for r in reactions:
            for t in r.getReactants():
                s = t.getSpecies()
                states.getSpecies(s.getName()).addAffectReaction(r.getReactionIndex())

    @staticmethod
    def computeTentativeTime():
        return -1

    @staticmethod
    def computeCombination(rate, states):
        return -1

    @staticmethod
    def executeReaction(fireReactionIndex, reactions, states, lowerStates, upperStates):
        return -1

class DataWriter:
    def __init__(self, trackingFile):
        self.trackingFile = trackingFile
    def write(self, string):
        print(trackingFile + ":" + string)
    def writeLine(self):
        print(trackingFile + ":" + "\n")
    def flush(self):
        print(trackingFile + ":" + "flush")
