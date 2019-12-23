import pygame

from Graphics import mouseChunkBuild, mouseChunkKill, findChunk, buildMap, eraseMap
from Settings import globDict, mapDict, shipImage

vec = pygame.math.Vector2


def initInputVars():
    keystate = []

    keystate.append(False)  # 0 pressed_right
    keystate.append(False)  # 1 pressed_left
    keystate.append(False)  # 2 pressed_down
    keystate.append(False)  # 3 pressed_up
    keystate.append(False)  # 4 buildmap
    keystate.append(False)  # 5
    keystate.append(False)  # 6
    keystate.append(False)  # 7 clearmap
    keystate.append(False)  # 8
    keystate.append(False)  # 9
    keystate.append(False)  # 10
    keystate.append(False)  # 11 changewidth
    keystate.append(False)  # 12 changeheight
    keystate.append(False)  # 13 colon
    keystate.append(False)  # 14 shoot
    keystate.append(False)  # 15 endgame
    keystate.append(False)  # 16 buildinput

    mousestate = []
    mousestate.append(False)  # 0 mouseKillClick
    mousestate.append(False)  # 1 mouseBuildClick

    print("Initialized KEYSTATE AND MOUSETATE")

    return keystate, mousestate


def inputChecker(gameobj):
    if not gameobj.keystate[11] and not gameobj.keystate[12] and not gameobj.keystate[16]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameobj.close = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    gameobj.keystate[0] = True
                elif event.key == pygame.K_LEFT:
                    gameobj.keystate[1] = True
                elif event.key == pygame.K_DOWN:
                    gameobj.keystate[2] = True
                elif event.key == pygame.K_UP:
                    gameobj.keystate[3] = True
                    if gameobj.keystate[5]:
                        gameobj.player.jump(mapDict["GRID_SIZE"] / 3, gameobj)
                elif event.key == pygame.K_SPACE:
                    gameobj.player.jump(mapDict["GRID_SIZE"] / 3, gameobj)
                elif event.key == pygame.K_LSHIFT:
                    if not gameobj.keystate[14]:
                        gameobj.keystate[14] = True
                        gameobj.player.rof = 29
                elif event.key == pygame.K_TAB:
                    gameobj.keystate[11] = True
                elif event.key == pygame.K_i:
                    if gameobj.keystate[13]:
                        gameobj.keystate[13] = False
                    else:
                        gameobj.keystate[13] = True
                elif event.key == pygame.K_o:
                    if globDict["collisionON"]:
                        print("Collision Turned OFF")
                        gameobj.player.image = pygame.Surface((mapDict["GRID_SIZE"] * 3, mapDict["GRID_SIZE"] * 3))
                        gameobj.player.PLAYER_ACC = mapDict["GRID_SIZE"] * 2
                        gameobj.player.rect.width = mapDict["GRID_SIZE"] * 3
                        gameobj.player.rect.height = mapDict["GRID_SIZE"] * 3
                        gameobj.player.image.fill((156, 91, 34))
                        gameobj.player.pos = vec(gameobj.player.pos.x, gameobj.player.pos.y)
                        gameobj.player.rect.topleft = gameobj.player.pos
                        gameobj.player.onGround = False

                        gameobj.player.collided = False
                        gameobj.player.hitright = False
                        gameobj.player.hitleft = False
                        gameobj.player.hitup = False
                        gameobj.player.hitdown = False
                        gameobj.player.gravity = 0
                        globDict["collisionON"] = False
                        print("Gravity Turned OFF")
                        gameobj.keystate[5] = False
                    else:
                        gameobj.player.image = shipImage
                        gameobj.player.PLAYER_ACC = mapDict["GRID_SIZE"]
                        gameobj.player.rect.width = mapDict["GRID_SIZE"]
                        gameobj.player.rect.height = mapDict["GRID_SIZE"]
                        gameobj.player.pos = vec(gameobj.player.pos.x, gameobj.player.pos.y)
                        gameobj.player.rect.topleft = gameobj.player.pos

                        print("Collision Turned ON")
                        globDict["collisionON"] = True
                elif event.key == pygame.K_u:  # clears out the whole map
                    gameobj.keystate[7] = True
                elif event.key == pygame.K_b:  # builds a whole new map
                    gameobj.keystate[4] = True
                elif event.key == pygame.K_g:
                    if gameobj.keystate[5]:
                        print("Gravity Turned OFF")
                        gameobj.keystate[5] = False
                    else:
                        print("Gravity Turned ON")
                        gameobj.keystate[5] = True
                elif event.key == pygame.K_p:
                    px = int(gameobj.player.pos.x / mapDict["GRID_SIZE"])
                    py = int(gameobj.player.pos.y / mapDict["GRID_SIZE"])

                    chunknum = findChunk(gameobj, px, py)

                    print("Objects:", len(gameobj.drawlist), "Chunk:", chunknum, "PX:", px, "PY:", py)
                elif event.key == pygame.K_LEFTBRACKET:
                    gameobj.player.PLAYER_ACC -= 10
                    if gameobj.player.PLAYER_ACC < 0:
                        gameobj.player.PLAYER_ACC = 0
                elif event.key == pygame.K_RIGHTBRACKET:
                    gameobj.player.PLAYER_ACC += 10
                elif event.key == pygame.K_1:
                    globDict["blockbuild"] = "Block"
                elif event.key == pygame.K_2:
                    globDict["blockbuild"] = "Point"
                elif event.key == pygame.K_3:
                    globDict["blockbuild"] = "Tower"
                elif event.key == pygame.K_4:
                    globDict["blockbuild"] = "Invincible"
                elif event.key == pygame.K_5:
                    globDict["blockbuild"] = "Respawn Tower"
                elif event.key == pygame.K_6:
                    globDict["blockbuild"] = "NPC"
                elif event.key == pygame.K_ESCAPE:
                    gameobj.close = True
                    break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    gameobj.keystate[0] = False
                elif event.key == pygame.K_LEFT:
                    gameobj.keystate[1] = False
                elif event.key == pygame.K_DOWN:
                    gameobj.keystate[2] = False
                elif event.key == pygame.K_UP:
                    gameobj.keystate[3] = False
                elif event.key == pygame.K_LSHIFT:
                    gameobj.keystate[14] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                but1, but2, but3 = pygame.mouse.get_pressed()
                if but3:
                    gameobj.mousestate[1] = True
                if but1:
                    gameobj.mousestate[0] = True
            if event.type == pygame.MOUSEBUTTONUP:
                gameobj.mousestate[0] = False
                if globDict["blockbuild"] != "NPC":
                    gameobj.mousestate[1] = False


def mouseHandler(gameobj):
    if gameobj.mousestate[0]:  # Turns Blocks into emptyBlocks
        mouseChunkKill(gameobj)
    if gameobj.mousestate[1]:  # Turns emptyBlocks into blocks
        mouseChunkBuild(gameobj)


def keystateHandler(gameobj):
    mouseHandler(gameobj)

    if gameobj.keystate[4]:  # fills every possible spot with a block
        buildMap(gameobj)
        gameobj.keystate[4] = False
    elif gameobj.keystate[7]:  # fills every possible spot with an empty block
        eraseMap(gameobj)
        gameobj.keystate[7] = False
