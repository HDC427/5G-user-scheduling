# -*- coding: utf-8 -*-

from Channel import Channel
import queue
import numpy as np

class Solution:
    
    def __init__(cls, channels):
        cls.__channels = channels
        cls.__len = len(cls.__channels)
        cls.p = 0
        cls.r = 0
        cls.LP = False
        
    def __assign(cls, i, l):
        '''assign to channel[i] the lth datum'''
        cls.__channels[i].power = cls.__channels[i].p[l]
        cls.__channels[i].rate = cls.__channels[i].r[l]
        cls.__channels[i].to_k_m(cls.__channels[i].L[l])
        
    def get_answer(cls):
        
        cls.p = 0
        cls.r = 0
        
        if cls.LP:
            for i in range(cls.__len):
                cls.p += sum(cls.__channels[i].p*cls.__channels[i].x)
                cls.r += sum(cls.__channels[i].r*cls.__channels[i].x)
        else:
            for i in range(cls.__len):
                cls.p += cls.__channels[i].power
                cls.r += cls.__channels[i].rate
                
        return cls.p, cls.r
            
    def show_answer(cls):
        
        print('Power budget:', Channel.P)
        
        if cls.LP:
           for i in range(cls.__len):
               print(cls.__channels[i].x)
        else:
            print('channel(n)\t p\t r\t user(k), m')
            for i in range(cls.__len):
                print('\t',i+1,'\t',cls.__channels[i].power,'\t',cls.__channels[i].rate,'\t',cls.__channels[i].k, ',', cls.__channels[i].m)
            
        print("total power: ", cls.p , "; total utility: ", cls.r)
        
    def __e(cls, l, i):
        if 0 < l and l < len(cls.__channels[i].p):
            return (cls.__channels[i].r[l] - cls.__channels[i].r[l-1] )/(cls.__channels[i].p[l] - cls.__channels[i].p[l-1])
        elif l == 0:
            return cls.__channels[i].r[0] / cls.__channels[i].p[0]
        else:
            return -1;
        
    def greedy_solution(cls):
        '''
        Each time we choose the channel whose current value of e
        is maximal to augment its power allocation by one step
        for the last allocation to satisfy the power budget restriction
        we may not augment by one full step and we calculate the ratio
        '''
        cls.LP = True
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        #chosen[n-1]=l means to allocate p_n,l to channel n
        chosen = [-1 for i in range(cls.__len)]
        
        #simulate a priority queue
        #PriorQ[:,1] are the serial numbers of channels
        #PriorQ[:,0] are the corresponding e values
        PriorQ = np.c_[[cls.__e(0, i) for i in range(cls.__len)], range(cls.__len)]
        
        p_current = 0
        while p_current < P:
            
            PriorQ = PriorQ[PriorQ[:,0].argsort()]
            if PriorQ[-1,0] == -1:
                break
            #augmenting channel
            ac = int(PriorQ[-1,1])
            
            #the power of ac advance by one step
            if chosen[ac] >= 0:
                p_current += cls.__channels[ac].p[chosen[ac]+1]  - cls.__channels[ac].p[chosen[ac]]
            else:
                p_current += cls.__channels[ac].p[0]
            chosen[ac] += 1
            
            PriorQ[-1,0] = cls.__e(chosen[ac]+1, ac)
        
        if P >= p_current:
            for i in range(cls.__len):
                if chosen[i] >= 0:
                    cls.__channels[i].x[chosen[i]] = 1
        else:
            last_assignment = int(PriorQ[-1,1])
            for i in range(cls.__len):
                if i != last_assignment:
                    if chosen[i] >= 0:
                        cls.__channels[i].x[chosen[i]] = 1
                elif chosen[i] > 0:
                    cls.__channels[i].x = cls.__channels[i].x.astype(np.float)
                    epsilon = (p_current - P)/(cls.__channels[i].p[chosen[i]] - cls.__channels[i].p[chosen[i]-1])
                    cls.__channels[i].x[chosen[i]-1] = epsilon
                    cls.__channels[i].x[chosen[i]] = 1 - epsilon
                    
    def DP_solution(cls):
        '''
        We define Pr(i,q) the problem of maximizing the total utility
        with the first i channels and power budget q
        we have the following DP equations
        Pr(i,q) = max_l{Pr(i-1,q-p_{i,l})+r_{i,l} i>0
        Pr(0,q) = 0
        '''
        cls.LP = False
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
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
        '''
        We define pr(i,q) the problem of minimizing the total power
        with the first i channels to achieve a utility of q <= U = sum(channels.r_max)
        we have the following DP equations
        pr(i,q) = min_l{pr(i-1,q-r_{i,l})+p_{i,l} i>0
        pr(i,q) = 0 q<0
        pr(i,0) = 0
        '''
        cls.LP = False
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        U = 0
        for i in range(cls.__len):
            U += cls.__channels[i].r[-1]
        
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
        '''
        We define Q(L_1,...,L_N) the problem of finding the upper utility bound
        with the restriction channel[n].p <= channel[n].p[L_n]
        each loop we decrease one of the L_n by 1 and add
        Q(L_1,...,L_n-1,...,L_N) to the tree
        if sum_n(channel[n].p[L_n]) <= budget, we get a feasible allocation
        and we no further decreasing L_n only leads to worse solution
        so we stop adding sub-nodes for this branch 
        '''
        cls.LP = False
        
        for i in range(cls.__len):
            cls.__channels[i].reset()
            
        P = Channel.P
        
        r_max = 0
        chosen = []
        
        root = [cls.__channels[i].size()-1 for i in range(cls.__len)]
        root.append(cls.__len) #*
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
            #* we added a supplemental element to help avoid adding duplicate nodes
            for i in range(l[-1]):
                if l[i] > 0:
                    l_new = l.copy()
                    l_new[i] -= 1
                    l_new[-1] = i+1
                    Q.append(l_new)
                    
        if chosen:
            for i in range(cls.__len):
                cls.__assign(i, chosen[i])
        
        