
import time
import numpy as np
import matplotlib.pyplot as plt

from Channel import Channel
from Solution import Solution


class Online_Solution:

    def __init__(self, cls):
        self.N = 4
        self.K = 10
        self.M = 2
        self.p_max = 50
        self.r_max = 100
        self.p = 100;
        self.powers = np.random.randint(1, self.p_max + 1, (self.K, self.N, self.M))
        self.rates = np.random.randint(1, self.r_max + 1, (self.K, self.N, self.M))
        cls.best_threshold = 0;

    def onlineScheduling(self, seuil):
        '''Online Solution given a seuil'''
        global max_index
        res = [];
        channel_used = []
        payoff_record = []
        total_utility = 0;
        total_power = 0;
        for k in range(self.K):
            power_k = self.powers[k].flatten()
            rate_k = self.rates[k].flatten();
            '''the value of payoff is simply the rate'''
            payoff = 1 * rate_k
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

        return res, total_utility, total_power


class Result_Analyse:
    def statisticalAnalyse(n = 100, lower_bound = 0, upper_bound = 100):
        '''repeat n times the random online scheduling.'''
        '''Search and return  the best threshold from lower_bound to upper_bound'''
        max_utility_online = []
        max_power_online = []
        best_threshold = []


        for _ in range(n):
            os = Online_Solution(Online_Solution)
            utility_serie = []
            power_serie = []
            for i in np.arange(lower_bound, upper_bound, 1):
                t = os.onlineScheduling(i)
                utility_serie.append(t[1])
                power_serie.append(t[2])
            max_utility_online.append(max(utility_serie))
            max_power_online.append(max(power_serie))
            best_threshold.append(np.argmax(utility_serie) + lower_bound)

        print("average best threshold: ", np.mean(best_threshold))
        return np.mean(best_threshold);

    def OptimalSolutionComparison(best_threshold):
        '''Show the difference between the Online Solution and Optimal Solution'''
        fig, ax = plt.subplots(2, 2)
        fig_online, ax_online = plt.subplots(2, 2)


        os = Online_Solution(Online_Solution)
        t = os.onlineScheduling(best_threshold)
        online_rate = t[1]
        online_power = t[2]
        res = t[0]
        channel_online = [[-1,-1], [-1,-1], [-1,-1], [-1,-1] ];
        for i in range(len(res)):
            if res[i][0] != -1:
                channel_online[ res[i][0] ] = [ os.powers[i, res[i][0], res[i][1]], os.rates[i, res[i][0], res[i][1]] ]
        channel = []
        for i in range(os.N):
            channel.append(Channel(Channel, os.N, os.M, os.K, os.p, \
                                   os.powers[:, i, :], \
                                   os.rates[:, i, :]))

        #        for i in range(Channel.N):
        #            channel[i].preprocess_simple()
        #            channel[i].preprocess_IP()
        #            channel[i].preprocess_LP()

        S = Solution(channel)
        S.DP_solution()
        p, r = S.get_answer()

        for i in range(Channel.N):
            ax[i // 2, i % 2].scatter(channel[i].p, channel[i].r)
            ax[i // 2, i % 2].scatter(channel[i].power, channel[i].rate)
            fig.suptitle("DP Solution")

            ax_online[i // 2, i % 2].scatter(channel[i].p, channel[i].r)
            ax_online[i // 2, i % 2].scatter(channel_online[i][0], channel_online[i][1])
            fig_online.suptitle("Online Solution")

        print("total power consumed by online solution : ", online_power)
        print("total rate gotten by online solution : ", online_rate)
        print("total power consumed by DP solution : ", p)
        print("total rate gotten by DP solution : ", r)

        return fig, fig_online


