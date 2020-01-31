# -*- coding: utf-8 -*-

from Channel import Channel
import numpy as np

class Solution:
    
    def __init__(cls, channels):
        cls.__channels = channels
        cls.__len = len(cls.__channels)
        cls.p = 0
        cls.r = 0
        
    def __assign(cls, i, l):
        '''assign to channel[i] the lth datum'''
        cls.__channels[i].power = cls.__channels[i].p[l]
        cls.__channels[i].rate = cls.__channels[i].r[l]
        cls.__channels[i].to_k_m(cls.__channels[i].L[l])
        
    def get_answer(cls, LP=False):
        
        if LP:
            for i in range(cls.__len):
                cls.p += sum(cls.__channels[i].p*cls.__channels[i].x)
                cls.r += sum(cls.__channels[i].r*cls.__channels[i].x)   
            
        else:
            for i in range(cls.__len):
                cls.p += cls.__channels[i].power
                cls.r += cls.__channels[i].rate
                
        return cls.p, cls.r
            
    def show_answer(cls, LP=False):
        
        print('Power budget:', Channel.P)
        
        if LP:
           for i in range(cls.__len):
               print(cls.__channels[i].x)
        else:
            print('channel(n)\t p\t r\t user(k), m')
            for i in range(cls.__len):
                print('\t',i+1,'\t',cls.__channels[i].power,'\t',cls.__channels[i].rate,'\t',cls.__channels[i].k, ',', cls.__channels[i].m)
            
        print("total power: ", cls.p , "; total utility: ", cls.r)
        
    def __e(cls, l, i):
        if 0 < l and l < len(cls.__channels[i].p)-1:
            return (cls.__channels[i].r[l] - cls.__channels[i].r[l-1] )/(cls.__channels[i].p[l] - cls.__channels[i].p[l-1])
        elif l == 0:
            return cls.__channels[i].r[0] / cls.__channels[i].p[0]
        else:
            return -1;
        
    def greedy_solution(cls):
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        p_current = 0
        l = [-1 for i in range(cls.__len)]
        
        e_max = -1
        n_max = 0
        
        while p_current < P:
            for i in range(cls.__len):
                e_current = cls.__e(l[i]+1, i)
                if e_current >= e_max:
                    e_max = e_current
                    n_max = i
    
            if e_max <= 0:
                break 
            
            if l[n_max] >= 0:
                p_current += cls.__channels[n_max].p[l[n_max]+1]  - cls.__channels[n_max].p[l[n_max]]
            else:
                p_current += cls.__channels[n_max].p[0]
            l[n_max] += 1
        
        print(n_max)
        print('l', l)
        if P == p_current:
            for i in range(cls.__len):
                if l[i] >= 0:
                    cls.__channels[i].x[l[i]] = 1
        elif P < p_current:
            for i in range(cls.__len):
                if i != n_max:
                    if l[i] >= 0:
                        cls.__channels[i].x[l[i]] = 1
                else:
                    cls.__channels[i].x = cls.__channels[i].x.astype(np.float)
                    epsilon = (p_current - P)/(cls.__channels[i].p[l[i]] - cls.__channels[i].p[l[i]-1])
                    cls.__channels[i].x[l[i]-1] = epsilon
                    cls.__channels[i].x[l[i]] = 1 - epsilon
                    
    def DP_solution(cls):
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        #We define Pr(i,q) the problem of maximizing the total utility
        #with the first i channels and power budget q
        
        #dp[i,q] stores the solution to Pr(i,q) 
        dp = np.zeros((cls.__len+1, P+1), dtype=np.int)
        
        #LastTask[i,q]=l means to solve Pr(i,q), the ith channel should
        #be allocated p_{l,i}
        LastTask = np.zeros((cls.__len+1, P+1), dtype=np.int)
        
        for q in range(1, P+1):
            for i in range(1, cls.__len+1):
                l_m = -1
                dp[i,q] = dp[i-1,q]
                
                L = cls.__channels[i-1].size()
                for l in range(L):
                    if q - cls.__channels[i-1].p[l] >= 0:
                        temp = dp[i-1, q - cls.__channels[i-1].p[l]] + cls.__channels[i-1].r[l]
                        if temp >= dp[i,q]:
                            dp[i,q] = temp 
                            l_m = l
                LastTask[i,q] = l_m
                
        q = P
        for i in range(cls.__len,0, -1):
            l = LastTask[i,q]
            if l == -1:
                continue;
            #cls.__channels[i-1].x[l] = 1
            cls.__assign(i-1, l)
            q -= cls.__channels[i-1].power
            if q <= 0:
                break
    
    def DP_solution_2(cls):
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        U = 0
        for i in range(cls.__len):
            U += cls.__channels[i].r[-1]
        
        #We define pr(i,q) the problem of minimizing the total power
        #with the first i channels to achieve a utility of q
        
        #dp[i,q] stores the solution to pr(i,q)
        dp = np.array( [(U+1)*[np.infty] for i in range(cls.__len+1)] )
        
        #LastTask[i,q]=l means to solve pr(i,q), the ith channel should
        #be allocated p_{l,i}
        LastTask = np.zeros((cls.__len+1, U+1), dtype=np.int)
        
        for i in range(cls.__len):
            dp[i,0] = 0;
        
        r_m = U
        for q in range(1,U+1):
            for i in range(1,cls.__len+1):
                l_m = -1
                dp[i,q] = dp[i-1,q]
                L = cls.__channels[i-1].size()
                for l in range(L):
                    if q - cls.__channels[i-1].r[l] >= 0:
                        temp = dp[i-1, q - cls.__channels[i-1].r[l]] + cls.__channels[i-1].p[l]
                        if temp <= dp[i,q]:
                            dp[i,q] = temp 
                            l_m = l
                    elif cls.__channels[i-1].p[l] <= dp[i,q]:
                        dp[i,q] = cls.__channels[i-1].p[l]
                        l_m = l
                LastTask[i,q] = l_m
            
            #If solving pr(N,q) surpasses already the budget,
            #no need to go further, and so the feasible 
            #maximun utitily is q-1
            if dp[cls.__len, q] > P:
                r_m = q - 1
                break;
    
        q = r_m 
        for i in range(cls.__len,0, -1):
            l = LastTask[i,q]
            if l == -1:
                continue;
            #cls.__channels[i-1].x[l] = 1
            cls.__assign(i-1, l)
            q -= cls.__channels[i-1].rate
            if q <= 0:
                break;
    
    def BB_solution(cls):
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        r_max = 0
        chosen = []
        
        root = [cls.__channels[i].size()-1 for i in range(cls.__len)]
        root.append(cls.__len)
        Q = [root]
        
        while Q:
            print(Q)
            l = Q.pop(0)
            #l[i] is the upper bound for the index of channel[i].p
           
            if sum(cls.__channels[i].p[l[i]] for i in range(cls.__len)) <= P:
                if sum(cls.__channels[i].r[l[i]] for i in range(cls.__len)) > r_max:
                    #case (2): we find a feasible solution so we update the max
                    r_max = sum(cls.__channels[i].r[l[i]] for i in range(cls.__len))
                    chosen = l
                #case (1): the upper bound is less than the current max
                #in both case we do not add subnode of l to Q
                continue
            
            #we add a new node to Q as long as one upper bound can be decreased
            #if no upper bounds can be decreased, this is cas (3) and no subnode of l is added
            for i in range(l[-1]):
                if l[i] > 0:
                    l_new = l.copy()
                    l_new[i] -= 1
                    l_new[-1] = i+1
                    Q.append(l_new)
                    
        if chosen:
            for i in range(cls.__len):
                cls.__assign(i, chosen[i])
        
        