import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

l = 1
n = 1500
dx = l/n
dt = 0.0005
c = 1

x = np.zeros((n))

#x[0:int(0.15*n)] = np.sin(2*np.pi/0.3*np.linspace(0,0.15,int(0.15*n)))

#x = np.sin(6*np.pi*np.linspace(0,l,n))

x[0:int(0.15*n)] = np.sin(2*np.pi/0.3*np.linspace(0,0.15,int(0.15*n)))
x[-int(0.15*n):] = np.sin(2*np.pi/0.3*np.linspace(0,0.15,int(0.15*n)))

#x[0:int(0.15*n)] = np.ones(int(0.15*n))

xold = x

def update():
    global x, xold

    xnew = np.zeros((n))
    xnew[1:-1] = (c*dt/dx)**2 * (x[2:] - 2*x[1:-1] + x[:-2]) + 2*x[1:-1] - xold[1:-1]
    xold = x
    x = xnew



fig, ax = plt.subplots()
line, = ax.plot(np.linspace(0,l,n), x)
ax.set_ylim(-1,1)


def animate(i):
    for i in range(15):
        update()
    line.set_ydata(x)
    return line,

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
plt.show()
