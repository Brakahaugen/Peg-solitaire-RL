from hexgames.hexGrid import HexGrid
from hexgames.cell import Cell
from hexgames.visualization import GameLoop
import playable
import random
import numpy as np
import time
import math


class SimWorld:
    def __init__(self, size, type, visualization, winReward, loseReward, initialPosition):
        self.hexGrid = HexGrid(size, type)
        self.size = size
        self.type = type
        self.winReward = winReward
        self.loseReward = loseReward
        self.initialPosition = initialPosition

        self.visualizationOn = visualization
        if self.visualizationOn:
            self.gameLoop = GameLoop(self.hexGrid, self)
        self.length = self.getLength()
        
        self.resetGame()


    def resetGame(self):
        self.maxActions = 0
        self.isFinished = False
        self.pegCount = None
        self.hexGrid = HexGrid(self.size, self.type)

        self.hexGrid.grid[self.initialPosition[0], self.initialPosition[1]].detachPin()

        """"
            Random detacher
        """
        # x = random.randrange(0, self.size - 1)
        # y = random.randrange(0, self.size - 1)
        # if self.type == "triangle":
        #     if x == 0:
        #         y = 0
        #     else: 
        #         y = random.randrange(0,x)
        # self.hexGrid.grid[x,y].detachPin()


        if self.visualizationOn:
            self.gameLoop.reset(self.hexGrid)


    def updateGame(self, action, policy_val):
        #Action is a jump from pin1 to pin to. [(x,y), (x,y)]
        if action != None:
            pin1 = self.hexGrid.grid[action[0][0], action[0][1]] 
            pin2 = self.hexGrid.grid[action[1][0], action[1][1]] 
            x = pin2.getX() - pin1.getX()
            y = pin2.getY() - pin1.getY()
            newPin = self.hexGrid.grid[pin2.getX() + x, pin2.getY() + y]

            if self.visualizationOn:
                self.gameLoop.updateGame(pin1,pin2, newPin, policy_val)
            self.jumpOver(pin1,pin2)
            self.isFinished = self.checkGameFinished()
            if self.isFinished:
                return self.createReward()        
        return 0
    

    def jumpOver(self, pin1, pin2):
        if not pin1.hasNeighbour(pin2):
            return "NEIGHBOUR"
        if pin1.isEmpty():
            return "EMPTY"
        elif pin2.isEmpty():
            return "EMPTY"
        x = pin2.getX() - pin1.getX()
        y = pin2.getY() - pin1.getY()
    
        newPin = None
        if pin2.getX() + x < self.size and pin2.getX() + x >= 0 and pin2.getY() + y < self.size and pin2.getY() + y >= 0:
            newPin = self.hexGrid.grid[pin2.getX() + x, pin2.getY() + y]

        if newPin != None:
            if newPin.isEmpty():
                newPin.attachPin()
                pin1.detachPin()
                pin2.detachPin()
                return "SUCCESS"
        return "EMPTY"


    def createSimpleState(self):
        #Creates a binary string, where each digit maps to a specific cell on the board.
        #Returns the int representing that string
        state = ""
        for x in range(0, self.hexGrid.grid.shape[0]):
            for y in range(0, self.hexGrid.grid.shape[1]):
                if self.hexGrid.grid[x,y] != None:
                    state += str(int(not self.hexGrid.grid[x,y].isEmpty()))
        return int(state, 2)
    

    def getSimpleStateActions(self, state):
        #State is a binary string where each position maps to a cell
        for i in range(len(state)):
            x = math.floor(i/self.size)
            y = i


    def ableToJumpOver(self, pin1, pin2):
        if not pin1.hasNeighbour(pin2):
            return "NEIGHBOUR"

        if pin1.isEmpty():
            return "EMPTY"
        elif pin2.isEmpty():
            return "EMPTY"
        x = pin2.getX() - pin1.getX()
        y = pin2.getY() - pin1.getY()
        newPin = None
        if pin2.getX() + x < self.size and pin2.getX() + x >= 0 and pin2.getY() + y < self.size and pin2.getY() + y >= 0:
            newPin = self.hexGrid.grid[pin2.getX() + x, pin2.getY() + y]

        if newPin != None:
            if newPin.isEmpty():
                return "SUCCESS"
        return "EMPTY"

    def getValidActions(self):
        actions = []        

        for x0 in range(0, self.hexGrid.grid.shape[0]):
            for y0 in range(0, self.hexGrid.grid.shape[1]):
                if self.hexGrid.grid[x0,y0] != None:
                    for x1 in range(0, self.hexGrid.grid.shape[0]):
                        for y1 in range(0, self.hexGrid.grid.shape[1]):
                            if self.hexGrid.grid[x1,y1] != None or (x0 == x1 and y0 == y1):
                                if self.ableToJumpOver(self.hexGrid.grid[x0,y0], self.hexGrid.grid[x1, y1]) == "SUCCESS":
                                    # print(self.ableToJumpOver(self.hexGrid.grid[x0,y0], self.hexGrid.grid[x1, y1]))
                                    # print(self.jumpOver(self.hexGrid.grid[x0,y0], self.hexGrid.grid[x1, y1]))

                                    actions.append([[x0, y0], [x1,y1]])
        if len(actions) > self.maxActions:
            self.maxActions = len(actions)
        return actions
    
    def checkGameFinished(self):
        if len(self.getValidActions()) == 0:
            count = 0
            for x in range(0, self.hexGrid.grid.shape[0]):
                for y in range(0, self.hexGrid.grid.shape[1]):
                    if self.hexGrid.grid[x,y] != None: 
                        count += int(not self.hexGrid.grid[x,y].isEmpty())
            self.pegCount = count
            return True
            #Kan også returnere count
        return False
    
    def createReward(self):
        if self.pegCount == 1:
            return self.winReward
        else:
            return self.loseReward


    def getLength(self):
        length = 0
        if self.type == "triangle":
            for i in range(self.size):
                length += i + 1
        else:
            length = self.size**2
        return length

if __name__ == "__main__":
    s = SimWorld(5, "triangle")
    print(s.length)