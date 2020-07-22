import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import cm

nx = 41
ny = 41
nt = 120
c = 1
dx = 2/(nx - 1)
dy = 2/(ny - 1)
sigma = 0.05
nu = 0.01
dt = (sigma*dx*dy)/nu
x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)
X, Y = np.meshgrid(x, y)  
u = np.zeros((nx,ny))
v = np.zeros((nx,ny))
u = np.exp(-(2*X-1)**2 - (2*Y-1)**2)
v = u


def update():
    un = u
    vn = v
    u[1:-1,1:-1] = un[1:-1,1:-1] - (dt/dx)*un[1:-1,1:-1]*(un[1:-1,1:-1]-un[0:-2,1:-1]) - (dt/dy)*vn[1:-1,1:-1]*(un[1:-1,1:-1]-un[1:-1,0:-2]) + (nu*dt/dx**2)*(un[2:nx,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1]) + (nu*dt/dy**2)*(un[1:-1,2:nx]-2*un[1:-1,1:-1]+un[1:-1,0:-2])
    v[1:-1,1:-1] = vn[1:-1,1:-1] - (dt/dx)*un[1:-1,1:-1]*(vn[1:-1,1:-1]-vn[0:-2,1:-1]) - (dt/dy)*vn[1:-1,1:-1]*(vn[1:-1,1:-1]-vn[1:-1,0:-2]) + (nu*dt/dx**2)*(vn[2:nx,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1]) + (nu*dt/dy**2)*(vn[1:-1,2:nx]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2])
    u[0, :],u[-1, :],u[:, 0],u[:, -1],v[0, :],v[-1, :],v[:, 0],v[:, -1] = 0,0,0,0,0,0,0,0
    return u,v

def animate(i, plot):
    plt.cla()
    update()
    plot = [ax.plot_surface(X, Y, v[:], cmap=cm.viridis, vmin=0, vmax=1)]
    ax.set_zlim(0, 1)

fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
plot = [ax.plot_surface(X, Y, v[:], cmap=cm.viridis)]
ani = animation.FuncAnimation(fig, animate, fargs=(plot), interval=1)
plt.show()
