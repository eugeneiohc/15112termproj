# spikes file

import random
import math


def startSpikes(self):
    cornerMult, vertices = 2, 5
    for lane in range(self.laneNum):
        for spike in range(self.spikesNum):
            cornersList = [0 for i in range(vertices)]
            for i in range(vertices):
                x = self.viewX - self.laneNum / 2 * self.laneWidth + lane * self.laneWidth
                y = 0
                z = (self.spikesNum - spike) * self.spikeDepth
                cornersList[i] = [x, y, z]
            self.spikes[lane][spike] = cornersList


def extendSpikes(self):
    corners, newSize = 5, self.spikesNum + len(self.spikes[0]) + 2
    spikes = [[[0 for i in range(corners)] for j in range(newSize)] for k in range(self.laneNum)]
    for i in range(self.laneNum):
        for j in range(self.spikesNum + 2, newSize):
            for k in range(corners):
                spikes[i][j][k] = self.spikes[i][j - self.spikesNum - 2][k]
    self.spikes = spikes  # new list has been created


def makeEmptySpikesLeft(self, spike):
    corners = 5
    for lane in range(self.laneNum):
        for corner in range(corners):
            x = self.viewX - self.pathWidth // 2 - (self.spikesNum - spike) * self.spikeDepth
            y = 0
            z = self.lastZ + self.prismX + lane * self.laneWidth
            self.spikes[lane][spike][corner] = [x, y, z]


def startSpikesLeft(self):
    if len(self.spikes[0]) <= self.spikesNum + 6:
        extendSpikes(self)
    corners, cornerMult = 5, 2
    self.prevSpikesAreEmpty = True
    for spike in range(self.spikesNum):
        if self.prevSpikesAreEmpty:  # checks if prev row is empty, can't make spikes if they're right before
            make = random.randint(1, self.spikesProb)
            if make <= 10:  # chance that it makes a new row of spikes
                for lane in range(self.laneNum):
                    make = random.randint(1, self.spikesProb)
                    if make <= 10:  # decides whether to even make a spike
                        corner = 0
                        cornersList = [0 for i in range(corners)]
                        for xk in range(cornerMult):
                            for zk in range(cornerMult):
                                x = self.viewX - self.pathWidth // 2 - ((self.spikesNum - spike) - zk) * self.spikeDepth
                                y = 0
                                z = self.lastZ + self.prismX + (lane + xk) * self.laneWidth
                                cornersList[corner] = [int(x), int(y), int(z)]
                                corner += 1
                        # top tip
                        x = self.viewX - self.pathWidth // 2 - ((self.spikesNum - spike) - 1 / 2) * self.spikeDepth
                        y = self.spikeY
                        z = self.lastZ + self.prismX + (lane + 1 / 2) * self.laneWidth
                        cornersList[corner] = [int(x), int(y), int(z)]
                    else:
                        cornersList = [0 for i in range(corners)]
                        for i in range(corners):
                            x = self.viewX - self.pathWidth // 2 - (self.spikesNum - spike) * self.spikeDepth
                            y = 0
                            z = self.lastZ + self.prismX + lane * self.laneWidth
                            cornersList[i] = [x, y, z]
                    self.spikes[lane][spike] = cornersList
                    self.prevSpikesAreEmpty = False
            else:
                makeEmptySpikesLeft(self, spike)
                self.prevSpikesAreEmpty = True
        else:
            makeEmptySpikesLeft(self, spike)
            self.prevSpikesAreEmpty = True

    # the two "fake" spikes
    for lane in range(self.laneNum):
        for corner in range(corners):
            x = self.viewX - self.pathWidth // 2 - self.spikeDepth
            y = 0
            z = self.lastZ + self.prismX + lane * self.laneWidth
            self.spikes[lane][self.spikesNum][corner] = [int(x), int(y), int(z)]
            self.spikes[lane][self.spikesNum + 1][corner] = [int(x), int(y), int(z)]


