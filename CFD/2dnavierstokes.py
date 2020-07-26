import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm

nx = 41
ny = 41
dx = 2/(nx-1)
dy = 2/(ny-1)
rho = 1
nu = 1e-2
dt = 0.005
x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)
X,Y = np.meshgrid(x,y)
u = np.zeros((ny,nx))
v = np.zeros((ny,nx))
p = np.zeros((ny,nx))

def set_conditions():
    print("\n")
    boundaries = []
    boundaries.append(bool(input("Top boundary? (0/1) ")))
    boundaries.append(bool(input("Right boundary? (0/1) ")))
    boundaries.append(bool(input("Left boundary? (0/1) ")))
    boundaries.append(bool(input("Bottom boundary? (0/1) ")))
    boundaries.append(int(input("Top inlet x velocity ")))
    boundaries.append(int(input("Top inlet y velocity ")))
    boundaries.append(int(input("Right inlet x velocity ")))
    boundaries.append(int(input("Right inlet y velocity ")))
    boundaries.append(int(input("Bottom inlet x velocity ")))
    boundaries.append(int(input("Bottom inlet y velocity ")))
    boundaries.append(int(input("Left inlet x velocity ")))
    boundaries.append(int(input("Left inlet y velocity ")))
    return boundaries

def boundary():
    global u,v,p
    
    if boundaries[0] == True:
        p[-1,:] = 0
    else:
        p[-1,:] = p[-2,:]
    if boundaries[1] == True:
        p[:,-1] = 0
    else:
        p[:,-1] = p[:,-2]
    if boundaries[2] == True:
        p[0,:] = 0
    else:
        p[0,:] = p[1,:]
    if boundaries[3] == True:
        p[:,0] = 0
    else:
        p[:,0] = p[:,1]
        
    u[-1,:] = boundaries[4]
    v[-1,:] = boundaries[5]
    u[:,-1] = boundaries[6]
    v[:,-1] = boundaries[7]
    u[0,:] = boundaries[8]
    v[0,:] = boundaries[9]
    u[:,0] = boundaries[10]
    v[:,0] = boundaries[11]


def update_vel(un, vn, pn):
    
    u[1:-1,1:-1] = un[1:-1,1:-1] - un[1:-1,1:-1]*(dt/dx)*(un[1:-1,1:-1] - un[1:-1,0:-2]) \
                    - vn[1:-1,1:-1]*(dt/dy)*(un[1:-1,1:-1] - un[0:-2,1:-1]) \
                    - (dt/(2*rho*dx))*(pn[1:-1,2:ny] - pn[1:-1,0:-2]) \
                    + ((nu*dt/(dx**2))*(un[1:-1,2:ny] - 2*un[1:-1,1:-1] + un[1:-1,0:-2])) \
                    + ((nu*dt/(dy**2))*(un[2:nx,1:-1] - 2*un[1:-1,1:-1] + un[0:-2,1:-1]))


    v[1:-1,1:-1] = vn[1:-1,1:-1] - un[1:-1,1:-1]*(dt/dx)*(vn[1:-1,1:-1] - vn[1:-1,0:-2]) \
                    - vn[1:-1,1:-1]*(dt/dy)*(vn[1:-1,1:-1] - vn[0:-2,1:-1]) \
                    - (dt/(2*rho*dy))*(pn[2:nx,1:-1] - pn[0:-2,1:-1]) \
                    + ((nu*dt/(dx**2))*(vn[1:-1,2:ny] - 2*vn[1:-1,1:-1] + vn[1:-1,0:-2])) \
                    + ((nu*dt/(dy**2))*(vn[2:nx,1:-1] - 2*vn[1:-1,1:-1] + vn[0:-2,1:-1]))
                   
    return u,v


def update_p(un,vn,pn):
    
    for i in range(50):
        
        p[1:-1,1:-1] = ((dy**2)*(pn[1:-1,2:ny]+pn[1:-1,0:-2]) + (dx**2)*(pn[2:nx,1:-1]+pn[0:-2,1:-1])) / (2*(dx**2 + dy**2)) \
            - (rho*(dx**2)*(dy**2))/(2*(dx**2+dy**2)) \
            *((1/dt)*((un[1:-1,2:ny] - un[1:-1,0:-2])/(2*dx) + (vn[2:ny,1:-1] - vn[0:-2,1:-1])/(2*dy)) \
              -   (((un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx)) * ((un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx))) \
              - 2*(((un[2:nx,1:-1] - un[0:-2,1:-1])/(2*dy)) * ((vn[1:-1,2:nx] - vn[1:-1,0:-2])/(2*dx))) \
              -   (((vn[2:nx,1:-1] - vn[0:-2,1:-1])/(2*dy)) * ((vn[0:-2,1:-1] - vn[2:ny,1:-1])/(2*dy))))
        
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
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
    plt.contour(X, Y, p, cmap=cm.viridis)  
    plt.quiver(X, Y, u, v)

opt = input("Preset or custom? (p/c) ")
if opt == "p":
    boundaries = [True,False,False,False,1,0,0,0,0,0,0,0,0]
else:
    boundaries = set_conditions()

boundary()
fig = plt.figure(figsize=(11,7), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
plt.contour(X, Y, p, cmap=cm.viridis)  
plt.quiver(X, Y, u, v)
plt.colorbar()
ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

print("Generating stream plot...")
fig = plt.figure(figsize=(11, 7), dpi=100)
plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
plt.colorbar()
plt.contour(X, Y, p, cmap=cm.viridis)
plt.streamplot(X, Y, u, v, density=2, arrowsize=0.75, minlength = 0.001, maxlength = 10)
plt.show()

