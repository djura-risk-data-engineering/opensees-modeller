import pickle
from pathlib import Path
from typing import List, Union
import openseespy.opensees as op
import numpy as np

from .intensity_measure import IntensityMeasure
from .solution_algorithm import SolutionAlgorithm, apply_time_series
from .gm_records import get_ground_motion
from .mdof.model import build_model


class IDA:
    PTAGX = 10
    PTAGY = 20
    TSTAGX = 51
    TSTAGY = 52
    EXTRA_DUR = 10.0
    g = 9.81

    IM = IntensityMeasure()

    outputs = dict()
    im_output = None

    def __init__(
        self,
        model,
        gm_folder: Path,
        output_path: Path,
        gm_filenames: List[Union[Path, str]],
        damping: float,
        omegas: List[float],
        period_cond: List[float],
        im_type: int,
        max_runs: int = 10,
        first_int: float = 0.05,
        incr_step: float = 0.05,
        dcap: float = 10.,
        analysis_time_step: float = None,
        export_at_each_step: bool = True,
        sa_avg_bounds=[0, 2],
        bnode: List = None,
        tnode: List = None,
    ) -> None:
        """Incremental Dynamic Analysis (IDA) using Hunt, trace and fill (HTF)
        algorithm

        Parameters
        ----------
        model : NonlinearModel
            Nonlinear model object
        gm_folder : Path
            Folder containing the ground motion files
        output_path : Path
            Path for outputs
        gm_filenames : List[Union[Path, str]]
            List of length 2 or 3 (2 for 2D analysis, 3 for 3D analysis)
            List contains path to the following:
                File containing the names of the ground motion files in 1st
                direction
                Optional, file containing the names of the ground motion files
                in 2nd direction
                File containing the time steps of the ground motion records
        damping : float
            Damping ratio
        omegas : List[float]
            Circular frequencies, [omega1, omega2]
        period_cond : List[float]
            Conditioning periods [T1, T2]
        im_type : int
            Intensity measure type
                1 - PGA
                2 - Sa(T)
                3 - Sa_avg(T)
        max_runs : int, optional
            Maximum runs to perform, by default 10
        first_int : float, optional
            First intensity measure value in [g], by default 0.05
        incr_step : float, optional
            Intensity measure increment in [g], by default 0.05
        dcap : float, optional
            Drift capacity, beyond which full collapse of building is assumed
            in [%], by default 10.
        analysis_time_step : float, optional
            Nonlinear analysis time step, by default None
            If None, will default to ground motion record time step, i.e., dt
        column_transformation : str, optional
            Column transformation type for OpenSees, by default None
        beam_transformation : str, optional
            Beam transformation type for OpenSees, by default None
        export_at_each_step : bool, optional
            Export time history results at each step of IDA, by default True
        """

        if output_path is None:
            raise ValueError("You must provide output_path for IDA outputs")

        self.nonlinear_model = model
        self.gm_folder = gm_folder
        self.output_path = output_path
        self.gm_filenames = gm_filenames
        self.damping = damping
        self.omegas = omegas
        self.period_cond = period_cond
        self.im_type = im_type
        self.max_runs = max_runs
        self.first_int = first_int
        self.incr_step = incr_step
        self.analysis_time_step = analysis_time_step
        self.export_at_each_step = export_at_each_step
        self.dcap = dcap
        self.sa_avg_bounds = sa_avg_bounds
        self.bnode = bnode
        self.tnode = tnode

    def _call_model(self, generate_model: bool = True):
        if not generate_model:
            return

        build_model()

    def _select_htf_step(
        self, im, im_geomean, rec, j, dt_record, eq_name_x,
        eq_name_y, output_path, analysis_time_step, dur, im_filename
    ) -> int:
        # Determine the scale factor that needs to be applied to the record
        sf_x = round(im[j - 1] / im_geomean * self.g, 3)
        sf_y = round(im[j - 1] / im_geomean * self.g, 3)

        # The hunting intensity has been determined, now analysis commences
        self._call_model()
        apply_time_series(dt_record, eq_name_x, eq_name_y, sf_x, sf_y,
                          self.omegas, self.damping,
                          self.TSTAGX, self.TSTAGY,
                          self.PTAGX, self.PTAGY)

        directions = 1 if eq_name_y is None else 2

        # Commence analysis
        th = SolutionAlgorithm(
            output_path, analysis_time_step, dur, self.dcap,
            self.bnode, self.tnode, directions=directions
        )

        self.outputs[rec][j] = th.solve()

        # Export results at each run
        if self.export_at_each_step:
            with open(
                output_path / f"Record{rec + 1}_Run{j}.pickle", "wb"
            ) as handle:
                pickle.dump(self.outputs[rec][j], handle)
            np.savetxt(im_filename, self.im_output, delimiter=',')

        return th.collapse_index

    def _hunt_trace_fill(self, im_geomean, dt_record, dur, eq_name_x,
                         eq_name_y, rec, output_path, im_filename):
        """
        Check the hunted run for collapse
        c_index = -1                Analysis failed to converge at control
                                    time of Tmax
        c_index = 0                 Analysis completed successfully
        c_index = 1                 Local structure collapse
        """
        # Set up the initial indices for HTF
        j = 1
        # Initialize the list of IM used
        im = np.zeros((self.max_runs, ))
        # A list to be used in filling
        im_list = np.array([])
        # Hunting flag (1 for when we are hunting)
        hflag = 1
        # Tracing flag (0 at first)
        tflag = 0
        # Filling flag (0 at first)
        fflag = 0
        # The run number we hunted to
        jhunt = 0

        # The aim is to run NLTHA max_runs times
        while j <= self.max_runs:

            # As long as hunting flag is 1, meaning that collapse have
            # not been reached
            if hflag == 1:

                if self.analysis_time_step is None:
                    analysis_time_step = dt_record
                else:
                    analysis_time_step = self.analysis_time_step

                print("[STEP] Gehrman joins the hunt...")
                # Determine the intensity to run at during the hunting
                if j == 1:
                    # First IM
                    im[j - 1] = self.first_int
                else:
                    # Subsequent IMs
                    im[j - 1] = im[j - 2] + (j - 1) * self.incr_step

                collapse_index = self._select_htf_step(
                    im, im_geomean, rec, j, dt_record, eq_name_x, eq_name_y,
                    output_path, analysis_time_step, dur, im_filename)

                # Check the hunted run for collapse
                if collapse_index > 0:
                    # Collapse is caught, so stop hunting
                    hflag = 0
                    # Start tracing
                    tflag = 1
                    # The value of j we hunted to
                    jhunt = j
                    # Check whether first increment is too large
                    if jhunt == 2:
                        print(
                            f"[IDA] Warning: {j} - Collapsed achieved on first"
                            " increment, reduce increment...")
                else:
                    self.im_output[rec, j - 1] = im[j - 1]
                    # increment j
                    j += 1

                op.wipe()

            # When first collapse is reached, tracing commences between
            # last convergence and the first collapse
            if tflag == 1:
                print("[STEP] Tracing...")

                if j == jhunt:
                    # This is the IM of the hunting collapse
                    # (IM to cause collapse)
                    firstC = im[j - 1]
                    # Remove that value of IM from the array
                    im[j - 1] = 0.0

                # Determine the difference between the hunting's non-collapse
                # and collapse IM
                diff = firstC - im[j - 2]

                # Take 20% of the difference
                inctr = 0.2 * diff

                # Place a lower threshold on the increment so it doesnt start
                # tracing too fine
                if inctr < 0.05:
                    inctr = 0.025

                # Calculate new tracing IM, which is previous non-collapse
                # plus increment
                im[j - 1] = im[j - 2] + inctr
                self.im_output[rec, j - 1] = im[j - 1]

                collapse_index = self._select_htf_step(
                    im, im_geomean, rec, j, dt_record, eq_name_x, eq_name_y,
                    output_path, analysis_time_step, dur, im_filename)

                if collapse_index > 0:
                    # Stop tracing
                    tflag = 0
                    # Start filling
                    fflag = 1
                    # The value of j we traced to
                    # jtrace = j
                    # Get the list of IMs
                    im_list = im
                    if j == jhunt:
                        print(
                            f"[IDA] Warning: {j} - First trace for collapse "
                            "resulted in collapse... ")
                j += 1
                op.wipe()

            # When the required resolution is reached, start filling until
            # max_runs is reached
            # Make sure that number of runs are not exceeded
            if fflag == 1 and j <= self.max_runs:
                print("[STEP] Filling the gaps...")

                # Reorder the list so we can account for filled runs
                im_list = np.sort(im_list)

                # Determine the biggest gap in IM for the hunted runs
                gap = 0.0
                im_fill = 0.0

                '''We go to the end of the list minus 1 because, if not we
                would be filling between a noncollapsing
                and a collapsing run, for which we are not sure if that
                filling run would be a non collapse -
                In short, does away with collapsing fills'''
                for ii in range(1, len(im_list) - 1):
                    # Find the running gap of hunted runs
                    temp = im_list[ii] - im_list[ii - 1]
                    if temp > gap:
                        # Update to maximum gap
                        gap = temp
                        # Determine new filling IM
                        im_fill = im_list[ii - 1] + gap / 2

                im[j - 1] = im_fill
                im_list = np.append(im_list, im_fill)
                self.im_output[rec, j - 1] = im_fill

                collapse_index = self._select_htf_step(
                    im, im_geomean, rec, j, dt_record, eq_name_x, eq_name_y,
                    output_path, analysis_time_step, dur, im_filename)

                # Increment run number
                j += 1
                op.wipe()

            # Wrap it up and finish
            if j == self.max_runs and hflag == 1:
                print(
                    '[IDA] Warning: Collapse not achieved, increase increment'
                    ' or number of runs...')
            if j == self.max_runs and fflag == 0:
                print('[IDA] Warning: No filling, algorithm still tracing for'
                      ' collapse (reduce increment & '
                      'increase runs)...')
            op.wipe()

    def analyze(self) -> None:
        """Performs IDA

        Raises
        ------
        ValueError
            Raises exception if wrong IM type is provided!
        """
        im_filename = self.output_path / "IM.csv"
        if im_filename.exists():
            im_filename = self.output_path / "IM_temp.csv"

        # Get the ground motion set information
        gm_1, gm_2, dts = get_ground_motion(self.gm_folder, self.gm_filenames)

        try:
            nrecs = len(dts)
        except Exception:
            dts = np.array([dts])
            nrecs = len(dts)

        # Initialize intensity measures (shape)
        self.im_output = np.zeros((nrecs, self.max_runs))

        # Loop for each record
        for rec in range(nrecs):
            # Counting starts from 0
            self.outputs[rec] = {}
            # Get the ground motion set information
            eq_name_x = self.gm_folder / gm_1[rec]
            eq_name_y = None

            dt_record = dts[rec]
            accg_x = np.loadtxt(eq_name_x)
            dur = dt_record * (len(accg_x) - 1)
            dur = self.EXTRA_DUR + dur

            if gm_2 is not None:
                eq_name_y = self.gm_folder / gm_2[rec]
                accg_y = np.loadtxt(eq_name_y)

            # Establish the IM
            if self.im_type == 1:
                print('[IDA] IM is the PGA')
                im_x = self.IM.get_pga(accg_x)
                if gm_2 is not None:
                    im_y = self.IM.get_pga(accg_y)

            elif self.im_type == 2:
                print('[IDA] IM is Sa at a specified period')
                im_x = self.IM.get_sat(
                    self.period_cond[0], accg_x, dt_record, self.damping)
                if gm_2 is not None:
                    im_y = self.IM.get_sat(
                        self.period_cond[1], accg_y, dt_record, self.damping)

            elif self.im_type == 3:
                print("[IDA] IM is Sa_avg")
                periods_x = []
                periods_y = []
                for factor in np.linspace(
                        self.sa_avg_bounds[0],
                        self.sa_avg_bounds[1],
                        10):
                    factor = round(factor, 2)
                    periods_x.append(factor * self.period_cond[0])
                    periods_y.append(factor * self.period_cond[1])

                im_x_0 = self.IM.get_sat(
                    np.array(periods_x), accg_x, dt_record, self.damping)
                im_x = im_x_0.prod() ** (1 / len(im_x_0))

                if gm_2 is not None:
                    im_y_0 = self.IM.get_sat(
                        np.array(periods_y), accg_y, dt_record, self.damping)
                    im_y = im_y_0.prod() ** (1 / len(im_y_0))

            else:
                raise ValueError('[EXCEPTION] IM type provided incorrectly'
                                 ' (must be 1, 2 or 3)')

            # Get the geometric mean
            if gm_2 is not None:
                im_geomean = np.power(im_x * im_y, 0.5)
            else:
                im_geomean = im_x

            self._hunt_trace_fill(
                im_geomean, dt_record, dur, eq_name_x, eq_name_y, rec,
                self.output_path, im_filename)

        print('[IDA] Finished IDA HTF')
