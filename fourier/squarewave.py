import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

h = 0.001

fig, ax = plt.subplots()
x = np.arange(0, 1, h)
line, = ax.plot(x, (4/np.pi) * np.sin(2*np.pi*x))

def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def square(n):
	y  = np.zeros(int(1/h))
	for i in range(1,n+2,2):
		y += (4/(i*np.pi)) * np.sin(2*np.pi*i*x)
	return y

def animate(i):
    n = 2*i+3
    line.set_ydata(square(n))  
    return line,

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=20, blit=True, save_count=50)
plt.show()

