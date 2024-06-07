from pathlib import Path
from src.rcmrf import RCMRF
from src.utilities import read_pickle


if __name__ == "__main__":
    path = Path.cwd()
    outputs_dir = path / "out2"
    gmdir = path / "data/case2/records1"

    gmfilenames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]

    model = RCMRF(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
    )

    model.bnode = [[7001, 100001, 200002, 300003, 400004],
                   [7001, 100001, 200002, 300003, 400004]]
    model.tnode = [[100001, 200002, 300003, 400004, 500005],
                   [100001, 200002, 300003, 400004, 500005]]

    model.modeller()

    model.wipe()
