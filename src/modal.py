from typing import List
import openseespy.opensees as op
import numpy as np


class Modal:
    def __init__(self, num_modes: int, damping: float = 0.05,
                 damping_modes: List[int] = None) -> None:
        """Performs eigenvalue analysis

        Parameters
        ----------
        num_modes : int
            Number of modes
        damping : float, optional
            Damping ratio, by default 0.05
        damping_modes : List[int], optional
            Modes to apply damping to, by default [1, 3] applies damping
            to 1st and 3rd modes
        """
        self.num_modes = num_modes
        self.damping_modes = damping_modes
        self.damping = damping

        if self.damping_modes is None:
            self.damping_modes = [1, 3]

        # Perform eigenvalue analysis
        self.eigenvectors = np.array(self._compute_eigenvectors())
        self._record_stuff()
        self.omega, self.freq, self.period = self._extract_eigenvalues()

        self.damping_modes = self._get_damping()

    def _compute_eigenvectors(self) -> List[float]:
        """Perofrm eigenvalue analysis

        Returns
        -------
        List[float]
            Eigenvectors
        """
        lam = None
        try:
            op.wipeAnalysis()
            lam = op.eigen(self.num_modes)
        except Exception:
            print('[Warning] Eigensolver failed, trying genBandArpack...')
            try:
                lam = op.eigen('-genBandArpack', self.num_modes)
            except Exception:
                print('[Warning] Eigensolver failed, trying fullGenLapack...')
                try:
                    lam = op.eigen('-fullGenLapack', self.num_modes)
                except Exception:
                    print('[Warning] Eigensolver failed, '
                          'trying symmBandLapack...')
                    try:
                        lam = op.eigen('-symmBandLapack', self.num_modes)
                    except Exception:
                        print('[Warning] Eigensolver failed.')

        return lam

    @staticmethod
    def _record_stuff():
        """Records the eigenvectors
        """
        op.record()

    def _extract_eigenvalues(
            self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Extracts eigenvalues to arrays

        Returns
        -------
        tuple[np.ndarray, np.ndarray, np.ndarray]
            Circular frequencies, frequencies and periods
        """
        omega = np.sqrt(self.eigenvectors)
        freq = np.sqrt(self.eigenvectors) / 2 / np.pi
        period = 2 * np.pi / np.sqrt(self.eigenvectors)
        return omega, freq, period

    def _get_damping(self) -> List[float]:
        """Gets damping values for the modes of interest

        Returns
        -------
        List[float]
            Damping ratios

        Raises
        ------
        TypeError
            If no damping is provided
        """
        if self.damping_modes is None:
            self.damping_modes = [1]

        n = len(self.damping_modes)
        if n > 1:
            wi = self.omega[(self.damping_modes[0] - 1)]
            wj = self.omega[(self.damping_modes[1] - 1)]
            a0 = 2 * wi * wj / (wj ** 2 - wi ** 2) * \
                (wj * self.damping - wi * self.damping)
            a1 = 2 * wi * wj / (wj ** 2 - wi ** 2) * \
                (-self.damping / wj + self.damping / wi)
            modes = []
            for m in range(self.num_modes):
                wn = self.omega[m]
                modes.append(0.5 * (a0 / wn + a1 * wn))
            else:
                return modes

        elif n == 1:
            modes = 0.0
            return modes

        else:
            raise TypeError('No damping mode was provided')
