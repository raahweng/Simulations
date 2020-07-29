import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm

nx = 200
ny = 100
dx = 2/(nx-1)
dy = 2/(ny-1)
rho = 0.1 #Density
nu = 1e-2 #Kinematic Viscosity
dt = 0.001
x = np.linspace(0,2,nx)
y = np.linspace(0,1,ny)
X,Y = np.meshgrid(x,y)
u = np.zeros((ny,nx)) #X velocity
v = np.zeros((ny,nx)) #Y velocity
p = np.zeros((ny,nx)) #Pressure
#External forces
fx = 0
fy = 0

def boundary():
    global u,v,p
    
    p[-1,:] = p[-2,:]
    p[0,:] = p[1,:]
    p[:,0] = 0

    u[:,0] = 1
##    u[-1,:] = 0
##    v[-1,:] = 0
##    u[0,:] = 0
##    v[-1,:] = 0
    u[-1,:] = -u[-2,:]
    v[-1,:] = -v[-2,:]
    u[0,:] = -u[1,:]
    v[-1,:] = -v[-2,:]

    u[int(ny/4):int(3*ny/4), int(1*nx/5):int(2*nx/5)] = 0
##    p[int(ny/4), int(1*nx/5):int(2*nx/5)] = p[int(ny/4)-1, int(1*nx/5):int(2*nx/5)]
##    p[int(3*ny/4), int(1*nx/5):int(2*nx/5)] = p[int(3*ny/4)+1, int(1*nx/5):int(2*nx/5)]
##    p[int(ny/4):int(3*ny/4), int(1*nx/5)] = p[int(ny/4):int(3*ny/4), int(1*nx/5)-1]
##    p[int(ny/4):int(3*ny/4), int(2*nx/5)] = p[int(ny/4):int(3*ny/4), int(2*nx/5)+1]
    u[int(ny/4), int(1*nx/5):int(2*nx/5)] = -u[int(ny/4)-1, int(1*nx/5):int(2*nx/5)]
    u[int(3*ny/4), int(1*nx/5):int(2*nx/5)] = -u[int(3*ny/4)+1, int(1*nx/5):int(2*nx/5)]
    u[int(ny/4):int(3*ny/4), int(1*nx/5)] = -u[int(ny/4):int(3*ny/4), int(1*nx/5)-1]
    u[int(ny/4):int(3*ny/4), int(2*nx/5)] = -u[int(ny/4):int(3*ny/4), int(2*nx/5)+1]
    v[int(ny/4), int(1*nx/5):int(2*nx/5)] = -v[int(ny/4)-1, int(1*nx/5):int(2*nx/5)]
    v[int(3*ny/4), int(1*nx/5):int(2*nx/5)] = -v[int(3*ny/4)+1, int(1*nx/5):int(2*nx/5)]
    v[int(ny/4):int(3*ny/4), int(1*nx/5)] = -v[int(ny/4):int(3*ny/4), int(1*nx/5)-1]
    v[int(ny/4):int(3*ny/4), int(2*nx/5)] = -v[int(ny/4):int(3*ny/4), int(2*nx/5)+1]

    
    #u[0:int(nx/2), 0:int(ny/2)] = 0
    #p[int(nx/2), 0:int(ny/2)] = p[int(nx/2)+1, 0:int(ny/2)]
    #p[0:int(nx/2), int(ny/2)] = p[0:int(nx/2), int(ny/2)+1]



def update_vel(un, vn, pn):
    
    u[1:-1,1:-1] = un[1:-1,1:-1] - un[1:-1,1:-1]*(dt/dx)*(un[1:-1,1:-1] - un[1:-1,0:-2]) \
                    - vn[1:-1,1:-1]*(dt/dy)*(un[1:-1,1:-1] - un[0:-2,1:-1]) \
                    - (dt/(2*rho*dx))*(pn[1:-1,2:nx] - pn[1:-1,0:-2]) \
                    + ((nu*dt/(dx**2))*(un[1:-1,2:nx] - 2*un[1:-1,1:-1] + un[1:-1,0:-2])) \
                    + ((nu*dt/(dy**2))*(un[2:ny,1:-1] - 2*un[1:-1,1:-1] + un[0:-2,1:-1])) \
                    + nu*fx*dt


    v[1:-1,1:-1] = vn[1:-1,1:-1] - un[1:-1,1:-1]*(dt/dx)*(vn[1:-1,1:-1] - vn[1:-1,0:-2]) \
                    - vn[1:-1,1:-1]*(dt/dy)*(vn[1:-1,1:-1] - vn[0:-2,1:-1]) \
                    - (dt/(2*rho*dy))*(pn[2:ny,1:-1] - pn[0:-2,1:-1]) \
                    + ((nu*dt/(dx**2))*(vn[1:-1,2:nx] - 2*vn[1:-1,1:-1] + vn[1:-1,0:-2])) \
                    + ((nu*dt/(dy**2))*(vn[2:ny,1:-1] - 2*vn[1:-1,1:-1] + vn[0:-2,1:-1])) \
                    + nu*fy*dt
                   
    return u,v


def update_p(un,vn,pn):
    
    for i in range(200):
        
        p[1:-1,1:-1] = ((dy**2)*(pn[1:-1,2:nx]+pn[1:-1,0:-2]) + (dx**2)*(pn[2:ny,1:-1]+pn[0:-2,1:-1])) / (2*(dx**2 + dy**2)) \
            - (rho*(dx**2)*(dy**2))/(2*(dx**2+dy**2)) \
            *((1/dt)*((un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx) + (vn[2:nx,1:-1] - vn[0:-2,1:-1])/(2*dy)) \
              -   (((un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx)) * ((un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx))) \
              - 2*(((un[2:ny,1:-1] - un[0:-2,1:-1])/(2*dy)) * ((vn[1:-1,2:nx] - vn[1:-1,0:-2])/(2*dx))) \
              -   (((vn[2:ny,1:-1] - vn[0:-2,1:-1])/(2*dy)) * ((vn[0:-2,1:-1] - vn[2:ny,1:-1])/(2*dy))))
        
    return p


def update():
    global u,v,p
    un = u
    vn = v
    pn = p
    p = update_p(un,vn,pn)
    u,v = update_vel(un,vn,pn)
    boundary()
    return u,v,p

def animate(i):
    plt.cla()
    update()
    update()
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
    plt.contour(X, Y, p, cmap=cm.viridis)  
    plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])

boundary()


fig = plt.figure(figsize=(15,5), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
plt.contour(X, Y, p, cmap=cm.viridis)  
plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
plt.colorbar()
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

print("Generating stream plot...")
fig = plt.figure(figsize=(15, 5), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
plt.colorbar()
plt.contour(X, Y, p, cmap=cm.viridis)
plt.streamplot(X, Y, u, v, density=2, arrowsize=0.75, minlength = 0.001, maxlength = 10)
plt.show()

