## File for Gameplay Code

import csv

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
    if len(self.prisms) == 0:  # only procs in the beginning
        self.prisms = [[[0 for i in range(corners)] for j in range(self.prismsNum)] for k in range(sides)]
        startPrisms(self)
    for side in range(sides):  # for each prism
        for prism in range(len(self.prisms[side])):
            for Side in generatePrismSides(self.prisms[side][prism]):
                pygame.draw.polygon(screen, (0, 0, 255), convertCornerTo2d(self, Side), 1)
    for prism in range(len(self.prisms[0])):  # for the horizontal lines
        pygame.draw.line(screen, (255, 0, 0), lawCos(self, self.prisms[0][prism][0]),
                         lawCos(self, self.prisms[1][prism][0]), 2)


def drawSpikes(self, screen):
    corners = 5
    if len(self.spikes) == 0:
        self.spikes = [[[0 for i in range(corners)] for j in range(self.spikesNum)] for k in range(self.laneNum)]
        startSpikes(self)
    for lane in range(self.laneNum):  # for each spike
        for spike in range(len(self.spikes[0])):
            for side in generateSpikeSides(self.spikes[lane][spike]):
                pygame.draw.polygon(screen, (255, 0, 0), convertCornerTo2d(self, side), 0)
                # pygame.draw.polygon(screen, (0, 0, 0), convertCornerTo2d(self, side), 1)


def drawHero(self, screen):
    if len(self.hero) == 0:
        startHero(self)
    for side in generateHeroSides(self.hero):
        pygame.draw.polygon(screen, (0, 255, 0), convertCornerTo2d(self, side), 5)
        # pygame.draw.polygon(screen, (0, 0, 0), convertCornerTo2d(self, side), 2)


def drawBackground(self, screen):
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, self.width, self.height), 0)


def drawCover(self, screen):
    pygame.draw.rect(screen, (255, 255, 0), (0, 0, self.width, self.height * 0.15), 0)


def drawHpBar(self, screen):
    pygame.draw.rect(screen, (255, 0, 0), (self.hpX, self.hpY, self.hpWidth * self.hp, self.hpHeight), 0)
    pygame.draw.rect(screen, (0, 0, 0), (self.hpX, self.hpY, self.hpWidth, self.hpHeight), 5)


def drawScore(self, screen):
    scoreText = "Score: %s" % (str(round(self.score)))
    scoreLabel = self.instructFont.render(scoreText, 1, (0, 0, 0))
    scoreRect = scoreLabel.get_rect(center=(self.scoreX, self.scoreY))
    screen.blit(scoreLabel, scoreRect)


def drawGameover(self, screen):
    textYShift = self.height / 6
    if self.timer == self.gameoverTimer:
        self.timer = 0
    if self.timer % self.gameoverTimer <= self.gameoverTimer // 2:
        gameoverRect = self.gameoverLabel.get_rect(center=(self.width / 2, textYShift * 2.5))
        enterNameRect = self.enterNameLabel.get_rect(center=(self.width / 2, textYShift * 3.5))
        backToMenuRect = self.backToMenuLabel.get_rect(center=(self.width / 2, textYShift * 4))
        screen.blit(self.gameoverLabel, gameoverRect)
        screen.blit(self.enterNameLabel, enterNameRect)
        screen.blit(self.backToMenuLabel, backToMenuRect)


def drawScoreEnter(self, screen):
    textYShift = self.height / 6
    typeNameRect = self.typeNameLabel.get_rect(center=(self.width / 2, textYShift * 2.75))
    scoreText = str(self.name) + " | Score: " + str(self.score)
    scoreLabel = self.instructFont.render(scoreText, 1, (0, 0, 0))
    scoreRect = scoreLabel.get_rect(center=(self.width / 2, textYShift * 3.75))
    if self.timer == self.gameoverTimer:
        self.timer = 0
    if self.timer % self.gameoverTimer <= self.gameoverTimer // 2:
        screen.blit(self.typeNameLabel, typeNameRect)
    screen.blit(scoreLabel, scoreRect)


