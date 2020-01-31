import pygame
import random
import sys
import math
import numpy as np

# define a main function
class GameLoop:
    def __init__(self, hexGrid, simWorld):
        self.simWorld = simWorld
        self.hexGrid = hexGrid

            
        pygame.init()
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (159,32,200)
        self.GREY = (30, 30, 30)
        self.BACKGROUND_COLOR = (240,240,180)
        self.WIDTH = 800
        self.HEIGHT = 600
        self.HOLE_RADIUS = int(250/hexGrid.grid.shape[0])
        self.circles = []
        self.circlesToPins = {}
        self.pinsToCircles = {}
        self.selectedCircle = None
        self.goneCircle = None
        self.newCircle = None
        self.toggleX = self.WIDTH - 100
        self.toggleY = 100
        self.toggleColor = self.YELLOW
        self.toggle = False

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.game_over = False

        self.myFont = pygame.font.SysFont("monospace", 35)

        self.reset(self.hexGrid)

    def drawGrid(self, grid):
        for circle in self.circles:
            # print(circle)
            # print(selectedCircle)
            # if circle[0] == selectedCircle[0] and circle[1] == selectedCircle[1]:
            if circle == self.selectedCircle:
                pygame.draw.circle(self.screen, self.RED, circle, self.HOLE_RADIUS)
            elif self.circlesToPins[circle].isEmpty():
                pygame.draw.circle(self.screen, self.GREY, circle, self.HOLE_RADIUS)
            elif circle == self.goneCircle:
                pygame.draw.circle(self.screen, self.YELLOW, circle, self.HOLE_RADIUS)
            else:
                pygame.draw.circle(self.screen, self.BLUE, circle, self.HOLE_RADIUS)
    
    def detectMouse(self):
        x0 = pygame.mouse.get_pos()[0]
        y0 = pygame.mouse.get_pos()[1]
        x = self.toggleX
        y = self.toggleY
        if (math.sqrt((x0-x)**2 + (y0-y)**2) < self.HOLE_RADIUS):
            self.toggle = not self.toggle
            if self.toggle:
                self.toggleColor = self.GREY
            else:
                self.toggleColor = self.YELLOW
            self.screen.fill(self.BACKGROUND_COLOR)        
            self.drawGrid(self.hexGrid.grid)
            pygame.draw.circle(self.screen, self.toggleColor, (self.toggleX, self.toggleY), self.HOLE_RADIUS)
            pygame.display.update()

    def reset(self, hexGrid):
        self.hexGrid = hexGrid
        if hexGrid.type == "triangle":
            for i in range (hexGrid.grid.shape[0]):
                    for j in range (i+1):
                        cell = hexGrid.grid[i,j]
                        circle = (int((2*(j-i) + hexGrid.grid.shape[0] + i)*(self.WIDTH/(hexGrid.grid.shape[0]*2))), int((2*i+1)*(self.HEIGHT / (hexGrid.grid.shape[0]*2))))
                        self.circlesToPins[circle] = cell
                        self.pinsToCircles[cell] = circle
                        self.circles.append(circle)
        else: 
            for i in range (hexGrid.grid.shape[0]):
                for j in range (hexGrid.grid.shape[0]):
                    cell = hexGrid.grid[i,j]
                    circle = [int(0.5*(i+1)*self.HEIGHT/hexGrid.grid.shape[0]), int(0.5*(j+1)*self.WIDTH/hexGrid.grid.shape[0])]
                    # circle = circle * np.matrix('0.70710678118 -0.70710678118; 0.70710678118 0.70710678118')
                    # circle = (circle.item((0, 0)), circle.item((0, 1)))
                    # print(circle[1])
                    circle = (int(circle[0]), int(circle[1]))
                    self.circlesToPins[circle] = cell
                    self.pinsToCircles[cell] = circle
                    self.circles.append(circle)


    def updateGame(self, startPin, jumpPin, newPin):

        i = 0
        max = 30
        self.selectedCircle = None
        self.goneCircle =None
        while i < max:
            i += 1   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.detectMouse()
            if self.toggle:
                continue

            if i > max/4:
                self.selectedCircle = self.pinsToCircles[startPin]
            if i > max/2:
                self.selectedCircle = self.pinsToCircles[newPin]
                self.goneCircle = self.pinsToCircles[startPin]

            self.screen.fill(self.BACKGROUND_COLOR)        
            self.drawGrid(self.hexGrid.grid)
            pygame.draw.circle(self.screen, self.toggleColor, (self.toggleX, self.toggleY), self.HOLE_RADIUS)
            pygame.display.update()


