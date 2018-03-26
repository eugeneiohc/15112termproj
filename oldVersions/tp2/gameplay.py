## File for Gameplay Code

import pygame
import math

from hero import *
from prisms import *
from spikes import *


def lawCos(self, corner):
    # for the x coordinate
    mainLeg = math.sqrt(corner[0] ** 2 + corner[2] ** 2)
    otherLeg = math.sqrt((corner[0] - self.viewX) ** 2 + corner[2] ** 2)
    if (otherLeg != 0):
        xAng = math.acos(
            (self.viewX ** 2 + otherLeg ** 2 - mainLeg ** 2) / \
            (2 * self.viewX * otherLeg))
        x = ((xAng - self.viewCameraLeft) / self.viewWidth) * self.width
    else:
        x = corner[0]
    # for the y coordinate
    mainLeg = math.sqrt(corner[1] ** 2 + corner[2] ** 2)
    otherLeg = math.sqrt((corner[1] - self.viewY) ** 2 + corner[2] ** 2)
    if otherLeg != 0:
        yAng = math.acos(
            (self.viewY ** 2 + otherLeg ** 2 - mainLeg ** 2) / \
            (2 * self.viewY * otherLeg))
        y = self.height - ((yAng - self.viewCameraBot) /
                           self.viewHeight) * self.height  # adjust flipped Y
    else:
        y = corner[1]
    return x, y


def convertCornerTo2d(self, side):
    corners = []
    for corner in side:
        corners.append(lawCos(self, corner))
    return corners


def drawPrisms(self, screen):
    sides, corners = 2, 8
    if len(self.prisms) == 0:
        self.prisms = [[[0 for i in range(corners)] for j in range(self.prismsNum)] for k in range(sides)]
        startPrisms(self)
    for side in range(sides):  # for each prism
        for prism in range(len(self.prisms[side])):
            for Side in generatePrismSides(self.prisms[side][prism]):
                pygame.draw.polygon(screen, (0, 0, 255), convertCornerTo2d(self, Side), 1)
    for prism in range(self.prismsNum):  # for the horizontal lines
        pygame.draw.line(screen, (255, 0, 0), lawCos(self, self.prisms[0][prism][0]),
                         lawCos(self, self.prisms[1][prism][0]), 2)


def drawSpikes(self, screen):
    corners = 5
    if len(self.spikes) == 0:
        self.spikes = [[[0 for i in range(corners)] for j in range(self.spikesNum)] for k in range(self.laneNum)]
        startSpikes(self)
    for lane in range(self.laneNum):  # for each prism
        for spike in range(self.spikesNum):
            for side in generateSpikeSides(self.spikes[lane][spike]):
                pygame.draw.polygon(screen, (255, 0, 0), convertCornerTo2d(self, side), 1)


def drawHero(self, screen):
    if len(self.hero) == 0:
        startHero(self)
    for side in generateHeroSides(self.hero):
        pygame.draw.polygon(screen, (0, 255, 0), convertCornerTo2d(self, side), 3)


def drawBackground(self, screen):
    pygame.draw.rect(screen, (255, 128, 223), (0, 0, self.width, self.height), 0)


def drawHpBar(self, screen):
    pygame.draw.rect(screen, (255, 0, 0), (self.hpX, self.hpY, self.hpWidth * self.hp, self.hpHeight), 0)
    pygame.draw.rect(screen, (0, 0, 0), (self.hpX, self.hpY, self.hpWidth, self.hpHeight), 5)


def drawGameover(self, screen):
    gameoverRect = self.instructButton.get_rect(center= (self.width / 2, self.height / 2))
    screen.blit(self.gameoverLabel, gameoverRect)


def checkOffScreen(self):
    sides = 2
    prismOnScreen, spikeOnScreen = False, False
    for side in range(sides):
        for Side in generatePrismSides(self.prisms[side][-1]):
            for corner in Side:
                # checks if y is less than the height of the screen
                if corner[2] > 0:
                    prismOnScreen = True
    if not prismOnScreen:
        newPrism(self)
        newSpike(self)


def gameplayKeyPressed(self, keyCode):  # all key presses only control hero, so no need for seperate
    heroKeyPressed(self, keyCode)


def gameplayTimerFired(self, dt):
    checkOffScreen(self)  # checks if an obstacle is off the screen
    movePrisms(self)
    moveSpikes(self)
    heroTimerFired(self)
    if self.mode == "gameover":  # the game decelerates at the end
        if self.runningSpeed > 0:
            self.runningSpeed *= self.endSlowRatio
        elif self.runningSpeed <= 1:
            self.runningSpeed = 0


def gameplayRedrawAll(self, screen):
    drawBackground(self, screen)
    drawPrisms(self, screen)
    drawSpikes(self, screen)
    if self.heroVisible:
        drawHero(self, screen)
    drawHpBar(self, screen)
    if self.mode == "gameover":
        drawGameover(self, screen)
        # drawCover(self, screen)
