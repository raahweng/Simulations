import numpy as np
import matplotlib, pygame
import matplotlib.pyplot as plt

g = 9.8
m = 100000000
l = 0.5
t1 = np.pi/2
t2 = np.pi/2
p1 = 0
p2 = 0
dt1, dt2, dp1, dp2 = 1,1,1,1

state = np.array([t1,t2,p1,p2])

def dtheta1(state):
    return (6/(m*l**2)) * (2*state[2] - 3*np.cos(state[0]-state[1])*state[3])/(16-9*np.cos(state[0]-state[1])**2)

def dtheta2(state):
    return (6/(m*l**2)) * (8*state[3] - 3*np.cos(state[0]-state[1])*state[2])/(16-9*np.cos(state[0]-state[1])**2)

def dmomentum1(state, dt1, dt2):
    return ((-1/2)*m*l**2)*(dt1*dt2*np.sin(state[0]-state[1])+3*(g/l)*np.sin(state[0]))

def dmomentum2(state, dt1, dt2):
    return ((-1/2)*m*l**2)*(-dt1*dt2*np.sin(state[0]-state[1])+(g/l)*np.sin(state[1]))

h = 0.01

def grad(state):
    gradstate = [dtheta1(state),dtheta2(state)]
    gradstate.append(dmomentum1(state, gradstate[0], gradstate[1]))
    gradstate.append(dmomentum2(state, gradstate[0], gradstate[1]))
    return np.array(gradstate)

def y1(state):
    return h*grad(state)

def y2(state, k1):
    return h*grad(state+0.5*k1)

def y3(state, k2):
    return h*grad(state+0.5*k2)

def y4(state, k3):
    return h*grad(state+k3)

def rungekutta():
    k1 = y1(state)
    k2 = y2(state, k1)
    k3 = y3(state, k2)
    k4 = y4(state, k3)
    return state + 1/6 * (k1+2*k2+2*k3+k4)


##hist = np.zeros((1000,4))
##for i in range(1000):
##    hist[i,:] = state
##    state = rungekutta()
##plt.plot(hist[:,0])



pygame.init()
displayWidth = 800
displayHeight = 800
disp = pygame.display.set_mode((displayWidth,displayHeight))
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
blue = (0,76,153)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    disp.fill(white)
    state = rungekutta()
    b1 = (int(150*np.sin(state[0])+400),int(150*np.cos(state[0])+400))
    b2 = (int(150*np.sin(state[1])+b1[0]),int(150*np.cos(state[1])+b1[1]))
    pygame.draw.line(disp, black, b1, b2, 3)
    pygame.draw.line(disp, black, (400,400), b1, 3)
    pygame.draw.circle(disp, blue, b2, 10)
    pygame.draw.circle(disp, blue, b1, 10)
    pygame.display.update()
    clock.tick(100)
    
    




        

        
    


    
