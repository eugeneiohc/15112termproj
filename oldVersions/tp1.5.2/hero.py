import pygame


def startHero(self):
    for lane in range(self.laneNum):
        self.heroLocs[lane] = self.viewX - self.pathWidth / 2 + lane * self.laneInterval + self.laneInterval // 2
    self.p0 = [self.x0, self.y0, self.z0]
    self.p1 = [self.x0 - self.heroWidth // 2, self.y0, self.z0 - self.heroDepth]
    self.p2 = [self.x0 + self.heroWidth // 2, self.y0, self.z0 - self.heroDepth]
    self.heroSides = [None]
    self.heroSides[0] = [self.p0, self.p1, self.p2]


def resetHero(self):
    self.heroSides.clear()
    self.p0[0] = self.heroLocs[self.heroCurrLoc]
    self.p1[0] = self.p0[0] - self.heroWidth // 2
    self.p2[0] = self.p0[0] + self.heroWidth // 2
    self.heroSides.append([self.p0, self.p1, self.p2])


def heroTimerFired(self):
    if self.strafing:
        if self.strafeNums <= 0:
            self.strafing = False
            self.heroCurrLoc += self.strafeDirec
            resetHero(self)
        else:
            for side in self.heroSides:
                for corner in side:
                    corner[0] += self.strafeDirec * self.strafeInterval
                    self.strafeNums -= 1
                    # print(self.strafeNums)
