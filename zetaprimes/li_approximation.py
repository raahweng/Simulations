import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def prime(n):

    if n == 1:
        return False
    
    for i in range(2, int(np.ceil(np.sqrt(n))+1)):
        if n % i == 0 and n != i:
            return False

    return True
            
n = 1000
pi_f = 0
pi_list = np.zeros((n))

for i in range(1, n+1):

    if prime(i):
        pi_f += 1

    pi_list[i-1] = pi_f


def li(n):
    
    return integrate.quad(lambda x: 1/np.log(x), 2, n)[0]

h = 5
R = np.zeros((h,n-1))
R[0] = [li(x) for x in range(2, n+1)]

for i in range(2,h):
    R[i] = [-1/i *li(x ** (1/i)) for x in range(2, n+1)]



plt.step(np.arange(1, n+1),pi_list)

harmonics = np.zeros(n-1)
for i in range(h):
    harmonics = harmonics + R[i] 
    plt.plot(np.arange(2,n+1), harmonics)

plt.show()



    
