import sys
import re
import copy

def main():
    #sys.setrecursionlimit(50000)
    f = open(sys.argv[2], 'r')
    day = f.readline()[:-1]
    #print ("day: " + day)
    player = f.readline()[0:2]

    rplRead = f.readline()[:-1]
    rplRead = re.split(",", rplRead)
    rpl = []
    regionList = {}
    for i in range (len(rplRead) / 2):
        rpl.append(float(rplRead[i * 2 + 1][:-1]))
        regionList[rplRead[i * 2][1:]] = i
    #print "rpl:", rpl

    if day == "Yesterday":
        totalProfit = 0
        for item in rpl:
            totalProfit += item
        avgProfit = totalProfit / len(rpl)
        for i in range(len(rpl)):
            rpl[i] = (avgProfit + rpl[i]) / 2

    amr = []
    amr.append(f.readline())
    amr[0] = amr[0][:-2]
    amr[0] = amr[0][1:]

    amr[0] = re.split(",", amr[0])
    for i in range(1, len(amr[0])):
        amr.append(f.readline())
        amr[i] = amr[i][:-2]
        amr[i] = amr[i][1:]
        amr[i] = re.split(",", amr[i])

    regionPicked = f.readline()[:-1]
    if regionPicked == "*":
        regionPicked = []
    else:
        regionPicked = re.split(",", regionPicked)

        for i in range (len(regionPicked)):
            if regionPicked[i] != "PASS":
                regionPicked[i] = regionList[regionPicked[i]]

    #print "regionPicked:", regionPicked
    maxDepth = int(f.readline())

    f.close()

    R1picked = []
    R2picked = []

    whoseTurn = player
    if len(regionPicked) % 2 == 0:
        whoseTurn = player
    else:
        if player == "R1":
            whoseTurn = "R2"
        else:
            whoseTurn = "R1"
    if len(regionPicked) > 0:
        for i in range (len(regionPicked)):
            if whoseTurn == "R1":
                if regionPicked[i] != "PASS":
                    R1picked.append(regionPicked[i])
                whoseTurn = "R2"
            else:
                if regionPicked[i] != "PASS":
                    R2picked.append(regionPicked[i])
                whoseTurn = "R1"

    R1profit = 0
    R2profit = 0

    for i in R1picked:
        R1profit += rpl[i]
    for i in R2picked:
        R2profit += rpl[i]


    leftDepth = maxDepth - len(R1picked) - len(R2picked)
    finalChoose = "a"

    alpha = -sys.maxint - 1
    beta = sys.maxint

    result = maxProfit(player, R1picked, R2picked, R1profit, R2profit, leftDepth, amr, rpl, player, alpha, beta)

    finalProfit = ""
    for i in range(len(result.printProfit)):
        result.printProfit[i] = int(round(result.printProfit[i]))
        if i == 0:
            finalProfit += str(result.printProfit[i])
        else:
            finalProfit += "," + str(result.printProfit[i])

    for k,v in regionList.items():
        if int(v) == result.regionChose:
            finalChoose = k

    fOut = open("output.txt", "w+")
    fOut.write("%s\n" % finalChoose)
    fOut.write(finalProfit)
    fOut.close()


