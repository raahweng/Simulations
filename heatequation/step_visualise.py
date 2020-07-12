import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

k = 2
n = 2
h = 0.005
l = 1
sq_n = 1000

def square():
	y  = np.zeros(int(l/h))
	for i in range(1,sq_n+2,2):
		y += (4/(i*np.pi)) * np.sin(2*np.pi*i*x)
	return y

fig, ax = plt.subplots()
x = np.arange(0, l, h)
line, = ax.plot(x, square())

def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def squaresol(t):
    y  = np.zeros(int(l/h))
    for i in range(1,sq_n+2,2):
        b = 4/(i*np.pi)
        n = 2*i*l
        y += b*np.sin(n*np.pi*x/l)*np.exp(-k*t*(n*np.pi/l)**2)
    return y

def animate(i):
    t = i * 0.0001
    line.set_ydata(squaresol(t))  
    return line,

ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=20, blit=True, save_count=50)

plt.show()

