from typing import List
from pathlib import Path
import pickle
import openseespy.opensees as op
import numpy as np

from .solution_algorithm import SolutionAlgorithm, apply_time_series
from .utilities import append_record, extract_tnodes_bnodes_nspa_file
from .mdof.model import build_model


class MSA:
    PTAGX = 10
    PTAGY = 20
    TSTAGX = 51
    TSTAGY = 52
    EXTRA_DUR = 10.0
    g = 9.81
    use_multiprocess = False

    outputs = dict()

    def __init__(
        self,
        gm_folder: Path,
        output_path: Path,
        damping: float,
        omegas: List[float],
        dcap: float = 10.,
        analysis_time_step: float = None,
        export_at_each_step: bool = True,
        bnode: List = None,
        tnode: List = None,
    ) -> None:
        """Multiple Stripe Analysis (MSA)

        Parameters
        ----------
        model : NonlinearModel
            Nonlinear model object
        gm_folder : Path
            Folder containing the ground motion files
        output_path : Path
            Path for outputs
        damping : float
            Damping ratio
        omegas : List[float]
            Circular frequencies, [omega1, omega2]
        dcap : float, optional
            Drift capacity, beyond which full collapse of building is assumed
            in [%], by default 10.
        analysis_time_step : float, optional
            Nonlinear analysis time step, by default None
            If None, will default to ground motion record time step, i.e., dt
        export_at_each_step : bool, optional
            Export time history results at each step of IDA, by default True
        """
        self.gm_folder = gm_folder
        self.output_path = output_path
        self.damping = damping
        self.omegas = omegas
        self.dcap = dcap
        self.analysis_time_step = analysis_time_step
        self.export_at_each_step = export_at_each_step

        if tnode is None and bnode is None:
            tnode, bnode = extract_tnodes_bnodes_nspa_file()
        self.bnode = bnode
        self.tnode = tnode

    def _call_model(self, generate_model: bool = True):
        if not generate_model:
            return

        build_model()

    def analyze(self, batch) -> None:
        """Performs MSA

        Parameters
        ----------
        batch : Tuple[str, RecordModel]
            Tuple containing name of batch and dictionary (RecordModel) of
                'X': names of records in X direction
                'Y': names of records in Y direction
                'dt': time step of records
        """
        name, data = batch
        print(f"[START] Running {name} records...")

        # Get the filenames of record pairs and time steps
        names_x = data["X"]
        names_y = data["Y"]
        dts = data["dt"]

        # initialize for second direction (if 3D modelling is utilized, both
        # directions of record, then the variables will be updated)
        accg_y = None
        eq_name_y = None

        # Initialize outputs
        self.outputs[name] = {}

        # For each record pair
        for rec in range(len(names_x)):
            if self.use_multiprocess:
                self.recorder_cache = f"{name}_{rec}.txt"

            # reading records
            eq_name_x = self.gm_folder / name / names_x[rec]
            dt = dts[rec]
            accg_x = np.loadtxt(eq_name_x)

            # Second direction
            if names_y is not None:
                eq_name_y = self.gm_folder / name / names_y[rec]
                accg_y = np.loadtxt(eq_name_y)
                # duration, make sure both directions have the same size
                accg_x, accg_y = append_record(accg_x, accg_y)

            # add extra duration of free vibrations to the records
            dur = round(self.EXTRA_DUR + dt * len(accg_x), 5)

            # analysis time step
            if self.analysis_time_step is None:
                analysis_time_step = dt
            else:
                analysis_time_step = self.analysis_time_step

            # Create the model
            self._call_model()

            # Create the time series
            apply_time_series(dt, eq_name_x, eq_name_y, self.g, self.g,
                              self.omegas, self.damping,
                              self.TSTAGX, self.TSTAGY,
                              self.PTAGX, self.PTAGY)

            if names_y is None:
                print(f"[MSA] Record: {rec} - {name}: {names_x[rec]};")
                directions = 1
            else:
                print(
                    f"[MSA] Record: {rec} - {name}: {names_x[rec]} and "
                    f"{names_y[rec]} pair;")
                directions = 2

            analysis_time_step = min(analysis_time_step, dt)
            if dt % analysis_time_step != 0:
                analysis_time_step = dt / (int(dt / analysis_time_step))

            # Commence analysis
            th = SolutionAlgorithm(
                self.output_path / name, analysis_time_step, dur, self.dcap,
                self.bnode, self.tnode,
                extra_dur=self.EXTRA_DUR,
                directions=directions
            )
            self.outputs[name][rec] = th.solve()

            if self.export_at_each_step:
                with open(self.output_path / name / f"Record{rec + 1}.pickle",
                          "wb") as handle:
                    pickle.dump(self.outputs[name][rec], handle)

            # Wipe the model
            op.wipe()
