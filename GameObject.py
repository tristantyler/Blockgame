from Cameras import *
from Graphics import *
from InputHandle import *
from Misc import checkAnimation
from Players import *
import MapGenerator


class GameObject(object):

    def __init__(self):

        self.keystate, self.mousestate = initInputVars()  # Sets up Mouse/Key States

        self.blocksetlist = []  # Initializes the list for all the blocks, entities, levels
        self.chunklist = []  # contains all the chunks that get generated once the map is built
        self.entlist = []

        self.player = Player()  # Setup a player

        self.poslist = []
        self.buildPositionList()

        self.camera = Camera(simple_camera, mapDict["MAP_WIDTH"], mapDict["MAP_HEIGHT"])
        self.fpsbox = TextBox(0, 0, 80, 20, "")
        self.drawlist = []
        self.drawrect = []

        self.fxlist = []

        self.end = 0
        self.start = time.time()
        self.st = time.time()  # the starting time for total time spent in app
        time.sleep(1)

        buildMap(self)
        draw(self)

        self.close = False

    def update(self):
        self.end = time.time()
        self.player.update(self, self.end - self.start)
        inputChecker(self)
        keystateHandler(self)
        for ent in self.entlist:
            ent.update(self)
        for fx in self.fxlist:
            if checkAnimation(self, fx[0], fx[1]):
                self.fxlist.remove(fx)
        self.camera.update(self.player)
        self.start = time.time()

    def draw(self):
        draw(self)

    def buildPositionList(self):
        self.poslist = [[] for _ in range(mapDict["YMAX_GRID"])]
        coordx = 0
        coordy = 0

        for i in range(mapDict["XMAX_GRID"] * mapDict["YMAX_GRID"]):
            self.poslist[coordy].append(i)
            if coordx == mapDict["XMAX_GRID"] - 1:
                coordx = 0
                coordy += 1
            else:
                coordx += 1

    def buildBlockListMap(self):
        self.blocksetlist = MapGenerator.getMap(mapDict["XMAX_GRID"], mapDict["YMAX_GRID"], random.random(), 32)
        count = 0
        for y in range(mapDict["YMAX_GRID"]):
            for x in range(mapDict["XMAX_GRID"]):
                if self.blocksetlist[count] == 1:
                    self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], 1,
                                                        "block")
                elif random.randint(0, 4) == 1:
                    self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], .5,
                                                        "point")
                else:
                    self.blocksetlist[count] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], 1,
                                                        "empty")
                count += 1
        getChunks(self)

    def buildBlockListEmpty(self):
        self.blocksetlist = [BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], 1, "empty") for y in
                                range(mapDict["YMAX_GRID"]) for x in range(mapDict["XMAX_GRID"])]
        getChunks(self)
