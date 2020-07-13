import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate, scipy.optimize

#Stuff to change
bounds = [0,10]
def f(t):
    return np.exp(t)
interval = 20
showhistory = False

def a(n):
    return (2/p) * scipy.integrate.quad(lambda t: f(t)*np.cos(2*np.pi*t*(n/p)), bounds[0], bounds[1], args=(), full_output=0, epsabs=1.49e-10, epsrel=1.49e-10, limit=10000)[0]

def b(n):
    return (2/p) * scipy.integrate.quad(lambda t: f(t)*np.sin(2*np.pi*t*(n/p)), bounds[0], bounds[1], args=(), full_output=0, epsabs=1.49e-10, epsrel=1.49e-10, limit=10000)[0]
    
def fourier(n):
    return a(n)*np.cos((2*np.pi*n*x)/p) + b(n)*np.sin((2*np.pi*n*x)/p)

h = 0.0001
p = bounds[1]-bounds[0]
fig, ax = plt.subplots()
x = np.arange(bounds[0], bounds[1], h)
y = np.zeros(np.shape(x)) + a(0)/2
line, = ax.plot(x,y)

def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def animate(i):
    global y
    y += fourier(i+1)
    line.set_ydata(y)
    if showhistory:
        plt.plot(x,y)
    return line,

plt.plot(x,f(x))
ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=interval, blit=True, save_count=50)
plt.show()

