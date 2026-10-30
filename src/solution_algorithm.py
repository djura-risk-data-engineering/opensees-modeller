from typing import List, Union, Tuple
from pathlib import Path
import openseespy.opensees as op
import numpy as np
import warnings

from .utilities import create_path, read_text, \
    remove_directory_contents


def apply_time_series(
    dt: float,
    pathx: Path,
    pathy: Path,
    fx: float,
    fy: float,
    omegas: List[float],
    damping: float,
    tstagx: int = 51,
    tstagy: int = 52,
    ptagx: int = 10,
    ptagy: int = 20,
    damping_type: str = 'Modal'
) -> None:
    """Applies time series

    Parameters
    ----------
    dt : float
        Analysis time step in [s]
    pathx : Path
        Path to ground motion record in X direction
    pathy : Path
        Path to ground motion record in Y direction
    fx : float
        Acceleration scaling factor for ground motion record in X direction
    fy : float
        Acceleration scaling factor for ground motion record in Y direction
    omegas : List[float]
        Circular frequencies, length must be larger than 2
    damping : List[float]
        Damping ratio, length must be larger than 2
    tstagx : int, optional
        Unique tag for time series in X direction, by default 51
    tstagy : int, optional
        Unique tag for time series in Y direction, by default 52
    ptagx : int, optional
        Uniform excitation load pattern tag for X direction, by default 10
    ptagy : int, optional
        Uniform excitation load pattern tag for Y direction, by default 20
    damping_type : str, optional
        Damping model, by default 'Modal-adjusted'
            'Rayleigh': mass and last-committed stiffness proportional,
            calibrated at the 1st and 3rd modes
            'Modal': modal damping in all modes in omegas
            'Modal-adjusted': initial stiffness proportional damping equal to
                the target at 10 x omega_1 (damps the high-frequency modes),
                plus modal damping for the rest in all modes in omegas
        Elements with -doRayleigh 0 (e.g., rigid links and hinges) do not
        contribute to the stiffness proportional part
    """
    # Delete the old analysis and all of its component objects
    op.wipeAnalysis()

    omegas = np.array(omegas)

    if damping_type == 'Rayleigh':
        w1 = omegas[0]
        w2 = omegas[2]
        a0 = 2 * w1 * w2 / (w2 ** 2 - w1 ** 2) * \
            (w2 * damping - w1 * damping)
        a1 = 2 * w1 * w2 / (w2 ** 2 - w1 ** 2) * \
            (-damping / w2 + damping / w1)
        #           M    KT   KI  Kn
        op.rayleigh(a0, 0.0, 0.0, a1)

    elif damping_type == 'Modal':
        num_modes = len(omegas)
        # Modal damping needs the eigen solution in the current domain
        op.eigen(num_modes)
        op.modalDamping(*[damping] * num_modes)

    elif damping_type == 'Modal-adjusted':
        num_modes = len(omegas)
        # Modal damping needs the eigen solution in the current domain
        op.eigen(num_modes)
        # Stiffness proportional part, equal to the target ratio at
        # 10 x omega_1 and larger above it (damps the high-frequency modes)
        omega_hf = 10 * omegas[0]
        a1 = 2 * damping / omega_hf
        op.rayleigh(0.0, 0.0, a1, 0.0)  # initial stiffness, never negative
        # Modal part, the rest, so that the total is the target in each mode
        ratios = [max(damping - a1 * w / 2, 0.0) for w in omegas]
        op.modalDamping(*ratios)

    else:
        raise ValueError(f"Unknown damping_type '{damping_type}'")

    # Time series excitation
    # op.timeSeries('Path', tstagx, '-dt', dt,
    #               '-filePath', str(pathx), '-factor', fx)
    try:
        accx = list(np.loadtxt(pathx)[:, 1])
    except IndexError:
        accx = list(np.loadtxt(pathx))

    op.timeSeries('Path', tstagx, '-dt', dt, '-values', *accx, '-factor', fx)

    op.pattern('UniformExcitation', ptagx, 1, '-accel', tstagx)

    if pathy is not None:
        # op.timeSeries('Path', tstagy, '-dt', dt,
        #               '-filePath', str(pathy), '-factor', fy)
        try:
            accy = list(np.loadtxt(pathy)[:, 1])
        except IndexError:
            accy = list(np.loadtxt(pathy))

        op.timeSeries('Path', tstagy, '-dt', dt, '-values', *accy,
                      '-factor', fy)
        op.pattern('UniformExcitation', ptagy, 2, '-accel', tstagy)

    # Constraints, enforced exactly (Penalty with 1e15 ill-conditions the
    # stiffness matrix)
    op.constraints("Transformation")

    op.numberer('RCM')
    op.system('UmfPack')


