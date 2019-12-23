import random


def getNeighbors(grid, row, col, num=1):
    """Returns a count of all surrounding neighbors that are == to num argument. 8 possible neighbors"""

    count = 0
    if grid[row - 1][col] == num:  # left
        count += 1
    if grid[row + 1][col] == num:  # right
        count += 1
    if grid[row][col - 1] == num:  # up
        count += 1
    if grid[row][col + 1] == num:  # down
        count += 1

    if grid[row - 1][col - 1] == num:  # left up
        count += 1
    if grid[row + 1][col - 1] == num:  # right up
        count += 1
    if grid[row - 1][col + 1] == num:  # left down
        count += 1
    if grid[row + 1][col + 1] == num:  # right down
        count += 1

    if count > 4:
        grid[row][col] = num


def smooth(grid, num=1, check=0):
    """Smooths out grid. Checks each specified check # and decides whether to change it to the num
       argument if it doesn't have the required number of neighbors"""
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] == check:
                getNeighbors(grid, i, j, num)

    return grid


def genMapFromSeed(rows, columns, seed="seed", fillrate=55):
    """Generates a grid from a random seed, can specify rows, columns, seed, fill rate"""
    grid = [[] for _ in range(columns)]

    random.seed(seed)

    # Fills grid with a 1 or 0 based on assigned fill rate
    [[(i.append(1)) if((random.randint(0, 100)) < fillrate) else (i.append(0)) for _ in range(rows)] for i in grid]

    for i in range(rows):
        # Fill top and bottom rows
        grid[0][i] = 1
        grid[len(grid) - 2][i] = 1

    for i in range(columns):
        grid[i][0] = 1
        grid[i][len(grid[0]) - 1] = 1

    return grid


def generateMap(grid):
    """Runs the smooth operations"""

    changes = 0

    while changes < 6:
        grid = smooth(grid)
        grid = smooth(grid, 0, 1)
        changes += 1

    return grid


def display(grid):
    """Takes a grid and displays it replacing 0's with # and 1's with ."""
    for r in grid:
        ts = ""  # String for each row in the grid
        for i in r:
            ts += str(i) + " "
        ts = ts.replace("0", "#")
        ts = ts.replace("1", ".")
        print(ts)


def getMap(rows, columns, seed="rand", fillrate=55):
    seedmap = genMapFromSeed(rows, columns, seed, fillrate)
    grid = generateMap(seedmap)
    grid = [j for sub in grid for j in sub]

    return grid
