from pathlib import Path
from ida_postprocessor import IDAPostprocessor

from src.utilities import export_results

path = Path(__file__).resolve().parent

ida_records = path / "assets/SeismicAnalysis/IDA"
ida_path = path / "assets/SeismicAnalysis/NLTHAout/IDA_outputs"


p = IDAPostprocessor(
    ida_path,
    ida_path / "IM.csv",
    gm_folder=ida_records,
)

results, cache = p.postprocess()

export_results(ida_path / "ida", results, "json")
