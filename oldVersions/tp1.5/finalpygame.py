'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''

import pygame
from PIL import Image, ImageFilter
from pygame.locals import *

from menuscreen import *
from gameplay import *

class PygameGame(object):

    def init(self):
        self.mode = "title"
        
        titleSize = self.width // 10        
        normSize = self.width // 14
        instructSize = self.width // 24
        
        self.titleFont = pygame.font.SysFont("Comic Sans MS", titleSize)
        self.normFont = pygame.font.SysFont("Comic Sans MS", normSize)
        self.instructFont = pygame.font.SysFont("Comic Sans MS", instructSize)
        
        self.titleLabel = self.titleFont.render("112 Runner", 1,\
        (255, 255, 255))
        self.instructLabel = self.titleFont.render("Instructions", 1,\
        (255, 255, 255))
        
        self.playButton = self.normFont.render("Play", 1, (255, 255, 255))
        self.instructButton = self.normFont.render("Instructions", 1,\
        (255, 255, 255))
        self.instructions1 = self.instructFont.render(\
        """W = Jump | S = Slide | A = Left | D = Right""", 1, (255, 255, 255))
        self.instructions2 = self.instructFont.render(\
        "<-- = Turn to Left Lane | --> = Turn to Right Lane", 1,\
        (255, 255, 255))
        self.backButton = self.normFont.render("Back", 1, (255, 255, 255))
        
        self.lzrs = []
        self.lzrShift = 1 # movement of cloud
        
        self.pathWidth = self.width // 2 #1000 width
        #self.pathHeight = self.height // 4 #600 height
        
        self.heroWidth = self.pathWidth // 10
        self.heroHeight = int(self.heroWidth * 1.5)
        self.heroX = self.width // 2 - self.heroWidth // 2
        self.heroY = self.height * 5 / 6
        self.hero = pygame.transform.scale(pygame.image.load\
            ("gameplayImages/motorcycle.png").convert_alpha(), (self.heroWidth,\
        self.heroHeight))
        self.heroSideShift = self.pathWidth // 5
        self.mInterval = self.width // 2 - self.heroWidth // 2
        self.lInterval = self.mInterval - self.heroSideShift
        self.rInterval = self.mInterval + self.heroSideShift
        self.runningSpeed = 10
        self.strafeSpeed = self.heroSideShift // 4
        self.strafeGoal = 0
        self.strafingL = False
        self.strafingR = False
        self.pathSideMove = 20
        
        # the view coordinates are the camera angle
        self.viewX = self.width / 2 # x coordinate
        self.viewY = self.height * 4 / 5 # y coordinate
        self.focalDepth = self.height * 2
        self.focalPoint = [self.width / 2, 0]
        self.z0Prop = 0.8 # proportion of Y we see at z = 0
        
        self.prisms = []
        self.prisms2d = []
        self.prismDepth = 50
        self.prismsNum = self.focalDepth // self.prismDepth + 1
        self.baseThickX = 50
        self.baseThickY = 100
        self.randThickX = 1
        self.randThickY = 2
        self.prismColor = (0, 0, 255)
    
    def mousePressed(self, x, y):
        if(self.mode == "title"):
            titleMousePressed(self, x, y)
        elif(self.mode == "instructions"):
            instructMousePressed(self, x, y)
    
    def mouseReleased(self, x, y):
        pass
        
    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass
    
    def keyPressed(self, keyCode, modifier):
        if(keyCode == 27): # pressed esc at any time brings back to start
            self.init()
        
        if(self.mode == "gameplay"):
            gameplayKeyPressed(self, keyCode, modifier)
        self._keys[keyCode] = True

    def keyReleased(self, keyCode, modifier):
        self._keys[keyCode] = False

    def timerFired(self, dt):
        if(self.mode == "title" or self.mode == "instructions"):
            menuTimerFired(self, dt)
        elif(self.mode == "gameplay"):
            gameplayTimerFired(self, dt)

    def redrawAll(self, screen):
        if(self.mode == "title"):
            titleRedrawAll(self, screen)
        elif(self.mode == "instructions"):
            instructionsRedrawAll(self, screen)
        elif(self.mode == "gameplay"):
            gameplayRedrawAll(self, screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        print("Game Start")
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
        
        print("Game Quit!")
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
