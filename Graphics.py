from Blocks import *
from Misc import removeBlock
from NPC import NPC
from Chunk import *
from Towers import *
from Misc import Animation


def draw(gameobj):
    chunkDraw(gameobj)
    uiList = updateUIText(gameobj)

    background.fill((17, 14, 33))
    background.blit(bg.image, gameobj.camera.apply(bg))
    # Draws the players and any active projectiles
    [background.blit(gameobj.player.bulletList[r].image, gameobj.camera.apply(gameobj.player.bulletList[r])) for r in
     range(len(gameobj.player.bulletList))]
    background.blit(gameobj.player.image, gameobj.camera.apply(gameobj.player))
    # Draws every block in drawlist(i.e the viewsize area)
    [background.blit(gameobj.drawlist[i].image, gameobj.camera.apply(gameobj.drawlist[i])) and gameobj.drawlist[
        i].update() for i in
     range(len(gameobj.drawlist))]

    for elt in uiList:
        elt.draw(background)

    # Draws any entity/npcs to the background
    for ent in gameobj.entlist:
        background.blit(ent.image, gameobj.camera.apply(ent))

    # Draws the cursor image and sets it at the current mouse pos
    cursorRect.center = pygame.mouse.get_pos()
    background.blit(cursorImage, cursorRect)

    # Blits the whole background as one image to the screen
    screen.blit(background, (0, 0))


def chunkDraw(gameobj):
    if len(gameobj.chunklist) > 0:
        px = int(gameobj.player.pos.x / mapDict["GRID_SIZE"])
        py = int(gameobj.player.pos.y / mapDict["GRID_SIZE"])

        chunknum = findChunk(gameobj, px, py)

        gameobj.drawlist = []
        gameobj.drawrect = []

        gameobj.drawlist += gameobj.chunklist[chunknum].bl
        gameobj.drawrect += gameobj.chunklist[chunknum].rl

        for i in gameobj.chunklist[chunknum].neighbors:
            gameobj.drawlist += gameobj.chunklist[i].bl
            gameobj.drawrect += gameobj.chunklist[i].rl


def buildMap(gameobj):
    start_time = time.time()

    gameobj.buildPositionList()
    gameobj.buildBlockListMap()

    print("Took", time.time() - start_time, "secs to build")


def eraseMap(gameobj):
    start_time = time.time()

    gameobj.buildBlockListEmpty()

    print("Took", time.time() - start_time, "secs to erase")


def updateUIText(gameobj):
    playerposbox = TextBox(mapDict["SCREEN_WIDTH"] - 120, 0, 120, 22, (
            "X:" + str(int(gameobj.player.pos.x / mapDict["GRID_SIZE"])) +
            "  Y:" + str(int((gameobj.player.pos.y / mapDict["GRID_SIZE"])))))
    buildtypebox = TextBox(int(mapDict["SCREEN_WIDTH"] / 2) - 60, 0, 120, 22, (globDict["blockbuild"]))
    gameobj.fpsbox = TextBox(0, 0, 40, 20, str(int(clock.get_fps())))

    lst = [playerposbox, gameobj.fpsbox, buildtypebox]
    return lst


def mouseChunkBuild(gameobj):
    tempx, tempy = pygame.mouse.get_pos()

    mousex = int(
        ((tempx + gameobj.player.pos.x) - mapDict["HALF_WIDTH"]) / mapDict["GRID_SIZE"])  # convert to grid system
    mousey = int(
        ((tempy + gameobj.player.pos.y) - mapDict["HALF_HEIGHT"]) / mapDict["GRID_SIZE"])  # convert to grid system

    try:
        ind = gameobj.poslist[mousey][mousex]
    except:
        return

    chunk = findChunk(gameobj, mousex, mousey)

    if gameobj.blocksetlist[ind].blockType == "empty":
        if globDict["blockbuild"].lower() == "block":
            gameobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"],
                                                 globDict["size"], "block")
            gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
            gameobj.chunklist[chunk].pl.append(ind)
            gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)
        elif globDict["blockbuild"].lower() == "npc":
            temp = NPC(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"], 1, "npc", gameobj.player,
                       globDict["vrange"])
            gameobj.entlist.append(temp)

            gameobj.mousestate[1] = False
            return
        elif globDict["blockbuild"].lower() == "point":
            gameobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"], .5,
                                                 "point")
            gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
            gameobj.chunklist[chunk].pl.append(ind)
            gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)
        elif globDict["blockbuild"].lower() == "tower":
            gameobj.blocksetlist[ind] = Tower(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"], 1, "tower",
                                              gameobj.player,
                                              globDict["vrange"])
            gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
            gameobj.chunklist[chunk].pl.append(ind)
            gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)
        elif globDict["blockbuild"].lower() == "invincible":
            gameobj.blocksetlist[ind] = BlockSet(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"], 1,
                                                 "invincible")
            gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
            gameobj.chunklist[chunk].pl.append(ind)
            gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)
        elif globDict["blockbuild"].lower() == "respawn tower":
            gameobj.blocksetlist[ind] = RespawnTower(mousex * mapDict["GRID_SIZE"], mousey * mapDict["GRID_SIZE"], 1,
                                                     "respawntower", gameobj.player)
            gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
            gameobj.chunklist[chunk].pl.append(ind)
            gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)


def mouseChunkKill(gameobj):
    tempx, tempy = pygame.mouse.get_pos()

    mousex = int(
        ((tempx + gameobj.player.pos.x) - mapDict["HALF_WIDTH"]) / mapDict["GRID_SIZE"])  # convert to grid system
    mousey = int(
        ((tempy + gameobj.player.pos.y) - mapDict["HALF_HEIGHT"]) / mapDict["GRID_SIZE"])  # convert to grid system

    try:
        ind = gameobj.poslist[mousey][mousex]
    except:
        return

    if gameobj.blocksetlist[ind].blockType not in ("empty", "animation"):
        removeBlock(gameobj, mousex, mousey)
        Animation(gameobj, mousex, mousey, explimages)


class TextBox:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (220, 220, 0)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.bkground = pygame.Surface((w, h))
        self.bkground.fill((0, 0, 0))

    def draw(self, screen):
        self.bkground.blit(self.txt_surface, (2, -3))
        screen.blit(self.bkground, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
