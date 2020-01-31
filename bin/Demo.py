# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
    
import matplotlib.pyplot as plt
from Channel import Channel
from Solution import Solution

channel = Channel.read_testfile(2)

for i in range(Channel.N):
    #channel[i].display('original')
    channel[i].preprocess_simple()
    channel[i].preprocess_IP()
    #channel[i].display('IP preprocess')
    channel[i].preprocess_LP()
    #channel[i].display('LP preprocess')

S = Solution(channel)

S.greedy_solution()
S.get_answer(True)
S.show_answer(True)



