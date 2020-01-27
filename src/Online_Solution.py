# -*- coding: utf-8 -*-

import numpy as np

class Online_Solution():
    
    p = 100
    p_max = 50
    r_max = 100
    M = 2
    N = 4
    K = 10
    
    def __init__(cls):
        
        cls.powers = np.random.randint((cls.N, cls.M, cls.K), cls.p_max)
        cls.rates = np.random.randint((cls.N, cls.M, cls.K), cls.r_max)