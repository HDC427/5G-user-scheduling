#!/usr/bin/env python
# coding: utf-8

# # USER SCHEDULING IN 5G

# ## Preparation

# In[1]:


import numpy as np


# In[92]:


# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

class Channel:
    
    __N = 0
    __M = 0
    __K = 0
    __p = 0
    __size = 0
    
    def __init__(self, p, r):
        
        self.__originalData = np.array([p, r])
        
        self.p = p.flatten()
        self.r = r.flatten()
        
        #keep track of the k, m index in __originalData
        self.L = np.argsort(self.p)
        
        #p sorted in increasing order, r reordered accordingly 
        self.p = self.p[self.L]
        self.r = self.r[self.L]
        #the solution
        
        self.x = np.zeros_like(self.__size, dtype=np.int)
        
    def delete(self, i):
        
        self.L = np.delete(self.L, i)
        self.p = np.delete(self.p, i)
        self.r = np.delete(self.r, i)
        self.__size -= len(i)
        
    def preprocess_IP(self):
        
        current_max = self.r[0]
        dominated = []
        for i in range(1, self.__size):
            if self.r[i] >= current_max:
                current_max = self.r[i]
                if self.p[i] == self.p[i-1]:
                    dominated.append(i-1)
            else: dominated.append(i)
        self.delete(dominated)
            
    def preprocess_LP(self):
        
        i = 0
        while self.p[i+1] == self.p[i]:
            self.delete(i)
            i += 1
        S = [i, i+1]
        
        for j in range(i+2, self.__size):
            while len(S) >1 and                   (self.r[j]-self.r[S[-1]]) * (self.p[S[-1]]-self.p[S[-2]]) >=                   (self.r[S[-1]]-self.r[S[-2]]) * (self.p[j]-self.p[S[-1]]):
                      S.pop(-1)
            S.append(j)
            
        self.L = self.L[S]
        self.p = self.p[S]
        self.r = self.r[S]

    @classmethod
    def read_testfile(cls, x):
        '''x is the number of testfile'''
        
        f = open("../testfiles/test%d.txt"%x)
        cls.__N = int(eval(f.readline()))
        cls.__M = int(eval(f.readline()))
        cls.__K = int(eval(f.readline()))
        cls.__p = int(eval(f.readline()))
        cls.__size = cls.__M * cls.__K
        
        pr_data = np.loadtxt(f, dtype=np.int)
        
        channel = []
        for i in range(cls.__N):
            channel.append(Channel(pr_data[i*cls.__K:(i+1)*cls.__K, :],                                    pr_data[(i+cls.__N)*cls.__K:(i+cls.__N+1)*cls.__K, :]))
        #for the ith channel, rows [i*K,(i+1)*K[ are its values of p, rows [(i+N)*K,(i+N+1)*K[ are those of r
        
        return channel
    
    def get_P(cls):
        return cls.__p
    
    def display(self):
        plt.plot(self.p, self.r)
        

channels = Channel.read_testfile(3)

print("The number of channels is: ", len(channels))

for i in range(len(channels)):
    channels[i].preprocess_IP()
    channels[i].preprocess_LP()
    print(channels[i].p)
    print(channels[i].r)
    print("------------------------------")

def check_answer(channels, x):
    '''print the possible ansswers'''
    r = 0
    p = 0
    for i in range(len(x)):
        print("channel %d: "%(i+1) , x[i])
        for j in range(len(x[i])):
            if x[i][j] == 1:
                p += channels[i].p[j]
                r += channels[i].r[j]
    print("total power: ", p , "; total utility: ", r)

# Greedy Solution

def e(l, i):
    if 0 < l and l < len(channels[i].p):
        return (channels[i].r[l] - channels[i].r[l-1] )/(channels[i].p[l] - channels[i].p[l-1])
    elif l == 0:
        return channels[i].r[0] / channels[i].p[0]
    else:
        return -1;

P = Channel.get_P(Channel)

