from pathlib import Path
from src.rcmrf import RCMRF


if __name__ == "__main__":
    path = Path(__file__).parent
    outputs_dir = path / "outs"
    gmdir = path / "data/MSA_Records"
    gmfilenames = ["GMR_filenames.txt", "GMR_dts.txt"]

    model = RCMRF(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
    )

    model.modeller()
    model.wipe()
