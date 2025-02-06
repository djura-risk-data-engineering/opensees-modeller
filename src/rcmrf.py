from typing import Union, List
from pathlib import Path
import json
import openseespy.opensees as op
from numpy import pi, asarray

from .modal import Modal
from .msa import MSA
from .ida import IDA

from .utilities import (create_path, export_results,
                        extract_tnodes_bnodes_nspa_file)
from .mdof.model import build_model
from .gm_records import get_records


class RCMRF:
    outputs = dict()
    STATIC_KEYS = set(['st', 'static', 'gravity'])
    MODAL_KEYS = set(['ma', 'modal', 'eigenvalue'])
    MSA_KEYS = set(['msa', 'multi-stripe-analysis'])
    IDA_KEYS = set(['ida', 'incremental-dynamic-analysis'])

    rcmrf = None
    g = 9.81

    def __init__(
        self,
        analysis_options: Union[int, List[int]] = None,
        export_dir: Union[Path, str] = None,
        gm_folder: Path = None,
        gm_filenames: List[Union[Path, str]] = None,
        im_type: int = 2,
        analysis_time_step: float = None,
        dcap: float = 10.,
        sa_avg_bounds=[0, 2],
        max_runs=10,
        workers=None
    ) -> None:
        """Initialize RCMRF modeller

        Parameters
        ----------
        analysis_options : Union[int, List[int]], optional
            Analysis types to consider, by default None
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
        dcap : float, optional
            Drift capacity, beyond which full collapse of building is assumed
            in [%], by default 10.
            Required for NLTHA
        workers : int, optional
            Number of workers to use in if it is desired to run IDA
            with multiple-processors, by default None.
        """

        self.analysis_options = analysis_options
        self.export_dir = export_dir
        self.gm_folder = gm_folder
        self.gm_filenames = gm_filenames
        self.im_type = im_type
        self.analysis_time_step = analysis_time_step
        self.dcap = dcap
        self.sa_avg_bounds = sa_avg_bounds
        self.max_runs = max_runs
        self.workers = workers

        tnode, bnode = extract_tnodes_bnodes_nspa_file()
        self.bnode = bnode
        self.tnode = tnode

        if isinstance(self.export_dir, str):
            self.export_dir = Path(self.export_dir)

        if self.export_dir is not None:
            create_path(self.export_dir)

        if analysis_options is not None:
            if not isinstance(analysis_options, list):
                self.analysis_options = [analysis_options.lower()]
            else:
                self.analysis_options = [ao.lower() for ao in analysis_options]
        else:
            self.analysis_options = analysis_options

    def wipe(self):
        op.wipe()

    def _build_model(self):
        # Build the model
        build_model()

    def modeller(
        self,
        eigenvalue_analysis: Union[str, Path] = None,
    ) -> None:
        if self.analysis_options is None or \
            not self.IDA_KEYS.union(self.MSA_KEYS) \
                & set(self.analysis_options):
            # Tests model builder (no analysis)
            self._build_model()
            print("Model Built")

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

        if self.IDA_KEYS & set(self.analysis_options):
            outs = self.perform_ida(
                eigenvalue_analysis,
            )
            self.outputs['ida'] = {
                'response': outs[0],
                'IMs': outs[1]
            }

        if self.MSA_KEYS & set(self.analysis_options):
            self.outputs['msa'] = self.perform_msa(
                eigenvalue_analysis,
            )

        # Export outputs
        if not self.IDA_KEYS.union(self.MSA_KEYS) \
                & set(self.analysis_options) and self.export_dir is not None:
            export_results(self.export_dir / "outputs", self.outputs, "json")

    def perform_ida(
        self,
        eigenvalue_analysis=None,
    ):
        modal_properties = self.get_modal_properties(eigenvalue_analysis)

        damping = modal_properties['Damping'][0]
        omegas = modal_properties['CircFreq'][:2]
        period_cond = 2 * pi / asarray(omegas)

        ida = IDA(
            self.rcmrf,
            self.gm_folder,
            self.export_dir,
            self.gm_filenames,
            damping,
            omegas,
            period_cond,
            self.im_type,
            analysis_time_step=self.analysis_time_step,
            sa_avg_bounds=self.sa_avg_bounds,
            max_runs=self.max_runs,
            bnode=self.bnode,
            tnode=self.tnode,
        )
        if self.workers is None:
            ida.analyze()
        else:
            ida.analyze_mp(self.workers)

        return ida.outputs, ida.im_output

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
            self.gm_folder,
            self.export_dir,
            damping,
            omegas,
            self.dcap,
            analysis_time_step=self.analysis_time_step,
            bnode=self.bnode,
            tnode=self.tnode,
        )

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
        if eigenvalue_analysis is not None:
            filename = None
            ma = eigenvalue_analysis
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
