#Helpful stuff
#https://lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
#http://developer.download.nvidia.com/books/HTML/gpugems/gpugems_ch38.html

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.ndimage import map_coordinates
from scipy.interpolate import griddata
from matplotlib import cm

#Real-time simulation if true, else generate MP3
realtime = True

nx = 250
ny = 125
dx = 1/(nx-1)
dy = 1/(ny-1)
nu = 1e-4 #Kinematic Viscosity
dt = 0.01 #Timestep
x = np.linspace(0,nx-1,nx)
y = np.linspace(0,ny-1,ny)
X,Y = np.meshgrid(x,y)
grid = np.dstack((Y,X))
u = np.zeros((ny,nx)) #X velocity
v = np.zeros((ny,nx)) #Y velocity
p = np.zeros((ny,nx)) #Pressure
d = np.zeros((ny,nx)) #Dye
divuv = np.zeros((ny,nx))




def uvboundary():
    global u,v

    u[int(3*ny/7):int(4*ny/7), int(1*nx/8):int(2*nx/8)] = 0
    v[int(3*ny/7):int(4*ny/7), int(1*nx/8):int(2*nx/8)] = 0
    d[int(3*ny/7):int(4*ny/7), int(1*nx/8):int(2*nx/8)] = 0

    u[0, 1:-1] = 0
    u[-1, 1:-1] = 0
    v[0, 1:-1] = 0
    v[-1, 1:-1] = 0


def pboundary():
    global p

    p[:,0] = 0
    p[0, 1:-1] = p[1, 1:-1]
    p[-1, 1:-1] = p[-2, 1:-1]

    p[int(3*ny/7), int(1*nx/8):int(2*nx/8)] = p[int(3*ny/7)-1, int(1*nx/8):int(2*nx/8)]
    p[int(4*ny/7), int(1*nx/8):int(2*nx/8)] = p[int(3*ny/7)+1, int(1*nx/8):int(2*nx/8)]
    p[int(3*ny/7):int(4*ny/7), int(1*nx/8)] = p[int(3*ny/7):int(4*ny/7), int(1*nx/8)-1]
    p[int(3*ny/7):int(4*ny/7), int(2*nx/8)] = p[int(3*ny/7):int(4*ny/7), int(2*nx/8)+1] 


    
    
def advection(un,vn,dn):
    global u,v,d

    tempvel = np.dstack((vn,un)).reshape(nx*ny,2)
    velreverse = np.transpose(grid.reshape(nx*ny,2) - tempvel*dt) # dx
    u = map_coordinates(u, velreverse, order=2).reshape((ny,nx))
    v = map_coordinates(v, velreverse, order=2).reshape((ny,nx))
    d = map_coordinates(d, velreverse, order=2).reshape((ny,nx))
    uvboundary()


def diffusion(un,vn,dn):
    global u,v,d
    
    alphau = (dx**2)/(nu*dt)
    alphav = (dy**2)/(nu*dt)
    alphad = (dy*dy)/(nu*dt)
    for i in range(1):
        u[1:-1,1:-1] = (un[1:-1,2:nx] + un[1:-1,0:-2] + un[2:ny,1:-1] + un[0:-2,1:-1] + alphau*un[1:-1,1:-1])/(4+alphau)
        v[1:-1,1:-1] = (vn[1:-1,2:nx] + vn[1:-1,0:-2] + vn[2:ny,1:-1] + vn[0:-2,1:-1] + alphav*vn[1:-1,1:-1])/(4+alphav)
        d[1:-1,1:-1] = (dn[1:-1,2:nx] + dn[1:-1,0:-2] + dn[2:ny,1:-1] + dn[0:-2,1:-1] + alphad*dn[1:-1,1:-1])/(4+alphad)
        uvboundary()
        un = u
        vn = v


def pressure(un,vn,pn):
    global u,v,p

    #divergence in v direction *-1 as axes are other way round in numpy
    divuv[1:-1,1:-1] = (un[1:-1,2:nx] - un[1:-1,0:-2])/(2*dx) + (vn[2:ny,1:-1] - vn[0:-2,1:-1])/(2*dy)
    p[1:-1,1:-1] = (pn[1:-1,2:nx] + pn[1:-1,0:-2] + pn[2:ny,1:-1] + pn[0:-2,1:-1] + (-dx*dy)*divuv[1:-1,1:-1])/4
    pboundary()
    
    un[1:-1,1:-1] -= (1/(2*dx))*(p[1:-1,2:nx] - p[1:-1,0:-2])
    vn[1:-1,1:-1] -= (1/(2*dy))*(p[2:ny,1:-1] - p[0:-2,1:-1])
    uvboundary()
    



def update():
    global u,v,p
    
    for i in range(10):
        
        u[:,0:3] += 60 #60
        d[int(3*ny/7):int(4*ny/7), 1] += 1 #1
        
        advection(u,v,d)
        pressure(u,v,p)
        diffusion(u,v,d)
        pressure(u,v,p)
        
    return u,v,p

def animate(i):
    
    plt.cla()
    update()
    #gradp = np.linalg.norm(np.gradient(p), axis=0)
    #plt.contourf(X, Y, gradp, alpha=0.5, cmap=cm.viridis)
    #plt.contour(X, Y, gradp, cmap=cm.viridis)
    
    dye = plt.imshow(d, cmap='Blues', vmax=1, interpolation='bilinear')
    dye.set_array(d)
    plt.quiver(X[::12, ::12], Y[::12, ::12], u[::12, ::12], v[::12, ::12])

    if not realtime:
        print(i)


if realtime == True:
    
    fig = plt.figure(figsize=(7,7), dpi=100)
    #plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
    #plt.contour(X, Y, p, cmap=cm.viridis)
    #plt.colorbar()
    dye = plt.imshow(d, cmap='Greys', vmax=1, interpolation='bilinear')
    plt.quiver(X[::4, ::4], Y[::4, ::4], u[::4, ::4], v[::4, ::4])
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()

    print("Generating stream plot...")
    fig = plt.figure(figsize=(7, 7), dpi=100)
    plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    plt.contour(X, Y, p, cmap=cm.viridis)
    plt.streamplot(X, Y, u, v, density=2, arrowsize=0.75, minlength = 0.001, maxlength = 10)
    plt.show()

else:

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, bitrate=1800)

    fig = plt.figure(dpi=200)
    #plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
    #plt.contour(X, Y, p, cmap=cm.viridis)
    #plt.colorbar()
    dye = plt.imshow(d, cmap='Greys', vmax=1, interpolation='bilinear')
    plt.quiver(X[::8, ::8], Y[::8, ::8], u[::8, ::8], v[::8, ::8])
    writer = animation.FFMpegWriter() 
    ani = animation.FuncAnimation(fig, animate, 100, interval = 0.001, repeat = False)
    ani.save("test.mp4", fps = 15)
    quit()






