from pathlib import Path
from src.rcmrf import RCMRF


if __name__ == "__main__":
    path = Path.cwd()
    outputs_dir = path / "out"
    gmdir = path / "records"

    # gmfilenames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]
    gmfilenames = ["GMR_names.txt", "GMR_names.txt", "GMR_dts.txt"]

    model = RCMRF(
        analysis_options=["msa"],
        workers=2,
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
        multiprocess=True,
    )

    model.bnode = [[7001, 100001, 200002, 300003, 400004],
                   [7001, 100001, 200002, 300003, 400004]]
    model.tnode = [[100001, 200002, 300003, 400004, 500005],
                   [100001, 200002, 300003, 400004, 500005]]

    model.modeller()
