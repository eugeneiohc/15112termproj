## File for Title Screen Code

import pygame
import csv

from operator import itemgetter


def startLzr(self, screen):  # only called once at the beginning
    self.lzrs.append([pygame.transform.scale(pygame.image.load("startImages/laserbackground.jpg").convert(),
                                             (self.width, self.height)), 0, 0])
    self.lzrs.append([pygame.transform.scale(pygame.image.load("startImages/laserbackground.jpg").convert(),
                                             (self.width, self.height)), self.width, 0])


def drawLzr(self, screen):  # to draw moving lzr
    if (len(self.lzrs) == 0):  # this will only get called at time = 0
        startLzr(self, screen)
    elif (self.lzrs[0][1] <= -self.width):  # when the first "cloud" isn't needed
        self.lzrs.pop(0)
        self.lzrs.append([pygame.transform.scale(pygame.image.load("startImages/laserbackground.jpg").convert(),
                                                 (self.width, self.height)), self.width, 0])
    for lzr in self.lzrs:  # drawing lzr
        screen.blit(lzr[0], (lzr[1], lzr[2]))


def titleRedrawAll(self, screen):
    drawLzr(self, screen)
    textYShift = self.height / 6
    textRectTitle = self.titleLabel.get_rect(center=(self.width / 2, textYShift))  # title
    self.textRectPlay = self.playButton.get_rect(center=(self.width / 2, textYShift * 2.75))  # play button
    self.textRectInstruct = self.instructButton.get_rect(center=(self.width / 2, textYShift * 3.5))  # instruct button
    self.textRectScoreboard = self.scoreboardButton.get_rect(center=(self.width / 2, textYShift * 4.25))  # scoreboard
    self.textRectOptions = self.optionsButton.get_rect(center=(self.width / 2, textYShift * 5))  # options button

    screen.blit(self.titleLabel, textRectTitle)  # title label
    screen.blit(self.playButton, self.textRectPlay)  # play button
    screen.blit(self.instructButton, self.textRectInstruct)  # instruct button
    screen.blit(self.scoreboardButton, self.textRectScoreboard)  # scoreboard button
    screen.blit(self.optionsButton, self.textRectOptions)  # instruct button


def instructionsRedrawAll(self, screen):
    drawLzr(self, screen)
    textYShift = self.height / 6
    textRectInstructTitle = self.instructLabel.get_rect(center=(self.width / 2, textYShift))  # instructions title text
    textInstructions1 = self.instructions1.get_rect(center=(self.width / 2, textYShift * 2.25))  # instructions text
    textInstructions2 = self.instructions2.get_rect(center=(self.width / 2, textYShift * 3))  # instructions text
    textInstructions3 = self.instructions3.get_rect(center=(self.width / 2, textYShift * 3.75))  # instructions text
    self.textRectBack = self.backButton.get_rect(center=(self.width / 2, textYShift * 5))  # back button

    screen.blit(self.instructLabel, textRectInstructTitle)  # instruct title
    screen.blit(self.instructions1, textInstructions1)  # instructions
    screen.blit(self.instructions2, textInstructions2)  # instructions
    screen.blit(self.instructions3, textInstructions3)  # instructions
    screen.blit(self.backButton, self.textRectBack)  # back button


def scoreboardRedrawAll(self, screen):
    drawLzr(self, screen)
    textYShift = self.height / 6
    numScores = 10  # number of scores to display
    file = open("scoreboard.txt", "r")
    scores = []
    for line in file:
        index1 = None
        for i in range(len(line)):
            if not index1:
                if not line[i].isdigit():
                    index1 = i
        spaceIndex = line.index(" ")
        index2 = None
        for i in range(spaceIndex + 1, len(line)):
            if not index2:
                if not line[i].isalpha() and not line[i].isdigit():
                    index2 = i
        scores.append([line[:spaceIndex], line[spaceIndex + 1:index2]])
    scores.sort(key = lambda x: int(x[0]))
    place = 1
    for i in range(len(scores) - 1, len(scores) - 1 - numScores, -1):
        scoreRow = str(place) + ". " + str(scores[i][1]) + "                         " + str(scores[i][0])
        scoreLabel = self.scoreFont.render(scoreRow, 1, (255, 255, 0))
        scoreRect = scoreLabel.get_rect(center=(self.width / 2, textYShift * (1 + 0.4 * place)))
        screen.blit(scoreLabel, scoreRect)
        place += 1

    textRectScoreboard = self.scoreboardLabel.get_rect(center=(self.width / 2, textYShift * 0.6))  # scoreboard title
    self.textRectBack = self.backButton.get_rect(center=(self.width / 2, textYShift * 5.5))  # back button

    screen.blit(self.scoreboardLabel, textRectScoreboard)  # scoreboard title text
    screen.blit(self.backButton, self.textRectBack)  # back button


