import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

k = 2
b = 2
n = 2
h = 0.01
l = 1


fig, ax = plt.subplots()
x = np.arange(0, l, h)
line, = ax.plot(x, b*np.sin(n*np.pi*x/l))

def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def animate(i):
    t = i * 0.0001
    line.set_ydata(b*np.sin(n*np.pi*x/l)*np.exp(-k*t*(n*np.pi/l)**2))  
    return line,

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=20, blit=True, save_count=50)
plt.show()

