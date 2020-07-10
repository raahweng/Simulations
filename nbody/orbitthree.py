import numpy as np
import scipy.constants
import time
import pygame
from pygame.color import *

n = 30
t = 0.05
t_theta = 0.01
G = scipy.constants.gravitational_constant

m = np.random.uniform(100, 100000, n)
m[0] = 100000000000000000
m[1] = 100000000000000000
m[2] = 100000000000000000
r = np.random.uniform(-200, 200, (n,2))
r[0] = [0,-173]
r[1] = [-200,173]
r[2] = [200,173]
v = np.random.uniform(-150,150, (n,2))
v[0] = [50,0]
v[1] = [-50,0]
v[2] = [50,0]
theta = 0
rhist = np.zeros((15,n,2))
for i in range(15):
    rhist[i] = r

def grav(a,b, ma,mb):
    rab = np.linalg.norm(b-a)
    rabhat= (b-a)/rab
    return (-G*ma*mb*rabhat)/(rab**2)

def step(r, v, n):
    global rhist, theta
    F = np.zeros((n,2))
    for i in range(n):
        Ftemp = np.zeros(2)
        for j,k in enumerate(r):
            if np.array_equal(k, r[i]):
                pass
            else:
                Ftemp += grav(r[i], k, m[i], m[j])
        F[i] = Ftemp
    v = (m[:, np.newaxis]*v-F*t)/m[:, np.newaxis]
    r += v*t
    rhist = np.roll(rhist,n*2)
    rhist[0] = r

    v[0][0] = 50*np.cos(theta)
    v[0][1] = 50*np.sin(theta)
    v[1][0] = -50*np.cos(theta)
    v[1][1] = -50*np.sin(theta)

    theta += t_theta
    
    return r,v

pygame.init()
dispWidth, dispHeight = 800,800
disp = pygame.display.set_mode((dispWidth,dispHeight))
white = (0,0,0)
colours = ["red", "green", "blue", "orange", "purple", "white", "grey"]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)
    r,v = step(r,v,n)
    pygame.draw.circle(disp, THECOLORS["yellow"], (400+int(r[0][0]),400+int(r[0][1])), 30)
    pygame.draw.circle(disp, THECOLORS["yellow"], (400+int(r[1][0]),400+int(r[1][1])), 30)
    for i in range(2,n):
        trail = [(j[0]+400,j[1]+400) for j in rhist[:,i,:]]
        pygame.draw.circle(disp, THECOLORS[colours[i%7]], (400+int(r[i][0]),400+int(r[i][1])), 7)
        pygame.draw.lines(disp, THECOLORS[colours[i%7]], False, trail)
    pygame.display.update()
    



