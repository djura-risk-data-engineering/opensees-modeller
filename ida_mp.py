
if __name__ == '__main__':
    from pathlib import Path
    from src.rcmrf import RCMRF

    path = Path.cwd()
    outputs_dir = path / "dump/outs"
    gmdir = path / "records1/POE-0.0001-in-50-years"

    gmfilenames = ["GMR_H1_names.txt", "GMR_dts.txt"]

    model = RCMRF(
        analysis_options=["ida"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
        dcap=5,
        max_runs=2,
        workers=2
    )

    model.modeller()
    model.wipe()
