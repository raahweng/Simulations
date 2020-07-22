import numpy as np
import matplotlib, pygame
import matplotlib.pyplot as plt

a = 10
b = 28
c = 8/3
x,y,z = 1,1,1
state = np.array([x,y,z])

def dx(state):
    return a*(state[1]-state[0])

def dy(state):
    return state[0]*(b-state[2])-state[1]

def dz(state):
    return state[0]*state[1] - c*state[2]

h = 0.005

def grad(state):
    return np.array([dx(state), dy(state), dz(state)])

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

hist = np.zeros((10000,3))
for i in range(10000):
    hist[i] = state
    state = rungekutta()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(hist[:,0], hist[:,1], hist[:,2])

a=10.1
x,y,z = 1,1,1
hist = np.zeros((10000,3))
for i in range(10000):
    hist[i] = state
    state = rungekutta()
ax.plot(hist[:,0], hist[:,1], hist[:,2])

plt.show()




    
    




        

        
    


    
