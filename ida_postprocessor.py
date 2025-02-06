import pickle
from typing import List, Union, Tuple
from pathlib import Path
from itertools import chain
import numpy as np
from scipy.interpolate import interp1d


class IDAPostprocessor:

    MTDISP_RANGE = np.linspace(0.01, 1, 200)
    MPSD_RANGE = np.linspace(0.01, 5, 200)

    # Quantile ranges to visualize for the IDAs
    QTILE_RANGE = np.array([0.16, 0.5, 0.84])

    def __init__(
        self,
        ida: Union[Path, dict],
        ims: Union[Path],
        dt_path: Union[np.ndarray, Path] = None,
        dur_path: Union[np.ndarray, Path] = None,
        gm_folder: Path = None,
    ) -> None:
        """IDA postprocessor

        Parameters
        ----------
        ida : Path
            Path to IDA outputs
        ims : Union[Path]
            Path to IM values output from IDA
        dt_path : Union[np.ndarray, Path], optional
            Path to file containing time steps of the ground motions used
            during IDA, by default None
        dur_path : Union[np.ndarray, Path], optional
            Path to file containing durations of the ground motions used
            during IDA, by default None
        gm_folder : Path, optional
            Path to ground motions used during IDA, by default None
            If dt_path and dur_path are left None, gm_folder must be provided.
            In that case, the tool will search the directory for any file
            containing characters "dt" for dt_path and "dur" for duration path.
            If "dur" file is missing, the durations will be computed using the
            "dt" file and the ground motion set.
        """
        self.ida = ida
        self.ims = ims
        self.durs, self.dts = self.get_durs_dts(dt_path, dur_path, gm_folder)

    def get_durs_dts(
        self,
        dt_path: Union[np.ndarray, Path] = None,
        dur_path: Union[np.ndarray, Path] = None,
        gm_folder: Path = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Get durations and time steps of ground motion records used for IDA

        Parameters
        ----------
        dt_path : Union[np.ndarray, Path], optional
            Path to file containing time steps of the ground motions used
            during IDA, by default None
        dur_path : Union[np.ndarray, Path], optional
            Path to file containing durations of the ground motions used
            during IDA, by default None
        gm_folder : Path, optional
            Path to ground motions used during IDA, by default None
            If dt_path and dur_path are left None, gm_folder must be provided.
            In that case, the tool will search the directory for any file
            containing characters "dt" for dt_path and "dur" for duration path.
            If "dur" file is missing, the durations will be computed using the
            "dt" file and the ground motion set.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            Durations
            Time steps

        Raises
        ------
        ValueError
            Ground motion information is not provided when all inputs are None
        ValueError
            Ground motion time steps not provided when gm_folder is provided,
            but time steps are not found
        ValueError
            Ground motion durations not provided, when gm_folder is provided,
            but durations are not found
        """
        if gm_folder is None and (dt_path is None or dur_path is None):
            raise ValueError("Ground motion information is not provided!")

        dts = None
        if dt_path is not None:
            if isinstance(dt_path, Path):
                dts = np.loadtxt(dt_path, ndmin=1)
            else:
                dts = dt_path
        else:
            dt_path = gm_folder.glob('**/*dt*')

            for file in dt_path:
                dts = np.loadtxt(file, ndmin=1)
                break

        if dts is None:
            raise ValueError("Ground motion time steps not provided!")

        durs = None
        if dur_path is not None:
            if isinstance(dur_path, Path):
                durs = np.loadtxt(dur_path, ndmin=1)
            else:
                durs = dur_path
        else:
            dur_path = gm_folder.glob('**/*dur*')

            for file in dur_path:
                durs = np.loadtxt(file, ndmin=1)
                break

        if durs is not None:
            return durs, dts

        # Durations file not found, computing based on dt and
        # ground motion length
        durs = np.zeros(dts.shape)

        # Find names of 1st components
        filenames_1 = chain(gm_folder.glob('**/*name*1*'),
                            gm_folder.glob('**/*1*name*'))
        filenames_2 = chain(gm_folder.glob('**/*name*2*'),
                            gm_folder.glob('**/*2*name*'))

        for file in filenames_1:
            names_1 = np.loadtxt(file, dtype="str", ndmin=1)
            break
        for file in filenames_2:
            names_2 = np.loadtxt(file, dtype="str", ndmin=1)
            break

        for i in range(len(durs)):
            len_1 = len(np.loadtxt(gm_folder / names_1[i]))
            len_2 = len(np.loadtxt(gm_folder / names_2[i]))

            durs[i] = dts[i] * (max(len_1, len_2) - 1)

        if np.any(durs == 0):
            raise ValueError("Ground motion durations not provided!")

        return durs, dts

    def _splinequery(
        self,
        edp_range: np.ndarray,
        qtile_range: Union[np.ndarray, List],
        im: np.ndarray,
        edp: np.ndarray,
        num_recs: int,
    ) -> Tuple[np.ndarray, np.ndarray]:

        im_spl = np.zeros([num_recs, len(edp_range)])
        im_spl[:] = np.nan
        im_qtile = np.zeros([len(qtile_range), len(edp_range)])

        # Getting the edp-based im values
        for rec in range(num_recs):
            spl = interp1d(edp[rec], im[rec])

            for i in range(len(edp_range)):
                if edp_range[i] <= max(edp[rec]):
                    im_spl[rec][i] = spl(edp_range[i])
                else:
                    im_spl[rec][i] = im_spl[rec][i - 1]

        # Getting the edp-based im quantiles
        for q in range(len(qtile_range)):
            for i in range(len(edp_range)):
                im_qtile[q][i] = np.quantile(im_spl[:, i], qtile_range[q])

        return im_spl, im_qtile

    def _read_ida(self):
        # Number of records
        nrecs = len(self.dts)

        if isinstance(self.ida, dict):
            data = self.ida
        elif self.ida.is_file():
            with open(self.ida, 'rb') as f:
                data = pickle.load(f)

        else:
            data = {}
            for rec in range(nrecs):
                data[rec] = {}

            for file in chain(self.ida.glob('*pickle*'),
                              self.ida.glob('*pkl*')):
                rec_run = file.name.replace(".pickle", "").replace(
                    "Record", "").replace("Run", "").split("_")

                rec = int(rec_run[0]) - 1
                run = int(rec_run[1])

                with open(file, 'rb') as f:
                    data[rec][run] = pickle.load(f)

        return data

    def postprocess(self) -> Tuple[dict, dict]:
        """Postprocess IDA outputs

        Returns
        -------
        Tuple containing
            dict: postprocessed IDA results
                {
                    "record_id" {
                        "Direction": {         # "1" and "2"
                            "IM": List[float],
                            "PSD": {
                                # peak values for each storey level
                                "storey level": List[float],
                                # peak values for the building
                                "global": List[float],
                            },
                            "PFA": {
                                "floor level": List[float],
                                "global": List[float],
                            },
                            "RPSD": {
                                "storey level": List[float],
                                "global": List[float],
                            }
                        },
                    }
                }

            dict: cached IDA results, interpolation results, quantiles
                Useful for data visualization
        """
        data = self._read_ida()
        nrecs = len(self.dts)

        if isinstance(self.ims, Path):
            im_ida = np.genfromtxt(self.ims, delimiter=',', ndmin=2)
        else:
            im_ida = self.ims

        # Number of runs
        nruns = im_ida.shape[1]

        # Loop for each direction for a 3D model
        n_dir = 2

        # Initialize some variables
        im = np.zeros([nrecs, nruns + 1])
        idx = np.zeros([nrecs, nruns], dtype='i')
        mpfa_us = np.full([nrecs, nruns], np.nan)
        mpsd_us = np.full([nrecs, nruns], np.nan)
        mrpsd_us = np.full([nrecs, nruns], np.nan)
        mtdisp_us = np.full([nrecs, nruns + 1], np.nan)
        # mtrx = np.full([nrecs, nruns + 1], np.nan)

        mpfa = {}
        mpsd = {}
        mtdisp = {}

        for d in range(n_dir):
            mpfa[d] = np.zeros([nrecs, nruns + 1])
            mpsd[d] = np.zeros([nrecs, nruns + 1])
            mtdisp[d] = np.zeros([nrecs, nruns + 1])

        # Initialize target dictionary with its first stage
        out = {}
        cache = {}

        # Loop for each record
        for rec in range(1, nrecs + 1):
            out[rec] = {}
            for d in range(n_dir):
                if d + 1 not in cache:
                    cache[d + 1] = {}

                print("\nDirection: %s" % d)

                out[rec][d + 1] = {
                    "IM": im_ida[rec - 1].tolist(),
                    'PSD': {}, 'PFA': {}, 'RPSD': {},
                }

                print("Record: gm_%s" % rec)

                # Sort the IM values
                im[rec - 1, 1:] = np.sort(im_ida[rec - 1])
                idx[rec - 1, :] = np.argsort(im_ida[rec - 1])

                # Loop over each run
                for run in range(1, nruns + 1):
                    print(f"Record: gm_{rec}, Run {run}")

                    # Select analysis results of rec and run
                    selection = data[rec - 1][run]

                    # Get PFAs in g
                    pfa = np.amax(abs(selection[0][:, :]), axis=2)[d]

                    for st, val in enumerate(pfa):
                        if st in out[rec][d + 1]['PFA']:
                            out[rec][d + 1]['PFA'][st].append(float(val))
                        else:
                            out[rec][d + 1]['PFA'][st] = [float(val)]

                    mpfa_us[rec - 1, run - 1] = max(pfa)

                    # Get PSDs in %
                    psd = np.amax(abs(selection[2]), axis=2)[d]

                    for st, val in enumerate(psd):
                        if st + 1 in out[rec][d + 1]['PSD']:
                            out[rec][d + 1]['PSD'][st + 1].append(float(val))
                        else:
                            out[rec][d + 1]['PSD'][st + 1] = [float(val)]

                    mpsd_us[rec - 1, run - 1] = max(psd)

                    # Getting the residual PSDs in %
                    # Analysis time step
                    dt = self.dts[rec - 1]
                    idxres = int(self.durs[rec - 1] / dt)
                    res_drifts = selection[2][:, :, idxres:][d]

                    for st in range(len(psd)):
                        if len(res_drifts[st]) > 0:
                            if st + 1 in out[rec][d + 1]['RPSD']:
                                out[rec][d + 1]['RPSD'][st + 1].append(
                                    float(sum(res_drifts[st])
                                          / len(res_drifts[st])))
                            else:
                                out[rec][d + 1]['RPSD'][st + 1] = \
                                    [float(sum(res_drifts[st])
                                           / len(res_drifts[st]))]

                        else:
                            if st + 1 in out[rec][d + 1]['RPSD']:
                                out[rec][d + 1]['RPSD'][st + 1].append(
                                    float(selection[2][0][st][-1]))
                            else:
                                out[rec][d + 1]['RPSD'][st + 1] = [
                                    float(selection[2][0][st][-1])]

                    # Record the peak value of residual drift at each run
                    # for each record
                    mrpsd_us[rec - 1, run - 1] = \
                        max(np.sum(res_drifts, axis=1) / res_drifts.shape[1])

                    # Get the top displacement in m
                    top_disp = np.amax(abs(selection[1]), axis=n_dir)[d]
                    mtdisp_us[rec - 1, run - 1] = top_disp[-1]

                # Sort the results
                out[rec][d + 1]['PFA']['global'] = mpfa_us[rec - 1, :].tolist()
                out[rec][d + 1]['PSD']['global'] = mpsd_us[rec - 1, :].tolist()
                out[rec][d + 1]['RPSD']['global'] = \
                    mrpsd_us[rec - 1, :].tolist()

                # Repopulate nans with max of data
                out[rec][d + 1]['RPSD']['global'] = [
                    max(out[rec][d + 1]['RPSD']['global'])
                    if np.isnan(x) else x for x in out[rec][d + 1]['RPSD'][
                        'global']
                ]

                mpfa[d][rec - 1, 1:] = mpfa_us[rec - 1, :][idx[rec - 1]]
                mpsd[d][rec - 1, 1:] = mpsd_us[rec - 1, :][idx[rec - 1]]
                mtdisp[d][rec - 1, 1:] = mtdisp_us[rec - 1, :][idx[rec - 1]]

        # Fit the splines to the data
        for d in range(n_dir):
            disps = mtdisp[d]
            drifts = mpsd[d]

            im_spl, im_qtile = self._splinequery(
                self.MTDISP_RANGE,
                self.QTILE_RANGE,
                im,
                disps,
                nrecs,
            )

            im_spl_psd, im_qtile_psd = self._splinequery(
                self.MPSD_RANGE,
                self.QTILE_RANGE,
                im,
                drifts,
                nrecs,
            )

            # Creating a dictionary for the spline fits
            cache[d + 1] = {
                "im_spl": im_spl.copy(), "disp": disps.copy(),
                "im": im.copy(), "im_qtile": im_qtile.copy(),
                "mtdisp": self.MTDISP_RANGE.copy(), "drift": drifts.copy(),
                "mpsd": self.MPSD_RANGE.copy(),
                "im_spl_psd": im_spl_psd.copy(),
                "im_qtile_psd": im_qtile_psd.copy()
            }

        return out, cache