def greedy_solution(channels, P):
    x = [len(channels[i].p) * [0] for i in range(len(channels))]
    
    p_current = 0;
    l = [0 for i in range(len(channels))]
    while p_current < P:
        e_max = -1
        n_max = 0
        for i in range(len(channels)):
            e_current = e(l[i],i)
            if e_current >= e_max:
                e_max = e_current
                n_max = i

        if e_max <= 0:
            break 

        if l[n_max] > 0:
            p_current += channels[n_max].p[l[n_max]]  - channels[n_max].p[l[n_max]-1]
        else:
            p_current += channels[n_max].p[l[n_max]]
        l[n_max] += 1
    
    if P == p_current:
        for i in range(len(channels)):
            x[i][l[i]] = 1
    elif P < p_current:
        for i in range(len(channels)):
            if i != n_max:
                if l[i] > 0:
                    x[i][l[i]-1] = 1
            else:
                epsilon = (p_current - P)/(channels[i].p[l[i]] - channels[i].p[l[i]-1])
                x[i][l[i] - 1] = epsilon
                x[i][l[i]] = 1 - epsilon
    return x

#x_0 = greedy_solution(channels, P)

#check_answer(channels, x_0)


# DP Solution

def dp_solution(channels, P):
    N = len(channels)
    x = [len(channels[i].p) * [0] for i in range(len(channels))]
    
    dp = [np.zeros(P+1) for i in range(N+1)]
    LastTask = [np.zeros(P+1) for i in range(N+1)]
    
    for q in range(1,P+1):
        for i in range(1,N+1):
            l_m = -1
            dp[i][q] = dp[i-1][q]
            
            L = len(channels[i-1].p)
            for l in range(L):
                if q - channels[i-1].p[l] >= 0 and dp[i-1][q - channels[i-1].p[l] ] + channels[i-1].r[l] >= dp[i][q]:
                    dp[i][q] = dp[i-1][q - channels[i-1].p[l] ] + channels[i-1].r[l] 
                    l_m = l
                
            LastTask[i][q] = l_m
            
    q = P
    for i in range(N,0, -1):
        l_m = int(LastTask[i][q])
        if l_m == -1:
            continue;
        x[i-1][int(l_m)] = 1
        q -= channels[i-1].p[l_m]
        if q <= 0:
            break
        
    print(dp)
    
    return x


#x_1 = dp_solution(channels, P)

#check_answer(channels, x_1)


# DP Solution 2

def dp_solution_2(channels, P):
    N = len(channels)
    x = [len(channels[i].p) * [0] for i in range(len(channels))]
    
    U = 0
    for i in range(N):
        U += channels[i].r[-1]
    
    dp = np.array( [(U+1)*[np.infty] for i in range(N+1)] )
    LastTask = [np.zeros(U+1) for i in range(N+1)]
    
    for i in range(N):
        dp[i][0] = 0;
    
    r_m = U
    for q in range(1,U+1):
        for i in range(1,N+1):
            l_m = -1
            dp[i][q] = dp[i-1][q]
            L = len(channels[i-1].r)
            for l in range(L):
                if q - channels[i-1].r[l] >= 0 and dp[i-1][q - channels[i-1].r[l] ] + channels[i-1].p[l] <= dp[i][q]:
                    dp[i][q] = dp[i-1][q - channels[i-1].r[l] ] + channels[i-1].p[l] 
                    l_m = l
                elif q - channels[i-1].r[l] < 0 and channels[i-1].p[l] <= dp[i][q]:
                    dp[i][q] = channels[i-1].p[l]
                    l_m = l
            LastTask[i][q] = l_m
        

        if dp[N][q] > P:
            r_m = q - 1
            break;

    q = r_m 
    for i in range(N,0, -1):
        l_m = int(LastTask[i][q])
        if l_m == -1:
            continue;
        x[i-1][int(l_m)] = 1
        q -= channels[i-1].r[l_m]
        if q <= 0:
            break;
    
    return x

x_2 = dp_solution_2(channels, P)

check_answer(channels, x_2)

