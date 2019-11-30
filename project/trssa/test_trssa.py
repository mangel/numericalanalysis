from pprint import pprint

from rate import SigmoidalRate
from simulator import TimedRSSAGeneral

nsim=1

max_time = 40
logInterval = 1
population_list = ["S1 = 0"]
reaction_list = ["_ -> S1"]

birthrate = 1

divisor = 20
exponentialCoefficient = 5

minor_increment = divisor/4
nextTime = 0
nextTimeList_Sigmoid = []

rates_sigmoid = [SigmoidalRate(birthrate, divisor, exponentialCoefficient)]

while (nextTime < max_time):
    nextTime = nextTime + minor_increment
    if nextTime > max_time:
        nextTime = max_time
        nextTimeList_Sigmoid.append(nextTime)
        break
    else:
        nextTimeList_Sigmoid.append(nextTime)

for i in range(1, nsim+1):
    print("Loop @{}".format(i))
    cloneNextTimeList = nextTimeList_Sigmoid.copy()
    output_resultfile = "TimedRSSA_Birth_One_Sigmoid_{}.txt".format(i)
    trssa = TimedRSSAGeneral()
    trssa.buildSimulator(cloneNextTimeList, logInterval, population_list, reaction_list, rates_sigmoid, output_resultfile)
    trssa.runSimulator()
