import random


def startSpikes(self):
    corners, cornerMult, vertices = 4, 2, 5
    for lane in range(self.laneNum):
        for spike in range(self.spikesNum):
            cornersList = [0 for i in range(vertices)]
            for i in range(vertices):
                cornersList[i] = [0, 0, ((self.spikesNum - spike) * self.spikeDepth)]
            self.spikes[lane][spike] = cornersList


def makeEmptyRowSpikes(self):
    vertices = 5
    for lane in range(self.laneNum):
        cornersList = [0 for i in range(vertices)]
        for i in range(vertices):
            cornersList[i] = [0, 0, (self.spikesNum * self.spikeDepth)]
        self.spikes[lane].insert(0, cornersList)
        self.spikes[lane].pop(-1)


def newSpikes(self):
    cornerMult, vertices = 2, 5
    if self.prevSpikesAreEmpty:  # checks if prev row is empty, can't make spikes if they're right before
        make = random.randint(1, self.spikesProb)
        if make == 1:  # 50% chance that it makes a new row of spikes
            for lane in range(self.laneNum):
                make = random.randint(1, 2)
                if make == 1:  # decides whether to even make a spike
                    corner = 0
                    Y = self.spikeY
                    cornersList = [0 for i in range(vertices)]
                    for xk in range(cornerMult):
                        for zk in range(cornerMult):
                            x = self.viewX - self.laneNum / 2 * self.laneWidth + (xk + lane) * self.spikeX
                            y = 0
                            z = (self.spikesNum - zk) * self.spikeDepth
                            cornersList[corner] = [int(x), int(y), int(z)]
                            corner += 1
                    x = self.viewX - (self.laneNum / 2 - 1 / 2) * self.laneWidth + lane * self.laneWidth
                    y = Y
                    z = ((self.spikesNum - 1 / 2) * self.spikeDepth)
                    cornersList[corner] = [int(x), int(y), int(z)]
                else:
                    cornersList = [0 for i in range(vertices)]
                    for i in range(vertices):
                        cornersList[i] = [0, 0, (self.spikesNum * self.spikeDepth)]
                self.spikes[lane].insert(0, cornersList)
                self.spikes[lane].pop(-1)
                self.prevSpikesAreEmpty = False
        else:
            makeEmptyRowSpikes(self)
            self.prevSpikesAreEmpty = True
    else:
        makeEmptyRowSpikes(self)
        self.prevSpikesAreEmpty = True


def generateSpikeSides(spike):
    sides = [[spike[0], spike[1], spike[3], spike[2]],
             [spike[0], spike[1], spike[4]], [spike[1], spike[3], spike[4]],
             [spike[3], spike[2], spike[4]], [spike[2], spike[0], spike[4]]]
    return sides


def moveSpikes(self):
    corners = 5
    for lane in range(self.laneNum):
        for spike in range(self.spikesNum):
            for corner in range(corners):
                self.spikes[lane][spike][corner][2] -= self.runningSpeed
