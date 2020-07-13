import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate, scipy.optimize

#Stuff to change
l = 10*np.pi
def f(t):
    return t*np.sin(t)
k = 0.5
boundary = "neumann"
fourier_n = 100
timestep = 0.01
h = 0.01
interval = 10

def c(n):
    if boundary == "dirichlet":
        return (2/l) * scipy.integrate.quad(lambda t: f(t)*np.sin((n*np.pi*t/l)), 0, l, args=(), full_output=0, epsabs=1.49e-8, epsrel=1.49e-8, limit=10000)[0]
    if boundary == "neumann":
        return (2/l) * scipy.integrate.quad(lambda t: f(t)*np.cos((n*np.pi*t/l)), 0, l, args=(), full_output=0, epsabs=1.49e-8, epsrel=1.49e-8, limit=10000)[0]
constants = np.zeros(fourier_n+1)
for i in range(1,fourier_n+1):
    constants[i] = c(i)
    
def heat(t):
    y = np.zeros(np.shape(x))
    for i in range(1,fourier_n+1):
        if boundary == "dirichlet":
            y += constants[i]*np.sin((np.pi*i*x)/l)*np.exp(-k*t*((i*np.pi)/l)**2)
        if boundary == "neumann":
            y += constants[i]*np.cos((np.pi*i*x)/l)*np.exp(-k*t*((i*np.pi)/l)**2)
    return y
                                                      

fig, ax = plt.subplots()
x = np.arange(0, l, h)
line, = ax.plot(x,heat(0))
    
def init():  
    line.set_ydata([np.nan] * len(x))
    return line,

def animate(i):
    t = i*timestep
    line.set_ydata(heat(t))
    return line,


ani = animation.FuncAnimation(
    fig, animate, init_func=init, interval=interval, blit=True, save_count=50)
plt.show()

