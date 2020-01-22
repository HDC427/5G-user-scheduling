# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
from Channel import Channel
from Solution import Solution

channel = Channel.read_testfile(5)

channel[1].display()
channel[1].preprocess_IP()
channel[1].display()
channel[1].preprocess_LP()
channel[1].display()

S = Solution(channel)

S.greedy_solution()
S.show_answer()



