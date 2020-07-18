import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

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

h = 0.015

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

hist1 = np.zeros((3,10000))
for i in range(10000):
    hist1[:,i] = state
    state = rungekutta()

state = np.array([x,y,z])
a = 10.1
hist2 = np.zeros((3,10000))
for i in range(10000):
    hist2[:,i] = state
    state = rungekutta()


def update_lines(num, dataLines, lines) :
    for line, data in zip(lines, dataLines) :
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2,:num])
    return lines

fig = plt.figure()
ax = p3.Axes3D(fig)
data = np.zeros((2,3,10000))
data[0,:,:] = hist1
data[1,:,:] = hist2
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]
ax.set_xlim3d([-20, 20])
ax.set_ylim3d([-20, 30])
ax.set_zlim3d([0, 50])

line_ani = animation.FuncAnimation(fig, update_lines, fargs=(data, lines),
                              interval=1, blit=False)

plt.show()



        

        
    


    
