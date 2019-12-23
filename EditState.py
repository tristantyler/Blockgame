from Settings import *
from InputHandle import *
from Graphics import *
from Cameras import *
import GameObject
import main


def loop():
    gameobj = GameObject.GameObject()
    gameobj.startup()

    exiting = False
    while not exiting:

        seconds = (gameobj.endTime - gameobj.start)
        gameobj.start = time.time()

        inputChecker(gameobj)
        if gameobj.keystate[15]:  # End Game
            exiting = True
            main.main()
            break
        keystateHandler(gameobj)

        for box in editboxlist:
            box.update(gameobj)
            if gameobj.keystate[16]:
                textInputChecker(gameobj, box, box.gvar)
                break

        gameobj.player.update(gameobj, seconds)
        for ent in gameobj.entlist:
            ent.update(gameobj)

        if gameobj.mousestate[0] or gameobj.mousestate[1] or len(gameobj.player.bulletList) >= 0:
            enhancedDraw(gameobj)

        gameobj.camera.update(gameobj.player)

        draw(gameobj)

        gameobj.fpsbox = TextBox(0, mapDict["SCREEN_HEIGHT"] - 20, 80, 20, str(int(clock.get_fps())))

        pygame.display.update(screenRect)
        clock.tick()
        gameobj.endTime = time.time()


def keystateHandler(gameobj):
    mouseHandler(gameobj)

    if gameobj.keystate[4]:  # fills every possible spot with a block
        print("building")
        buildMap(gameobj)
        print("Done building")
        gameobj.keystate[4] = False
    elif gameobj.keystate[7]:  # fills every possible spot with an empty block
        eraseMap(gameobj)
        gameobj.loadname = ""
        gameobj.keystate[7] = False
    elif gameobj.keystate[11]:  # Changing the width of the map
        TempX = textInputChecker(gameobj)
        if type(TempX) == int:
            mapDict["XMAX_GRID"] = TempX
        else:
            gameobj.keystate[11] = True
            gameobj.keystate[12] = False
    elif gameobj.keystate[12]:  # changing the height of the map
        TempY = textInputChecker(gameobj)
        if type(TempY) == int:
            mapDict["YMAX_GRID"] = TempY
        else:
            gameobj.keystate[12] = True
