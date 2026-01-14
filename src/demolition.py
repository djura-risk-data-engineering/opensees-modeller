import numpy as np


class Demolition:
    def __init__(self, demand: dict) -> None:
        """Init Demolition object

        Parameters
        ----------
        demand : dict
            Demands following NLTHA
        """
        self.demand = demand

    def get_residuals(self) -> np.ndarray:
        """Transform residual drifts into an array format

        Returns
        -------
        np.ndarray
            Residual drifts
            (number of stripes, number of ground motion records)
        """
        rec_key = next(iter(self.demand))
        directions = self.demand[rec_key].keys()

        residuals = None

        for d in directions:
            res_temp = np.zeros((
                len(self.demand[rec_key][d]['IM']),
                len(self.demand)
            ))

            if residuals is None:
                residuals = np.zeros((
                    len(self.demand[rec_key][d]['IM']),
                    len(self.demand)
                ))

            # For each ground motion
            for i, gm in enumerate(self.demand.keys()):
                order = np.argsort(self.demand[gm][d]['IM'])
                data = np.array(self.demand[gm][d]['RPSD']['global'])[order]

                res_temp[:, i] = data

            residuals = np.maximum(residuals, res_temp)

        return residuals
