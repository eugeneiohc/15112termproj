# this is for prisms (the borders of the lane)

import random
import math


def startPrisms(self):
    # draw the borders (prisms)
    sides, cornerMult = 2, 2
    X = self.prismX
    # -1 is left, 1 is right
    for side in range(sides):  # for left and right sides
        for prism in range(self.prismsNum):
            corner = 0
            Y = random.randint(1, self.randThickY) * self.prismY
            for xk in range(cornerMult):  # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if side == 0:
                            x = self.viewX - ((self.pathWidth / 2) + xk * X)
                        else:
                            x = self.viewX + ((self.pathWidth / 2) + xk * X)
                        y = yk * Y
                        z = ((self.prismsNum - prism) - zk) * self.prismDepth
                        self.prisms[side][prism][corner] = [int(x), int(y), int(z)]
                        corner += 1


def extendPrisms(self):  # extends the list so it can hold more prisms for the upcoming lanes
    sides, corners, newSize = 2, 8, self.prismsNum + len(self.prisms[0]) + 2
    prisms = [[[0 for i in range(corners)] for j in range(newSize)] for k in range(sides)]
    for i in range(sides):
        for j in range(self.prismsNum + 2, newSize):
            for k in range(corners):
                prisms[i][j][k] = self.prisms[i][j - self.prismsNum - 2][k]
    self.prisms = prisms  # new list has been created


