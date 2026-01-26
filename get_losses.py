import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from src.hazard import Hazard
from src.utilities import to_json_serializable
from scipy.interpolate import interp1d
from scipy import stats


def get_mafe_ls(h: np.ndarray, s: np.ndarray,
                theta: np.ndarray, beta: np.ndarray, add_tail=True):
    """
    Compute the mean annual frequency of exceedance (MAFE) of a limit state
    defined by a lognormal fragility function, by direct integration with
    a seismic hazard curve.

    The method evaluates:

        λ_LS = ∫ P(LS | IM) · |dλ(IM) / dIM| dIM

    where λ(IM) is the mean annual frequency of exceedance (MAFE) of the
    intensity measure IM. The integral is computed using the closed-form
    bin-wise formulation described in Porter et al. (2004), assuming:
        - the hazard curve is log-linear between adjacent IM points
        (i.e. exponential in linear IM space),
        - the fragility (conditional exceedance probability) varies linearly
        between adjacent IM points.

    Pre-processing is applied to the hazard input to improve numerical
    stability:
        1. Hazard values H≤0 are removed (typically occurring at very low IM).
        2. Non-decreasing or duplicated IM points are removed (typically
        occurring at the high-IM tail of the hazard curve).

    Parameters
    ----------
    H : np.ndarray
        Mean annual frequency of exceedance (MAFE) values of the hazard curve,
        λ(IM), defined at discrete IM levels.
    s : np.ndarray
        Intensity measure (IM) levels corresponding to the hazard values H.
    eta : float
        Median of the lognormal fragility function (IM at 50% probability).
    beta : float
        Lognormal dispersion of the fragility function (total logarithmic
        standard deviation).
    add_tail : bool, optional
        If True, includes a tail contribution to account for hazard exceedances
        beyond the largest intensity measure (IM) explicitly included in the
        numerical integration.

    Returns
    -------
    lambda_ls : float
        Mean annual frequency of exceedance (MAFE) of the specified limit
        state.

    References
    ----------
    Porter, K. A., Beck, J. L., & Shaikhutdinov, R. V. (2004).
    Simplified Estimation of Economic Seismic Risk for Buildings.
    Earthquake Spectra, 20(4), 1239-1263.
    https://doi.org/10.1193/1.1809129
    """
    h = np.asarray(h, dtype=float)
    s = np.asarray(s, dtype=float)

    # Strip non-positive hazard values
    mask = h > 0
    h = h[mask]
    s = s[mask]

    # Strip non-decreasing hazard segments (keep only where H decreases with s)
    keep = [0]
    for i in range(len(s) - 1):
        if h[i+1] < h[i] and s[i+1] > s[i]:
            keep.append(i+1)
    keep = np.array(sorted(set(keep)))

    h = h[keep]
    s = s[keep]

    # Fragility / conditional probability at hazard points
    p = stats.lognorm.cdf(s, s=beta, scale=theta)  # P(LS | IM=s)

    # Bin integration (Porter et al. method 1)
    ds = np.diff(s)
    k = np.log(h[1:] / h[:-1]) / ds          # d(ln H)/ds
    dp = np.diff(p)

    dl = (
        p[:-1] * h[:-1] * (1 - np.exp(k * ds))
        - (dp / ds) * h[:-1] * (np.exp(k * ds) * (ds - 1 / k) + 1 / k)
    )

    lambda_ls = float(np.sum(dl))

    # Tail beyond last hazard point
    if add_tail:
        lambda_ls += float(p[-1] * h[-1])

    return lambda_ls


def get_eal(
    iml: np.ndarray, loss: np.ndarray, hazard: dict, rc: float = 1.0
):
    """Computes expected annual loss (EAL)

    Parameters
    ----------
    iml : np.ndarray
        IM levels
    loss : np.ndarray
        Expected Losses
    hazard : dict
        Hazard function
    rc : float
        Replacement cost

    Returns
    -------
    tuple[float, dict]
        float - EAL as a % of the total replacement cost
        dict - Cached results
            {
                'eal-bins': List,
                'iml': List,
                'mafe': List,
                'loss-ratio': float,
            }
    """
    # Hazard
    hazard = {key.lower(): value for key, value in hazard.items()}
    iml_hazard = np.array(hazard['s'])
    mafe = np.asarray(hazard["mafe"])

    non_zero_indices = mafe != 0
    iml_hazard = iml_hazard[non_zero_indices]
    mafe = mafe[non_zero_indices]

    # Add zeros to beginning of iml and loss
    iml = np.insert(iml, 0, 0)
    loss = np.insert(loss, 0, 0)

    # Interpolation function for the loss
    spline = interp1d(iml, loss, fill_value=loss[-1], bounds_error=False)

    # Loss as the ratio of replacement cost
    mdf = spline(iml_hazard) / rc

    # Hazard IML tests
    diml = np.diff(iml_hazard)

    # dMAFEdIML, logarithmic gradient divided by IML step
    dmafe_diml = np.log(mafe[1:] / mafe[:-1]) / diml

    # Loss ratio step
    dmdf = np.diff(mdf)

    # EAL contributions of each subgroup
    eal_bins = np.zeros(dmafe_diml.shape)
    eal_bins[dmafe_diml != 0] = mdf[:-1] * mafe[:-1] * (
        1 - np.exp(dmafe_diml * diml)) - dmdf / diml * mafe[:-1] * (
        np.exp(dmafe_diml * diml) * (diml - 1 / dmafe_diml) + 1 / dmafe_diml)

    # EAL expressed in the units of total replacement cost
    eal = rc * (sum(eal_bins) + mafe[-1])

    # EAL ratio in % of the total replacement cost
    eal_ratio = eal / rc * 100

    # Cache the results
    cache = {
        'eal-bins': list(eal_bins),
        'hazard-iml': list(iml_hazard),
        'hazard-mafe': list(mafe),
        'loss-ratio': list(mdf),
    }

    return eal_ratio, cache


def weibull(x, popt):
    a, b, c = popt
    return a * (1 - np.exp(-((x / b) ** c)))


def papadopoulos(x, popt):
    a, b, c, d, e = popt
    return e * x**a / (b**a + x**a) + (1 - e) * x**c / (d**c + x**c)


if __name__ == '__main__':

    # HAZARD
    hazard_poes = [
        9.99E-01, 9.93E-01, 9.70E-01, 9.08E-01,
        7.89E-01, 6.20E-01, 4.36E-01, 2.76E-01, 1.57E-01, 8.19E-02,
        3.88E-02, 1.65E-02, 6.19E-03, 1.98E-03, 5.13E-04, 9.77E-05
    ]
    hazard_imls = [
        0.0145422, 0.0211474, 0.0307529,
        0.0447214, 0.0650345, 0.0945742, 0.1375312, 0.2, 0.2908431,
        0.4229485, 0.6150582, 0.8944272, 1.3006898, 1.8914832, 2.7506241, 4
    ]

    # DEMANDS
    path = Path(__file__).parent
    path_loss = path / 'outputs/Loss'
    msa_path = path / 'outputs/MSA/msa.json'
    msa_data = json.load(open(msa_path))
    frag_path = path / 'outputs/MSA/frags_msa.json'
    frag_data = json.load(open(frag_path))
    theta_c = frag_data['DLS-4']['median']
    beta_c = frag_data['DLS-4']['beta']

    # STOREY LOSS FUNCTIONS
    methods = {'weibull': weibull, 'papadopoulos': papadopoulos}
    slfs_path = path / 'data/slfs' / "edp-dv-standard.json"
    edp_dv = json.load(open(slfs_path))
    groups = list(edp_dv.keys())

    # LOSS SETTINGS
    percentile = 'mean'  # loss percentile
    direction = '1'  # SRSS can used for two-directional dynamic analysis
    nst = 3  # number of storeys
    rc = 1600000  # replacement cost

    # INITIALIZE SOME PARAMETERS
    rps = []  # Return periods (considered in MSA)
    mafe = []  # Mean annual frequence of exceedance (considered in MSA)
    imls = []  # Intensity measure levels (considered in MSA)
    s_mean_losses_nc = []  # E[L_S|NC,IM]
    ns_mean_losses_nc = []  # E[L_NS|NC,IM]
    tot_mean_losses_nc = []  # E[L_T|NC,IM]
    ns_keys = ['2 - NS: PSD', '3 - NS: PFA']
    s_keys = ['1 - S: PSD']
    # Loop through each return period
    for rp in msa_data.keys():
        s_loss = 0.0  # initialise losses from structural comp.
        ns_loss = 0.0  # initialise losses from non-structural comp.
        s_mean_loss = 0.0  # initialise mean losses from structural comp.
        ns_mean_loss = 0.0  # initialise mean losses from non-structural comp.
        for group in groups:
            # Get regression parameters
            method = methods.get(edp_dv[group]['regression'])
            params = edp_dv[group]['fitting_parameters'][percentile]
            coeffs = params['popt']
            multiplier = params['multiplier']
            # Set the engineering demand parameter
            if 'PSD' in group:
                edp = 'PSD'
            elif 'PFA' in group:
                edp = 'PFA'
            # Assemble the losses for non-collapse cases
            demands = msa_data[rp][direction]['PFA']
            loss = 0.0  # total building loss per record for the group
            for st in range(0, nst + 1):
                if edp == 'PSD' and st == 0:  # consider only NS-PFA at level 0
                    continue
                x = np.array(demands[str(st)])
                st_loss = multiplier * method(x, coeffs)
                loss += st_loss  # add to total building loss
            # Compute the mean from losses obtained for all records
            mean_loss = np.mean(loss)
            if group in s_keys:
                s_loss += loss
                s_mean_loss += mean_loss
            elif group in ns_keys:
                ns_loss += loss
                ns_mean_loss += mean_loss
        # Append results for current rt
        s_mean_losses_nc.append(float(s_mean_loss))  # E[L_S|NC,IM]
        ns_mean_losses_nc.append(float(ns_mean_loss))  # E[L_NS|NC,IM]
        tot_mean_losses_nc.append(float(s_mean_loss+ns_mean_loss))
        rps.append(msa_data[rp]['return-period'])
        imls.append(msa_data[rp]['intensity-measure'])
        mafe.append(1 / rps[-1])

    # COMPUTE FINAL TOTAL LOSS E[L_T|IM]
    p_c = stats.norm.cdf(
        np.log(np.array(imls) / theta_c) / beta_c, loc=0, scale=1
    )  # P[C|IM]
    p_c[np.isnan(p_c)] = 0
    p_nc = 1 - p_c  # P[NC|IM]
    tot_mean_losses_c = rc * np.ones_like(p_c)  # E[L_T|C,IM]
    tot_mean_losses = (p_c * tot_mean_losses_c +
                       p_nc * np.array(tot_mean_losses_nc))  # E[L_T|IM]

    # EXPECTED LOSSES AT RETURN PERIOD OF 1500
    iml_1500 = interp1d(rps, imls)(1500)  # im
    e_s_loss_nc_1500 = interp1d(rps, s_mean_losses_nc)(1500)  # E[L_S|NC,im]
    e_ns_loss_nc_1500 = interp1d(rps, ns_mean_losses_nc)(1500)  # E[L_NS|NC,im]
    e_tot_loss_nc_1500 = e_s_loss_nc_1500 + e_ns_loss_nc_1500  # E[L_T|NC,im]
    e_tot_loss_c = rc  # E[L_T|C,im]
    p_c = stats.norm.cdf(np.log(iml_1500 / theta_c) / beta_c)  # P[C|im]
    p_nc = 1 - p_c  # P[NC|im]
    tot_loss_1500 = (p_c*e_tot_loss_c + p_nc*e_tot_loss_nc_1500)  # E[L_T|im]
    c_loss_ratio_1500 = (e_tot_loss_c * p_c) / tot_loss_1500 * 100
    s_loss_ratio_1500 = (e_s_loss_nc_1500 * p_nc) / tot_loss_1500 * 100
    ns_loss_ratio_1500 = (e_ns_loss_nc_1500 * p_nc) / tot_loss_1500 * 100
    print(f'E[L_S|im]/E[L_T|im]: {s_loss_ratio_1500:.2f}%')
    print(f'E[L_NS|im]/E[L_T|im]: {ns_loss_ratio_1500:.2f}%')

    # PLOT VULNERABILITY CURVE
    plt.plot(imls, tot_mean_losses / rc * 100)
    plt.ylabel('Expected loss ratio [%]')
    plt.xlabel('Intensity Measure, IM [g]')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig(path_loss / "vulnerability.png", dpi=100,
                bbox_inches="tight", format="png")
    plt.show()
    plt.close()

    # PLOT LOSS CURVE
    plt.plot(tot_mean_losses / rc * 100, mafe)
    plt.xlabel('Expected loss ratio [%]')
    plt.ylabel('Mean Annual Frequency of Exceedance')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig(path_loss / "loss.png", dpi=100,
                bbox_inches="tight", format="png")
    plt.show()
    plt.close()

    # PLOT HAZARD CURVE
    mafe_hz = Hazard().get_mafe(poe=hazard_poes)
    hazard = {'s': np.array(hazard_imls), 'mafe': mafe_hz}
    plt.loglog(hazard_imls, mafe_hz)
    plt.ylabel('Mean Annual Frequency of Exceedance')
    plt.xlabel('Intensity Measure, IM [g]')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.savefig(path_loss / "hazard.png", dpi=100,
                bbox_inches="tight", format="png")
    plt.show()
    plt.close()

    # COMPUTE EXPECTED ANNUAL LOSS RATIO
    eal_ratio, cache = get_eal(
        np.array(imls), np.array(tot_mean_losses), hazard, rc=rc
    )
    print(f"EALR = {eal_ratio:.2f}%")

    # COMPUTE MEAN ANNUAL FREQUENCY OF EXCEEDANCE
    mafc = get_mafe_ls(hazard['mafe'], hazard['s'], theta_c, beta_c)
    print(f"MAFC = {100*mafc:.5f}%")

    # SAVE DATA
    cache['EALR'] = eal_ratio
    cache['RepCost'] = rc
    loss = {
        'msa-imls': imls,
        'msa-mafe': mafe_hz,
        'E[L_S|NC,IM]': s_mean_losses_nc,
        'E[L_NS|NC,IM]': ns_mean_losses_nc,
        'E[L_T|NC,IM]': tot_mean_losses_nc,
        'E[L_T|IM]': tot_mean_losses,
        }
    data = loss | cache
    data = to_json_serializable(data)
    with open(path_loss / "loss.json", "w") as f:
        json.dump(data, f, indent=4)
