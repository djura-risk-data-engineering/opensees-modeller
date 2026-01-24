from pathlib import Path
from src.ida_postprocessor import IDAPostprocessor

from src.utilities import export_results

path = Path(__file__).resolve().parent

ida_records = path / "data/IDA-Records"
ida_path = path / "outputs/IDA"


p = IDAPostprocessor(
    ida_path,
    ida_path / "IM.csv",
    gm_folder=ida_records,
)

results, cache = p.postprocess(n_dir=1)

export_results(ida_path / "ida", results, "json")
export_results(ida_path / "ida", cache, "pickle")
