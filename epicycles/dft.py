import numpy as np
import matplotlib.pyplot as plt

m = 100
N = 2*m+1
P = 2*m
pi = np.pi
t = np.linspace(-pi,pi,N)
x = 16*np.sin(t)**3
y = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
p = x + y*1.0j

fig,ax = plt.subplots()
ax.scatter(p.real,p.imag)
plt.show()

coeff = np.zeros((N)) + np.zeros((N))*1.0j
for k in range(-m,m+1):
    for n,x in enumerate(p):
        coeff[k+m] += x * np.exp(-2*pi*1.0j*k*(n-m)/N)

def f(t):
    return sum(np.exp((2*pi*1.0j*t)/N*np.arange(-m,m+1)) * coeff) / N

pnew = np.array([f(t) for t in range(-m,m+1)])

fig,ax = plt.subplots()
ax.scatter(pnew.real,pnew.imag)
plt.show()


