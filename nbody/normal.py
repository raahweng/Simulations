import numpy as np
import scipy.constants
import time
import pygame
from pygame.color import *

n = 30
t = 0.01
G = scipy.constants.gravitational_constant
m = np.random.uniform(10000000, 10000000000000000, n)
r = np.random.uniform(-200, 200, (n,2))
v = np.random.uniform(-50,50, (n,2))
traillength = 20
rhist = np.zeros((traillength,n,2))
for i in range(traillength):
    rhist[i] = r

def grav(a,b, ma,mb):
    rab = np.linalg.norm(b-a)
    rabhat= (b-a)/rab
    return (-G*ma*mb*rabhat)/(rab**2)

def step(r, v, n):
    global rhist
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
##    for i in range(n):
##        if r[i][0]+400 > 793 or r[i][0]+400 < 7:
##            v[i][0] *= -0.9
##        if r[i][1]+400 > 793 or r[i][1]+400 < 7:
##            v[i][1] *= -0.9
    rhist = np.roll(rhist,n*2)
    rhist[0] = r
    return r,v

pygame.init()
dispWidth, dispHeight = 800,800
disp = pygame.display.set_mode((dispWidth,dispHeight))
white = (255,255,255)
colours = ["red", "green", "blue", "orange", "purple", "black", "grey"]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)
    r,v = step(r,v,n)
    for i in range(0,n):
        trail = [(j[0]+400,j[1]+400) for j in rhist[:,i,:]]
        pygame.draw.circle(disp, THECOLORS[colours[i%7]], (400+int(r[i][0]),400+int(r[i][1])), 7)
        pygame.draw.lines(disp, THECOLORS[colours[i%7]], False, trail)
    pygame.display.update()
    



