# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

class Channel:
    
    def __init__(self, cls, N, M, K, P, p, r):
        
        cls.N = N
        cls.M = M
        cls.K = K
        cls.P = P
        
        '''input p and r are both K*M matrices'''
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
        
        #used only in LP problems
        #sum(x*p) is the power allocated
        #sum(x*r) is the rate obtained
        self.x = np.zeros(self.__size, dtype=np.int)
        
        #by referring to channel.k_m, we can know which
        #power for this channel is chosen. -1 indicates the 
        #channel's power is not yet decided
        self.k = -1
        self.m = -1
        self.power = 0
        self.rate = 0
        
    def __delete(self, i):
        
        self.L = np.delete(self.L, i)
        self.p = np.delete(self.p, i)
        self.r = np.delete(self.r, i)
        self.__size = len(self.p)
        
    def preprocess_simple(self):
        
        a = []
        for i in range(1, self.__size):
            if self.p[i] > self.P:
                a.append(i)
        
        self.__delete(a)
        self.x = np.zeros(self.__size, dtype=np.int)
        
    def preprocess_IP(self):
        
        current_max = self.r[0]
        dominated = []
        for i in range(1, self.__size):
            if self.r[i] > current_max:
                current_max = self.r[i]
                if self.p[i] == self.p[i-1]:
                    dominated.append(i-1)
            else: dominated.append(i)
        self.__delete(dominated)
        self.x = np.zeros(self.__size, dtype=np.int)
            
    def preprocess_LP(self):
        
        if len(self.p) < 2:
            return
        
        S = [0, 1]
        
        for j in range(2, self.__size):
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
        '''x is the serial number of testfile'''
        
        f = open("F:/X/2A/P2/INF421/testfiles/test%d.txt"%x)
        N = int(eval(f.readline()))
        M = int(eval(f.readline()))
        K = int(eval(f.readline()))
        P = int(eval(f.readline()))
        
        pr_data = np.loadtxt(f, dtype=np.int)
        
        channel = []
        for i in range(N):
            channel.append(Channel(Channel, N, M, K, P, \
                                   pr_data[i*K:(i+1)*K, :], \
                                   pr_data[(i+N)*K:(i+N+1)*K, :]))
        #for the ith channel, rows [i*K,(i+1)*K[ are its values of p, rows [(i+N)*K,(i+N+1)*K[ are those of r
        
        return channel
        
    def reset(self):
        self.x = np.zeros(self.__size, dtype=np.int)
        self.k, self.m, self.power, self.rate = -1, -1, 0, 0
        
    def to_k_m(self, l):
        #if we choose channel.p[l], we can use this formula to
        #retrieve its k m index in the original data
        self.k, self.m = l//self.K+1, l%self.K+1
    
    def size(self):
        return self.__size
        
    