def makeEmptySpikesRight(self, spike):
    corners = 5
    for lane in range(self.laneNum):
        for corner in range(corners):
            x = self.viewX + self.pathWidth // 2 + (self.spikesNum - spike) * self.spikeDepth
            y = 0
            z = self.lastZ + self.prismX + lane * self.laneWidth
            self.spikes[lane][spike][corner] = [x, y, z]


def startSpikesRight(self):
    if len(self.spikes[0]) <= self.spikesNum + 6:
        extendSpikes(self)
    corners, cornerMult = 5, 2
    self.prevSpikesAreEmpty = True
    for spike in range(self.spikesNum):
        if self.prevSpikesAreEmpty:  # checks if prev row is empty, can't make spikes if they're right before
            make = random.randint(1, self.spikesProb)
            if make <= 10:  # chance that it makes a new row of spikes
                for lane in range(self.laneNum):
                    make = random.randint(1, self.spikesProb)
                    if make <= 10:  # decides whether to even make a spike
                        corner = 0
                        cornersList = [0 for i in range(corners)]
                        for xk in range(cornerMult):
                            for zk in range(cornerMult):
                                x = self.viewX + self.pathWidth // 2 + ((self.spikesNum - spike) - zk) * self.spikeDepth
                                y = 0
                                z = self.lastZ + self.prismX + self.pathWidth - (lane + xk) * self.laneWidth
                                cornersList[corner] = [int(x), int(y), int(z)]
                                corner += 1
                        # top tip
                        x = self.viewX + self.pathWidth // 2 + ((self.spikesNum - spike) - 1 / 2) * self.spikeDepth
                        y = self.spikeY
                        z = self.lastZ + self.prismX + self.pathWidth - (lane + 1 / 2) * self.laneWidth
                        cornersList[corner] = [int(x), int(y), int(z)]
                    else:
                        cornersList = [0 for i in range(corners)]
                        for i in range(corners):
                            x = self.viewX + self.pathWidth // 2 + (self.spikesNum - spike) * self.spikeDepth
                            y = 0
                            z = self.lastZ + self.prismX + self.pathWidth - lane * self.laneWidth
                            cornersList[i] = [x, y, z]
                    self.spikes[lane][spike] = cornersList
                    self.prevSpikesAreEmpty = False
            else:
                makeEmptySpikesRight(self, spike)
                self.prevSpikesAreEmpty = True
        else:
            makeEmptySpikesRight(self, spike)
            self.prevSpikesAreEmpty = True

    # the two "fake" spikes
    for lane in range(self.laneNum):
        for corner in range(corners):
            x = self.viewX + self.pathWidth // 2 + self.spikeDepth
            y = 0
            z = self.lastZ + self.prismX + lane * self.laneWidth
            self.spikes[lane][self.spikesNum][corner] = [int(x), int(y), int(z)]
            self.spikes[lane][self.spikesNum + 1][corner] = [int(x), int(y), int(z)]


def makeEmptyRowSpikes(self):
    vertices = 5
    for lane in range(self.laneNum):
        cornersList = [0 for i in range(vertices)]
        for i in range(vertices):
            cornersList[i] = [0, 0, (self.spikesNum * self.spikeDepth)]
        self.spikes[lane].insert(0, cornersList)
        self.spikes[lane].pop(-1)


