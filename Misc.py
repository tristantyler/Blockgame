import random

from Blocks import BlockSet, mapDict
from Chunk import findChunk
from Settings import globDict


def removeBlock(gameobj, x, y):
    try:
        ind = gameobj.poslist[y][x]
    except:
        return

    if gameobj.blocksetlist[ind].blockType != "empty":
        chunk = findChunk(gameobj, x, y)
        try:
            i = gameobj.chunklist[chunk].pl.index(ind)
        except:
            return

        gameobj.blocksetlist[ind] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"], 1, "empty")
        gameobj.chunklist[chunk].bl.pop(i)
        gameobj.chunklist[chunk].pl.pop(i)
        gameobj.chunklist[chunk].rl.pop(i)


def Animation(gameobj, x, y, images):
    try:
        ind = gameobj.poslist[y][x]
    except:
        return

    chunk = findChunk(gameobj, x, y)

    if gameobj.blocksetlist[ind].blockType == "empty":
        gameobj.blocksetlist[ind] = BlockSet(x * mapDict["GRID_SIZE"], y * mapDict["GRID_SIZE"],
                                             globDict["size"], "animation")
        gameobj.blocksetlist[ind].images = images
        gameobj.blocksetlist[ind].image = gameobj.blocksetlist[ind].images[0]
        gameobj.blocksetlist[ind].indexMax = len(images) - 1
        gameobj.chunklist[chunk].bl.append(gameobj.blocksetlist[ind])
        gameobj.chunklist[chunk].pl.append(ind)
        gameobj.chunklist[chunk].rl.append(gameobj.blocksetlist[ind].rect)

        gameobj.fxlist.append([x, y])


def checkAnimation(gameobj, x, y):
    try:
        ind = gameobj.poslist[y][x]
    except:
        return False

    if gameobj.blocksetlist[ind].done:
        removeBlock(gameobj, x, y)
        return True
    else:
        return False


def random_block_color():
    r = random.randint(0, 100)
    g = random.randint(0, 100)
    b = random.randint(200, 255)
    rgbl = [r, g, b]
    return tuple(rgbl)
