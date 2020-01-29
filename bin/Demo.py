# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
    
import matplotlib.pyplot as plt
from Channel import Channel
from Solution import Solution

channel = Channel.read_testfile(5)

for i in range(Channel.N(Channel)):
    channel[i].display('original')
    channel[i].preprocess_IP()
    channel[i].display('IP preprocess')
    channel[i].preprocess_LP()
    channel[i].display('LP preprocess')
    
    plt.savefig('../report/channel%d.png'%i)
    plt.close()

S = Solution(channel)

S.DP_solution()
S.show_answer()