def newSpike(self):
    cornerMult, vertices = 2, 5
    if self.prevSpikesAreEmpty:  # checks if prev row is empty, can't make spikes if they're right before
        make = random.randint(1, self.spikesProb)
        if make <= 10:  # 50% chance that it makes a new row of spikes
            for lane in range(self.laneNum):
                make = random.randint(1, self.spikesProb)
                if make <= 10:  # decides whether to even make a spike
                    corner = 0
                    cornersList = [0 for i in range(vertices)]
                    for xk in range(cornerMult):
                        for zk in range(cornerMult):
                            x = self.viewX - self.pathWidth // 2 + (xk + lane) * self.spikeX
                            y = 0
                            z = self.lastZ - zk * self.spikeDepth
                            cornersList[corner] = [int(x), int(y), int(z)]
                            corner += 1
                    # top tip
                    x = self.viewX - self.pathWidth // 2 + self.laneWidth // 2 + lane * self.laneWidth
                    y = self.spikeY
                    z = self.lastZ - self.spikeDepth // 2
                    cornersList[corner] = [int(x), int(y), int(z)]
                else:
                    cornersList = [0 for i in range(vertices)]
                    for i in range(vertices):
                        x = self.viewX - self.pathWidth // 2
                        y = 0
                        z = self.lastZ
                        cornersList[i] = [x, y, z]
                self.spikes[lane].insert(0, cornersList)
                self.spikes[lane].pop(-1)
                self.prevSpikesAreEmpty = False
        else:
            makeEmptyRowSpikes(self)
            self.prevSpikesAreEmpty = True
    else:
        makeEmptyRowSpikes(self)
        self.prevSpikesAreEmpty = True


def removeLastSpike(self):
    for lane in range(self.laneNum):
        self.spikes[lane].pop(-1)


def generateSpikeSides(spike):
    sides = [[spike[0], spike[1], spike[3], spike[2]],
             [spike[2], spike[0], spike[4]], [spike[0], spike[1], spike[4]],
             [spike[1], spike[3], spike[4]], [spike[3], spike[2], spike[4]],]
    return sides


def moveSpikes(self):
    corners = 5
    for lane in range(self.laneNum):
        for spike in range(len(self.spikes[0])):
            for corner in range(corners):
                self.spikes[lane][spike][corner][2] -= self.runningSpeed


def setSpikesAngles(self):
    corners, data = 5, 2
    self.spikesAngles = [[[[0 for a in range(data)] for b in range(corners)]
                          for c in range(len(self.spikes[0]))] for d in range(self.laneNum)]
    for lane in range(self.laneNum):
        for spike in range(len(self.spikes[0])):
            for corner in range(corners):
                diffX = self.spikes[lane][spike][corner][0] - self.turningX
                diffZ = self.spikes[lane][spike][corner][2] - self.turningZ
                radius = math.sqrt(diffX ** 2 + diffZ ** 2)
                if diffX == 0 and diffZ > 0:
                    angle = math.pi / 2
                elif diffX == 0 and diffZ < 0:
                    angle = math.pi * 3 / 2
                else:
                    angle = math.atan(diffZ / diffX)
                if diffX < 0:
                    angle += math.pi
                elif diffZ < 0:
                    angle += math.pi * 2
                self.spikesAngles[lane][spike][corner][0] = angle
                self.spikesAngles[lane][spike][corner][1] = radius


def adjustAngles(self, angle, lane, spike, corner):
    if angle < 0:
        self.spikesAngles[lane][spike][corner][0] += math.pi * 2
    elif angle >= math.pi * 2:
        self.spikesAngles[lane][spike][corner][0] -= math.pi * 2


def checkCoordinates(self, newX, newZ):
    return newX + self.turningX, newZ + self.turningZ


def turnSpikes(self):
    corners = 5
    for lane in range(self.laneNum):
        for spike in range(len(self.spikes[0])):
            for corner in range(corners):
                if self.turningDirection == "right":
                    self.spikesAngles[lane][spike][corner][0] += self.turningAmount
                else:
                    self.spikesAngles[lane][spike][corner][0] -= self.turningAmount
                angle = self.spikesAngles[lane][spike][corner][0]
                adjustAngles(self, angle, lane, spike, corner)
                newX = math.cos(angle) * (self.spikesAngles[lane][spike][corner][1])
                newZ = math.sin(angle) * (self.spikesAngles[lane][spike][corner][1])
                self.spikes[lane][spike][corner][0], self.spikes[lane][spike][corner][2] = \
                    checkCoordinates(self, newX, newZ)
