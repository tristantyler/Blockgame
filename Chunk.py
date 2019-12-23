from Settings import mapDict


class Chunk:

    def __init__(self, size):
        self.bl = []
        self.rl = []
        self.pl = []
        self.neighbors = []
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0
        self.size = size


def findChunk(gameobj, px, py):
    l = gameobj.chunklist[0].size - 1
    if py >= mapDict["YMAX_GRID"] - l:
        py = mapDict["YMAX_GRID"] - l
    elif py < 0:
        py = 1

    if px >= mapDict["XMAX_GRID"] - l:
        px = mapDict["XMAX_GRID"] - l
    elif px < 0:
        px = 1

    chunknum = 0
    for chunk in gameobj.chunklist:
        if chunk.xstart <= px <= chunk.xend and chunk.ystart <= py <= chunk.yend:
            break
        chunknum += 1
    else:
        print("Couldn't find it")

    return chunknum


def getChunks(gameobj):
    gameobj.chunklist.clear()
    chunksize = int(((mapDict["SCREEN_WIDTH"] / mapDict["GRID_SIZE"]) / 9) + 2)
    cw = int(mapDict["XMAX_GRID"] / chunksize)
    ch = int(mapDict["YMAX_GRID"] / chunksize)
    for i in range(cw):
        for j in range(ch):
            chk = Chunk(chunksize)
            chk.ystart = i * chunksize
            chk.xstart = j * chunksize

            chk.yend = (i * chunksize + chunksize) - 1
            chk.xend = (j * chunksize + chunksize) - 1
            for y in range(i * chunksize, i * chunksize + chunksize):
                for x in range(j * chunksize, j * chunksize + chunksize):
                    ind = gameobj.poslist[y][x]
                    if gameobj.blocksetlist[ind].blockType != "empty":
                        chk.bl.append(gameobj.blocksetlist[ind])
                        chk.pl.append(ind)
                        chk.rl.append(gameobj.blocksetlist[ind].rect)
            gameobj.chunklist.append(chk)

    mat = [[] for _ in range(cw)]
    count = 0
    for i in range(cw):
        for j in range(ch):
            mat[i].append(count)
            count += 1
    print(count, "Total Chunks,", "Chunks are size", chunksize)

    # Size of "board"
    X = ch - 1
    Y = cw - 1

    neighbors = lambda x, y, radx, rady: [mat[x2][y2] for x2 in range(x - radx, x + radx + 1)
                                          for y2 in range(y - rady, y + rady + 1)
                                          if (-1 < x <= X and
                                              -1 < y <= Y and
                                              (x != x2 or y != y2) and
                                              (0 <= x2 <= X) and
                                              (0 <= y2 <= Y))]

    count = 0
    for i in range(cw):
        for j in range(ch):
            gameobj.chunklist[count].neighbors = neighbors(i, j, 3, 4)
            count += 1
