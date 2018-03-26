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
        
        self.titleLabel = self.titleFont.render("112 Runner", 1, (0, 0, 0))
        self.instructLabel = self.titleFont.render("Instructions", 1, (0, 0, 0))
        
        self.playButton = self.normFont.render("Play", 1, (0, 0, 0))
        self.instructButton = self.normFont.render("Instructions", 1, (0, 0, 0))
        self.instructions1 = self.instructFont.render(\
        """W = Jump | S = Slide | A = Left | D = Right""", 1, (0, 0, 0))
        self.instructions2 = self.instructFont.render(\
        "<-- = Turn to Left Lane | --> = Turn to Right Lane", 1, (0, 0, 0))
        self.backButton = self.normFont.render("Back", 1, (0, 0, 0))
        
        self.clouds = []
        self.cloudShift = 1 # movement of cloud
        
        self.pathWidth = self.width // 2 #1000 width
        self.pathHeight = self.height // 4
        
        self.heroWidth = self.pathWidth // 4
        self.heroHeight = self.pathHeight // 2
        self.heroX = self.width // 2 - self.heroWidth // 2
        self.heroY = self.height * 5 / 6
        self.hero = []
        self.runningSpeed = 10
        
        self.viewX = self.width / 2 # x coordinate
        #self.viewY = self.height / 2 # y coordinate
        self.viewDepth = self.width # this is the z coordinate of depth
        self.focalP = (self.width / 2, 0, 0) # always 1.0 of height
        self.focalHeight = self.height
        
        self.prisms = []
    
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

    def __init__(self, width=1000, height=600, fps=50, title="112 Pygame Game"):
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