def startPrismsLeft(self):  # creates a left lane so that the user can see the lane coming up
    if len(self.prisms[0]) <= self.prismsNum + 6:
        extendPrisms(self)
    sides, cornerMult = 2, 2
    for side in range(sides):  # for left and right sides
        for prism in range(self.prismsNum):
            corner = 0
            Y = random.randint(1, self.randThickY) * self.prismY
            for xk in range(cornerMult):  # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):  # im keeping all of these variable names to help keep track
                        x = self.viewX - (self.pathWidth // 2) - ((self.prismsNum - prism) - zk) * self.prismDepth
                        y = yk * Y
                        if side == 0:
                            z = (self.lastZ + self.prismX) - xk * self.prismX
                        else:
                            z = (self.lastZ + self.prismX) + self.pathWidth + xk * self.prismX
                        self.prisms[side][prism][corner] = [int(x), int(y), int(z)]
                        corner += 1
    # adding the prism pairs that only have one (for the turning corner)
    for side in range(sides):
        corner = 0
        Y = random.randint(1, self.randThickY) * self.prismY
        for xk in range(cornerMult):
            for yk in range(cornerMult):
                for zk in range(cornerMult):
                    if side == 0:
                        x1 = self.viewX - (self.pathWidth // 2)
                        x2 = self.viewX + (self.pathWidth // 2)
                        y1, y2 = 0, 0
                    else:  # side == 1 (right side)
                        x1 = self.viewX - (self.pathWidth // 2) + (zk * (self.pathWidth + self.prismX))
                        x2 = self.viewX + ((self.pathWidth // 2) + xk * self.prismX)
                        y1 = yk * Y
                        y2 = yk * Y
                    z1 = (self.lastZ + self.prismX) + self.pathWidth + xk * self.prismX
                    z2 = (self.lastZ + self.pathWidth + self.prismX) - zk * (self.pathWidth + self.prismX)
                    self.prisms[side][self.prismsNum][corner] = [int(x1), int(y1), int(z1)]
                    self.prisms[side][self.prismsNum + 1][corner] = [int(x2), int(y2), int(z2)]
                    corner += 1


def startPrismsRight(self):  # creates a left lane so that the user can see the lane coming up
    if len(self.prisms[0]) <= self.prismsNum + 6:
        extendPrisms(self)
    sides, cornerMult = 2, 2
    for side in range(sides):  # for left and right sides
        for prism in range(self.prismsNum):
            corner = 0
            Y = random.randint(1, self.randThickY) * self.prismY
            for xk in range(cornerMult):  # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):  # im keeping all of these variable names to help keep track
                        x = self.viewX + (self.pathWidth // 2) + ((self.prismsNum - prism) - zk) * self.prismDepth
                        y = yk * Y
                        if side == 0:
                            z = (self.lastZ + self.prismX) + self.pathWidth + xk * self.prismX
                        else:
                            z = (self.lastZ + self.prismX) - xk * self.prismX
                        self.prisms[side][prism][corner] = [int(x), int(y), int(z)]
                        corner += 1
    # adding the prism pairs that only have one (for the turning corner)
    for side in range(sides):
        corner = 0
        Y = random.randint(1, self.randThickY) * self.prismY
        for xk in range(cornerMult):
            for yk in range(cornerMult):
                for zk in range(cornerMult):
                    if side == 0:
                        x1 = self.viewX + (self.pathWidth // 2) - (zk * (self.pathWidth + self.prismX))
                        x2 = self.viewX - ((self.pathWidth // 2) + xk * self.prismX)
                        y1 = yk * Y
                        y2 = yk * Y
                    else:
                        x1 = self.viewX + (self.pathWidth // 2)
                        x2 = self.viewX - (self.pathWidth // 2)
                        y1, y2 = 0, 0
                    z1 = (self.lastZ + self.prismX) + self.pathWidth + xk * self.prismX
                    z2 = (self.lastZ + self.pathWidth + self.prismX) - zk * (self.pathWidth + self.prismX)
                    self.prisms[side][self.prismsNum][corner] = [int(x1), int(y1), int(z1)]
                    self.prisms[side][self.prismsNum + 1][corner] = [int(x2), int(y2), int(z2)]
                    corner += 1


def newPrism(self):
    sides, cornerMult, corners = 2, 2, 8
    # -1 is left, 1 is right
    for side in range(sides):  # for left and right sides
        # makes random thicknesses
        X = self.prismX
        Y = random.randint(1, self.randThickY) * self.prismY
        cornersList = [0 for i in range(corners)]
        count = 0
        for xk in range(cornerMult):  # 0,1
            for yk in range(cornerMult):
                for zk in range(cornerMult):
                    if side == 0:
                        x = self.viewX + -((self.pathWidth / 2) + xk * X)
                    else:
                        x = self.viewX + ((self.pathWidth / 2) + xk * X)
                    y = yk * Y
                    z = self.prisms[side][0][zk][2] + self.prismDepth
                    cornersList[count] = [int(x), int(y), int(z)]
                    count += 1
        self.prisms[side].insert(0, cornersList)
        self.prisms[side].pop(-1)


def removeLastPrism(self):
    sides = 2
    for side in range(sides):
        self.prisms[side].pop(-1)


def generatePrismSides(prism):
    sides = [[prism[0], prism[1], prism[3], prism[2]], [prism[0], prism[1], prism[5], prism[4]],
             [prism[4], prism[5], prism[7], prism[6]], [prism[2], prism[3], prism[7], prism[6]],
             [prism[1], prism[3], prism[7], prism[5]], [prism[0], prism[2], prism[6], prism[4]]]
    return sides


def movePrisms(self):
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(len(self.prisms[0])):
            for corner in range(corners):
                # moves z coordinate only
                self.prisms[side][prism][corner][2] -= self.runningSpeed


def setPrismsAngles(self):
    sides, corners, data = 2, 8, 2
    self.prismsAngles = [[[[0 for a in range(data)] for b in range(corners)]
                          for c in range(len(self.prisms[0]))] for d in range(sides)]
    for side in range(sides):
        for prism in range(len(self.prisms[0])):
            for corner in range(corners):
                diffX = self.prisms[side][prism][corner][0] - self.turningX
                diffZ = self.prisms[side][prism][corner][2] - self.turningZ
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
                self.prismsAngles[side][prism][corner][0] = angle
                self.prismsAngles[side][prism][corner][1] = radius


def adjustAngles(self, angle, side, prism, corner):
    if angle < 0:
        self.prismsAngles[side][prism][corner][0] += math.pi * 2
    elif angle >= math.pi * 2:
        self.prismsAngles[side][prism][corner][0] -= math.pi * 2


def checkCoordinates(self, newX, newZ):
    return newX + self.turningX, newZ + self.turningZ


def turnPrisms(self):
    sides, cornerMult = 2, 2
    for side in range(sides):
        for prism in range(len(self.prisms[0])):
            corner = 0
            for xk in range(cornerMult):
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if self.turningDirection == "right":
                            self.prismsAngles[side][prism][corner][0] += self.turningAmount
                        else:
                            self.prismsAngles[side][prism][corner][0] -= self.turningAmount
                        angle = self.prismsAngles[side][prism][corner][0]
                        adjustAngles(self, angle, side, prism, corner)
                        newX = math.cos(angle) * (self.prismsAngles[side][prism][corner][1])
                        newZ = math.sin(angle) * (self.prismsAngles[side][prism][corner][1])
                        self.prisms[side][prism][corner][0], self.prisms[side][prism][corner][2] = \
                            checkCoordinates(self, newX, newZ)
                        corner += 1
