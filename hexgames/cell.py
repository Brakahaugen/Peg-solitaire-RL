import math

class Cell:
    def __init__(self, x,y):
        self.x, self.y = x, y
        self.empty = False   
        self.neighbours = []


    #  Function for adding neighbours for all cells in the grid,
    #  based on a list of defining connectivity in the neighbourhood
    #  This way to do it does not scale very well.
    def addNeighbours(self, hexNeighbours, grid, size):
        for n in hexNeighbours:
            if self.x+n[0] >= 0 and self.x+n[0] < size and self.y+n[1] >= 0 and self.y+n[1] < size:
                c = grid[self.x+n[0], self.y+n[1]]
                if not self.neighbours.__contains__(c):
                    if c != None:
                        self.neighbours.append(c)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def hasNeighbour(self, cell):
        if self.neighbours.__contains__(cell):
            return True
        else:
            return False

    def getNeighbours(self):
        return self.neighbours

    def detachPin(self):
        self.empty = True

    def attachPin(self):
        self.empty = False

    def isEmpty(self):
        return self.empty
        
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) +  ")" + str(self.empty)
