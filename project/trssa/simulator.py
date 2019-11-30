import random
from model import StateList
from utility import DataWriter, ComputingMachine
from datetime import datetime

class TimedRSSAGeneral:
    def __init__(self):
        #random generator
        self.rand = random
        #model info
        self.states = None
        self.reactions = None
        #simulation info
        self.currentTime = 0
        self.simulationTime = None
        # Log info
        self.logInterval = 0
        self.logPoint = 0
        #simulation firing
        self.firing = 0
        self.trial = 0
        self.update = 0
        #info for rejection-based rssa
        self.threshold = 25
        self.absoluteSize = 4
        self.relativeSize = 0.1

        self.upperStates = StateList()
        self.lowerStates = StateList()

        self.TRSSANodes = None

        self.totalMaxPropensity = 0

        self.mapReactionIndexToNode = {}

        self.nextTimeList = []

        dataWriter = None
        performanceWriter = None

    def buildSimulator(self, nextTimeList, logInterval, populationList, reactionList, rates, outputFilename):
        #info for simulation
        self.nextTimeList = nextTimeList
        #logging point
        self.logInterval = logInterval
        self.logPoint = logPoint
        #build states
        self.states = ComputingMachine.buildPopulationList(populationList)
        #build reactions
        self.reactions = ComputingMachine.buildReactionList(reactionList, rates, self.states)
        #build bipartie species-reaction dependency
        ComputingMachine.buildBipartieDependency(reactionList, rates, self.states)
        #writer
        self.dataWriter = DataWriter("(Data){}".format(outputFilename))
        self.performanceWriter = DataWriter("(Perf){}".format(outputFilename))
        #write data
        dataWriter.write("Time \t")
        for i in self.states.getSpeciesList():
            dataWriter.write(i.getName() + "\t")
        dataWriter.writeLine()

        dataWriter(str(self.currentTime) + "\t")
        for i in self.states.getSpeciesList():
            pop = self.states.getPopulation(i)
            dataWriter(str(pop) + "\t")
        dataWriter.writeLine()
        dataWriter.flush()

        #write performance
        self.performanceWriter.writeLine("Time\tTrial\tFiring\tUpdate\tRunTime")
        self.performanceWriter.flush()

    def runSimulator(self):
        print("---------------------- Timed RSSA ----------------------")
        self.simulationTime = self.nextTimeList[0]
        del(self.nextTimeList[0])
        #build the datastructure for the simulator
        self.buildTimedRSSANode(self.currentTime, self.simulationTime)

        #simulator variables
        randomValue = 0.0
        searchValue = 0.0
        acceptantProb = 0.0

        nodeIndex = -1
        trialPerStep = 1

        #simulation performance
        simPerformance = 0

        #start clock
        startSimTime = datetime.now()

        while True:
            #generate delta
            delta = ComputingMachine.computeTentativeTime(self.rand, self.totalMaxPropensity)
            #update Time
            self.currentTime += delta
            if self.currentTime >= self.logPoint:
                #end clock
                endSimTime = datetime.now()
                simPerformance += (endSimTime - startSimTime)

                self.dataWriter.write(str(self.logPoint) + "\t")
                for s in self.states.getSpeciesList():
                    pop = self.states.getPopulation(s)
                    self.dataWriter.write(str(pop) + "\t")
                self.dataWriter.writeLine()
                self.performanceWriter.writeLine("{}\t{}\t{}\t{}\t{}".format(str(self.logPoint), str(self.trial), str(self.firing), str(self.update), str(simPerformance/1000.0)))
                self.logPoint += self.logInterval

            if not (self.currentTime >= self.simulationTime):
                self.currentTime = self.simulationTime
                if len(arr) > 0:
                    self.simulationTime = self.nextTimeList[0]
                    del(self.nextTimeList[0])
                    self.updateRateTimedRSSANode(self.currentTime, self.simulationTime)
                    self.update += 1
                    continue
                else:
                    break
            #rejection-based selection
            randomValue = self.rand.random()
            searchValue = randomValue * self.totalMaxPropensity

            partialSumMaxPropensity = 0.0
            maxPropensity = 0.0

            nodeIndex = 0

            for i in range(0, len(self.TRSSANodes)):
                nodeIndex = i
                maxPropensity = self.TRSSANodes[nodeIndex].getMaxPropensity()
                partialSumMaxPropensity += maxPropensity
                if partialSumMaxPropensity >= searchValue:
                    break

            acceptantProb = self.rand.random()
            accept = True

            if acceptantProb <= self.TRSSANodes[nodeIndex].getMinPropensity() / maxPropensity:
                accept = true

            if not accept:
                r = self.reactions.getReation(self.TRSSANodes[nodeIndex].getReactionIndex())

                rate = r.getRate().evaluate(self.currentTime)
                combination = ComputingMachine.computeCombination(r, self.states)

                currentPropensity = rate * combination

                if acceptantProb <= (currentPropensity/maxPropensity):
                    accept = True

            if accept:
                #fire reaction
                fireReactionIndex = self.TRSSANodes[nodeIndex].getReactionIndex()
                #update population
                updateSpecies = ComputeMachine.executeReaction(fireReactionIndex, self.reactions, self.states, self.lowerStates, self.upperStates)

                if not (len(updateSpecies) == 0):
                    self.updateCombinationTimedRSSANode(updateSpecies)
                    self.update += 1
                #update firing
                self.firing += 1
                self.trial += trialPerStep
                trialPerStep = 1
            else:
                trialPerStep += 1

    def buildTimedRSSANode(self, currentTime, nextTime):
        return -1

    def updateRateTimedRSSANode(self, currentTime, nextTime):
        return -1

    def updateCombinationTimedRSSANode(self, updateSpecies):
        return -1
