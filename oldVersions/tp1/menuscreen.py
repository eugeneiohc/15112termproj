## File for Title Screen Code

import pygame
    
def startClouds(self, screen): #only called once at the beginning
    self.clouds.append([pygame.transform.scale(pygame.image.load\
        ("startImages/bigclouds.jpg").convert(), (self.width, self.height)),
        0, 0])
    self.clouds.append([pygame.transform.scale(pygame.image.load\
        ("startImages/bigclouds.jpg").convert(), (self.width, self.height)),
        self.width, 0])
    
def drawClouds(self, screen): # to draw moving clouds
    if(len(self.clouds) == 0): #this will only get called at time = 0
        startClouds(self, screen)
    elif(self.clouds[0][1] <= -self.width): #when the first "cloud" isn't needed
        self.clouds.pop(0)
        self.clouds.append([pygame.transform.scale(pygame.image.load\
            ("startImages/bigclouds.jpg").convert(), (self.width, self.height)),
            self.width, 0])
    for cloud in self.clouds: #drawing clouds
        screen.blit(cloud[0], (cloud[1], cloud[2]))
    
def titleRedrawAll(self, screen):
    drawClouds(self, screen)
    textYShift = self.height / 6
    textRectTitle = self.titleLabel.get_rect(center = (self.width / 2,\
        textYShift)) # title
    self.textRectPlay = self.playButton.get_rect(center = (self.width / 2,\
        textYShift * 3)) # play button
    self.textRectInstruct = self.instructButton.get_rect(center = (self.width\
        / 2, textYShift * 4)) # instruct button
    
    screen.blit(self.titleLabel, textRectTitle) # title label
    screen.blit(self.playButton, self.textRectPlay) # play button
    screen.blit(self.instructButton, self.textRectInstruct) # instruct button
    
def menuTimerFired(self, dt):
    #cloud movement
    for cloud in self.clouds:
        cloud[1] -= self.cloudShift
    
def instructionsRedrawAll(self, screen):
    drawClouds(self, screen)
    textYShift = self.height / 6
    textRectInstructTitle = self.instructLabel.get_rect(center = \
        (self.width / 2, textYShift)) # instructions title text
    textInstructions1 = self.instructions1.get_rect(center = \
        (self.width / 2, textYShift * 2.5)) # instructions text
    textInstructions2 = self.instructions2.get_rect(center = \
        (self.width / 2, textYShift * 3.5)) # instructions text
    self.textRectBack = self.backButton.get_rect(center = \
        (self.width / 2, textYShift * 5)) # back button
        
    screen.blit(self.instructLabel, textRectInstructTitle) #instruct title        
    screen.blit(self.instructions1, textInstructions1) #instructions       
    screen.blit(self.instructions2, textInstructions2) #instructions
    screen.blit(self.backButton, self.textRectBack) # back button
    
    
def titleMousePressed(self, x, y):
    if(self.textRectPlay.collidepoint(x, y)): #if play is pressed
        self.mode = "gameplay"
    if(self.textRectInstruct.collidepoint(x, y)): #if instructions are pressed
        self.mode = "instructions"

def instructMousePressed(self, x, y):
    if(self.textRectBack.collidepoint(x, y)): #if play is pressed
        self.mode = "title"
    


