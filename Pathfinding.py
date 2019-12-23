import math
import time


class PathFinder:
    def __init__(self, start, goal, ):
        self.closedSet = []
        self.goal = goal
        self.start = start
        self.start.previous = None

        self.openSet = [self.start]
        self.start.h = self.heuristic(self.start, self.goal)

        self.lastChecked = self.start

        self.startTime = time.time()
        self.currentTime = None

        self.closest = 1

    def heuristic(self, a, b):
        relx = a.x - b.x
        rely = a.y - b.y
        dist = math.hypot(relx, rely)
        return dist

    def step(self, gameobj):
        if len(self.openSet) > 0:
            winner = 0

            for i, os in enumerate(self.openSet):
                if os.f < self.openSet[winner].f:
                    winner = i
                if os.f == self.openSet[winner].f:
                    if os.g > self.openSet[winner].g:
                        winner = i

            current = self.openSet[winner]
            self.lastChecked = current
            if self.closest == 1 or self.closest.h > current.h:
                self.closest = current
            elif (self.currentTime - self.startTime) <= 0.1:
                pass
            else:
                self.clear()
                return self.closest

            self.currentTime = time.time()

            if current.pos == self.goal.pos:
                self.clear()
                return current
            if self.currentTime - self.startTime >= 1:
                self.clear()
                return self.closest

            self.openSet.remove(current)
            self.closedSet.append(current)

            neighbors = current.getNeighbors(gameobj)

            for neighbor in neighbors:
                if neighbor not in self.closedSet:
                    tempG = current.g + self.heuristic(neighbor, current)

                    if neighbor not in self.openSet:
                        self.openSet.append(neighbor)
                    elif tempG >= neighbor.g:
                        continue

                    neighbor.g = tempG
                    neighbor.h = self.heuristic(neighbor, self.goal)

                    neighbor.f = neighbor.g + neighbor.h * 50  # change the last number to improve speed, but increase path length
                    neighbor.previous = current

            return 0
        self.clear()
        return self.closest

    def clear(self):
        for set in self.openSet:
            set.clearNeighbors()
        for set in self.closedSet:
            set.clearNeighbors()
