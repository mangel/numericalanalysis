class TimedRSSAGeneralNode:
    def __init__(self, reactionIndex, minRate, maxRate, minCombination, maxCombination):
        self.reactionIndex = reactionIndex
        self.minRate = minRate
        self.maxRate = maxRate
        self.minCombination = minCombination
        self.maxCombination = maxCombination

        self.minPropensity = minRate*minCombination
        self.maxPropensity = maxRate*maxCombination

    def getReactionIndex(self):
        return self.reactionIndex

    def setReactionIndex(self, reactionIndex):
        self.reactionIndex = reactionIndex

    def getMinPropensity(self):
        return self.minPropensity

    def getMaxPropensity(self):
        return self.maxPropensity

    def setRate(self, minRate, maxRate):
        self.minRate = minRate
        self.maxRate = maxRate

        self.minPropensity = minRate*self.minCombination
        self.maxPropensity = maxRate*self.maxCombination

    def setCombination(self, minCombination, maxCombination):
        self.minCombination = minCombination
        self.maxCombination = maxCombination

        self.minPropensity = self.minRate*minCombination
        self.maxPropensity = self.maxRate*maxCombination
