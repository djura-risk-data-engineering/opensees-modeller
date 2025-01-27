from src.msa_plotter import MSAPlotter
from pathlib import Path
import json

path = Path(__file__).parent / "figs"
filename = Path(__file__).parent / "out/msaTomas.json"
demands = json.load(open(filename))

direction = 1   # Can be 1 or 2

# For PSD it can be from 1 to number of storeys
# For PFA it can be from 0 to number of storeys
storey = 1

# drift or PSD
# acc or PFA
edptype = "drift"
xlabel = f"PSD, storey {storey+1}"

ylabel = "Return period [year]"
xlimit = 1.5
ylimit = None

p = MSAPlotter(demands)
rp = p.get_return_periods()

# factor is a non_directional_factor
edp = p.get_edp(direction, storey, edptype, rp, factor=1.0)
fig, ax = p.plot_vs_rp(edp, rp, xlabel, ylabel, xlimit, ylimit)

fig.savefig(path / "msa.svg", bbox_inches="tight", format="svg")
