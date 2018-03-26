## File for Gameplay Code

import pygame
import math
import random

from hero import *


def startPrisms(self):
    sides, cornerMult = 2, 2
    # -1 is left, 1 is right
    for side in range(sides):  # for left and right sides
        for prism in range(self.prismsNum):  # 0 to 10
            corner = 0
            X = self.baseThickX
            Y = random.randint(1, self.randThickY) * self.baseThickY
            for xk in range(cornerMult):  # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if side == 0:
                            x = self.viewX + -((self.pathWidth / 2) + xk * X)
                        else:
                            x = self.viewX + ((self.pathWidth / 2) + xk * X)
                        y = yk * Y
                        z = ((self.prismsNum - prism) - zk) * self.prismDepth
                        self.prisms[side][prism][corner] = \
                            [int(x), int(y), int(z)]
                        corner += 1


def newPrism(self):
    sides, cornerMult, corners = 2, 2, 8
    # -1 is left, 1 is right
    for side in range(sides):  # for left and right sides
        # makes random thicknesses
        X = self.baseThickX
        Y = random.randint(1, self.randThickY) * self.baseThickY
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


def generateSides(prism):
    sides = [[prism[0], prism[1], prism[3], prism[2]], [prism[0], prism[1], prism[5], prism[4]],
             [prism[4], prism[5], prism[7], prism[6]], [prism[2], prism[3], prism[7], prism[6]],
             [prism[1], prism[3], prism[7], prism[5]], [prism[0], prism[2], prism[6], prism[4]]]
    return sides


def lawCos(self, corner):
    # for the x coordinate
    mainLeg = math.sqrt(corner[0] ** 2 + corner[2] ** 2)
    otherLeg = math.sqrt((corner[0] - self.viewX) ** 2 + corner[2] ** 2)
    xAng = math.acos(
        (self.viewX ** 2 + otherLeg ** 2 - mainLeg ** 2) / \
        (2 * self.viewX * otherLeg))
    x = ((xAng - self.viewCameraLeft) / self.viewWidth) * self.width
    # for the y coordinate
    mainLeg = math.sqrt(corner[1] ** 2 + corner[2] ** 2)
    otherLeg = math.sqrt((corner[1] - self.viewY) ** 2 + corner[2] ** 2)
    yAng = math.acos(
        (self.viewY ** 2 + otherLeg ** 2 - mainLeg ** 2) / \
        (2 * self.viewY * otherLeg))
    y = self.height - ((yAng - self.viewCameraBot) /
                       self.viewHeight) * self.height  # adjust flipped Y
    return (x, y)


def convertCornerTo2d(self, side):
    corners = []
    for corner in side:
        corners.append(lawCos(self, corner))
    return corners


def drawPrisms(self, screen):
    sides, corners = 2, 8
    if len(self.prisms) == 0:
        self.prisms = [[[0 for i in range(corners)] for j in range \
            (self.prismsNum)] for k in range(sides)]
        self.prisms2d = [[0 for j in range(self.prismsNum)] \
                         for k in range(sides)]
        startPrisms(self)
    for side in range(sides):  # for each prism
        for prism in range(len(self.prisms[side])):
            for Side in generateSides(self.prisms[side][prism]):
                # randColor = random.randint(self.randColorRange[0], self.randColorRange[1])
                pygame.draw.polygon(screen, (0, 0, 255), convertCornerTo2d(self, Side), 1)
    for prism in range(self.prismsNum):  # for the horizontal lines
        pygame.draw.line(screen, (255, 0, 0), lawCos(self, self.prisms[0][prism][0]),
                         lawCos(self, self.prisms[1][prism][0]), 2)


def drawHero(self, screen):
    if len(self.heroSides) == 0:
        startHero(self)
    for side in self.heroSides:
        pygame.draw.polygon(screen, (0, 255, 0), convertCornerTo2d(self, side), 3)


"""
def drawLaser(self, screen):
    screen.blit(pygame.image.load\
        ("gameplayImages/redlaser.png").convert_alpha(), (0, 0))
        
def drawCover(self, screen):
    coverHeight = self.height // 6
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.width, coverHeight))"""


def movePrisms(self):
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(self.prismsNum):
            for corner in range(corners):
                # moves z coordinate only
                self.prisms[side][prism][corner][2] -= self.runningSpeed


def checkOffScreen(self):
    sides, corners = 2, 8
    onScreen = False
    for side in range(sides):
        for Side in generateSides(self.prisms[side][-1]):
            for corner in Side:
                # checks if y is less than the height of the screen
                if corner[2] > 0:
                    onScreen = True
    if not (onScreen):
        newPrism(self)


def gameplayKeyPressed(self, keyCode, modifier):  # all key presses only control hero, so no need for seperate
    if keyCode == 119:  # up
        self.runningSpeed += 4
    elif keyCode == 115:  # down
        self.runningSpeed -= 4
    if keyCode == 97:  # left
        if self.strafing == False:
            if self.heroCurrLoc != 0:
                self.strafing = True
                self.strafeDirec = -1
                self.strafeNums = 5
    elif keyCode == 100:  # right
        if self.strafing == False:
            if self.heroCurrLoc != self.laneNum - 1:
                self.strafing = True
                self.strafeDirec = 1
                self.strafeNums = 5


def gameplayTimerFired(self, dt):
    checkOffScreen(self)  # checks if an obstacle is off the screen
    movePrisms(self)
    heroTimerFired(self)


def drawText(self, screen):
    pass


def gameplayRedrawAll(self, screen):
    drawPrisms(self, screen)
    drawHero(self, screen)
    drawText(self, screen)
    # drawCover(self, screen)
