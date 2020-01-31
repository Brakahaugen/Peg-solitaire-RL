import pygame
import random
import sys
import math
import numpy as np

# define a main function
def GameLoop(hexGrid, simWorld):

        
    pygame.init()

    WIDTH = 800
    HEIGHT = 600
    HOLE_RADIUS = int(250/hexGrid.grid.shape[0])
    circles = []
    circlesToPins = {}
    pinsToCircles = {}
    print("sef")
    selectedCircle = None
    print("Hey")
    if hexGrid.type == "triangle":
        for i in range (hexGrid.grid.shape[0]):
                for j in range (i+1):
                    cell = hexGrid.grid[i,j]
                    circle = (int((2*(j-i) + hexGrid.grid.shape[0] + i)*(WIDTH/(hexGrid.grid.shape[0]*2))), int((2*i+1)*(HEIGHT / (hexGrid.grid.shape[0]*2))))
                    circlesToPins[circle] = cell
                    pinsToCircles[cell] = circle
                    circles.append(circle)
    else: 
        for i in range (hexGrid.grid.shape[0]):
            for j in range (hexGrid.grid.shape[0]):
                cell = hexGrid.grid[i,j]
                circle = [int(0.5*(i+1)*HEIGHT/hexGrid.grid.shape[0]), int(0.5*(j+1)*WIDTH/hexGrid.grid.shape[0])]
                # circle = circle * np.matrix('0.70710678118 -0.70710678118; 0.70710678118 0.70710678118')
                # circle = (circle.item((0, 0)), circle.item((0, 1)))
                # print(circle[1])
                circle = (int(circle[0]), int(circle[1]))
                circlesToPins[circle] = cell
                pinsToCircles[cell] = circle
                circles.append(circle)







    RED = (255,0,0)
    BLUE = (0,0,255)
    YELLOW = (159,32,200)
    GREY = (30, 30, 30)
    BACKGROUND_COLOR = (240,240,180)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game_over = False

    clock = pygame.time.Clock()

    myFont = pygame.font.SysFont("monospace", 35)

    def drawGrid(grid):
        for circle in circles:
            # print(circle)
            # print(selectedCircle)
            # if circle[0] == selectedCircle[0] and circle[1] == selectedCircle[1]:
            if circle == selectedCircle:
                pygame.draw.circle(screen, RED, circle, HOLE_RADIUS)
            elif circlesToPins[circle].isEmpty():
                pygame.draw.circle(screen, GREY, circle, HOLE_RADIUS)
            else:
                pygame.draw.circle(screen, BLUE, circle, HOLE_RADIUS)
                


    def detectMouse():
        x0 = pygame.mouse.get_pos()[0]
        y0 = pygame.mouse.get_pos()[1]
        for circle in circles:
            x = circle[0]
            y = circle[1]
            if (math.sqrt((x0-x)**2 + (y0-y)**2) < HOLE_RADIUS):
                if circle != selectedCircle:
                    pygame.draw.circle(screen, YELLOW, circle, HOLE_RADIUS)
                return circle

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if selectedCircle != None:
                    print(selectedCircle)
                    secondCircle = detectMouse()
                    if secondCircle != None and secondCircle != selectedCircle:
                        actionResult = simWorld.jumpOver(circlesToPins[selectedCircle], circlesToPins[secondCircle])
                        print(actionResult)
                        #Do something with result
                        if actionResult == "SUCCESS":
                            print("Great success")
                            # circles.remove(selectedCircle)
                            # circles.remove(secondCircle)
                            # circles.append(pinsToCircles[actionResult])
                            selectedCircle = None
                            secondCircle = None
                        else: 
                            print("Nope")
                            selectedCircle = None
                            secondCircle = None

                    else:
                        selectedCircle = None
                        secondCircle = None
                else: 
                    selectedCircle = detectMouse()

        screen.fill(BACKGROUND_COLOR)        
        drawGrid(hexGrid.grid)
        detectMouse()

        clock.tick(30)

        pygame.display.update()


