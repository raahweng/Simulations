import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm

nx = 31
ny = 31
dx = 2/(nx-1)
dy = 2/(ny-1)
x = np.linspace(0,2,nx)
y = np.linspace(0,1,ny)
X,Y = np.meshgrid(x,y)
p = np.zeros((nx,ny))
p[0,:], p[-1,:], p[:,0], p[:,1] = 0, 0, 0, 0
b = np.zeros((nx,ny))
b[int(nx/4),int(ny/4)] = 100
b[int(3*nx/4),int(3*ny/4)] = -100

def update():
    pn = p
    p[1:-1,1:-1] = ((dy**2) * (pn[2:nx,1:-1]+pn[0:-2,1:-1]) + ((dx**2)*(pn[1:-1,2:ny]+pn[1:-1,0:-2])) - b[1:-1,1:-1]*(dx**2)*(dy**2)) / (2*(dx**2 + dy**2))
    p[0,:], p[-1,:], p[:,0], p[:,1] = 0, 0, 0, 0
    return p

def animate(i, plot):
    plt.cla()
    update()
    plot = [ax.plot_surface(X, Y, p[:], cmap=cm.plasma, vmin=-0.5, vmax=0.5)]
    ax.set_zlim(-0.5, 0.5)

fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(x, y)  
plot = [ax.plot_surface(X, Y, p[:], cmap=cm.plasma)]
ani = animation.FuncAnimation(fig, animate, fargs=(plot), interval=1)
plt.show()
