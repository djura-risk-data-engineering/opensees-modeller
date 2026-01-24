import numpy as np
import json
import matplotlib.pyplot as plt
from pathlib import Path
from src.fragility import plot_fragility, Fragility
from src.demand import Demand, convert_demands, convert_list_to_ndarray
from src.utilities import export_results

path = Path(__file__).parent

drift_thresholds = [0.4, 1.0, 1.8, 2.6]
fit = 'msa'

frags = {}

msa_path = path / "outputs/MSA"
filename = msa_path / "msa.json"
demands = json.load(open(filename))
demands = convert_demands(demands)
demands = convert_list_to_ndarray(demands)

# Process demands
dem_obj = Demand(demands, non_directional_factor=1, modelling_uncertainty=None)
imls = dem_obj.imls
demands = dem_obj.demand
demands_nd = dem_obj.get_non_directional_demands()
nst = int(demands_nd.shape[2] / 2)

# Fragility functions
frag_obj = Fragility(imls)
iml_range = np.linspace(0.0, 2*np.max(imls), 1000)

betas = []
medians = []
labels = ['DLS-1', 'DLS-2', 'DLS-3', 'DLS-4']
colors = ['b', 'g', 'r', 'k']

for i, threshold in enumerate(drift_thresholds):
    # Collapse fragility
    frag = frag_obj.collapse_capacity(
        demands, dcap=threshold, fit=fit
    )

    frags[f"DLS-{i+1}"] = {
        'median': frag['median'],
        'beta': frag['beta'],
        'imls': frag['ecdf'][0],
        'ecdf': frag['ecdf'][1]
    }
    betas.append(frag['beta'])
    medians.append(frag['median'])

# Plotting a fragility function
fig, ax = plot_fragility(
    iml_range, "SA(0.5) [g]", mean=medians, std=betas, colors=colors,
    show=False
)
for i in range(4):
    ax.scatter(
        frags[f"DLS-{i+1}"]["imls"], frags[f"DLS-{i+1}"]["ecdf"],
        color=colors[i]
    )

export_results(msa_path / f"frags_{fit}", frags, "json")
fig.savefig(msa_path / f"frag_{fit}.svg", bbox_inches="tight", format="svg")
plt.show()
