import time
import numpy as np
import matplotlib.pyplot as plt

from Channel import Channel
from Solution import Solution

from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.layouts import row, gridplot
from bokeh.models import BoxAnnotation, Span, Label

output_notebook(hide_banner=True)


class Online_Solution:

    def __init__(self):
        self.N = 4
        self.K = 10
        self.M = 2
        self.p_max = 50
        self.r_max = 100
        self.p = 100;
        self.powers = np.random.randint(1, self.p_max + 1, (self.K, self.N, self.M))
        self.rates = np.random.randint(1, self.r_max + 1, (self.K, self.N, self.M))

    def onlineScheduling(self, seuil):
        res = [];
        channel_used = []
        payoff_record = []
        total_utility = 0;
        total_power = 0;
        for k in range(self.K):
            power_k = self.powers[k].flatten()
            rate_k = self.rates[k].flatten();
            payoff = 1*rate_k
            payoff_sorted = np.sort(payoff)

            max_payoff = 0
            for i in range(self.M * self.N - 1, -1, -1):
                max_payoff = payoff_sorted[i]
                max_index = np.where(payoff == max_payoff)[0][0]
                if total_power + power_k[max_index] <= self.p:
                    break

            if max_payoff >= seuil:

                max_channel = max_index // self.M
                max_m = max_index % self.M
                if max_channel not in channel_used:
                    channel_used.append(max_channel)
                    res.append([max_channel, max_m])

                    total_utility += rate_k[max_index]
                    total_power += power_k[max_index]
                else:
                    res.append([-1, -1])
            else:
                res.append([-1, -1])

        # print("total utility: ", total_utility)
        # print("total power: ", total_power)
        # print(res)
        return res, total_utility, total_power
            

def statisticalAnalyse(lower_bound, upper_bound, n):
    max_utility_online = []
    max_power_online = []
    max_utility_real = []
    max_power_real = []
    best_threshold = []
    
    fig, ax = plt.subplots(2, 2)
    
    for _ in range(n):
        os = Online_Solution()
        utility_serie = []
        power_serie = []
        for i in np.arange(lower_bound, upper_bound, 1):
            t = os.onlineScheduling(i)
            utility_serie.append(t[1])
            power_serie.append(t[2])
        max_utility_online.append(max(utility_serie))
        max_power_online.append(max(power_serie))
        best_threshold.append(np.argmax(utility_serie) + lower_bound)
        
        channel = []
        for i in range(os.N):
            channel.append(Channel(Channel, os.N, os.M, os.K, os.p, \
                                    os.powers[:,i,:], \
                                    os.rates[:,i,:]))    
        
#        for i in range(Channel.N):
#            channel[i].preprocess_simple()
#            channel[i].preprocess_IP()
#            channel[i].preprocess_LP()
        
        S = Solution(channel)
        S.DP_solution()
        p, r = S.get_answer()
        
        for i in range(Channel.N):
            ax[i//2, i%2].scatter(channel[i].p, channel[i].r)
            ax[i//2, i%2].scatter(channel[i].power, channel[i].rate)
        
        max_utility_real.append(r)
        max_power_real.append(p)
        
    print("average best threshold: ", np.mean(best_threshold))
    
    #plt.plot(range(n), max_utility_online)
    #plt.plot(range(n), max_utility_real)
#    print(max_utility_online)
#    print(max_utility_real)
#    print(np.mean(np.array(max_utility_real) - np.array(max_utility_online)))


statisticalAnalyse(80, 100, 1)

    
    
    
    

