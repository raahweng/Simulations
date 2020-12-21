#http://developer.download.nvidia.com/books/HTML/gpugems/gpugems_ch38.html

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import map_coordinates
from scipy.interpolate import griddata
from matplotlib import cm

nx = 200
ny = 200
dx = 1/(nx-1)
dy = 1/(ny-1)
rho = 0.001 #Density
nu = 1e-2#Kinematic Viscosity
dt = 0.1
x = np.linspace(0,nx-1,nx)
y = np.linspace(0,ny-1,ny)
X,Y = np.meshgrid(x,y)
grid = np.dstack((Y,X))
u = np.zeros((ny,nx)) #X velocity
v = np.zeros((ny,nx)) #Y velocity
u[0:int(ny/4),:int(nx/2)] = 10
p = np.zeros((ny,nx)) #Pressure
divuv = np.zeros((ny,nx))

def boundary(x):
    x[0, 1:-1] = -x[1, 1:-1]
    x[-1, 1:-1] = -x[-2, 1:-1]
    x[1:-1,  0] = -x[1:-1, 1]
    x[1:-1, -1] = -x[1:-1, -2]
    x[ 0,  0] = 0.5 * (x[1,  0] + x[ 0, 1])
    x[ 0, -1] = 0.5 * (x[1, -1] + x[ 0, -2])
    x[-1,  0] = 0.5 * (x[-2,  0] + x[-1, 1])
    x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])
    
    
def advection(un,vn):
    global u,v

    tempvel = np.dstack((vn,un)).reshape(nx*ny,2)
    velreverse = np.transpose(grid.reshape(nx*ny,2) - tempvel*dt) # dx
    #print(velreverse[50,0,:])
    u = map_coordinates(tempvel[:,1].reshape((ny,nx)), velreverse, order=2).reshape((ny,nx))
    v = map_coordinates(tempvel[:,0].reshape((ny,nx)), velreverse, order=2).reshape((ny,nx))
    boundary(u)
    boundary(v)
    

def diffusion(un,vn):
    global u,v
    alphau = (dx**2)/(nu*dt)
    alphav = (dy**2)/(nu*dt)
    for i in range(1):
        u[1:-1,1:-1] = (un[1:-1,2:nx] + un[1:-1,0:-2] + un[2:ny,1:-1] + un[0:-2,1:-1] + alphau*un[1:-1,1:-1])/(4+alphau)
        v[1:-1,1:-1] = (vn[1:-1,2:nx] + vn[1:-1,0:-2] + vn[2:ny,1:-1] + vn[0:-2,1:-1] + alphav*vn[1:-1,1:-1])/(4+alphav)
        boundary(u)
        boundary(v)
        un = u
        vn = v
    

def force(un,vn):
    global u,v
    pass
    

def pressure(un,vn,pn):
    global u,v,p

#divergence in v direction *-1 as axes are the wrong way round
    divuv[1:-1,1:-1] = (un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx) + (vn[2:ny,1:-1] - vn[0:-2,1:-1])/(2*dy)
    boundary(divuv)
    p[1:-1, 1:-1] = 0
    for i in range(50):
        p[1:-1,1:-1] = (pn[1:-1,2:nx] + pn[1:-1,0:-2] + pn[2:ny,1:-1] + pn[0:-2,1:-1] + (-dx*dy)*divuv[1:-1,1:-1])/4
        pn = p
        boundary(p)

    
    un[1:-1,1:-1] -= (1/(2*dx))*(p[1:-1,2:nx] - p[1:-1,0:-2])
    vn[1:-1,1:-1] -= (1/(2*dy))*(p[2:ny,1:-1] - p[0:-2,1:-1])
    boundary(u)
    boundary(v)

def update():
    global u,v,p
    advection(u,v)
    pressure(u,v,p)
    diffusion(u,v)
    pressure(u,v,p)
    return u,v,p

def animate(i):
    plt.cla()
    update()
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
    plt.contour(X, Y, p, cmap=cm.viridis)  
    plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])


fig = plt.figure(figsize=(7,7), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
plt.contour(X, Y, p, cmap=cm.viridis)  
plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
plt.colorbar()
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

print("Generating stream plot...")
fig = plt.figure(figsize=(7, 7), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
plt.colorbar()
plt.contour(X, Y, p, cmap=cm.viridis)
plt.streamplot(X, Y, u, v, density=2, arrowsize=0.75, minlength = 0.001, maxlength = 10)
plt.show()


def show():
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis) 
    plt.contour(X, Y, p, cmap=cm.viridis) 
    plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
    plt.show()


