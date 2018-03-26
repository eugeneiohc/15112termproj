# file for hero
from prisms import *
from spikes import *

import pygame


def startHero(self):
    for lane in range(self.laneNum):
        self.heroLocs[lane] = self.viewX - self.pathWidth / 2 + lane * self.laneWidth + self.laneWidth // 2
    corners = 4
    self.hero = [None for i in range(corners)]
    self.hero[0] = [self.x0, self.y0, self.z0]
    self.hero[1] = [self.x0 - self.heroWidth // 2, self.y0, self.z0 - self.heroDepth]
    self.hero[2] = [self.x0 + self.heroWidth // 2, self.y0, self.z0 - self.heroDepth]
    self.hero[3] = [self.x0, self.heroHeight, self.z0 - self.heroDepth]


def generateHeroSides(hero):
    sides = [[hero[0], hero[1], hero[2]], [hero[0], hero[1], hero[3]],
             [hero[0], hero[2], hero[3]], [hero[1], hero[2], hero[3]]]
    return sides


def resetHeroStrafe(self):
    self.hero[0][0] = self.heroLocs[self.heroCurrLoc]
    self.hero[1][0] = self.hero[0][0] - self.heroWidth // 2
    self.hero[2][0] = self.hero[0][0] + self.heroWidth // 2
    self.hero[3][0] = self.hero[0][0] + 0  # +0 for aliases bugs


def setHeroY(self, yCoordinate):
    self.hero[0][1] = yCoordinate
    self.hero[1][1] = yCoordinate
    self.hero[2][1] = yCoordinate
    self.hero[3][1] = yCoordinate + self.heroHeight


def setHeroZ(self, zCoordinate):
    self.hero[0][2] = zCoordinate
    self.hero[1][2] = zCoordinate - self.heroDepth
    self.hero[2][2] = zCoordinate - self.heroDepth
    self.hero[3][2] = zCoordinate - self.heroDepth


def shiftZ(self, shift):  # always add the shift
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(len(self.prisms[0])):
            for corner in range(corners):
                self.prisms[side][prism][corner][2] += shift
    corners = 5
    for lane in range(self.laneNum):
        for spike in range(len(self.spikes[0])):
            for corner in range(corners):
                self.spikes[lane][spike][corner][2] += shift


def heroKeyPressed(self, keyCode):
    if keyCode == 119:  # W
        if not self.jumping:
            self.jumpSound.play()
            self.jumping = True
    # self.runningSpeed += 4
    elif keyCode == 115:  # S
        pass
        # self.runningSpeed -= 4
        # if self.runningSpeed < 0:
        #     self.runningSpeed = 0
    if keyCode == 97:  # A
        if not self.strafing:
            if self.heroCurrLoc != 0:
                self.strafing = True
                self.strafeDirec = -1
                self.strafeNums = 5
    elif keyCode == 100:  # D
        if not self.strafing:
            if self.heroCurrLoc != self.laneNum - 1:
                self.strafing = True
                self.strafeDirec = 1
                self.strafeNums = 5
    if self.approachingTurn:
        turningPoint = self.prisms[0][self.prismsNum + 1][1][2] + self.pathWidth // 2 + self.prismX
        if turningPoint - self.pathWidth // 2 < self.hero[0][2] < turningPoint + self.pathWidth // 2:
            shiftZ(self, self.hero[0][2] - turningPoint)
            if keyCode == 276 and self.turningDirection == "left":
                self.approachingTurn = False
                self.turning = True
                self.amountTurned = 0
                setPrismsAngles(self)
                setSpikesAngles(self)
            elif keyCode == 275 and self.turningDirection == "right":
                self.approachingTurn = False
                self.turning = True
                self.amountTurned = 0
                setPrismsAngles(self)
                setSpikesAngles(self)


def heroCollision(self):
    for heroC in self.hero:
        # firstSpike = len(self.spikes[0]) - self.heroZShift
        for lane in range(self.laneNum):
            # for spike in range(firstSpike - 2, firstSpike):
            for spike in range(len(self.spikes[0])):
                if self.spikes[lane][spike]:  # only checks spikes that exist
                    if self.spikes[lane][spike][0][0] <= heroC[0] <= self.spikes[lane][spike][2][0]:
                        if self.spikes[lane][spike][0][1] <= heroC[1] <= self.spikes[lane][spike][4][1]:
                            if self.spikes[lane][spike][1][2] <= heroC[2] <= self.spikes[lane][spike][0][2]:
                                self.collisionSound.play()
                                return True
    return False


def heroTimerFired(self):
    self.timer += 1
    if self.approachingTurn and self.mode == "gameplay" and\
            self.hero[0][2] >= self.prisms[0][self.prismsNum + 1][1][2] + self.pathWidth + self.prismX:  # hit wall
        self.hp = 0
        self.mode = "gameover"
        self.endSlowRatio = 0.5
        pygame.mixer.stop()
        self.lolYouDiedMusic.play()
    if self.jumping:
        if self.jumpingTimer < self.jumpStrength / self.gravity:  # a y coordinate
            self.jumpingTimer += 1
            y = -(self.gravity * self.jumpingTimer ** 2) + self.jumpStrength * self.jumpingTimer
            setHeroY(self, y)
        else:
            setHeroY(self, 0)
            self.jumping = False
            self.jumpingTimer = 0
    if self.strafing:
        if self.strafeNums <= 0:
            self.strafing = False
            self.heroCurrLoc += self.strafeDirec
            resetHeroStrafe(self)
        else:
            for side in self.hero:
                side[0] += self.strafeDirec * self.strafeInterval
                self.strafeNums -= 1
    if not self.mode == "gameover" and not self.mode == "scoreenter":
        if not self.heroInvulnerable:
            self.score += self.scoreIncrement * self.scoreMultiplier
            if heroCollision(self):
                self.hp = round(self.hp - self.spikeDamage, 2)
                self.heroInvulnerable = True
                if self.hp <= 0:
                    self.hp = 0
                    self.mode = "gameover"
                    pygame.mixer.stop()
                    self.lolYouDiedMusic.play()
        else:  # this is when you're invulnerable
            self.heroBlinker += 1
            if self.heroBlinker % 6 <= 3:
                self.heroVisible = True
            else:
                self.heroVisible = False
            if self.heroBlinker > 50:
                self.heroBlinker = 0
                self.heroInvulnerable = False
