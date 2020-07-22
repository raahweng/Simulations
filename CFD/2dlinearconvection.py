import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import cm

c = 1
nx = 101
ny = 101
dx = 2/(nx-1)
dy = 2/(ny-1)
x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)
u = np.ones((nx,ny))
u[1:25,1:50] = 2
sigma = 0.2
dt = sigma*dx

def update_u():
    global u
##    un = u
##    for i in range(1,100):
##        for j in range(1,100):
##            u[i][j] = un[i][j] - c*(dt/dx)*(un[i][j]-un[i-1][j])-c*(dt/dy)*(un[i][j]-u[i][j-1])
    un = u
    u[1:-1,1:-1] = un[1:-1,1:-1] - c*(dt/dx)*(un[1:-1,1:-1]-un[0:-2,1:-1]) - c*(dt/dy)*(un[1:-1,1:-1]-un[1:-1,0:-2])
    return u

def animate(i, plot):
    plt.cla()
    update_u()
    plot = [ax.plot_surface(X, Y, u[:], cmap=cm.viridis)]

fig = plt.figure(figsize=(11, 7), dpi=100)
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(x, y)  
plot = [ax.plot_surface(X, Y, u[:], cmap=cm.viridis)]
ani = animation.FuncAnimation(fig, animate, fargs=(plot), interval=10)
plt.show()


