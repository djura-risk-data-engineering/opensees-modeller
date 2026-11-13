import openseespy.opensees as op
import numpy as np
import pickle
from .SDOF_model import build
from ..intensity_measure import IntensityMeasure
from .solution_algorithm_sdof import SolutionAlgorithm


class RCMRF:
    outputs = dict()
    STATIC_KEYS = set(['st', 'static', 'gravity'])
    MODAL_KEYS = set(['ma', 'modal', 'eigenvalue'])
    MSA_KEYS = set(['msa', 'multi-stripe-analysis'])
    IDA_KEYS = set(['ida', 'incremental-dynamic-analysis'])

    rcmrf = None
    g = 9.81
    EXTRA_DUR = 10.0
    PTAGX = 10
    PTAGY = 20
    TSTAGX = 51
    IM = IntensityMeasure()
    outputs = dict()

    def __init__(self, outputsDir,  gmdir, gmfileNames, Fvect, Dvect, mass,
                 damage=False, IM_type=3,
                 max_runs=15, analysis_time_step=None, drift_capacity=10.0,
                 analysis_type=None, system="Space",
                 flag3d=False, direction=0, export_at_each_step=True,
                 period_assignment=None, periods_ida=None,
                 modal_analysis_path=None,
                 use_recorder=True, recorder_cache=None):

        self.outputsDir = outputsDir
        self.gmdir = gmdir
        self.gmfileNames = gmfileNames
        self.IM_type = IM_type
        self.max_runs = max_runs
        self.analysis_time_step = analysis_time_step
        self.drift_capacity = drift_capacity
        self.analysis_type = analysis_type
        self.system = system
        self.flag3d = flag3d
        self.export_at_each_step = export_at_each_step
        self.direction = direction
        self.period_assignment = period_assignment
        self.periods_ida = periods_ida
        self.use_recorder = use_recorder
        self.recorder_cache = recorder_cache
        self.Fvect = Fvect
        self.Dvect = Dvect
        self.mass = mass
        self.damage = damage

        if modal_analysis_path:
            self.modal_analysis_path = modal_analysis_path
        else:
            self.modal_analysis_path = self.outputsDir / "MA.json"

        # Constants
        self.APPLY_GRAVITY_ELF = False
        self.FIRST_INT = .05
        self.INCR_STEP = .05
        self.DAMPING = .05

        # Records for MSA
        self.records = None

        if direction != 0 and flag3d and analysis_type == "MA":
            print("[WARNING] Direction should be set to 0 for Modal Analysis!")

    @staticmethod
    def wipe():
        """
        Perform a clean wipe
        :return: None
        """
        op.wipe()

    def call_model(self):
        """
        Calls the Model
        :return: class Object Model
        """
        op.wipe()
        build(self.Fvect, self.Dvect, self.mass, self.damage)

    def get_modal_parameters(self):
        self.call_model()
        lamb = op.eigen(1)
        omega = lamb[0]**0.5
        period = 2*np.pi/omega
        damping = 0.05

        return period, damping, omega

    def _get_gm(self):
        names_x = np.loadtxt(
            self.gmdir / self.gmfileNames[0], dtype="str", ndmin=1)
        names_y = np.loadtxt(
            self.gmdir / self.gmfileNames[1], dtype="str", ndmin=1)
        dts_list = np.loadtxt(self.gmdir / self.gmfileNames[2], ndmin=1)
        return names_x, names_y, dts_list

    def estimate_im_record(self, period, accg_x, accg_y, dt, xi):
        im_x = self.IM.get_sa_avg(accg_x, dt, period, xi, bounds=[0.2, 3.0])
        im_y = self.IM.get_sa_avg(accg_y, dt, period, xi, bounds=[0.2, 3.0])
        return im_x, im_y

    def ida_step(self, im, sa_record, dt, eq_name_x, damping, omegas,
                 analysis_time_step, dur, rec, im_idx):
        sf = round(im / sa_record * self.g, 3)

        self.call_model()

        op.wipeAnalysis()

        w = omegas
        a0 = 2 * w * damping
        b0 = 2 * damping / w
        op.rayleigh(a0, 0.0, b0, 0.0)
        op.timeSeries('Path', self.TSTAGX, '-dt', dt, '-filePath',
                      str(eq_name_x), '-factor', sf)
        op.pattern('UniformExcitation', self.PTAGX, 1, '-accel', self.TSTAGX)
        op.constraints('Plain')
        op.numberer('RCM')
        op.system('UmfPack')

        th = SolutionAlgorithm(
            self.outputsDir / "cache", analysis_time_step, dur,
            self.drift_capacity, [1], [2],
        )
        self.outputs[rec][im_idx] = th.solve()

        if self.export_at_each_step:
            with open(
                self.outputsDir / f"Record{rec + 1}_Run{im_idx}.pickle", "wb"
            ) as handle:
                pickle.dump(self.outputs[rec][im_idx], handle)

    def run_model(self, period, imls):
        """
        Initializes model creator and runs analysis
        :return: None
        """
        imls = np.asarray(imls)

        # Run analysis and record the goodies

        # Nonlinear time history analysis
        print("[INITIATE] IDA started")

        # Get MA parameters
        _, xi, omegas = self.get_modal_parameters()

        # Initialize
        eqnms_list_x, eqnms_list_y, dts_list = self._get_gm()

        for rec, (eq_name_x, eq_name_y, dt) in enumerate(zip(
                eqnms_list_x, eqnms_list_y, dts_list)):
            self.outputs[rec] = {}

            accg_x = np.loadtxt(self.gmdir / eq_name_x)
            accg_y = np.loadtxt(self.gmdir / eq_name_y)
            dur = round(self.EXTRA_DUR + dt * len(accg_x), 5)
            sa_x, sa_y = self.estimate_im_record(
                period, accg_x, accg_y, dt, xi
            )
            sa_record = np.power(sa_x * sa_y, 0.5)

            if self.analysis_time_step is None:
                analysis_time_step = dt
            else:
                analysis_time_step = min(self.analysis_time_step, dt)

            for im_idx, im in enumerate(imls):
                self.ida_step(
                    im, sa_record, dt, self.gmdir / eq_name_x, xi,
                    omegas, analysis_time_step, dur, rec, im_idx)

                # Export results
                if not self.export_at_each_step:
                    with open(self.outputsDir / "IDA.pickle", "wb") as handle:
                        pickle.dump(self.outputs, handle)

                print("[SUCCESS] IDA done")
