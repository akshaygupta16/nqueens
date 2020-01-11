# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 04:44:08 2019

@author: Akshay
"""

import numpy as np
import copy
import random


#Create a list to store the number of steps for every successful run
steps_when_success=[]

#Create a list to store the number of steps for every failed run
steps_when_failure=[]




#function to create a random initial configuration of dimension dim x dim
def create_intial_config(dim):
    all_zero_arr = np.zeros((dim,dim),dtype=int)
    for row in all_zero_arr:
        row[random.randint(0,dim-1)]=1
    initial=all_zero_arr.tolist()
    return initial
 
#function returns the heuristic value of state passed an a argument
def cal_heuristic(initial):
    usethis = copy.deepcopy(initial)
    h=0
    for i in range(dim):
        for j in range(dim):
            for k in range(i-1, -1, -1):
                if(usethis[i][j] == usethis[k][j] and usethis[i][j]==1):
                    h = h + 1

            for l in range(i+1, dim):
                if(usethis[i][j] == usethis[l][j] and usethis[i][j]==1):
                    h = h + 1

            for m,n in zip(range(i-1, -1, -1),range(j-1, -1, -1)):
                if(usethis[i][j] == usethis[m][n] and usethis[i][j]==1):
                    h = h + 1

            for o,p in zip(range(i+1, dim, 1), range(j+1, dim, 1)):
                if(usethis[i][j] == usethis[o][p] and usethis[i][j]==1):
                    h = h + 1

            for r,s in zip(range(i+1, dim, 1), range(j-1, -1, -1)):
                if(usethis[i][j] == usethis[r][s] and usethis[r][s]==1):
                    h = h + 1
                    
            usethis[i][j] = 0
    return h

#function that returns a list of all successors of a state passed as an argument
def find_successors(initial):
    num_dim = dim
    current = np.asarray(initial)
    childrennp = np.array([], dtype='int')
    
    for x,y in np.argwhere(current==1):
        temp = current.copy()
        temp[x,y]=0
        for k in range(y+1,dim):
            temp[x,k]=1
#            print(temp)
            childrennp = np.append(childrennp,temp)
            temp[x,k]=0
        for l in range(y-1,-1,-1):
            temp[x,l]=1
#            print(temp)
            childrennp = np.append(childrennp,temp)
            temp[x,l]=0
    
    childrennp = childrennp.reshape(-1, num_dim, num_dim).tolist()
    
    return childrennp

#this function returns the best successors from the list of successors passed as the argument
def best_neighbour(successors):
    all_heuristics = []
    for n in successors:
        all_heuristics.append(cal_heuristic(n))
    best_h = min(all_heuristics)
    best_at = all_heuristics.index(best_h)
    return successors[best_at]
   
#this functions run the basic hill climbing algorithm with that state passed to it as the initial state
def hill_climb(initial):
    global no_of_steps,steps_when_failure,steps_when_success
    current = initial.copy()
    successors = find_successors(current)
    best_successor=best_neighbour(successors)

    
    if cal_heuristic(current) <= cal_heuristic(best_successor):
        if cal_heuristic(current) == 0:
            steps_when_success.append(no_of_steps)
        else:
            steps_when_failure.append(no_of_steps)
        return current
    else:
        no_of_steps=no_of_steps+1
        current = best_successor
        hill_climb(current)
  
#taking input from the user for the number of queens      
try:
    dim = input("Enter N i.e the number of queens : ")
    dim = int(dim)
except:
    print("Please enter an integer value")
    dim = input("Enter N i.e the number of queens : ")
    dim = int(dim)
    
    
print("Loading ....")
#runs the basic climbing 200 times
for iterations in range(201):
    no_of_steps=0
    initial = create_intial_config(dim)
    hill_climb(initial)

    
print("       ")
print("The Average of Steps for success", np.average(steps_when_success))
print("Success Rate", 100*(len(steps_when_success)/(len(steps_when_success)+len(steps_when_failure))),"%")
print("       ")
print("The Average of Steps for a failure",np.average(steps_when_failure))
print("Failure Rate", 100*(len(steps_when_failure)/(len(steps_when_success)+len(steps_when_failure))),"%")


