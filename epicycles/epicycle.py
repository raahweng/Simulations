import numpy as np
import matplotlib.pyplot as plt
import pygame
import operator
from functools import reduce


m = 100
N = 2*m+1
P = 2*m
pi = np.pi
x = np.zeros(N)
y = np.zeros(N)

x[0:int(N/4)] = np.linspace(-1,1,int(N/4))
x[int(N/4):int(N/2)] = np.ones(int(N/4))
x[int(N/2):int(3*N/4)] = np.linspace(1,-1,int(N/4))
x[int(3*N/4):-1] = - np.ones(int(N/4))

y[0:int(N/4)] = np.ones(int(N/4))
y[int(N/4):int(N/2)] = np.linspace(1,-1,int(N/4))
y[int(N/2):int(3*N/4)] = -np.ones(int(N/4))
y[int(3*N/4):-1] = np.linspace(-1,1,int(N/4))

p = x + y*1.0j
p[-1] = -1 + 1.0j


fig,ax = plt.subplots()
ax.scatter(p.real,p.imag)
plt.show()

coeff = np.zeros((N)) + np.zeros((N))*1.0j
for k in range(-m,m+1):
    for n,x in enumerate(p):
        coeff[k+m] += x * np.exp(-2*pi*1.0j*k*(n-m)/N)

pygame.init()
dispWidth, dispHeight = 800,800
disp = pygame.display.set_mode((dispWidth,dispHeight))
white = (255,255,255)
black = (0,0,0)
running = True

grid = 2
def coord(c):
    return (int(dispWidth/(2*grid) * (c[0] + grid)), int(dispHeight/(2*grid) * (c[1] + grid)))

t = 0
points = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add()
    disp.fill(white)

    start = (0,0)
    for k in reduce(operator.add, zip(range(m,2*m+1),range(m-1,-1, -1))):
        temp = (start[0] + np.abs(coeff[k])*np.cos((k-m)*t - np.angle(coeff[k]))/N, start[1] + np.abs(coeff[k])*np.sin((k-m)*t - np.angle(coeff[k]))/N)
        pygame.draw.line(disp, black, coord(start), coord(temp))
        r = int(dispWidth/(2*grid) * (np.abs(coeff[k])/N))
        if r > 1:
            pygame.draw.circle(disp, (0,255,255), coord(start), r, 1)
        start = temp

    if len(points) <= 1500:
        points.append(coord(start))
    if len(points) > 2:
        pygame.draw.lines(disp, (255,0,0), False, points, 2)

    t += 0.005
    pygame.display.update()
