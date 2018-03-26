## File for Gameplay Code

import pygame
import random

def startHero(self, screen):
    self.hero = [pygame.transform.scale(pygame.image.load\
        ("gameplayImages/motorcycle.png").convert_alpha(), (self.heroWidth,\
        self.heroHeight)), 0] #-1: left, 0: center, 1: right
    
def drawHero(self, screen):
    if(len(self.hero) == 0):
        startHero(self, screen)
    screen.blit(self.hero[0], (self.heroX + (self.pathWidth / 4) *\
        self.hero[1], self.heroY))

def startPrisms(self):
    sides, startPrismsNum, cornerMult, baseThick = 2, 11, 2, 40
    Z = 100 #the depth must always be constant
    # -1 is left, 1 is right
    for side in range(sides): #for left and right sides
        for prism in range(startPrismsNum): # 0 to 10
            corner = 0
            X = random.randint(1, 3) * baseThick
            Y = random.randint(1, 3) * baseThick
            for xk in range(cornerMult): # 0,1
                for yk in range(cornerMult):
                    for zk in range(cornerMult):
                        if(side == 0):
                            x = self.viewX + -((self.pathWidth / 2) + xk * X)
                        else:
                            x = self.viewX + ((self.pathWidth / 2) + xk * X)
                        y = -yk * Y
                        z = ((prism - 1) + zk) * Z
                        self.prisms[side][prism][corner] =\
                            [int(x), int(y), int(z)]
                        corner += 1
    
def newPrism(self):
    sides, cornerMult, baseThick, corners = 2, 2, 40, 8
    Z = 100 #the depth must always be constant
    # -1 is left, 1 is right
    for side in range(sides): #for left and right sides
        X = random.randint(1, 3) * baseThick #makes random thicknesses
        Y = random.randint(1, 3) * baseThick
        cornersList = [0 for i in range(corners)]
        count = 0
        for xk in range(cornerMult): # 0,1
            for yk in range(cornerMult):
                for zk in range(cornerMult):
                    if(side == 0):
                        x = self.viewX + -((self.pathWidth / 2) + xk * X)
                    else:
                        x = self.viewX + ((self.pathWidth / 2) + xk * X)
                    y = -yk * Y
                    z = -zk * Z
                    cornersList[count] = [int(x), int(y), int(z)]
                    count += 1
        self.prisms[side].pop(-1)
        self.prisms[side].insert(0, cornersList)
    
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
        corners.append((self.viewX - ((corner[2] / self.viewDepth) *\
            (self.viewX - corner[0])), ((corner[2] / self.viewDepth) *\
            (corner[1] + self.focalHeight))))
    return corners
    
def drawPrisms(self, screen):
    sides, prismsNum, corners = 2, 11, 8
    if(len(self.prisms) == 0):
        self.prisms = [[[0 for i in range(corners)] for j in range(prismsNum)]\
            for k in range(sides)]
        startPrisms(self)
    for side in range(sides):
        for prism in range(prismsNum):
            for Side in generateSides(self.prisms[side][prism]):
                #print(convertTo2d(self, Side))
                pygame.draw.polygon(screen, (255, 0, 0), \
                    convertTo2d(self, Side), 1)
    
def movePrisms(self):
    sides, prismsNum, corners = 2, 11, 8
    for side in range(sides):
        for prism in range(prismsNum):
            for corner in range(corners):
                # moves z coordinate only
                self.prisms[side][prism][corner][2] += self.runningSpeed
    
def checkOffScreen(self):
    sides, corners = 2, 8
    onScreen = False
    for side in range(sides):
        for corner in range(corners):
            #checks if z is on screen, if at least is on, it leaves it alone
            if(self.prisms[side][-1][corner][2] <= self.viewDepth):
                onScreen = True
    if not(onScreen):
        newPrism(self)
    
def gameplayKeyPressed(self, keyCode, modifier):
    if(keyCode == 97):
        if(self.hero[1] != -1):
            self.hero[1] -= 1
    elif(keyCode == 100):
        if(self.hero[1] != 1):
            self.hero[1] += 1
    
def gameplayTimerFired(self, dt):
    checkOffScreen(self) # checks if an obstacles is off the screen
    movePrisms(self)

def gameplayRedrawAll(self, screen):
    drawHero(self, screen)
    drawPrisms(self,screen)
    
    
    
    
