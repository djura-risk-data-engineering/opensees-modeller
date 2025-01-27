from pathlib import Path
from src.msa_postprocessor import MSAPostprocessor
from src.utilities import export_results


msa_path = Path(__file__).parent / "out2"


model = MSAPostprocessor(msa_path)

out = model.postprocess(4, imls=[0.1, 0.2], return_periods=[50, 100])
export_results(msa_path / "msa", out, "json")