class SolutionAlgorithm:
    g = 9.81
    ITERATIONS = 50
    ALGORITHM_TYPE = ['SecantNewton']
    # Converged only when both the displacement increment and the unbalanced
    # force are small, so that steps with a large residual are not accepted.
    # NOTE: always pass the print flag and nothing after it, the openseespy
    # parser overwrites the max iterations with the norm type otherwise
    TEST_TYPE = 'NormDispAndUnbalance'
    TOL = 1e-06  # displacement increment norm [m]
    TOL_R = 1e-04  # unbalanced force norm [kN]
    # INTEGRATOR_TYPE = ['Newmark', 0.5, 0.25]
    INTEGRATOR_TYPE = ['TRBDF2']  # dissipates high-frequency response
    # Time step factors tried in descending order when a step fails
    DT_FACTORS = [1.0, 0.5, 0.25, 0.1, 0.01]
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
        directions: int = 2,
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
        self.directions = directions

        # TODO, remove pflag and do logging instead
        self.pflag = pflag

        self._set_analysis()

    def _set_analysis(self):
        """Set up initial analysis parameters
        """
        self._set_test(self.TOL, self.ITERATIONS)
        op.algorithm(*self.ALGORITHM_TYPE)
        op.integrator(*self.INTEGRATOR_TYPE)
        op.analysis('Transient')

    def _set_test(self, tol: float, iterations: int) -> None:
        """Sets the convergence test, scaling the force tolerance with tol

        Parameters
        ----------
        tol : float
            Tolerance on the displacement increment norm
        iterations : int
            Maximum number of iterations before returning failure
        """
        op.test(self.TEST_TYPE, tol, tol / self.TOL * self.TOL_R,
                iterations, 0)

    def _reset_solver(self) -> None:
        """Restores the original test and algorithm, so that the settings
        of a recovered step are not carried over to the next steps"""
        self._set_test(self.TOL, self.ITERATIONS)
        op.algorithm(*self.ALGORITHM_TYPE)

    def _try_algorithms(self, tol: float, dt: float,
                        iterations: int = 50) -> int:
        """Tries alternative algorithms to perform a single analysis step

        Parameters
        ----------
        tol : float
            Tolerance on the displacement increment norm
        dt : float
            Analysis time step
        iterations : int, optional
            Maximum number of iterations, by default 50

        Returns
        -------
        int
            0 if the step converged, != 0 otherwise
        """
        self._set_test(tol, iterations)
        op.algorithm('KrylovNewton')
        ok = op.analyze(1, dt)
        if ok != 0:
            op.algorithm('NewtonLineSearch', '-InitialInterpolated', 0.8)
            ok = op.analyze(1, dt)
        if ok != 0:
            op.algorithm('BFGS')
            ok = op.analyze(1, dt)
        return ok

    def _do_single_analysis_step(self, dt: float) -> Tuple[int, float, float]:
        """Performs a single analysis step, if it fails tries alternative
        algorithms, then smaller time steps, and relaxed tolerances as a last
        resort. After a reduced time step, the time step is increased back
        gradually.

        Parameters
        ----------
        dt : float
            Time step used for the previous step

        Returns
        -------
        Tuple[int, float, float]
            0 if the step converged, != 0 otherwise
            Current time
            Time step used for this step
        """
        dt_values = sorted([f * self.dt for f in self.DT_FACTORS],
                           reverse=True)
        dt_idx = dt_values.index(dt)

        # Gradually increase the time step back after a reduced one
        if dt_idx != 0:
            dt_idx -= 1
            dt = dt_values[dt_idx]

        # Do the analysis with the original test and algorithm
        self._reset_solver()
        ok = op.analyze(1, dt)

        # Try alternative algorithms with the same time step first
        if ok != 0:
            ok = self._try_algorithms(self.TOL, dt)

        # If still failing, keep decreasing the time step
        while ok != 0 and dt_idx < len(dt_values) - 1:
            dt_idx += 1
            dt = dt_values[dt_idx]
            ok = self._try_algorithms(self.TOL, dt)

        # Relax the tolerances as a last resort (10 x TOL and 10 x TOL_R),
        # the next step starts again from the original ones
        if ok != 0:
            ok = self._try_algorithms(10 * self.TOL, dt, 100)

        if ok != 0:
            if self.pflag:
                print(f"[FAILURE] Failed at {op.getTime()} of {self.dur} "
                      "seconds - exit analysis...")
            self.collapse_index = -1

        return ok, op.getTime(), dt

    def _verify_against_zerolength(self) -> np.ndarray:
        """Verify that the elements of the model are not of zero length

        Returns
        -------
        np.ndarray
            Storey heights
        """
        for d in range(len(self.tnode)):
            top_nodes = self.tnode[d]
            bot_nodes = self.bnode[d]

            h = np.array([])
            for i, top_node in enumerate(top_nodes):
                top = op.nodeCoord(int(top_node), 3)
                bot = op.nodeCoord(int(bot_nodes[i]), 3)

                dist = top - bot
                h = np.append(h, dist)

                if dist == 0:
                    warnings.warn('[WARNING] Zerolength found in drift check.')
        return h

    def solve(self, rec: int = None
              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
        """Looks for a solution, performs nonlinear time history analysis

        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]
            Tuple contains:
                Accelerations in [g]
                Displacements in [m]
                Drifts in [%]
                Residual drifts in [%]
                Collapse index
                    -1: analysis failed to converge
                    0: analysis completed successfully
                    1: drift capacity exceeded (collapse)
        """
        # Create self.output_path and a temporary cache folder
        if self.output_path is not None:
            if rec is None:
                cache_path = self.output_path / 'cache'
            else:
                cache_path = self.output_path / f'rec{rec}_cache'
        else:
            if rec is None:
                cache_path = Path('cache')
            else:
                cache_path = Path(f'rec{rec}_cache')
        create_path(cache_path)

        # Set up analysis parameters
        control_time = 0.0
        ok = 0
        mdrift_init = 0.0

        # Recorders for both horizontal directions
        for j in range(self.directions):
            filename = f'accelerations_{j + 1}.txt'

            # Recorders for nodal accelerations, because in current version of
            # openseespy ground accelerations are not being recorded otherwise
            # op.recorder('Node', '-file', str(cache_path / filename),
            #             '-timeSeries', int(f"5{j + 1}"),
            #             '-nodeRange', int(self.bnode[0, 0]
            #                               ), int(self.tnode[0, -1]),
            #             '-dof', j + 1, 'accel')

            _nodes = np.concatenate(
                ([self.bnode[0][0]], self.tnode[0])).tolist()

            op.recorder('Node', '-file', str(cache_path / filename),
                        '-timeSeries', int(f"5{j + 1}"),
                        '-node', *_nodes,
                        '-dof', j + 1, 'accel')

        # Number of storeys
        nst = self.tnode.shape[1]

        # initialize maximum drifts and accelerations
        mdrift = np.zeros((self.directions, nst))
        # maccel = np.zeros((directions, nst + 1))

        # Recorders for displacements, accelerations and drifts, initialization
        displacements = np.zeros((self.directions, nst + 1, 1))
        accelerations = np.zeros((self.directions, nst + 1, 1))
        drifts = np.zeros((self.directions, nst, 1))
        residuals = np.zeros((self.directions, nst, 1))

        h = self._verify_against_zerolength()
        dt_cur = self.dt

        # Run the actual analysis now
        while self.collapse_index == 0 and control_time <= self.dur and \
                not ok:
            # Analysis step, if it fails alternative algorithms, smaller time
            # steps and relaxed tolerances are tried
            ok, control_time, dt_cur = self._do_single_analysis_step(dt_cur)

            # Recorders
            temp_accel = np.zeros((self.directions, nst + 1, 1))
            temp_disp = np.zeros((self.directions, nst + 1, 1))
            temp_drift = np.zeros((self.directions, nst, 1))
            temp_res = np.zeros((self.directions, nst, 1))

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
                            int(self.tnode[0, i - 1]), j + 1)

                    else:
                        temp_disp[j, i, 0] = op.nodeDisp(
                            int(self.bnode[0, i]), j + 1)

                    if i > 0:
                        # Storey height
                        cht = h[i - 1]
                        # Storey drifts in %
                        temp_drift[j, i - 1, 0] = 100.0 * \
                            abs(temp_disp[j, i, 0]
                                - temp_disp[j, i - 1, 0]) / cht

                        if control_time >= self.dur - self.extra_dur:
                            temp_res[j, i - 1, 0] = 100.0 * \
                                abs(temp_disp[j, i, 0]
                                    - temp_disp[j, i - 1, 0]) / cht

            # Appending into the global numpy arrays to return
            displacements = np.append(displacements, temp_disp, axis=2)
            drifts = np.append(drifts, temp_drift, axis=2)
            if control_time >= self.dur - self.extra_dur:
                residuals = np.append(residuals, temp_res, axis=2)

            # Check storey drifts and accelerations
            for i in range(1, nst + 1):
                # Top node displacement
                tnode_disp_x = op.nodeDisp(int(self.tnode[0, i - 1]), 1)
                tnode_disp_y = op.nodeDisp(int(self.tnode[0, i - 1]), 2)
                # Bottom node displacement
                bnode_disp_x = op.nodeDisp(int(self.bnode[0, i - 1]), 1)
                bnode_disp_y = op.nodeDisp(int(self.bnode[0, i - 1]), 2)
                # Storey height
                cht = h[i - 1]
                # Storey drift in %
                cdrift_x = 100.0 * abs(tnode_disp_x - bnode_disp_x) / cht
                cdrift_y = 100.0 * abs(tnode_disp_y - bnode_disp_y) / cht
                # Record the peak storey drifts
                if cdrift_x >= mdrift[0, i - 1]:
                    mdrift[0, i - 1] = cdrift_x

                if self.directions == 2 and cdrift_y >= mdrift[1, i - 1]:
                    mdrift[1, i - 1] = cdrift_y

                if max(cdrift_x, cdrift_y) >= mdrift_init:
                    mdrift_init = max(cdrift_x, cdrift_y)

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
        for j in range(self.directions):
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

        return (accelerations, displacements, drifts, residuals,
                self.collapse_index)
