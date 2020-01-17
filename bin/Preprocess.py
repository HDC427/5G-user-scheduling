# -*- coding: utf-8 -*-

import sys
if '../' not in sys.path:
    sys.path.append('../')
    sys.path.append('../src')
from Channel import Channel

channel = Channel.read_testfile(5)

channel[0].display()
channel[0].preprocess_IP()
channel[0].display()
channel[0].preprocess_LP()
channel[0].display()