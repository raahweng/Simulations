#http://empslocal.ex.ac.uk/people/staff/mrwatkin/zeta/encoding2.htm

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate
from scipy.special import zeta


def prime(n):

    if n == 1:
        return False
    
    for i in range(2, int(np.ceil(np.sqrt(n))+1)):
        if n % i == 0 and n != i:
            return False

    return True

def power(n,p):

    x = n
    while True:

        if x == 1:
            return True
        
        elif x % p == 0:
            x = x / p

        else:
            return False

            
n = 50
phi_f = 0
phi_list = []

primes = [prime(i) for i in range(1,n+1)]

for i in range(n):
    
    if primes[i]:
        phi_f += np.log(i+1)

    else:
        
        for p in range(i+1):
            
            if primes[p]:

                if power(i+1,p+1):
                    phi_f += np.log(p+1)
                    
                    break

    phi_list.append(phi_f)

            
    

zeroes = [0.5-2*i*1.0j for i in range(1,51)]
with open("zeroes.txt", "r") as f:
    zeroes = [float(i[5:-2]) if i[4] == " " else float(i[4:-2]) for i in f]


def phi(x, d):
    
    return x - sum([(x**(0.5 +rho*1.0j)/(0.5 +rho*1.0j)) for rho in zeroes[:d]]) - sum([(x**(0.5 - rho*1.0j)/(0.5 - rho*1.0j)) for rho in zeroes[:d]]) - np.log(2*np.pi) - 0.5*np.log(1-(x**-2))


##plt.step(np.arange(2, n+2),phi_list)
##plt.plot(np.linspace(1,n,1000, dtype=float), [phi(x,100) for x in np.linspace(1,n,1000, dtype=float)])
##plt.show()


fig, ax = plt.subplots()
line, = ax.plot(np.linspace(1,n,1000, dtype=float), [phi(x,100) for x in np.linspace(1,n,1000, dtype=float)])

def animate(i):
    line.set_ydata([phi(x,i) for x in np.linspace(1,n,1000, dtype=float)])
    return line,

plt.step(np.arange(2, n+2),phi_list)
ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
plt.show()



    
