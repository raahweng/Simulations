#draw with mouse, enter to render, space to reset

import numpy as np
import pygame

n = 300
dx = 1/n
dt = 0.0005
c = 1

pygame.init()
displayWidth = 1200
displayHeight = 500
disp = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
drawing = False
render = False
running = True

x = np.zeros((n))
xold = x

def update():
    global x, xold

    xnew = np.zeros((n))
    xnew[1:-1] = (c*dt/dx)**2 * (x[2:] - 2*x[1:-1] + x[:-2]) + 2*x[1:-1] - xold[1:-1]
    xold = x
    x = xnew

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                buttons = pygame.mouse.get_pressed()
                
                if buttons[0] == True:
                    drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                render = False
                x = np.zeros((n))
                xold = x
            
            elif event.key == pygame.K_RETURN:
                render = True

    if render == False:

        if drawing == True:
            mx,my = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if mx > 105 and mx < 1090:
                x[round(((mx-100)/1000)*n)] = (my-250)/250
    
    else:
        update()



    disp.fill(white)
    pygame.draw.lines(disp, black, False, [(100 + i*dx*1000, 250 + j*200) for i,j in enumerate(x)], width=5)
    pygame.draw.circle(disp, black, (97,250), 6)
    pygame.draw.circle(disp, black, (1100,250), 6)

    pygame.display.update()