def optionsRedrawAll(self, screen):
    self.multiplierLabel = self.instructFont.render("Multiplier: x" + str(self.scoreMultiplier), 1, (255, 255, 0))
    drawLzr(self, screen)
    textXShift = self.width / 6
    textYShift = self.height / 6
    textRectOptionsTitle = self.optionsLabel.get_rect(center=(self.width / 2, textYShift * 0.5))  # options title
    textRectOptionsInstructTitle = self.optionsInstructLabel.get_rect(center=(self.width / 2, textYShift * 1.5))
    textRectSpeedTitle = self.speedLabel.get_rect(center=(textXShift * 1.1, textYShift * 2.25))  # speed title
    textRectHealthTitle = self.healthLabel.get_rect(center=(textXShift * 1.1, textYShift * 3))  # health title
    textRectSpikeTitle = self.spikeLabel.get_rect(center=(textXShift * 1.1, textYShift * 3.75))  # spike title
    textRectLaneTitle = self.laneLabel.get_rect(center=(textXShift * 1.1, textYShift * 4.5))  # spike title
    textRectMultiplierTitle = self.multiplierLabel.get_rect(center=(textXShift * 4.5, textYShift * 5.5))  # spike title
    self.textRectBack = self.backButton.get_rect(center=(textXShift * 1, textYShift * 5.5))  # back button
    options, choices = 4, 4
    self.optionsRect = [[0 for i in range(choices)] for j in range(options)]
    for i in range(options):
        for j in range(choices):
            self.optionsRect[i][j] = self.options[i][j][0].get_rect \
                (center=(textXShift * (2.6 + j * 0.9), textYShift * (2.31 + i * 0.75)))
            if self.options[i][j][1] == False:
                if self.drawOptions:
                    screen.blit(self.options[i][j][0], self.optionsRect[i][j])
            else:
                screen.blit(self.options[i][j][0], self.optionsRect[i][j])

    screen.blit(self.optionsLabel, textRectOptionsTitle)  # options title
    screen.blit(self.optionsInstructLabel, textRectOptionsInstructTitle)  # options title
    screen.blit(self.speedLabel, textRectSpeedTitle)  # speed title
    screen.blit(self.healthLabel, textRectHealthTitle)  # health title
    screen.blit(self.spikeLabel, textRectSpikeTitle)  # spike title
    screen.blit(self.laneLabel, textRectLaneTitle)  # spike title
    screen.blit(self.multiplierLabel, textRectMultiplierTitle)  # spike title
    screen.blit(self.backButton, self.textRectBack)  # back button


def menuTimerFired(self, dt):
    # cloud movement
    for lzr in self.lzrs:
        lzr[1] -= self.lzrShift
    if self.mode == "options":
        self.timer += 1
        if self.timer % self.optionsTimer <= self.optionsTimer * 2 // 3:
            self.drawOptions = True
        else:
            self.drawOptions = False
    if not pygame.mixer.get_busy():
        self.titleMusic.play()


def titleMousePressed(self, x, y):
    if (self.textRectPlay.collidepoint(x, y)):  # if play is pressed
        self.mode = "gameplay"
        setOptions(self)
        self.gameplayInit()
        pygame.mixer.stop()
        self.helloKittyMusic.play()
    elif (self.textRectInstruct.collidepoint(x, y)):  # if instructions are pressed
        self.mode = "instructions"
    elif (self.textRectScoreboard.collidepoint(x, y)):  # if scoreboard is pressed
        self.mode = "scoreboard"
    elif (self.textRectOptions.collidepoint(x, y)):  # if options are pressed
        self.mode = "options"
        self.optionsTimer = 30
        self.drawOptions = True
        self.timer = 0


def instructMousePressed(self, x, y):
    if self.textRectBack.collidepoint(x, y):  # if play is pressed
        self.mode = "title"


def scoreboardMousePressed(self, x, y):
    if self.textRectBack.collidepoint(x, y):
        self.mode = "title"


def optionsMousePressed(self, x, y):
    if self.textRectBack.collidepoint(x, y):  # if play is pressed
        self.mode = "title"
    options, choices = 4, 4
    for i in range(options):
        for j in range(choices):
            if self.optionsRect[i][j].collidepoint(x, y):
                resetChoices(self, i)
                self.options[i][j][1] = True
    setOptions(self)


def resetChoices(self, option):
    choices = 4
    for i in range(choices):
        self.options[option][i][1] = False


def setOptions(self):
    runningMult, healthMult, spikeMult, laneMult = 1, 1, 1, 1
    choices = 4
    self.scoreMultiplier = 1
    for i in range(choices):
        # speed
        if self.options[0][i][1]:
            if i == 3:
                self.runningSpeed = 300
            else:
                self.runningSpeed = 50 + i * 50
            runningMult = self.options[0][i][2]
        # health
        if self.options[1][i][1]:
            if i == 3:
                self.spikeDamage = 1  # ant is instadeath lol
            else:
                self.spikeDamage = 0.05 + i * 0.05
            healthMult = self.options[1][i][2]
        # spike
        if self.options[2][i][1]:
            self.spikesProb = 40 - i * 6
            spikeMult = self.options[2][i][2]
        # lane
        if self.options[3][i][1]:
            if i == 3:
                self.laneNum = 2  # special case again
            else:
                self.laneNum = 7 - i * 2
            laneMult = self.options[3][i][2]
        self.scoreMultiplier = runningMult * healthMult * spikeMult * laneMult
