'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
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
        instructSize = self.width // 20

        self.titleFont = pygame.font.SysFont("Comic Sans MS", titleSize)
        self.normFont = pygame.font.SysFont("Comic Sans MS", normSize)
        self.instructFont = pygame.font.SysFont("Comic Sans MS", instructSize)

        self.titleLabel = self.titleFont.render("112 Runner", 1, (255, 255, 255))
        self.instructLabel = self.titleFont.render("Instructions", 1, (255, 255, 255))

        self.playButton = self.normFont.render("Play", 1, (255, 255, 255))
        self.instructButton = self.normFont.render("Instructions", 1, (255, 255, 255))
        self.instructions1 = self.instructFont.render("W = Speed Up | S = Slow Down", 1, (255, 255, 255))
        self.instructions2 = self.instructFont.render("A = Strafe Left | D = Strafe Right", 1, (255, 255, 255))
        self.instructions3 = self.instructFont.render("<-- = Turn Left | --> = Turn Right", 1, (255, 255, 255))
        self.backButton = self.normFont.render("Back", 1, (255, 255, 255))

        self.lzrs = []
        self.lzrShift = 1  # movement of laser background

        self.pathWidth = self.width * 3  # 800 width
        # self.pathHeight = self.height // 4  #600 height

        self.runningSpeed = 30

        # the view coordinates are the camera angle
        self.viewX = self.width / 2  # x coordinate viewing point
        self.viewY = self.height * 4 / 4  # y coordinate viewing point
        self.viewCameraTop = math.pi / 2
        self.viewCameraBot = math.pi / 3
        self.viewHeight = self.viewCameraTop - self.viewCameraBot
        self.viewCameraLeft = math.pi / 6
        self.viewCameraRight = math.pi * 5 / 6
        self.viewWidth = self.viewCameraRight - self.viewCameraLeft
        self.focalDepth = self.height * 15
        # self.focalPoint = [self.width / 2, 0]

        self.prisms = []
        self.prismDepth = 400
        self.prismsNum = self.focalDepth // self.prismDepth
        self.baseThickX = 200
        self.baseThickY = 50
        self.randThickY = 2
        self.randColorRange = (150, 255)

        self.heroWidth = self.pathWidth // 10
        self.heroDepth = self.prismDepth * 3 // 4
        self.heroTopY = 0
        self.heroTopZ = self.prismDepth * 4  # there is hidden shift
        self.heroSides = []
        self.currLocs = [0, 0, 0]  # 0 is path, 1 is spike, 3 lanes to start
        self.heroLocs = [0, 0, 0]
        self.laneNum = len(self.currLocs)
        self.heroCurrLoc = 0
        self.strafeDirec = 0
        self.laneInterval = self.pathWidth // len(self.currLocs)
        self.strafeInterval = self.laneInterval // 5  # how fast it strafes per tick
        self.strafeNums = 0
        self.strafing = False
        #  variables calculated for top of triangle
        self.x0 = self.viewX - self.pathWidth / 2 + self.heroCurrLoc * self.laneInterval + self.laneInterval // 2
        self.y0 = 0  # remember this is height, since it's 3d
        self.z0 = ((self.prismDepth - self.heroDepth) // 2) + self.heroTopZ

    def mousePressed(self, x, y):
        if self.mode == "title":
            titleMousePressed(self, x, y)
        elif self.mode == "instructions":
            instructMousePressed(self, x, y)

    def mouseReleased(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == 27:  # pressed esc at any time brings back to start
            self.init()

        if self.mode == "gameplay":
            gameplayKeyPressed(self, keyCode, modifier)
        self._keys[keyCode] = True

    def keyReleased(self, keyCode, modifier):
        self._keys[keyCode] = False

    def timerFired(self, dt):
        if self.mode == "title" or self.mode == "instructions":
            menuTimerFired(self, dt)
        elif self.mode == "gameplay":
            gameplayTimerFired(self, dt)

    def redrawAll(self, screen):
        if self.mode == "title":
            titleRedrawAll(self, screen)
        elif self.mode == "instructions":
            instructionsRedrawAll(self, screen)
        elif self.mode == "gameplay":
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
                    self.mousePressed(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*event.pos)
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
