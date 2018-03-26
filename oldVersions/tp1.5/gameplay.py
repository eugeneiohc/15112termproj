## File for Gameplay Code

import pygame
import math
import random
    
def drawHero(self, screen):
    """
    angle = (self.focalPoint[0] - self.width / 2)/\
        (self.height - self.focalPoint[1]) * 180 / math.pi
    print("Angle:", angle)
    self.hero[0] = pygame.transform.rotate(self.hero[0], math.atan(angle))"""
    
    screen.blit(self.hero, (self.heroX, self.heroY))

def startPrisms(self):
    sides, cornerMult = 2, 2
    # -1 is left, 1 is right
    for side in range(sides): #for left and right sides
        for prism in range(self.prismsNum): # 0 to 10
            corner = 0
            X = random.randint(1, self.randThickX) * self.baseThickX
            Y = random.randint(1, self.randThickY) * self.baseThickY
            for xk in range(cornerMult): # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if(side == 0):
                            x = self.viewX + -((self.pathWidth / 2) + xk * X)
                        else:
                            x = self.viewX + ((self.pathWidth / 2) + xk * X)
                        y = yk * Y
                        z = ((self.prismsNum - prism) - zk) * self.prismDepth
                        self.prisms[side][prism][corner] =\
                            [int(x), int(y), int(z)]
                        corner += 1
    
def newPrism(self):
    neededPrisms, sides, cornerMult, corners = 2, 2, 2, 8
    # -1 is left, 1 is right
    for side in range(sides): #for left and right sides
        #makes random thicknesses
        X = random.randint(1, self.randThickX) * self.baseThickX
        Y = random.randint(1, self.randThickY) * self.baseThickY
        cornersList = [0 for i in range(corners)]
        count = 0
        for xk in range(cornerMult): # 0,1
            for yk in range(cornerMult):
                for zk in range(cornerMult):
                    if(side == 0):
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
    sides = []
    sides.append([prism[0], prism[1], prism[3], prism[2]])
    sides.append([prism[0], prism[1], prism[5], prism[4]])
    sides.append([prism[4], prism[5], prism[7], prism[6]])
    sides.append([prism[2], prism[3], prism[7], prism[6]])
    sides.append([prism[1], prism[3], prism[7], prism[5]])
    sides.append([prism[0], prism[2], prism[6], prism[4]])
    return sides
    
def convertTo2d(self, side):
    corners = []
    for corner in side:
        # append a tuple of coordinates
        x2d = corner[0] + (((corner[2]) / self.focalDepth) *\
            (self.focalPoint[0] - corner[0]))
        y2d = int((self.focalPoint[1] +\
            (((self.focalDepth - corner[2]) / self.focalDepth) ** 1) *\
            ((self.height - self.focalPoint[1]) - corner[1]))) +\
            (self.height - self.viewY)
        corners.append((x2d, y2d))
    return corners
    
def drawPrisms(self, screen):
    sides, corners = 2, 8
    if(len(self.prisms) == 0):
        self.prisms = [[[0 for i in range(corners)] for j in range\
            (self.prismsNum)] for k in range(sides)]
        self.prisms2d = [[0 for j in range (self.prismsNum)]\
            for k in range(sides)]
        startPrisms(self)
    for side in range(sides):
        for prism in range(self.prismsNum):
            for Side in generateSides(self.prisms[side][prism]):
                #print(convertTo2d(self, Side))
                pygame.draw.polygon(screen, self.prismColor, \
                    convertTo2d(self, Side), 1)
    
def drawLaser(self, screen):
    screen.blit(pygame.image.load\
        ("gameplayImages/redlaser.png").convert_alpha(), (0, 0))
        
def drawCover(self, screen):
    coverHeight = self.height // 6
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.width, coverHeight))

def movePrisms(self):
    sides, corners = 2, 8
    for side in range(sides):
        for prism in range(self.prismsNum):
            for corner in range(corners):
                # moves z coordinate only
                self.prisms[side][prism][corner][2] -= self.runningSpeed
    """
    self.focalPoint[0] += self.pathSideMove
    if(self.focalPoint[0] > self.width or self.focalPoint[0] < 0):
        self.pathSideMove *= -1"""
    
def checkOffScreen(self):
    sides, corners = 2, 8
    onScreen = False
    for side in range(sides):
        for Side in generateSides(self.prisms[side][-1]):
            #print(Side)
            for corner in Side:
                #checks if y is less than the height of the screen
                if(int((self.focalPoint[1] +\
                (((self.focalDepth - corner[2]) / self.focalDepth) ** 2) *\
                ((self.height - self.focalPoint[1]) - corner[1]))) +\
                (self.height - self.viewY) < self.height):
                    onScreen = True
    if not(onScreen):
        newPrism(self)
    #print()
    
def gameplayKeyPressed(self, keyCode, modifier):
    if(keyCode == 97): # left
        if(self.strafingR == False):
            self.strafingL = True
            if(self.strafeSpeed > 0):
                self.strafeSpeed *= -1
    elif(keyCode == 100):
        if(self.strafingL == False):
            self.strafingR = True
            if(self.strafeSpeed < 0):
                self.strafeSpeed *= -1
    
def gameplayTimerFired(self, dt):
    checkOffScreen(self) # checks if an obstacles is off the screen
    movePrisms(self)
    if(self.strafingL): # when pressed A
        if(self.heroX == self.lInterval):
            self.strafingL = False
        else:
            if(self.heroX == self.mInterval): #initalize
                self.strafeGoal = self.lInterval
            elif(self.heroX == self.rInterval): #initalize
                self.strafeGoal = self.mInterval
            self.heroX += self.strafeSpeed
            if(self.heroX <= self.strafeGoal):
                self.heroX = self.strafeGoal
                self.strafingL = False
    elif(self.strafingR): # when pressed D
        if(self.heroX == self.rInterval):
            self.strafingR = False
        else:
            if(self.heroX == self.mInterval): #initalize
                self.strafeGoal = self.rInterval
            elif(self.heroX == self.lInterval): #initalize
                self.strafeGoal = self.mInterval
            self.heroX += self.strafeSpeed
            #print("heroX:", self.heroX, "strafeGoal:", self.strafeGoal)
            if(self.heroX >= self.strafeGoal):
                self.heroX = self.strafeGoal
                self.strafingR = False

def gameplayRedrawAll(self, screen):
    drawHero(self, screen)
    drawPrisms(self,screen)
    #drawLaser(self, screen)
    #print("There are", len(self.prisms[0]), "prisms.")
    #drawCover(self, screen)
    
    
    
    
