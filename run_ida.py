from pathlib import Path
from src.rcmrf import RCMRF
from src.utilities import create_path


path = Path(__file__).parent
outputs_dir = path / "outs"
create_path(outputs_dir)

gmdir = path / "data/IDA_Records"

gmfilenames = ["names_x.txt", "dts.txt"]

model = RCMRF(
    analysis_options=["ida"],
    export_dir=outputs_dir,
    gm_folder=gmdir,
    gm_filenames=gmfilenames,
    dcap=5,
    analysis_time_step=0.005,
)

model.modeller()
model.wipe()
