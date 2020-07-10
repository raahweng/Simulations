import numpy as np
import matplotlib.pyplot as plt
import pygame
import time

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3
    
    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:  ,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:  ,1:  ].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]  )) * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]  )) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

x = 64

def update(grid):
    ngrid = grid
    for i in range(x):
        for j in range(x):
            if i == 0 and j == 0:
                ngrid[i][j] = (grid[i+1][j] + grid[i][j+1] + grid[i+1][j+1] + grid[i][j])/4
            elif i == x-1 and j == x-1:
                ngrid[i][j] = (grid[i-1][j] + grid[i][j-1] + grid[i-1][j-1] + grid[i][j])/4
            elif i == 0 and j == x-1:
                ngrid[i][j] = (grid[i][j-1] + grid[i+1][j-1] + grid[i+1][j] + grid[i][j])/4
            elif i == x-1 and j == 0:
                ngrid[i][j] = (grid[i-1][j] + grid[i][j+1] + grid[i-1][j+1] + grid[i][j])/4
            elif i == 0:
                ngrid[i][j] = (grid[i][j-1] + grid[i+1][j-1] + grid[i+1][j] + grid[i][j+1] + grid[i+1][j+1] + grid[i][j])/6
            elif i == x-1:
                ngrid[i][j] = (grid[i-1][j-1] + grid[i-1][j] + grid[i-1][j+1] + grid[i][j-1] + grid[i][j+1] + grid[i][j])/6
            elif j == 0:
                ngrid[i][j] = (grid[i-1][j] + grid[i+1][j] + grid[i-1][j+1] + grid[i][j+1] + grid[i+1][j+1] + grid[i][j])/6
            elif j == x-1:
                ngrid[i][j] = (grid[i-1][j] + grid[i+1][j] + grid[i-1][j-1] + grid[i][j-1] + grid[i+1][j-1] + grid[i][j])/6
            else:
                ngrid[i][j] = (grid[i-1][j-1] + grid[i-1][j] + grid[i-1][j+1] + grid[i][j-1] + grid[i][j] + grid[i][j+1] + grid[i+1][j-1] + grid[i+1][j] + grid[i+1][j+1])/9
    return ngrid

def colour(n):
    if n < 155:
        return (n+100,n+100,255)
    elif n >= 155:
        return (255,410-n,410-n)

pygame.init()
dispWidth, dispHeight = 768,768
disp = pygame.display.set_mode((dispWidth,dispHeight))
running = True
res = 4
noise = generate_perlin_noise_2d((x, x), (res,res))
noise = (noise+1)/2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    noise = update(noise)
    for i in range(x):
        for j in range(x):
            c = noise[i][j] * 255
            pygame.draw.rect(disp, colour(noise[i][j] * 310), (i*(dispWidth/x),j*(dispHeight/x),dispWidth/x,dispWidth/x))
    pygame.display.update()



                               
