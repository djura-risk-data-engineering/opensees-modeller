from pathlib import Path
from src.rcmrf import RCMRF
from src.utilities import create_path


path = Path.cwd()
outputs_dir = path / "outs"
create_path(outputs_dir)

gmdir = path / "data/IDA_Records"

gmfilenames = ["names_x.txt", "names_y.txt"]

model = RCMRF(
    analysis_options=["ida"],
    export_dir=outputs_dir,
    gm_folder=gmdir,
    gm_filenames=gmfilenames,
    dcap=5,
)

model.modeller()
model.wipe()
