from Blocks import BlockSet, Block
from Towers import *
import pickle
from NPC import *


def save(gameobj):
    gameobj.blocklist = []
    for block in gameobj.blocksetlist:
        tempBlock = Block(block.x, block.y, block.size, block.blockType)
        if tempBlock.blockType == "tower":
            tempBlock.rofMax = block.rofMax
            tempBlock.range = block.range
        gameobj.blocklist.append(tempBlock)

    tempEntList = [(EmptyNPC(ent.startX, ent.startY, ent.size, ent.blockType, ent.range, ent.rofMax)) for ent in
                   gameobj.entlist]
    name = "levels/%s.lvl" % gameobj.savename

    print(name)
    with open(name, "wb") as file:
        pickle.dump((gameobj.blocklist, tempEntList, mapDict["XMAX_GRID"], mapDict["YMAX_GRID"], gameobj.player.pos.x,
                     gameobj.player.pos.y, globDict["scoregoal"]), file)


def load(gameobj):
    print("LOADING....")
    name = "levels/%s.lvl" % gameobj.loadname
    print(name)

    with open(name, "rb")as file:
        gameobj.blocklist, tempEntList, XMG, YMG, startX, startY, SG = pickle.load(file)

    gameobj.blocksetlist.clear()
    gameobj.poslist.clear()
    gameobj.entlist.clear()
    gameobj.entlist = []

    gameobj.player.startPos.x = startX
    gameobj.player.startPos.y = startY
    mapDict["XMAX_GRID"] = XMG
    mapDict["YMAX_GRID"] = YMG
    globDict["scoregoal"] = SG

    mapDict["MAP_WIDTH"] = mapDict["GRID_SIZE"] * mapDict["XMAX_GRID"]
    mapDict["MAP_HEIGHT"] = mapDict["GRID_SIZE"] * mapDict["YMAX_GRID"]

    coordx = 0
    coordy = 0

    gameobj.poslist = [[] for p in range(mapDict["YMAX_GRID"])]

    for i in range(mapDict["XMAX_GRID"] * mapDict["YMAX_GRID"]):
        gameobj.poslist[coordy].append(i)
        if coordx == mapDict["XMAX_GRID"] - 1:
            coordx = 0
            coordy += 1
        else:
            coordx += 1

    for block in gameobj.blocklist:
        if block.blockType == "tower":
            setblock = Tower(block.x, block.y, block.size, block.blockType, gameobj.player, block.range)
            setblock.rofMax = block.rofMax
        elif block.blockType == "respawntower":
            setblock = RespawnTower(block.x, block.y, block.size, block.blockType, gameobj.player)
        elif block.blockType == "end":
            setblock = EndTower(block.x, block.y, block.size, block.blockType, gameobj.player)
        else:
            setblock = BlockSet(block.x, block.y, block.size, block.blockType)
        gameobj.blocksetlist.append(setblock)
    del gameobj.blocklist

    for ent in tempEntList:
        setent = NPC(ent.x, ent.y, ent.size, ent.blockType, gameobj.player, ent.range)
        setent.rofMax = ent.rofMax
        gameobj.entlist.append(setent)
    del tempEntList