def checkOffScreen(self):
    if not self.turning:  # when it's not turning the screen
        sides = 2
        prismOffScreen, spikeOnScreen = True, False
        for side in range(sides):
            for Side in generatePrismSides(self.prisms[side][-1]):
                for corner in Side:
                    # checks if y is less than the height of the screen
                    if corner[2] > 0:
                        prismOffScreen = False
        if prismOffScreen:
            if not self.approachingTurn:  # when it's just going straight
                willTurn = random.randint(1, self.turnChance)
                self.lastZ = self.prisms[0][0][0][2]  # the last Z point for reference
                if willTurn == 1:
                    self.approachingTurn = True
                    self.notCreatedLane = True
                    direction = random.randint(1, 2)
                    if direction == 1:
                        self.turningDirection = "left"
                        startPrismsLeft(self)
                        startSpikesLeft(self)
                    else:  # direct is 2
                        self.turningDirection = "right"
                        startPrismsRight(self)
                        startSpikesRight(self)
                else:
                    while len(self.prisms[0]) > self.prismsNum - 2:  # just pops if it's on a corner
                        removeLastPrism(self)
                        removeLastSpike(self)
                    else:
                        newPrism(self)
                        newSpike(self)
            elif self.approachingTurn:  # when there's a turn coming up
                removeLastPrism(self)
                removeLastSpike(self)


def gameplayKeyPressed(self, keyCode):  # all key presses only control hero, so no need for separate
    if not self.mode == "gameover" and not self.mode == "scoreenter":
        heroKeyPressed(self, keyCode)
    elif self.mode == "gameover":
        if keyCode == 13:
            self.mode = "scoreenter"
    elif self.mode == "scoreenter":
        if keyCode == 8 and len(self.name) > 0:  # backspace
            self.name = self.name[:len(self.name) - 1]
        if 48 <= keyCode <= 57 and len(self.name) < 16:
            self.name += chr(keyCode)
        charNum = (keyCode - 32)
        if 65 <= charNum <= 90 and len(self.name) < 16:  # within A and Z, inclusive, under 20 characters
            self.name += chr(charNum)
        if keyCode == 13 and len(self.name) > 0:  # pressed enter, with some kind of name
            file = open("scoreboard.txt", "a")
            file.write(str(int(self.score)) + " " + self.name + "\n")
            self.mode = "title"
            self.runningSpeed = 100
            self.gameplayInit()
            pygame.mixer.stop()
            self.titleMusic.play()


def roundValues(self):
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(len(self.prisms[0])):
            for corner in range(corners):
                self.prisms[side][prism][corner][0] = round(self.prisms[side][prism][corner][0])
                self.prisms[side][prism][corner][2] = round(self.prisms[side][prism][corner][2])
    corners = 5
    for lane in range(self.laneNum):
        for spike in range(len(self.spikes[0])):
            for corner in range(corners):
                self.spikes[lane][spike][corner][0] = round(self.spikes[lane][spike][corner][0])
                self.spikes[lane][spike][corner][2] = round(self.spikes[lane][spike][corner][2])


def gameplayTimerFired(self, dt):
    if self.mode == "gameover" or self.mode == "scoreenter":  # the game decelerates at the end
        if self.runningSpeed > 0.01:  # once it hits speed a low enough speed, speed set to 0
            self.runningSpeed *= self.endSlowRatio
        else:
            self.runningSpeed = 0
    self.timer += 1
    heroTimerFired(self)
    if self.turning:
        if self.amountTurned < math.pi / 2:
            turnPrisms(self)
            turnSpikes(self)
            roundValues(self)
            self.amountTurned += self.turningAmount
        else:
            self.turning = False
    else:
        checkOffScreen(self)  # checks if an obstacle is off the screen
        movePrisms(self)
        moveSpikes(self)
    if not pygame.mixer.get_busy():
        if self.mode == "gameplay":
            self.helloKittyMusic.play()
        elif self.mode == "gameover" or self.mode == "scoreenter":
            self.lolYouDiedMusic.play()


def gameplayRedrawAll(self, screen):
    drawBackground(self, screen)
    drawPrisms(self, screen)
    drawSpikes(self, screen)
    if self.heroVisible:
        drawHero(self, screen)
    drawCover(self, screen)
    drawHpBar(self, screen)
    drawScore(self, screen)
    if self.mode == "gameover":
        drawGameover(self, screen)
    elif self.mode == "scoreenter":
        drawScoreEnter(self, screen)
