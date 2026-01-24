from src.msa_plotter import MSAPlotter
import json
from pathlib import Path
import matplotlib.pyplot as plt

path = Path(__file__).parent

msa_path = path / 'outputs' / 'MSA'
filename = msa_path / "msa.json"
demands = json.load(open(filename))


tresholds = [0.4, 1.0, 1.8, 2.6]  # EDP thresholds
colors = ['green', 'orange', 'red', 'black']

plotter = MSAPlotter(demands)
rps = plotter.get_return_periods()
edps = plotter.get_edp(1, 'global', 'psd', rps)
plotter.plot_vs_rp(edps, rps, xlabel='MIDR [%]', ylabel='Return Period')
for i in range(4):
    plt.axvline(x=tresholds[i], color=colors[i], linestyle="--",
                lw=2, label=(f'DLS-{i + 1}'))
plt.xlim(left=0)
plt.ylim([min(rps)*0.9, max(rps)*1.1])
plt.legend()
plt.show()
