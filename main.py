from pathlib import Path
from src.rcmrf import RCMRF


if __name__ == "__main__":
    path = Path(__file__).parent
    outputs_dir = path / "out2"
    gmdir = path / "records1"
    gmfilenames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]

    model = RCMRF(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
    )

    model.modeller()

    model.wipe()
