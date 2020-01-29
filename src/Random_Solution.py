import numpy
import matplotlib.pyplot as plt

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
        self.powers = numpy.random.randint(1, self.p_max + 1, (self.K, self.N * self.M))
        self.rates = numpy.random.randint(1, self.r_max + 1, (self.K, self.N * self.M))

    def onlineScheduling(self, seuil):
        res = [];
        channel_used = []
        payoff_record = []
        total_utility = 0;
        total_power = 0;
        for k in range(self.K):
            power_k = self.powers[k]
            rate_k = self.rates[k];
            payoff = rate_k
            payoff_sorted = numpy.sort(payoff)

            max_payoff = 0
            for i in range(self.M * self.N - 1, -1, -1):
                max_payoff = payoff_sorted[i]
                max_index = numpy.where(payoff == max_payoff)[0][0]
                if total_power + self.powers[k, max_index] <= self.p:
                    break

            if max_payoff >= seuil:

                max_channel = max_index // self.M
                max_m = max_index % self.M
                if max_channel not in channel_used:
                    channel_used.append(max_channel)
                    res.append([max_channel, max_m])

                    total_utility += self.rates[k, max_index]
                    total_power += self.powers[k, max_index]
                else:
                    res.append([-1, -1])
            else:
                res.append([-1, -1])

        # print("total utility: ", total_utility)
        # print("total power: ", total_power)
        # print(res)
        return res, total_utility, total_power


def statisticalAnalyse(lower_bound, upper_bound, n):
    max_utility = []
    for _ in range(n):
        os = Online_Solution()
        utility_serie = []
        for i in numpy.arange(lower_bound, upper_bound, 1):
            t = os.onlineScheduling(i)
            utility_serie.append(t[1])
        max_utility.append(max(utility_serie))

    fig = figure(title='max Utility', width=490, height=300, background_fill_color="#fafafa")
    hist, edges = numpy.histogram(max_utility, bins=20)
    fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
             fill_color="navy", line_color="white", alpha=0.5, legend="simulation")
    fig.yaxis.axis_label = 'count'
    fig.xaxis.axis_label = 'max Utility'
    fig.grid.grid_line_color = "white"

    plt.hist(max_utility)
    plt.show()
    print("average max utility: ", sum(max_utility)/n)
    return fig


show(statisticalAnalyse(50, 100, 1000))
