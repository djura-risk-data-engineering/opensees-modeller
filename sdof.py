from pathlib import Path
from src.sdof.rcmrf import RCMRF


# Directories
main_dir = Path.cwd()
outputsDir = main_dir / "out/ida"

# Ensure the directories exist
gmdir = main_dir / "sdof_records"

# GM directory, first one will be the records to be applied
# second one will be the records necessary for the calculation of
# scaling factor
gmfileNames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]

# RCMRF inputs
system = "space"
analysis_type = ["IDA"]
flag3d = False
# Export outputs as a single file (this time :))
export_at_each_step = True
analysis_time_step = 0.01
max_runs = 10

# Use lists instead of sets for Fvect and Dvect
Fvect = [755.9460974, 768.5833743, 0]
Dvect = [0.034459713, 0.115543952, 0.14896678]

mass = 555.90

imls = [0.021, 0.044, 0.072, 0.123, 0.166, 0.268, 0.383, 0.577, 0.746, 0.945]

# Initialize the RCMRF model
m = RCMRF(outputsDir, gmdir, gmfileNames, Fvect, Dvect, mass,
          analysis_type=analysis_type, system=system, flag3d=flag3d,
          export_at_each_step=export_at_each_step,
          max_runs=max_runs)

# Wipe the previous model
m.wipe()

# Run the model
m.run_model(0.605, imls)

# Wipe the model again after the run
m.wipe()
