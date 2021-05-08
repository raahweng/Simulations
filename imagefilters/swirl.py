#Implementation of https://www.desmos.com/calculator/zumhhxhkyy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n = 20000
tlist = np.linspace(0,1,n)
T = np.cos(26*np.pi*tlist), np.sin(34*np.pi*tlist)
P = np.array([0,0]) #centre of rotation

#Change these!
d = 1 #direction: 1 or -1; toggled on right and left click
swirl = 0.1 #swirl factor (per frame)
r = 3 #swirl concentraion
     
def rotate(xy,theta):
    return xy[0]*np.cos(theta)- xy[1]*np.sin(theta), xy[0]*np.sin(theta)+ xy[1]*np.cos(theta)

def translate(xy,P):
    return xy[0] - P[0], xy[1] - P[1]

fig, ax = plt.subplots(figsize=(10,10))

def onclick(event):
    global T, flag, P, d
    flag = True
    P = np.array([event.xdata,event.ydata])
    if event.button == 1:
        d = 1
    elif event.button == 3:
        d = -1

def onmotion(event):
    global P
    P = np.array([event.xdata,event.ydata])

def onrelease(event):
    global flag
    flag = False
    P = np.array([event.xdata,event.ydata])


cidpress = fig.canvas.mpl_connect('button_press_event', onclick)
cidmotion = fig.canvas.mpl_connect('motion_notify_event', onmotion)
cidrelease = fig.canvas.mpl_connect('button_release_event', onrelease)
flag = False

def animate(i):
    global T,P
    plt.cla()
    if flag:
        T = translate(rotate(translate(T,P), d*swirl*(np.sqrt(2) - np.linalg.norm(translate(T,P),None,0))**r), -1 * P)
    ax.fill_between(T[0], T[1], color = "black")

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()

