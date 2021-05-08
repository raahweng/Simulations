import numpy as np
import cmath
import matplotlib.pyplot as plt
from scipy.special import comb


def zeta(s, maxn=100):

    def subseries(n):
        c = 0
        for k in range(n+1):
            c = c + comb(n,k)*((-1)**k)/((k+1)**s)
        return c

    return sum([ subseries(n) / (2**(n+1)) for n in range(0,maxn) ]) / (1 - 2**(1-s))



zeta_values = [zeta(0.5 + i*1.0j) for i in np.linspace(0, 50, 1000)]

fig, ax = plt.subplots()
ax.plot(np.real(zeta_values), np.imag(zeta_values))
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
plt.show()
