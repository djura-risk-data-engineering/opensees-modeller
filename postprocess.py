from pathlib import Path
from src.msa_postprocessor import MSAPostprocessor
from src.utilities import export_results


msa_path = Path.cwd() / "out"


model = MSAPostprocessor(msa_path)
out = model.postprocess(5, imls=[0.1], return_periods=[50])

export_results(msa_path / "msa", out, "json")
