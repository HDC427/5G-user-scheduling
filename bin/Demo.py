# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
    
import matplotlib.pyplot as plt
from Channel import Channel
from Solution import Solution


def display(ax, channel, label):
    ax.plot(channel.p. channel.r, label=label)

fig, ax = plt.subplots(5, 1)
fig.set_figheight(20)
for f in range(5):
    print('testfile%d'%(f+1))
    channel = Channel.read_testfile(f+1)
    
    ax[f].plot(channel[0].p, channel[0].r, label = 'original', color='black')
    size = [Channel.N*Channel.K*Channel.M]
    
    for i in range(Channel.N):
        channel[i].preprocess_simple()
    ax[f].plot(channel[0].p, channel[0].r, label = 'simple preprocess')
    size.append(sum([channel[i].size() for i in range(Channel.N)]))
    
    for i in range(Channel.N):
        channel[i].preprocess_IP()
    ax[f].plot(channel[0].p, channel[0].r, label = 'IP preprocess')
    size.append(sum([channel[i].size() for i in range(Channel.N)]))   
    
    for i in range(Channel.N):
        channel[i].preprocess_LP()
    ax[f].plot(channel[0].p, channel[0].r, label = 'LP preprocess')
    size.append(sum([channel[i].size() for i in range(Channel.N)]))
    
    print(size)
  
plt.legend()
    
    
#    S = Solution(channel)
#    
#    S.greedy_solution()
#    S.get_answer(True)
#    S.show_answer(True)



