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
        self.instructions1 = self.instructFont.render("W = Jump | S = Nothing", 1, (255, 255, 255))
        self.instructions2 = self.instructFont.render("A = Strafe Left | D = Strafe Right", 1, (255, 255, 255))
        self.instructions3 = self.instructFont.render("<-- = Turn Left | --> = Turn Right", 1, (255, 255, 255))
        self.backButton = self.normFont.render("Back", 1, (255, 255, 255))

        self.gameoverLabel = self.titleFont.render("Game Over", 1, (255, 255, 255))

        self.lzrs = []
        self.lzrShift = 1  # movement of laser background

        self.runningSpeed = 150

        # the view coordinates are the camera angle
        self.viewX = self.width / 2  # x coordinate viewing point
        self.viewY = self.height  # y coordinate viewing point
        self.viewCameraTop = math.pi * 0.5
        self.viewCameraBot = math.pi * 0.33
        self.viewHeight = self.viewCameraTop - self.viewCameraBot
        self.viewCameraLeft = math.pi * 2 / 5
        self.viewCameraRight = math.pi * 3 / 5
        self.viewWidth = self.viewCameraRight - self.viewCameraLeft
        self.depth = self.height * 15
        # self.focalPoint = [self.width / 2, 0]

        self.prisms = []
        self.prismDepth = 400
        self.prismsNum = self.depth // self.prismDepth
        self.prismX = 200
        self.prismY = 50
        self.randThickY = 2
        self.randColorRange = (150, 255)

        self.pathWidth = self.width  # 800 width
        # self.pathHeight = self.height // 4  #600 height

        self.laneNum = 3
        self.laneWidth = self.pathWidth // self.laneNum
        self.heroWidth = self.laneWidth // 2
        self.heroHeight = self.prismY * 2
        self.heroDepth = self.prismDepth // 2
        self.heroTopY = 0
        self.heroZShift = 3  # shift from law of cosine asympotes
        self.heroTopZ = self.prismDepth * self.heroZShift
        self.heroLocs = [0 for i in range(self.laneNum)]
        self.hero = []
        self.heroInvulnerable = False
        self.heroCurrLoc = 0
        self.strafeDirec = 0
        self.heroBlinker = 0
        self.heroVisible = True

        #  variables calculated for top of triangle
        self.x0 = self.viewX - self.pathWidth / 2 + self.heroCurrLoc * self.laneWidth + self.laneWidth // 2
        self.y0 = 0  # remember this is height, since it's 3d
        self.z0 = ((self.prismDepth - self.heroDepth) // 2) + self.heroTopZ

        self.strafeInterval = self.laneWidth // 5  # how fast it strafes per tick
        self.strafeNums = 0
        self.strafing = False

        self.spikes = []
        self.spikesProb = 2
        self.spikeDepth = self.prismDepth
        self.spikeBuffer = 2 * self.spikeDepth
        self.spikesNum = self.prismsNum
        self.spikeX = self.laneWidth
        self.spikeY = 100
        self.prevSpikesAreEmpty = True
        self.spikeDamage = 0.5

        self.jumping = False
        self.jumpingTimer = 0
        self.jumpStrength = self.spikeY * 0.9
        self.gravity = self.spikeY // 20

        self.hp = 1
        self.hpWidth = self.width * 0.6
        self.hpX = self.width // 100
        self.hpHeight = self.height // 10
        self.hpY = self.height // 100

        self.endSlowRatio= 0.97


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
            gameplayKeyPressed(self, keyCode)
        self._keys[keyCode] = True

    def keyReleased(self, keyCode, modifier):
        self._keys[keyCode] = False

    def timerFired(self, dt):
        if self.mode == "title" or self.mode == "instructions":
            menuTimerFired(self, dt)
        elif self.mode == "gameplay" or self.mode == "gameover":
            gameplayTimerFired(self, dt)

    def redrawAll(self, screen):
        if self.mode == "title":
            titleRedrawAll(self, screen)
        elif self.mode == "instructions":
            instructionsRedrawAll(self, screen)
        elif self.mode == "gameplay" or self.mode == "gameover":
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
