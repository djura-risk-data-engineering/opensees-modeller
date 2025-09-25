from pathlib import Path
from src.rcmrf import RCMRF
from src.utilities import create_path


if __name__ == "__main__":
    path = Path(__file__).parent
    outputs_dir = path / "outs"
    create_path(outputs_dir)

    gmdir = path / "data/MSA_Records"

    model = RCMRF(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
    )

    model.modeller()
    model.wipe()
