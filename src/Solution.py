# -*- coding: utf-8 -*-

from Channel import Channel
import numpy as np

class Solution:
    
    def __init__(cls, channels):
        cls.__channels = channels
        cls.__len = len(cls.__channels)
    
    def show_answer(cls):
        
        r = 0
        p = 0
        
        print(Channel.P)
        
        for i in range(cls.__len):
            print("channel %d: "%(i+1) , cls.__channels[i].x)
            print(cls.__channels[i].p)
            print(cls.__channels[i].r)
            p += sum(cls.__channels[i].x*cls.__channels[i].p)
            r += sum(cls.__channels[i].x*cls.__channels[i].r)
        print("total power: ", p , "; total utility: ", r)
        
    def __e(cls, l, i):
        if 0 < l and l < len(cls.__channels[i].p):
            return (cls.__channels[i].r[l] - cls.__channels[i].r[l-1] )/(cls.__channels[i].p[l] - cls.__channels[i].p[l-1])
        elif l == 0:
            return cls.__channels[i].r[0] / cls.__channels[i].p[0]
        else:
            return -1;
        
    def greedy_solution(cls):
        
        P = Channel.P
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
        
        p_current = 0;
        l = [0 for i in range(cls.__len)]
        while p_current < P:
            e_max = -1
            n_max = 0
            for i in range(cls.__len):
                e_current = cls.__e(l[i],i)
                if e_current >= e_max:
                    e_max = e_current
                    n_max = i
    
            if e_max <= 0:
                break 
    
            if l[n_max] > 0:
                p_current += cls.__channels[n_max].p[l[n_max]]  - cls.__channels[n_max].p[l[n_max]-1]
            else:
                p_current += cls.__channels[n_max].p[l[n_max]]
            l[n_max] += 1
        
        if P == p_current:
            for i in range(cls.__len):
                cls.__channels[i].x[l[i]] = 1
        elif P < p_current:
            for i in range(cls.__len):
                if i != n_max:
                    if l[i] > 0:
                        cls.__channels[i].x[l[i]-1] = 1
                else:
                    cls.__channels[i].x = cls.__channels[i].x.astype(np.float)
                    epsilon = (p_current - P)/(cls.__channels[i].p[l[i]] - cls.__channels[i].p[l[i]-1])
                    cls.__channels[i].x[l[i]-1] = epsilon
                    cls.__channels[i].x[l[i]] = 1 - epsilon
                    
    def DP_solution(cls):
        
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
            cls.__channels[i-1].x[l] = 1
            q -= cls.__channels[i-1].p[l]
            if q <= 0:
                break
    
    def DP_solution_2(cls):
        
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
            cls.__channels[i-1].x[l] = 1
            q -= cls.__channels[i-1].r[l]
            print(q)
            if q <= 0:
                break;
    
    def BB_solution(cls):
        
        P = Channel.P
        
        r_max = 0
        chosen = []
        Q = [[cls.__channels[i].size()-1 for i in range(cls.__len)]]
        
        while Q:
            l = Q.pop(0)
            #l[i] is the upper bound for the index of channel[i].p
#            p_c = sum(cls.__channels[i].p[l[i]] for i in range(cls.__len))
#            print(l, p_c)
#            
#            
#            time.sleep(1)
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
            for i in range(cls.__len):
                if l[i] > 0:
                    l_new = l.copy()
                    l_new[i] -= 1
                    Q.append(l_new)
                    
        if chosen:
            for i in range(cls.__len):
                cls.__channels[i].x[chosen[i]] = 1
        
        