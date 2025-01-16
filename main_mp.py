from pathlib import Path
from src.gm_records import get_records
from src.msa_mp import MSA_MP
from src.rcmrf import RCMRF


if __name__ == "__main__":
    path = Path.cwd()
    outputs_dir = path / "out2"
    gmdir = path / "data/case2/records1"

    gmfilenames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]
    # gmfilenames = ["GMR_names.txt", "GMR_names.txt", "GMR_dts.txt"]

    rcmrf = RCMRF(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
    )

    eigenvalues = rcmrf.get_modal_properties()

    records = get_records(gmdir, gmfilenames, outputs_dir)

    msa = MSA_MP(
        analysis_options=["msa"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
        multiprocess=False,
        damping=eigenvalues["Damping"][0],
        omegas=eigenvalues["CircFreq"],
    )

    msa.start(records, workers=1)
