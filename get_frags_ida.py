import numpy as np
import json
from pathlib import Path
from src.demolition import Demolition
from src.fragility import plot_fragility, Fragility
from src.demand import Demand, convert_demands, convert_list_to_ndarray

path = Path(__file__).parent / "figs"
filename = Path(__file__).parent / "outputs/IDA/ida.json"
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
ff = frag_obj.collapse_capacity(
    demands, dcap=2.0, fit='ida', n_dir=1
)

# Plotting a fragility function
x = np.linspace(0, 4, 100)
mean = ff['median']
std = ff['beta']
colors = ['r']
fig, ax = plot_fragility(x, "IM",
                         mean=mean,
                         std=std,
                         colors=colors)
