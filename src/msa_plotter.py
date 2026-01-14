import numpy as np
import matplotlib.pyplot as plt
from .plot_styles import *


class MSAPlotter:
    def __init__(self, out) -> None:
        self.out = out

    def get_return_periods(self):
        rp = []
        for period in self.out.keys():
            rp.append(int(period))
        rp.sort()

        return rp

    def get_edp(self, direction, storey, edptype, rps, factor=1.0):
        edptype = edptype.lower()
        edp = []
        # For each return period
        for rp in rps:
            rp = str(rp)
            if edptype == "drift" or edptype == "psd":
                try:
                    edp.append(self.out[rp][str(direction)]
                               [edptype][str(storey)])
                except KeyError:
                    edp.append(self.out[rp][str(direction)]
                               ["PSD"][str(storey)])

            else:
                # acc
                try:
                    critical = np.array(max(
                        self.out[rp][str(1)][edptype][str(storey)],
                        self.out[rp][str(2)][edptype][str(storey)])) \
                        * factor
                except KeyError:
                    critical = np.array(max(
                        self.out[rp][str(1)]["PFA"][str(storey)],
                        self.out[rp][str(2)]["PFA"][str(storey)])) \
                        * factor

                edp.append(list(critical))

        return edp

    def plot_vs_rp(self, edp, rp, xlabel=None, ylabel=None,
                   xlimit=None, ylimit=None):
        def median(lst):
            n = len(lst)
            s = sorted(lst)
            return (s[n // 2 - 1] / 2.0 + s[n // 2] / 2.0, s[n // 2])[n % 2] \
                if n else None

        average = []
        for i in edp:
            average.append(median(i))

        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        for i in range(len(edp)):
            x = edp[i]
            y = [rp[i]] * len(edp[i])
            if i == 0:
                label = "Records"
            else:
                label = None
            plt.scatter(
                x, y, color=color_grid[3], marker="o", label=label)

        plt.plot(
            average, rp, color=color_grid[0], marker="o", label="Median")
        plt.xlabel(xlabel, fontsize=FONTSIZE)
        plt.ylabel(ylabel, fontsize=FONTSIZE)
        plt.grid(True, which="major", axis='both', ls="--", lw=1.0)
        plt.grid(True, which="minor", axis='both', ls="--", lw=0.5)
        plt.yscale("log")
        if xlimit is not None and ylimit is not None:
            plt.xlim([0, xlimit])
            plt.ylim([1, ylimit])
        plt.rc('xtick', labelsize=FONTSIZE)
        plt.rc('ytick', labelsize=FONTSIZE)

        ax.legend(frameon=False, loc='best', fontsize=8)

        return fig, ax
