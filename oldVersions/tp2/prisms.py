import random


def startPrisms(self):
    # draw the borders (prisms)
    sides, cornerMult = 2, 2
    # -1 is left, 1 is right
    for side in range(sides):  # for left and right sides
        for prism in range(self.prismsNum):
            corner = 0
            X = self.prismX
            Y = random.randint(1, self.randThickY) * self.prismY
            for xk in range(cornerMult):  # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if side == 0:
                            x = self.viewX + -((self.pathWidth / 2) + xk * X)
                        else:
                            x = self.viewX + ((self.pathWidth / 2) + xk * X)
                        y = yk * Y
                        z = ((self.prismsNum - prism) - zk) * self.prismDepth
                        self.prisms[side][prism][corner] = [int(x), int(y), int(z)]
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


def generatePrismSides(prism):
    sides = [[prism[0], prism[1], prism[3], prism[2]], [prism[0], prism[1], prism[5], prism[4]],
             [prism[4], prism[5], prism[7], prism[6]], [prism[2], prism[3], prism[7], prism[6]],
             [prism[1], prism[3], prism[7], prism[5]], [prism[0], prism[2], prism[6], prism[4]]]
    return sides


def movePrisms(self):
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(self.prismsNum):
            for corner in range(corners):
                # moves z coordinate only
                self.prisms[side][prism][corner][2] -= self.runningSpeed
