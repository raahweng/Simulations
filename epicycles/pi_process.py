import numpy as np
import pickle

f = open("pi.txt", "r")

p = []
flag = False
for x,i in enumerate([i for i in f]):
    temp = []
    for y,j in enumerate(i):
        if j == "0" or j == "1":
            if flag == False and j == "1":
                pixel = (x,y)
                flag = True
            temp.append(int(j))
    p.append(temp)

#21 371

def check(c):
    try:
        if p[c[0]][c[1]] == 1:
            return True
    except IndexError:
        pass

def adj(x,y):

    neighbour = []
    for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                neighbour.append((i,j))
    neighbour.remove((x,y))   
    
    for i in range(len(neighbour)):
        if check(neighbour[i]):
            return neighbour[i]

    for i in range(x-2,x+3):
        for j in range(y-2,y+3):
            neighbour.append((i,j))
    neighbour.remove((x,y))  

    for i in range(len(neighbour)):
        if check(neighbour[i]):
            return neighbour[i]

    for i in range(x-4,x+5):
        for j in range(y-4,y+5):
            neighbour.append((i,j))
    neighbour.remove((x,y))  

    for i in range(len(neighbour)):
        if check(neighbour[i]):
            return neighbour[i]
    
    return False


coord = []
while True:
    coord.append((pixel[1]-325) - 1.0j*(pixel[0]-325))
    p[pixel[0]][pixel[1]] = 0
    pixel = adj(pixel[0],pixel[1])
    if pixel == False:
        break

import matplotlib.pyplot as plt
import numpy as np
coord = np.array(coord)
fig,ax = plt.subplots()
ax.scatter(coord.real,coord.imag)
plt.show()

print(coord)

pickle.dump( coord/325, open( "pi.p", "wb" ) )



                 
            

