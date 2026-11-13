from typing import List, Union, Tuple
from pathlib import Path
import openseespy.opensees as op
import numpy as np

from ..utilities import create_path, read_text, \
    remove_directory_contents


class SolutionAlgorithm:
    g = 9.81
    ITERATIONS = 50
    ALGORITHM_TYPE = 'KrylovNewton'
    TEST_TYPE = 'NormDispIncr'
    TOL = 1e-04
    collapse_index = 0

    def __init__(
        self,
        output_path: Path,
        dt: float,
        dur: float,
        dc: float,
        bnode: Union[np.array, List[int]],
        tnode: Union[np.array, List[int]],
        pflag: bool = True,
        extra_dur: float = 10.,
    ) -> None:
        """Algorithms to execute nonlinear time history analysis (NLTHA)

        Parameters
        ----------
        output_path : Path
            Base output path for outputting the results, e.g., Path(directory)
            without suffix
        dt : float
            Initial analysis time step, [s]
            NOT ground motion time step
        dur : float
            Length of ground motion record, [s]
        dc : float
            Drift capacity for both storey and rooft drif, [%]
        bnode : Union[np.array, List[int]]
            List of bottom nodes
        tnode : Union[np.array, List[int]]
            List of top nodes
        pflag : bool, optional
            Print statements, by default True
        extra_dur : float, optional
            Extra duration for free vibrations in [s], by default 10.
        """
        self.output_path = output_path
        if self.output_path is not None:
            self.output_path = self.output_path
        self.dt = dt
        self.dur = dur
        self.extra_dur = extra_dur
        self.dc = dc
        self.bnode = np.array(bnode)
        self.tnode = np.array(tnode)

        # TODO, remove pflag and do logging instead
        self.pflag = pflag

        self._set_analysis()

    def _set_analysis(self):
        """Set up initial analysis parameters
        """
        op.test(self.TEST_TYPE, self.TOL, self.ITERATIONS)
        op.algorithm(self.ALGORITHM_TYPE)
        op.integrator('Newmark', 0.5, 0.25)
        op.analysis('Transient')

    def _algorithm(self, ok: int, control_time: float) -> None:
        """Algorithms necessary to perform the analysis

        Parameters
        ----------
        ok : int
            Analysis performed successfully or not, 0 stands for ok,
            != stands for not ok
        control_time : float
            Control time in seconds
        """
        dtt = self.dt
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} of {self.dur}"
                      " seconds")
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Reduced timestep by half...")
            dtt = 0.5 * self.dt
            ok = op.analyze(1, dtt)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Reduced timestep by quarter...")
            dtt = 0.25 * self.dt
            ok = op.analyze(1, dtt)
        if ok:
            if self.pflag:
                print(
                    f"[FAILURE] Failed at {control_time} - Trying Broyden...")
            op.algorithm('Broyden', 8)
            dtt = self.dt
            ok = op.analyze(1, dtt)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying Newton with initial tangent...")
            op.algorithm('Newton', '-initial')
            dtt = self.dt
            ok = op.analyze(1, dtt)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying NewtonWithLineSearch...")
            op.algorithm('NewtonLineSearch', 0.8)
            dtt = self.dt
            ok = op.analyze(1, self.dt)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying Newton with initial tangent & relaxed "
                      f"convergence...")
            op.test('NormDispIncr', self.TOL * 0.1, self.ITERATIONS * 50)
            op.algorithm('Newton', '-initial')
            dtt = self.dt
            ok = op.analyze(1, dtt)
            op.test(self.TEST_TYPE, self.TOL, self.ITERATIONS)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying NewtonWithLineSearch & relaxed convergence...")
            op.test('NormDispIncr', self.TOL * 0.1, self.ITERATIONS * 50)
            op.algorithm('NewtonLineSearch', 0.8)
            dtt = self.dt
            ok = op.analyze(1, dtt)
            op.test(self.TEST_TYPE, self.TOL, self.ITERATIONS)
            op.algorithm(self.ALGORITHM_TYPE)
        # Next, halve the timestep with both algorithm and tolerance reduction
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying Newton with initial tangent, reduced timestep &"
                      f" relaxed convergence...")
            op.test('NormDispIncr', self.TOL * 0.1, self.ITERATIONS * 50)
            op.algorithm('Newton', '-initial')
            dtt = 0.5 * self.dt
            ok = op.analyze(1, dtt)
            op.test(self.TEST_TYPE, self.TOL, self.ITERATIONS)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - "
                      "Trying NewtonWithLineSearch, reduced timestep &"
                      f" relaxed convergence...")
            op.test('NormDispIncr', self.TOL * 0.1, self.ITERATIONS * 50)
            op.algorithm('NewtonLineSearch', 0.8)
            dtt = 0.5 * self.dt
            ok = op.analyze(1, dtt)
            op.test(self.TEST_TYPE, self.TOL, self.ITERATIONS)
            op.algorithm(self.ALGORITHM_TYPE)
        if ok:
            if self.pflag:
                print(f"[FAILURE] Failed at {control_time} - exit analysis...")
            self.collapse_index = -1

    def solve(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Looks for a solution, performs nonlinear time history analysis

        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray]
            Tuple contains:
                Accelerations in [g]
                Displacements in [m]
                Drifts in [%]
                Residual drifts in [%]
        """
        # Create self.output_path and a temporary cache folder
        if self.output_path is not None:
            create_path(self.output_path / "cache")
            cache_path = self.output_path / 'cache'
        else:
            create_path(Path("cache"))
            cache_path = Path('cache')

        # Set up analysis parameters
        control_time = 0.0
        ok = 0
        mdrift_init = 0.0

        # Recorders for both horizontal directions
        directions = 1
        for j in range(directions):
            filename = f'accelerations_{j + 1}.txt'

            # Recorders for nodal accelerations, because in current version of
            # openseespy ground accelerations are not being recorded otherwise
            op.recorder('Node', '-file', str(cache_path / filename),
                        '-timeSeries', int(f"5{j + 1}"),
                        '-nodeRange', int(self.bnode), int(self.tnode),
                        '-dof', j + 1, 'accel')

        # Number of storeys
        nst = self.tnode.shape[0]

        # Recorders for displacements, accelerations and drifts, initialization
        displacements = np.zeros((directions, nst + 1, 1))
        accelerations = np.zeros((directions, nst + 1, 1))
        drifts = np.zeros((directions, nst, 1))
        residuals = np.zeros((directions, nst, 1))

        # Run the actual analysis now
        while self.collapse_index == 0 and control_time <= self.dur and \
                not ok:
            # Start analysis
            ok = op.analyze(1, self.dt)
            control_time = op.getTime()

            # If the analysis fails, try the following changes to achieve
            # convergence
            # Analysis will be slower in here though...
            self._algorithm(ok, control_time)

            # Recorders
            temp_accel = np.zeros((directions, nst + 1, 1))
            temp_disp = np.zeros((directions, nst + 1, 1))
            temp_res = np.zeros((directions, nst, 1))

            # Recording EDPs at each storey level to return
            # For each direction
            for j in range(temp_accel.shape[0]):
                # At each storey level
                for i in range(nst + 1):
                    if i == nst:
                        # Index 0 indicates along X direction, and 1 indicates
                        # along Y direction
                        # Nodal displacements in m
                        temp_disp[j, i, 0] = op.nodeDisp(
                            int(self.tnode), j + 1)

                    else:
                        temp_disp[j, i, 0] = op.nodeDisp(
                            int(self.bnode), j + 1)

            # Appending into the global numpy arrays to return
            displacements = np.append(displacements, temp_disp, axis=2)
            if control_time >= self.dur - self.extra_dur:
                residuals = np.append(residuals, temp_res, axis=2)

            # Check whether drift capacity has been exceeded
            if mdrift_init >= self.dc:
                # If it was exceeded then local structure collapse is assumed
                self.collapse_index = 1
                # Hard cap the mdrift_init value to the drift capacity
                mdrift_init = self.dc

        # Wipe the model
        op.wipe()

        # Record the absolute accelerations, when use_recorder is True
        accelerations = []
        for j in range(directions):
            filename = f'accelerations_{j + 1}.txt'

            accelerations.append(np.transpose(
                read_text(cache_path / filename) / self.g))

        remove_directory_contents(cache_path)

        accelerations = np.asarray(accelerations)

        if self.collapse_index == -1:
            print(f"[FAILURE] Analysis failed to converge at {control_time}"
                  f" of {self.dur}.")
        if self.collapse_index == 0:
            print('[SUCCESS] Analysis completed successfully.')
        if self.collapse_index == 1:
            print('[FAILURE] Local structure collapse.')

        return accelerations, displacements, drifts, residuals
