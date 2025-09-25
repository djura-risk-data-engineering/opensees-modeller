from pathlib import Path
import numpy as np
from src.msa_postprocessor import MSAPostprocessor
from src.utilities import export_results


msa_path = Path(__file__).parent / "outs"


poes = [0.4, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.0025, 0.001, 0.0004, 0.0002, 0.0001]
imls = [0.148, 0.248, 0.377, 0.541, 0.822, 1.08, 1.4, 1.75, 2.29, 2.91, 3.4, 3.98]
inv_t = 50
return_period = np.round(-inv_t / np.log(1 - np.array(poes))).astype(int).tolist()
model = MSAPostprocessor(msa_path)

out = model.postprocess(3, imls=imls, return_periods=return_period)
export_results(msa_path / "msa", out, "json")
