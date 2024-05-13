import pytest
import pickle
from pathlib import Path
import pandas as pd
import openseespy.opensees as op

from pbe.NonlinearModelling.rcmrf import RCMRF
from pbe.NonlinearModelling.schemas import *
from pbe.SeismicAnalysis.models import RecordBatchModel, RecordModel, AnalysisOutModel
from pbe.utils.utilities import get_records
from pbe.utils.validation import validate


path = Path(__file__).resolve().parent


@pytest.mark.analysis
class TestMSA:
    hinge_models_file = path.parents[0] / \
        "assets/NonlinearModelling/hinge_models.pickle"
    
    with open(hinge_models_file, "rb") as f:
        hinge_models = pickle.load(f)

    hinge_1 = hinge_models['x_seismic']
    hinge_2 = hinge_models['y_seismic']
    hinge_internal = hinge_models['internal']
    concrete_modulus = 23500.
    loads = pd.read_csv(
        path.parents[0] / "assets/NonlinearModelling/action.csv")

    ma_path = path.parents[0] / \
        "assets/SeismicAnalysis/outputs/outputs.json"
    path = path.parents[0] / "assets/SeismicAnalysis"

    def test_records(self):
        records = get_records(self.path / "MSA", ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"])

        batches = list(records.items())

        validate(RecordBatchModel, records)

        for batch in batches:
            name, data = batch
            error_msg = f"{name}: "

            validate(RecordModel, data, error_msg)

    def test_run_msa(self):
        op.wipe()
        
        # Call RCMRF modeller
        model = RCMRF(
            self.concrete_modulus,
            self.loads,
            self.hinge_1,
            self.hinge_2,
            self.hinge_internal,
            "MSA",
            export_dir=self.path / "MSA_outputs",
            gm_folder=self.path / "MSA",
            gm_filenames=["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"],
        )
        
        model.modeller(eigenvalue_analysis=self.ma_path)

        op.wipe()

        data = model.outputs['msa']
        with open(self.path / "msa.pickle", "wb") as handle:
            pickle.dump(data, handle)
        
        validate(AnalysisOutModel, data)
