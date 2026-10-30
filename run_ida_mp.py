from pathlib import Path
from src.rcmrf import RCMRF
from src.utilities import create_path


if __name__ == "__main__":
    path = Path(__file__).parent
    outputs_dir = path / "outputs" / "IDA"
    create_path(outputs_dir)

    gmdir = path / "data/IDA-Records"

    gmfilenames = ["names_x.txt", "dts.txt"]

    # Each record is analysed in a separate process (0 uses all CPUs)
    model = RCMRF(
        analysis_options=["ida"],
        export_dir=outputs_dir,
        gm_folder=gmdir,
        gm_filenames=gmfilenames,
        dcap=5,
        analysis_time_step=0.005,
        workers=12,
    )

    model.modeller()
    model.wipe()
