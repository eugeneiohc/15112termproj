'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
# this is the main file
from pygame.locals import *

from menuscreen import *
from gameplay import *


class PygameGame(object):
    def init(self):
        self.mode = "title"
        self.lzrs = []
        self.lzrShift = 2  # movement of laser background

        titleSize = self.width // 8
        normSize = self.width // 14
        instructSize = self.width // 20
        scoreSize = self.width // 30
        optionsSize = self.width // 48

        self.titleFont = pygame.font.SysFont("Comic Sans MS", titleSize)
        self.normFont = pygame.font.SysFont("Comic Sans MS", normSize)
        self.instructFont = pygame.font.SysFont("Comic Sans MS", instructSize)
        self.scoreFont = pygame.font.SysFont("Comic Sans MS", scoreSize)
        self.optionsFont = pygame.font.SysFont("Comic Sans MS", optionsSize)

        self.titleLabel = self.titleFont.render("112 Runner", 1, (255, 255, 0))
        self.instructLabel = self.titleFont.render("Instructions", 1, (255, 255, 0))
        self.scoreboardLabel = self.titleFont.render("Leaderboard", 1, (255, 255, 0))
        self.optionsLabel = self.titleFont.render("Options", 1, (255, 255, 0))
        self.optionsInstructLabel = self.instructFont.render("Select Options Below!", 1,
                                                             (255, 255, 0))
        self.speedLabel = self.instructFont.render("Hero Speed", 1, (255, 255, 0))
        self.healthLabel = self.instructFont.render("Hero Health", 1, (255, 255, 0))
        self.spikeLabel = self.instructFont.render("Spike Rate", 1, (255, 255, 0))
        self.laneLabel = self.instructFont.render("Lane Number", 1, (255, 255, 0))

        self.playButton = self.normFont.render("Play", 1, (255, 255, 0))
        self.instructButton = self.normFont.render("Instructions", 1, (255, 255, 0))
        self.scoreboardButton = self.normFont.render("Leaderboard", 1, (255, 255, 0))
        self.optionsButton = self.normFont.render("Options", 1, (255, 255, 0))
        self.instructions1 = self.instructFont.render("W = Jump", 1, (255, 255, 0))
        self.instructions2 = self.instructFont.render("A = Strafe Left | D = Strafe Right", 1, (255, 255, 0))
        self.instructions3 = self.instructFont.render("<-- = Turn to Left | --> = Turn to Right", 1, (255, 255, 0))
        self.gameoverLabel = self.titleFont.render("Game Over", 1, (0, 0, 0))
        self.enterNameLabel = self.instructFont.render("Press 'Enter' to submit your High Score!", 1, (0, 0, 0))
        self.backToMenuLabel = self.instructFont.render("Press 'Esc' to go back to the menu", 1, (0, 0, 0))
        self.typeNameLabel = self.instructFont.render("Press 'Enter' to submit your score!", 1, (0, 0, 0))
        options, choices = 4, 4
        self.options = [[[None, False] for i in range(choices)] for j in range(options)]
        self.options[0][0] = [self.optionsFont.render("Snail x0.1", 1, (255, 255, 0)), False, 0.1]
        self.options[0][1] = [self.optionsFont.render("Dog x1.0", 1, (255, 255, 0)), True, 1]
        self.options[0][2] = [self.optionsFont.render("Cheetah x1.5", 1, (255, 255, 0)), False, 1.5]
        self.options[0][3] = [self.optionsFont.render("Sonic x4", 1, (255, 255, 0)), False, 4]
        self.options[1][0] = [self.optionsFont.render("Elephant x0.5", 1, (255, 255, 0)), False, 0.5]
        self.options[1][1] = [self.optionsFont.render("Bull x1.0", 1, (255, 255, 0)), True, 1]
        self.options[1][2] = [self.optionsFont.render("Human x1.5", 1, (255, 255, 0)), False, 1.5]
        self.options[1][3] = [self.optionsFont.render("Ant x6", 1, (255, 255, 0)), False, 6]
        self.options[2][0] = [self.optionsFont.render("Desert x0.75", 1, (255, 255, 0)), False, 0.75]
        self.options[2][1] = [self.optionsFont.render("Plains x1.0", 1, (255, 255, 0)), True, 1]
        self.options[2][2] = [self.optionsFont.render("Forest x1.5", 1, (255, 255, 0)), False, 1.5]
        self.options[2][3] = [self.optionsFont.render("Uncrossable x3", 1, (255, 255, 0)), False, 3]
        self.options[3][0] = [self.optionsFont.render("Cruising x0.5", 1, (255, 255, 0)), False, 0.5]
        self.options[3][1] = [self.optionsFont.render("Average x1.0", 1, (255, 255, 0)), True, 1]
        self.options[3][2] = [self.optionsFont.render("Tense x1.5", 1, (255, 255, 0)), False, 1.5]
        self.options[3][3] = [self.optionsFont.render("Finger God x3", 1, (255, 255, 0)), False, 3]

        self.backButton = self.normFont.render("Back", 1, (255, 255, 0))

        self.runningSpeed = 100
        self.spikeDamage = 0.1
        self.spikesProb = 24
        self.laneNum = 5
        self.scoreMultiplier = 1

    def musicInit(self):
        self.titleMusic = pygame.mixer.Sound("sounds/title.ogg")
        self.helloKittyMusic = pygame.mixer.Sound("sounds/hellokitty.ogg")
        self.helloKittyMusic.set_volume(0.5)
        self.lolYouDiedMusic = pygame.mixer.Sound("sounds/lolyoudied.ogg")
        self.jumpSound = pygame.mixer.Sound("sounds/jump.ogg")
        self.collisionSound = pygame.mixer.Sound("sounds/collision.ogg")
        self.titleMusic.play(1)

    def gameplayInit(self):
        # the view coordinates are the camera angle
        self.viewX = self.width / 2  # x coordinate viewing point
        self.viewY = self.height  # y coordinate viewing point
        self.viewCameraTop = math.pi * 0.5
        self.viewCameraBot = math.pi * 0.35
        self.viewHeight = self.viewCameraTop - self.viewCameraBot
        self.viewCameraLeft = math.pi * 0.4
        self.viewCameraRight = math.pi * 0.6
        self.viewWidth = self.viewCameraRight - self.viewCameraLeft
        self.depth = self.height * 14
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
        self.laneWidth = self.pathWidth // self.laneNum
        self.heroWidth = self.laneWidth // 2
        self.heroHeight = self.prismY * 2
        self.heroDepth = self.prismDepth // 2
        self.heroTopY = 0
        self.heroZShift = 4  # shift from law of cosine asympotes
        self.heroTopZ = self.prismDepth * self.heroZShift
        self.heroLocs = [0 for i in range(self.laneNum)]
        self.hero = []
        self.heroInvulnerable = False
        self.heroCurrLoc = 0
        self.strafeDirec = 0
        self.heroVisible = True
        self.heroBlinker = 0

        #  variables calculated for top of triangle
        self.x0 = self.viewX - self.pathWidth / 2 + self.laneWidth // 2
        self.y0 = 0  # remember this is height, since it's 3d
        self.z0 = ((self.prismDepth - self.heroDepth) // 2) + self.heroTopZ
        self.turningX = self.viewX
        self.turningZ = self.z0

        self.strafeInterval = self.laneWidth // 5  # how fast it strafes per tick
        self.strafeNums = 0
        self.strafing = False

        self.spikes = []
        self.spikeDepth = self.prismDepth
        self.spikeBuffer = 3 * self.spikeDepth
        self.spikesNum = self.prismsNum
        self.spikeX = self.laneWidth
        self.spikeY = 100
        self.prevSpikesAreEmpty = True

        self.lastZ = 0
        self.notCreatedLane = False
        self.turnChance = 40
        self.approachingTurn = False
        self.turning = False
        self.turningAmount = math.pi / 8
        self.amountTurned = 0
        self.turningDirection = ""

        self.jumping = False
        self.jumpingTimer = 0
        self.jumpStrength = self.spikeY * 0.85
        self.gravity = self.spikeY // 20

        self.timer = 0

        self.hp = 1
        self.hpWidth = self.width * 0.3
        self.hpX = self.width // 15
        self.hpHeight = self.height // 15
        self.hpY = self.height // 30
        self.score = 0
        self.scoreIncrement = 100
        self.scoreX = self.width * 0.75
        self.scoreY = self.height * 0.06

        self.gameoverTimer = 50

        self.endSlowRatio = 0.9

        self.name = ""

    def mousePressed(self, x, y):
        if self.mode == "title":
            titleMousePressed(self, x, y)
        elif self.mode == "instructions":
            instructMousePressed(self, x, y)
        elif self.mode == "scoreboard":
            scoreboardMousePressed(self, x, y)
        elif self.mode == "options":
            optionsMousePressed(self, x, y)

    def mouseReleased(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == 27:  # pressed esc at any time brings back to start
            self.mode = "title"
            self.runningSpeed = 100
            self.gameplayInit()
            pygame.mixer.stop()
            self.titleMusic.play()
        if self.mode == "gameplay" or self.mode == "gameover" or self.mode == "scoreenter":
            gameplayKeyPressed(self, keyCode)
        self._keys[keyCode] = True

    def keyReleased(self, keyCode, modifier):
        self._keys[keyCode] = False

    def timerFired(self, dt):
        if self.mode == "title" or self.mode == "instructions" or self.mode == "scoreboard" or self.mode == "options":
            menuTimerFired(self, dt)
        elif self.mode == "gameplay" or self.mode == "gameover" or self.mode == "scoreenter":
            gameplayTimerFired(self, dt)

    def redrawAll(self, screen):
        if self.mode == "title":
            titleRedrawAll(self, screen)
        elif self.mode == "instructions":
            instructionsRedrawAll(self, screen)
        elif self.mode == "scoreboard":
            scoreboardRedrawAll(self, screen)
        elif self.mode == "options":
            optionsRedrawAll(self, screen)
        elif self.mode == "gameplay" or self.mode == "gameover" or self.mode == "scoreenter":
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
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        self.musicInit()

    def run(self):
        clock = pygame.time.Clock()
        flags = DOUBLEBUF
        screen = pygame.display.set_mode((self.width, self.height), flags)
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
