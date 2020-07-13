import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate
import pygame

#Stuff to change
l = 8*np.pi
def f(t):
    return t*np.sin(t)
k = 0.5
boundary = "neumann"
fourier_n = 100
timestep = 0.1
h = 0.01
interval = 1

def c(n):
    if boundary == "dirichlet":
        return (2/l) * scipy.integrate.quad(lambda t: f(t)*np.sin((n*np.pi*t/l)), 0, l, args=(), full_output=0, epsabs=1.49e-8, epsrel=1.49e-8, limit=10000)[0]
    if boundary == "neumann":
        return (2/l) * scipy.integrate.quad(lambda t: f(t)*np.cos((n*np.pi*t/l)), 0, l, args=(), full_output=0, epsabs=1.49e-8, epsrel=1.49e-8, limit=10000)[0]
constants = np.zeros(fourier_n+1)
for i in range(1,fourier_n+1):
    constants[i] = c(i)
    
def heat(t):
    y = np.zeros(np.shape(x))
    for i in range(1,fourier_n+1):
        if boundary == "dirichlet":
            y += constants[i]*np.sin((np.pi*i*x)/l)*np.exp(-k*t*((i*np.pi)/l)**2)
        if boundary == "neumann":
            y += constants[i]*np.cos((np.pi*i*x)/l)*np.exp(-k*t*((i*np.pi)/l)**2)
    return y
                                                      
pygame.init()
displayWidth = 1000
displayHeight = 400
disp = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
running = True
t = 0

x = np.arange(0, l, h)
tempbound = (np.amin(heat(0)), np.amax(heat(0)))

def colour(n):
    c = (n-tempbound[0])/(tempbound[1]-tempbound[0])*310
    if c < 155:
        return (c+100,c+100,255)
    elif c >= 155:
        return (255,410-c,410-c)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)
    pygame.draw.rect(disp, black, (93,145,812,110))
    for i,j in enumerate(heat(t)):
        pygame.draw.rect(disp, colour(j), (100+i/int(l/h)*800, 150, 1/int(l/h), 100))
    pygame.display.update()
    t += timestep
    

