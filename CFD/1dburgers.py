import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pi = np.pi
nu = .07
dx = 2*pi/100
dt = dx * nu
x = np.linspace(0,2*pi,101)
t = 0
#u = -2*nu*(-(-8*t + 2*x)*np.exp(-(-4*t + x)**2/(4*nu*(t + 1)))/(4*nu*(t + 1)) - (-8*t + 2*x - 4*pi)*np.exp(-(-4*t + x - 2*pi)**2/(4*nu*(t + 1)))/(4*nu*(t + 1)))/(np.exp(-(-4*t + x - 2*pi)**2/(4*nu*(t + 1))) + np.exp(-(-4*t + x)**2/(4*nu*(t + 1)))) + 4
u = np.exp(-2*(x-3*pi/4)**2)


def update_u():
    global u
    un = u
    for i in range(1,100):
        u[i] = un[i] - un[i]*(dt/dx)*(un[i]-un[i-1])+nu*(dt/(dx**2))*(un[i+1]-2*un[i]+un[i-1])
    u[0] = un[0] - un[0]*(dt/dx)*(un[0]-un[-2])+nu*(dt/(dx**2))*(un[1]-2*un[0]+un[-2])
    u[-1] = u[0]
    return u

fig, ax = plt.subplots()
line, = ax.plot(x,u)

def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def animate(i):
    line.set_ydata(update_u())
    return line,

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=10, blit=True, save_count=50)
plt.show()
