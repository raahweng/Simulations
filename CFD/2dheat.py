import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import cm

nu = 0.05
nx = 31
ny = 31
dx = 2/(nx-1)
dy = 2/(ny-1)
x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)
u = np.ones((nx,ny))
u[int(nx/4):int(3*nx/4),int(ny/4):int(3*ny/4)] = 2
sigma = 0.2
dt = sigma*dx

def update_u():
    global u
##    un = u
##    for i in range(1,nx-1):
##        for j in range(1,ny-1):
##            u[i][j] = un[i][j] + (nu*dt/dx**2)*(un[i+1][j] - 2*un[i][j] + un[i-1][j]) + (nu*dt/dy**2)*(un[i][j+1] - 2*un[i][j] + un[i][j-1])
    un = u
    u[1:-1,1:-1] = un[1:-1,1:-1] + (nu*dt/dx**2) * (un[2:nx,1:-1] - 2*un[1:-1,1:-1] + un[0:-2,1:-1]) + (nu*dt/dy**2) * (un[1:-1,2:nx] - 2*un[1:-1,1:-1] + un[1:-1,0:-2])
    return u

def animate(i, plot):
    plt.cla()
    update_u()
    plot = [ax.plot_surface(X, Y, u[:], cmap=cm.plasma, vmin=1, vmax=2)]
    ax.set_zlim(1, 2)

fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(x, y)  
plot = [ax.plot_surface(X, Y, u[:], cmap=cm.plasma)]
ani = animation.FuncAnimation(fig, animate, fargs=(plot), interval=1)
plt.show()


