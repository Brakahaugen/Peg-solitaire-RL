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

        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (159,32,200)
        self.GREY = (30, 30, 30)
        self.BACKGROUND_COLOR = (240,240,180)
        self.WIDTH = 600
        self.HEIGHT = 600

        self.HOLE_RADIUS = self.create_hole_radius(simWorld.size, simWorld.type)
        self.LINE_WIDTH = 10
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

            
        pygame.init()
        pygame.font.init() 
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.game_over = False
        self.reset(self.hexGrid)

    def create_hole_radius(self, size, type):
        if type == "triangle":
            return int(250/size)
        else:
            return int(175/size)


    def drawGrid(self, grid):
        visited_circles = []
        for circle in self.circles:
            pin = self.circlesToPins[circle]
            neighbours = pin.getNeighbours()

            for n in neighbours:
                if n not in visited_circles:
                    new_circle = self.pinsToCircles[n]
                    pygame.draw.line(self.screen, self.GREY, circle, new_circle, self.LINE_WIDTH)
            visited_circles.append(circle)
            
        self.drawCircles(grid)

    def drawCircles(self, grid):
        for circle in self.circles:
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

                    circle = (int((self.WIDTH * (self.simWorld.size + j - i)) / (self.simWorld.size*2 - 1) - self.WIDTH/(2*(2*self.simWorld.size - 1))), int((self.HEIGHT * (j + i + 1)) / (self.simWorld.size*2 - 1) - self.HEIGHT/(2*(2*self.simWorld.size - 1))))

                    self.circlesToPins[circle] = cell
                    self.pinsToCircles[cell] = circle
                    self.circles.append(circle)


    def updateGame(self, startPin, jumpPin, newPin, policy_val):

        i = 0
        max = 3
        self.selectedCircle = None
        self.goneCircle =None
        while i < max:
            if not self.toggle:    
                self.clock.tick(max)

            i += 1   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.detectMouse()
            if self.toggle:
                return    

            if i >= max/3:
                self.selectedCircle = self.pinsToCircles[startPin]
            if i >= 2*max/3:
                self.selectedCircle = self.pinsToCircles[newPin]
                self.goneCircle = self.pinsToCircles[startPin]

            self.screen.fill(self.BACKGROUND_COLOR)        
            self.drawGrid(self.hexGrid.grid)
            pygame.draw.circle(self.screen, self.toggleColor, (self.toggleX, self.toggleY), self.HOLE_RADIUS)
            textsurface = self.myfont.render(str(policy_val), False, (0, 0, 0))
            self.screen.blit(textsurface,(15,15))
            pygame.display.update()


