from pathlib import Path
from src.gm_records import get_records
from src.msa_mp import MSA_MP
from src.rcmrf import RCMRF


if __name__ == "__main__":
    path = Path.cwd()
    outputs_dir = path / "outs"
    gmdir = path / "data/MSA_Records"
    gmfilenames = ["GMR_filenames.txt", "GMR_dts.txt"]

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
        multiprocess=True,
        damping=eigenvalues["Damping"][0],
        omegas=eigenvalues["CircFreq"],
        analysis_time_step=0.005
    )

    msa.start(records, workers=4)