def maxProfit(player, R1picked, R2picked, R1profit, R2profit, leftDepth, amr, rpl, startPlayer, alpha, beta):

    if leftDepth < 0 or len(R1picked) + len(R2picked) == len(rpl):

        printProfit = []
        if startPlayer == "R1":
            printProfit.append(R1profit)
            return pickState(regionChose = -1, R1profit = R1profit, R2profit = R2profit, printProfit = copy.deepcopy(printProfit))
        if startPlayer == "R2":
            printProfit.append(R2profit)
            return pickState(regionChose = -1, R1profit = R1profit, R2profit = R2profit, printProfit = copy.deepcopy(printProfit))

    #print "player:", player
    pickStates = []
    indexOfMaxProfit = 0
    isPass = 0
    mustBreak = False

    if player == "R1":
        #print "REACH_HERE!"
        if len(R1picked) == 0:
            for j in range(len(amr[0])):
                if j not in R2picked:
                    newR1picked = copy.deepcopy(R1picked)
                    newR1picked.append(j)
                    newR1profit = R1profit + rpl[j]

                    aPickState = maxProfit("R2", newR1picked, R2picked, newR1profit, R2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                    if startPlayer == "R1":
                        if aPickState.R1profit > alpha:
                            alpha = aPickState.R1profit
                            aPickState.alpha = alpha
                    if startPlayer == "R2":
                        if aPickState.R2profit < beta:
                            beta = aPickState.R2profit
                            aPickState.beta = beta

                    aPickState.regionChose = j
                    pickStates.append(aPickState)

        if len(R1picked) != 0:
            thisPicked = []
            for i in R1picked:
                if mustBreak == True:
                    break
                for j in range(len(amr[i])):
                    #print "j:", j
                    if (amr[i][j] == "1") and (j not in R1picked) and (j not in R2picked) and (j not in thisPicked):
                        isPass = 1
                        thisPicked.append(j)
                        newR1picked = copy.deepcopy(R1picked)
                        newR1picked.append(j)
                        newR1profit = R1profit + rpl[j]
                        aPickState = maxProfit("R2", newR1picked, R2picked, newR1profit, R2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                        if startPlayer == "R1":
                            if aPickState.R1profit > alpha:
                                alpha = aPickState.R1profit
                                aPickState.alpha = alpha
                        if startPlayer == "R2":
                            if aPickState.R2profit < beta:
                                beta = aPickState.R2profit
                                aPickState.beta = beta

                        aPickState.regionChose = j
                        pickStates.append(aPickState)

                        if alpha >= beta:
                            mustBreak = True
                            break

            if isPass == 0:
                # print "R1picked.len:", len(R1picked)
                # print "R2picked.len:", len(R2picked)
                # print "rpl.len:", len(rpl)
                # print "thisPicked:", thisPicked
                aPickState = maxProfit("R2", R1picked, R2picked, R1profit, R2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                if startPlayer == "R1":
                    if aPickState.R1profit > alpha:
                        alpha = aPickState.R1profit
                        aPickState.alpha = alpha
                if startPlayer == "R2":
                    if aPickState.R2profit < beta:
                        beta = aPickState.R2profit
                        aPickState.beta = beta

                pickStates.append(aPickState)

        for i in range(len(pickStates)):
            #print "pickStates[0]:", pickStates[0].R1profit
            if pickStates[i].R1profit > pickStates[indexOfMaxProfit].R1profit:
                indexOfMaxProfit = i

        #print "len(pickStates):", len(pickStates)

        if len(pickStates) > 1:
            for i in range(1, len(pickStates)):
                for j in pickStates[i].printProfit:
                    pickStates[0].printProfit.append(j)
        pickStates[indexOfMaxProfit].printProfit = copy.deepcopy(pickStates[0].printProfit)

        return pickStates[indexOfMaxProfit]


    if player == "R2":
        #print "R2picked:", R2picked
        if len(R2picked) == 0:
            for j in range(len(amr[0])):
                if j not in R1picked:
                    newR2picked = copy.deepcopy(R2picked)
                    newR2picked.append(j)
                    newR2profit = R2profit + rpl[j]
                    aPickState = maxProfit("R1", R1picked, newR2picked, R1profit, newR2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                    if startPlayer == "R2":
                        if aPickState.R2profit > alpha:
                            alpha = aPickState.R2profit
                            aPickState.alpha = alpha
                    if startPlayer == "R1":
                        if aPickState.R1profit < beta:
                            beta = aPickState.R1profit
                            aPickState.beta = beta

                    aPickState.regionChose = j
                    pickStates.append(aPickState)

        if len(R2picked) != 0:
            thisPicked = []
            for i in R2picked:
                if mustBreak == True:
                    break
                for j in range(len(amr[i])):
                    if amr[i][j] == "1" and (j not in R1picked) and (j not in R2picked) and (j not in thisPicked):
                        #print "REACH_HERE!"
                        isPass = 1
                        thisPicked.append(j)
                        newR2picked = copy.deepcopy(R2picked)
                        newR2picked.append(j)
                        newR2profit = R2profit + rpl[j]
                        aPickState = maxProfit("R1", R1picked, newR2picked, R1profit, newR2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                        if startPlayer == "R2":
                            if aPickState.R2profit > alpha:
                                alpha = aPickState.R2profit
                                aPickState.alpha = alpha
                        if startPlayer == "R1":
                            if aPickState.R1profit < beta:
                                beta = aPickState.R1profit
                                aPickState.beta = beta

                        aPickState.regionChose = j
                        pickStates.append(aPickState)
                        if alpha >= beta:
                            mustBreak = True
                            break

            if isPass == 0:
                aPickState = maxProfit("R1", R1picked, R2picked, R1profit, R2profit, leftDepth - 1, amr, rpl, startPlayer, alpha, beta)

                if startPlayer == "R2":
                    if aPickState.R2profit > alpha:
                        alpha = aPickState.R2profit
                        aPickState.alpha = alpha
                if startPlayer == "R1":
                    if aPickState.R1profit < beta:
                        beta = aPickState.R1profit
                        aPickState.beta = beta

                pickStates.append(aPickState)

        for i in range(len(pickStates)):
            #print "pickStates[0]:", pickStates[0].R1profit
            if pickStates[i].R2profit > pickStates[indexOfMaxProfit].R2profit:
                indexOfMaxProfit = i

        if len(pickStates) > 1:
            for i in range(1, len(pickStates)):
                for j in pickStates[i].printProfit:
                    pickStates[0].printProfit.append(j)
        pickStates[indexOfMaxProfit].printProfit = copy.deepcopy(pickStates[0].printProfit)

        return pickStates[indexOfMaxProfit]


class pickState:
    def __init__(self, regionChose = -1, R1profit = 0, R2profit = 0, printProfit = [], alpha = 0, beta = 0):
        self.regionChose = regionChose
        self.R1profit = R1profit
        self.R2profit = R2profit
        self.printProfit = copy.deepcopy(printProfit)
        self.alpha = alpha
        self.beta = beta


if __name__=="__main__":
    main()
