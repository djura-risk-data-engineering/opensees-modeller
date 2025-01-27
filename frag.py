import numpy as np
import json
from scipy import stats
from pathlib import Path
from src.demolition import Demolition
from src.fragility import plot_fragility, Fragility, retrieve_demand_for_calc
from src.demand import Demand, convert_demands, convert_list_to_ndarray

path = Path(__file__).parent / "figs"
filename = Path(__file__).parent / "out/msaTomas.json"
demands = json.load(open(filename))
demands = convert_demands(demands)
demands = convert_list_to_ndarray(demands)

# Get residuals
demo = Demolition(demands)
residuals = demo.get_residuals()

# Process demands
dem_obj = Demand(demands, non_directional_factor=1, modelling_uncertainty=None)
imls = dem_obj.imls
demands = dem_obj.demand
demands_nd = dem_obj.get_non_directional_demands()
nst = int(demands_nd.shape[2] / 2)

# Fragility functions
frag_obj = Fragility(imls)
iml_range = frag_obj.iml_range

# Collapse fragility
frag_col = frag_obj.collapse_capacity(
    demands, dcap=10.0
)

# Demolition fragility
demolition = {'median': 1.5, 'beta': 0.3}
frag_demo = frag_obj.demolition_capacity(
    residuals, demolition['median'], demolition['beta'])

# Probability of exceedances gor a given demand
# For PSD add '+ nst'
level = 1 + nst
# For PFA just the floor level
# level = 1

# directionality can be None for non-directional componentns
# __ 1 for components in 1st direction
# __ 2 for componetns in 2nd direction
dem = retrieve_demand_for_calc(
    directionality=None,
    level=level,
    demands_nd=demands_nd,
    demands=demands
)

medians, betas = frag_obj.edp_given_im(dem)

betas[betas < 0.01] = 0.01

psd = np.linspace(0, 20.0, 1001)[1:]
probs = stats.norm.pdf(np.log(
    psd / medians[:, np.newaxis]) / betas[:, np.newaxis],
    loc=0, scale=1)


# Plotting a fragility function
x = np.linspace(0, 2, 100)
mean = 0.5
std = 0.5
colors = ['r']
fig, ax = plot_fragility(x, "EDP",
                         mean=mean,
                         std=std,
                         colors=colors)

fig.savefig(path / "frag.svg", bbox_inches="tight", format="svg")
