def startHero(self):
    for lane in range(self.laneNum):
        self.heroLocs[lane] = self.viewX - self.pathWidth / 2 + lane * self.laneWidth + self.laneWidth // 2
    self.hero = [None for i in range(4)]
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


def heroKeyPressed(self, keyCode):
    if not self.mode == "gameover":
        if keyCode == 119:  # W
            if not self.jumping:
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


def heroCollision(self):
    for heroC in self.hero:
        firstSpike = self.spikesNum - self.heroZShift
        for lane in range(self.laneNum):
            for spike in range(firstSpike - 2, firstSpike):
                if(self.spikes[lane][spike][0][0]):  # only checks spikes that exist
                    if(self.spikes[lane][spike][0][0] <= heroC[0] <= self.spikes[lane][spike][2][0]):
                        if(self.spikes[lane][spike][0][1] <= heroC[1] <= self.spikes[lane][spike][4][1]):
                            if(self.spikes[lane][spike][1][2] <= heroC[2] <=  self.spikes[lane][spike][0][2]):
                                return True
    return False


def heroTimerFired(self):
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
    if not self.heroInvulnerable and not self.mode == "gameover":
        # self.hp += 0.0001
        if self.hp > 1:
            self.hp = 1
        if heroCollision(self):
            self.hp -= self.spikeDamage
            self.heroInvulnerable = True
            if self.hp <= 0:
                self.hp = 0
                self.mode = "gameover"
    else: # this is when you're invulnerable
        self.heroBlinker += 1
        if self.heroBlinker % 6 <= 3:
            self.heroVisible = True
        else:
            self.heroVisible = False
        if self.heroBlinker > 50:
            self.heroBlinker = 0
            self.heroInvulnerable = False


