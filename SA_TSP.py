#!/usr/bin/env python
# coding: utf-8

# In[25]:


import numpy as np
import matplotlib.pyplot as plt
import random


# In[51]:


def getDistance(x1, x2):
    sum = 0
    for i in range(len(x1)):
        sum += (x1[i] - x2[i]) ** 2
    return np.sqrt(sum)
#total distance between all city
def cost(currentState): 
    cost = 0
    
    for i in range(len(currentState)-1):
        cost += getDistance(currentState[i],currentState[i+1])
    cost += getDistance(currentState[0],currentState[-1])
      
    return cost
        
#using combinatorial optimization to select neighbors
def Combinatorial(currentState):
   #swap two neighbors along the path
    xi = np.random.randint(0, len(currentState)-1)
    xj = np.random.randint(0, len(currentState)-1)
    
    neighbor = currentState.copy()
    temp = neighbor[xj].copy()
    
    neighbor[xj] = neighbor[xi]
    neighbor[xi] = temp

    return neighbor

#perform optimization
def optimize(maxStep,tMin,tMax,currentState,currentCost,cooling):
    step =  1
    bestState = currentState
    bestCost = currentCost
    t=tMax
    #SA loop
    while step < maxStep and t >= tMin and t>0:
        
        # get current itteration neighbor using combinatorial method
        currentNeighbor = Combinatorial(currentState)
        
        # compute current  neighbor distance cost from neighbor
        neighborCost = cost(currentNeighbor)
        costDifference = neighborCost - currentCost 

        # check if I should accept the current neighbor
        if np.random.random() < np.exp(-costDifference / t):
            currentCost = neighborCost
            currentState = currentNeighbor
            
        # check if the current neighbor has a best cost
        if neighborCost < bestCost:
            bestCost = neighborCost
            bestState = currentNeighbor

        
        #cooling method
        
        if cooling == 'linear additive':
            t = tMin + (tMax - tMin) * ((maxStep - step)/maxStep)
        elif cooling == 'quadratic additive':
            t= tMin + (tMax - tMin) * ((tMin - step)/tMin)**2
        
        elif cooling == 'exponential':
            t=tMax * 0.8**step
        else:
            t = tMax / 0.1 * np.log(step + 1)
        step += 1
        
    return bestState,bestCost


# In[57]:


#sa requied variables
indices = 20
tempMax = 4
tempMin = 1
iterMax =6000
cooling = 'linear additive'
#initial State
state = np.array([[random.random()*100 for i in range(2)] for j in range(indices)])
#initialize state
initialState = np.copy(state)
currentCost = cost(initialState)
bestSate = optimize(iterMax,tempMin,tempMax,initialState,currentCost,cooling)[0]


# In[58]:


#compare plot of previous state with the last state
x = state[:,0]
y = state[:,1]

cl = np.zeros((2,2))

cl[0] = state[0]
cl[-1] = state[-1]

xj = cl[:,0]
yj = cl[:,1]

plt.scatter(x,y,color="red")
for i in range(len(x)):
    xe = x[i]
    ye = y[i]
    
    if(i == 0):
        plt.scatter(xe, ye,color='red')
        plt.text(xe, ye, " r" + str(i+1), fontsize=9)
        continue
    
    plt.scatter(xe, ye,color='blue')
    plt.text(xe, ye, " r" + str(i+1), fontsize=9)


plt.plot(xj,yj,color="blue")
plt.plot(x,y,color="blue")
plt.title("The path of the Sales man before SA") 
plt.show()

xi = bestSate[:,0]
yi = bestSate[:,1]

cl2 = np.zeros((2,2))

cl2[0] = bestSate[0]
cl2[-1] = bestSate[-1]

xk = cl2[:,0]
yk = cl2[:,1]


for i in range(len(x)):
    xe = xi[i]
    ye = yi[i]
    
    if(i == 0):
        plt.scatter(xe, ye,color='red')
        plt.text(xe, ye, " r" + str(i+1), fontsize=9)
        continue
    
    plt.scatter(xe, ye,color='blue')
    plt.text(xe, ye, " r" + str(i+1), fontsize=9)

plt.plot(xk,yk,color="blue")
plt.plot(xi,yi,color="blue")
plt.title("After SA with "+  str(indices) + " cities. Max Temp="+ str(tempMax)+", cooling: "+cooling+",Max iteration:"+str(iterMax))
plt.show()


# In[ ]:




