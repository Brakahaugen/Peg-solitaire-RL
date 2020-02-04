import sys
import numpy as np
from hexgames.cell import Cell

class HexGrid:
    def __init__(self, size, type):
        self.size = size
        self.type = type
        self.grid = np.ndarray(shape=(size, size), dtype=Cell)
        self.createBoard()



    def createBoard(self):
        #Initiate the boardgrid and the cells
        if self.type == "diamond":
            self.createDiamondBoard()
        else:
            self.createTriangleBoard()

    def createTriangleBoard(self):
        for i in range(self.size):
            for j in range(i+1):
                self.grid[i,j] = Cell(i,j)

        #Create the neighbouring arrays of each internal cell for cheaper computations later
        triangleHexNeighbours = [[-1,-1],[-1,0],[0,-1],[0,1],[1,0],[1,1]]
        for i in range(self.size):
            for j in range(i+1):
                self.grid[i, j].addNeighbours(triangleHexNeighbours, self.grid, self.size)

    def createDiamondBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i,j] = Cell(i,j)

        #Create the neighbouring arrays of each cell for cheaper computations later
        diamondHexNeighbours = [[-1,0],[-1,1],[0,1],[0,-1],[1,-1],[1,0]]
        
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i, j].addNeighbours(diamondHexNeighbours, self.grid, self.size)
    
    def getJumpResult(self, cell1, cell2):
        i = cell1.x + 2*(cell2.x-cell1.x)
        j = cell1.y + 2*(cell2.y-cell1.y)
        if i < self.size and i >= 0 and j < self.size and j >= 0:
            return self.grid[i,j]
        else:
            return False