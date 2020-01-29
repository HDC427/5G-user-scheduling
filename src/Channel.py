# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

class Channel:
    
#    N = 0
#    M = 0
#    K = 0
#    __p = 0
    
    def __init__(self, p, r):
        '''input p and r are K*M matrices'''
        self.__originalData = np.array([p, r])
        
        self.p = p.flatten()
        self.r = r.flatten()
        
        #keep track of the current number of p and r, may change 
        #after preprocessing
        self.__size = self.M * self.K
        
        #keep track of the k, m index in __originalData
        self.L = np.argsort(self.p)
        
        #p sorted in increasing order, r reordered accordingly 
        self.p = self.p[self.L]
        self.r = self.r[self.L]
        
        #sum(x*p) is the power allocated
        #sum(x*r) is the rate obtained
        self.x = np.zeros(self.__size, dtype=np.int)
        
        #by referring to channel.k_m, we can know which
        #power for this channel is chosen. -1 indicates the 
        #channel's power is not yet decided
        self.k_m = (-1, -1)
        
        plt.xlabel('power')
        plt.ylabel('rate')
        
    def __delete(self, i):
        
        self.L = np.delete(self.L, i)
        self.p = np.delete(self.p, i)
        self.r = np.delete(self.r, i)
        self.__size -= len(i)
        
    def preprocess_simple(self):
        
        a = []
        for i in range(1, self.__size):
            if self.p[i] > self.P:
                a.append(i)
        
        self.__delete(a)
        
    def preprocess_IP(self):
        
        current_max = self.r[0]
        dominated = []
        for i in range(1, self.__size):
            if self.r[i] >= current_max:
                current_max = self.r[i]
                if self.p[i] == self.p[i-1]:
                    dominated.append(i-1)
            else: dominated.append(i)
        self.__delete(dominated)
        self.x = np.zeros(self.__size, dtype=np.int)
            
    def preprocess_LP(self):
        
        if len(self.p) < 2:
            return
        
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
        
        self.__size = len(S)
        self.x = np.zeros(self.__size, dtype=np.int)

    @classmethod
    def read_testfile(cls, x):
        '''x is the number of testfile'''
        
        f = open("F:/X/2A/P2/INF421/testfiles/test%d.txt"%x)
        cls.N = int(eval(f.readline()))
        cls.M = int(eval(f.readline()))
        cls.K = int(eval(f.readline()))
        cls.P = int(eval(f.readline()))
        
        pr_data = np.loadtxt(f, dtype=np.int)
        
        channel = []
        for i in range(cls.N):
            channel.append(Channel(pr_data[i*cls.K:(i+1)*cls.K, :], \
                                   pr_data[(i+cls.N)*cls.K:(i+cls.N+1)*cls.K, :]))
        #for the ith channel, rows [i*K,(i+1)*K[ are its values of p, rows [(i+N)*K,(i+N+1)*K[ are those of r
        
        return channel
    
    def display(self, lab='label'):
        plt.plot(self.p, self.r, label=lab)
        plt.legend()
        
    def reset(self):
       self.x = np.zeros(self.__size, dtype=np.int)
       self.k_m = (-1, -1)
        
    def to_k_m(self, l):
        #if we choose channel.p[l], we can use this formula to
        #retrieve its k m index in the original data
        self.k_m = (l//self.K, l%self.K)
    
    def size(self):
        return self.__size
        
    