#http://www.josleys.com/article_show.php?id=82

import numpy as np
import matplotlib.pyplot as plt


pi = np.pi
import cv2

img = cv2.imread("test.png",0)
indices = np.where(img!= [0])
p = np.array(indices[0]) + np.array(indices[1])* 1.0j
p = p/300 - 0.5 - 0.5j

plt.scatter(p.real,p.imag)
plt.show()

def log(p):
    pold = p
    p = np.log(np.abs(pold)) + (np.angle(pold)+2*np.pi*5)*1.0j
    for i in range(-5,5):
        p = np.concatenate((p, np.log(np.abs(pold)) + (np.angle(pold)+2*np.pi*i)*1.0j))
    return p

r1 = 0.18
r2 = 0.66
a = np.arctan(np.log(r2/r1)/(2*np.pi))
f = np.cos(a)
b = f*np.exp(1.0j*a)


p = np.exp(b*log(p/r1))
p = (p + 1100 + 2550j)/5
p = np.unique(np.round(np.real(p)) + np.round(np.imag(p)) * 1.0j)

##fig,ax = plt.subplots()
##ax.scatter(p.real,p.imag)
##plt.show()

new = np.zeros((630,800,3))
np.add.at(new, [p.real.astype(int),p.imag.astype(int),0], 14)

cv2.imshow("Droste Effect",new)
