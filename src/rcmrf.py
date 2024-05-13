from typing import Union, List
from pathlib import Path
import json
import openseespy.opensees as op

from .modal import Modal
from .msa import MSA

from .utilities import create_path, export_results
from .model import build
from .analysis1 import gravity
from .gm_records import get_records


class RCMRF:
    outputs = dict()
    STATIC_KEYS = set(['st', 'static', 'gravity'])
    MODAL_KEYS = set(['ma', 'modal', 'eigenvalue'])
    MSA_KEYS = set(['msa', 'multi-stripe-analysis'])
    IDA_KEYS = set(['ida', 'incremental-dynamic-analysis'])

    bnode = []
    tnode = []

    rcmrf = None
    g = 9.81

    def __init__(
        self,
        analysis_options: Union[int, List[int]] = None,
        workers: int = None,
        export_dir: Union[Path, str] = None,
        gm_folder: Path = None,
        gm_filenames: List[Union[Path, str]] = None,
        im_type: int = 2,
        analysis_time_step: float = None,
        dt_record: float = None,
        eq_name_x: str = None,
        eq_name_y: str = None,
        dcap: float = 10.,
        multiprocess: bool = True,
    ) -> None:
        """Initialize RCMRF modeller

        Parameters
        ----------
        concrete_modulus : float
            Concrete elastic modulus in MPa
        loads : ActionModel
            Gravity loads, as well as seismic loads, based on which
            seismic masses are computed
        hinge_1 : HingeModel, optional
            Lumped hinge properties in 1 direction, by default None
        hinge_2 : HingeModel, optional
            Lumped hinge properties in 2 direction, by default None
        hinge_internal : InternalHingeModel, optional
            Lumped hinge properties of internal elements, by default None
        analysis_options : Union[int, List[int]], optional
            Analysis types to consider, by default None
        system : str, optional
            System configuration, 'perimeter' or 'space', by default 'space'
        export_dir : Union[Path, str], optional
            Directory where to export outputs, by default None
            Required for MSA and IDA
        gm_folder : Path, optional
            Folder containing the ground motion files, by default None
            Required for MSA and IDA
        gm_filenames : List[Union[Path, str]], optional
            Required for MSA and IDA
            List of length 2 or 3 (2 for 2D analysis, 3 for 3D analysis)
            List contains path to the following:
                File containing the names of the ground motion files in
                1st direction
                Optional, file containing the names of the ground motion files
                in 2nd direction
                File containing the time steps of the ground motion records
        im_type : int, optional
            Necessary for MSA and IDA
            Intensity measure type, by default 1
                1 - PGA
                2 - Sa(T)
                3 - Sa_avg(T)
        column_transformation : str, optional
            Column transformation value, by default PDelta
        beam_transformation : str, optional
            Beam transformation value, by default PDelta
        analysis_time_step : float, optional
            Nonlinear analysis time step, by default None
            If None, will default to ground motion record time step
        dt_record : float, optional
            Record time step, required for NLTHA, by default None
        eq_name_x : str, optional
            Record filename in X direction, required for NLTHA, by default None
        eq_name_y : str, optional
            Record filename in Y direction, required for NLTHA, by default None
        dcap : float, optional
            Drift capacity, beyond which full collapse of building is assumed
            in [%], by default 10.
            Required for NLTHA
        """

        self.analysis_options = analysis_options
        self.workers = workers
        self.export_dir = export_dir
        self.gm_folder = gm_folder
        self.gm_filenames = gm_filenames
        self.im_type = im_type
        self.analysis_time_step = analysis_time_step
        self.dt_record = dt_record
        self.eq_name_x = eq_name_x
        self.eq_name_y = eq_name_y
        self.dcap = dcap
        self.multiprocess = multiprocess

        if isinstance(self.export_dir, str):
            self.export_dir = Path(self.export_dir)

        if self.export_dir is not None:
            create_path(self.export_dir)

    def wipe():
        op.wipe()

    def _build_model(self):
        # Build the model
        build()
        gravity()

    def modeller(
        self,
        eigenvalue_analysis: Union[str, Path] = None,
    ) -> None:
        self._build_model()

        self.analyze(eigenvalue_analysis)

    def analyze(
        self,
        eigenvalue_analysis=None,
    ) -> None:
        """Performs analysis

        Parameters
        ----------
        damping : float
            Damping ratio
        num_modes : int
            Number of modes to consider
        damping_modes : List[int]
            At which modes to apply damping
        load_pattern : List[float], optional
            Load pattern to apply for static pushover analysis (SPO),
            by default None
        eigenvalue_analysis : Union[str, Path, ModalProperties]
            Eigenvalue analysis results, by default None
        pushover_direction: Union[int, List[int]]
            SPO direction of application, by default 1, can be 1 or 2,
            or both [1, 2]
        """

        if self.MODAL_KEYS & set(self.analysis_options):
            m = Modal(3, 0.05, [1, 3])

            self.outputs['eigenvalue'] = {}

            # self.outputs['eigenvalue']['Periods'] = list(m.period)
            self.outputs['eigenvalue']['Damping'] = list(m.damping_modes)
            self.outputs['eigenvalue']['CircFreq'] = list(m.omega)

        if self.MSA_KEYS & set(self.analysis_options):
            self.outputs['msa'] = self.perform_msa(
                eigenvalue_analysis,
            )

        # Export outputs
        if not self.IDA_KEYS.union(self.MSA_KEYS) \
                & set(self.analysis_options) and self.export_dir is not None:
            export_results(self.export_dir / "outputs", self.outputs, "json")

    def perform_msa(
        self,
        eigenvalue_analysis=None,
    ):
        """Perform multiple stripe analysis (MSA)

        Parameters
        ----------
        eigenvalue_analysis : Union[str, Path, ModalProperties], optional
            Eigenvalue analysis results, by default None
            If None, will try to read from self.export_dir
            If cannot find, will run eigenvalue analysis

        Returns
        -------
        MSAOutputModel
            MSA outputs
        """
        modal_properties = self.get_modal_properties(eigenvalue_analysis)

        damping = modal_properties['Damping'][0]
        omegas = modal_properties['CircFreq'][:2]

        records = get_records(
            self.gm_folder, self.gm_filenames, self.export_dir)

        msa = MSA(
            self.bnode,
            self.tnode,
            self.gm_folder,
            self.export_dir,
            damping,
            omegas,
            self.dcap,
            analysis_time_step=self.analysis_time_step,
        )

        if self.multiprocess:
            msa.start(records, workers=self.workers)
        else:
            for batch in list(records.items()):
                msa.analyze(batch)

        return msa.outputs

    def get_modal_properties(
        self, eigenvalue_analysis=None
    ):
        """Retrieves eigenvalue analysis outputs

        Parameters
        ----------
        eigenvalue_analysis : Union[str, Path, ModalProperties]
            Eigenvalue analysis results, by default None

        Returns
        -------
        ModalProperties
            Eigenvalue analysis outputs in a dictionary format
        """
        # Reading directly from input
        if eigenvalue_analysis:
            filename = None
            ma = eigenvalue_analysis
        elif eigenvalue_analysis:
            filename = eigenvalue_analysis
            ma = None
        else:
            filename = None
            ma = None

        if ma:
            try:
                # validate the model
                self.outputs = ma
                if 'eigenvalue' in ma:
                    return ma['eigenvalue']

            except ValueError:
                print(
                    "Wrong eigenvalue analysis outputs provided..."
                    "Trying to read from file...")

        # Trying to read from file
        if filename:
            if isinstance(filename, str):
                filename = Path(filename)

            with open(filename) as f:
                ma = json.load(f)

        else:
            if Path(self.export_dir / "outputs.json").exists():
                with open(self.export_dir / "outputs.json") as f:
                    ma = json.load(f)

        # Validate the model
        if ma:
            try:
                self.outputs = ma
                if 'eigenvalue' in ma:
                    return ma['eigenvalue']

            except ValueError:
                # rerun modal analysis and retrieve modal properties if file
                # or outputs do not exist
                print("Outputs file not found... "
                      "Running eigenvalue analysis...")
        else:
            print("Outputs file not found... Running eigenvalue analysis...")

        analysis_options_tmp, self.analysis_options = self.analysis_options, [
            "ma"]

        op.wipe()
        self.modeller()

        # Resetting analysis options
        self.analysis_options = analysis_options_tmp

        # Wipe the model
        op.wipe()

        return self.outputs['eigenvalue']
