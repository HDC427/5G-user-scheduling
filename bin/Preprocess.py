# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
from Channel import Channel
from Solution import Solution

channel = Channel.read_testfile(3)

for i in range(Channel.N(Channel)):
    channel[i].preprocess_IP()
    channel[i].preprocess_LP()

S = Solution(channel)

S.BB_solution()
S.show_answer()



