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
            while len(S) >1 and \
                  (self.r[j]-self.r[S[-1]]) * (self.p[S[-1]]-self.p[S[-2]]) >= \
                  (self.r[S[-1]]-self.r[S[-2]]) * (self.p[j]-self.p[S[-1]]):
                      S.pop(-1)
            S.append(j)
            
        self.L = self.L[S]
        self.p = self.p[S]
        self.r = self.r[S]

    @classmethod
    def read_testfile(cls, x):
        '''x is the number of testfile'''
        
        f = open("F:/X/2A/P2/INF421/testfiles/test%d.txt"%x)
        cls.__N = int(eval(f.readline()))
        cls.__M = int(eval(f.readline()))
        cls.__K = int(eval(f.readline()))
        cls.__p = int(eval(f.readline()))
        cls.__size = cls.__M * cls.__K
        
        pr_data = np.loadtxt(f, dtype=np.int)
        
        channel = []
        for i in range(cls.__N):
            channel.append(Channel(pr_data[i*cls.__K:(i+1)*cls.__K, :], \
                                   pr_data[(i+cls.__N)*cls.__K:(i+cls.__N+1)*cls.__K, :]))
        #for the ith channel, rows [i*K,(i+1)*K[ are its values of p, rows [(i+N)*K,(i+N+1)*K[ are those of r
        
        return channel
    
    def display(self):
        plt.plot(self.p, self.r)
        
        
        