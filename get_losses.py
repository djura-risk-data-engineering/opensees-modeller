import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from src.hazard import Hazard
from src.utilities import to_json_serializable
from scipy.interpolate import interp1d
from scipy import stats


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
    tuple[float, EALBaseModel]
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
    msa_path = path / 'data/MSA-outs/msa.json'
    msa_data = json.load(open(msa_path))
    frag_path = path / 'data/MSA-outs/frags_msa.json'
    frag_data = json.load(open(frag_path))
    theta_c = frag_data['DLS-4']['median']
    beta_c = frag_data['DLS-4']['beta']

    # STOREY LOSS FUNCTIONS
    methods = {'weibull': weibull, 'papadopoulos': papadopoulos}
    slfs_path = path / 'slfs' / "edp-dv-standard.json"
    edp_dv = json.load(open(slfs_path))
    groups = list(edp_dv.keys())

    # LOSS SETTINGS
    percentile = 'mean'  # loss percentile
    direction = '1'  # SRSS can used for two-directional dynamic analysis
    nst = 3  # number of storeys
    rc = 1000000  # replacement cost

    # INITIALIZE SOME PARAMETERS
    rts = []
    mafe = []
    imls = []
    s_mean_losses_nc = []  # E[L_S|NC,IM]
    ns_mean_losses_nc = []  # E[L_NS|NC,IM]
    tot_mean_losses_nc = []  # E[L_T|NC,IM]
    ns_keys = ['2 - NS: PSD', '3 - NS: PFA']
    s_keys = ['1 - S: PSD']

    for rt in msa_data.keys():
        s_loss = 0.0
        ns_loss = 0.0
        s_mean_loss = 0.0
        ns_mean_loss = 0.0
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
            demands = msa_data[rt][direction]['PFA']
            loss = 0.0  # total building loss per record for the group
            for st in range(1, nst + 1):
                x = np.array(demands[str(st)])
                if edp == 'PSD':
                    st_loss = multiplier * method(x*100, coeffs)  # Storey loss
                elif edp == 'PFA':
                    st_loss = multiplier * method(x, coeffs)  # Storey loss
                loss += st_loss  # add to total building loss
            # Compute the mean from losses obtained for all records
            mean_loss = np.mean(loss)
            if group in s_keys:
                s_loss += loss
                s_mean_loss += mean_loss
            elif group in ns_keys:
                ns_loss += loss
                ns_mean_loss += mean_loss

        s_mean_losses_nc.append(float(s_mean_loss))
        ns_mean_losses_nc.append(float(ns_mean_loss))
        tot_mean_losses_nc.append(float(s_mean_loss+ns_mean_loss))
        rts.append(msa_data[rt]['return-period'])
        imls.append(msa_data[rt]['intensity-measure'])
        mafe.append(1 / rts[-1])

    # COMPUTE FINAL TOTAL LOSS E[L_T|IM]
    p_c = stats.norm.cdf(
        np.log(np.array(imls) / theta_c) / beta_c, loc=0, scale=1
    )  # P[C|IM]
    p_c[np.isnan(p_c)] = 0
    p_nc = 1 - p_c  # P[NC|IM]
    tot_mean_losses_c = rc * np.ones_like(p_c)
    tot_mean_losses = (p_c * tot_mean_losses_c +
                       p_nc * np.array(tot_mean_losses_nc))

    # PLOT VULNERABILITY CURVE
    plt.plot(imls, tot_mean_losses/rc, label='E[L_T|IM]')
    plt.ylabel('Expected loss ratio')
    plt.xlabel('Intensity Measure, IM')
    plt.legend()
    plt.savefig(path / "vulnerability.svg", bbox_inches="tight", format="svg")
    plt.show()
    plt.close()

    # PLOT LOSS CURVE
    plt.plot(tot_mean_losses, mafe, label='E[L_T|IM]')
    plt.xlabel('Expected loss [EUR]')
    plt.ylabel('Mean Annual Frequency of Exceedance')
    plt.legend()
    plt.savefig(path / "loss.svg", bbox_inches="tight", format="svg")
    plt.show()
    plt.close()

    # PLOT HAZARD CURVE
    mafe_hz = Hazard().get_mafe(poe=hazard_poes)
    hazard = {'s': np.array(hazard_imls), 'mafe': mafe_hz}
    plt.loglog(hazard_imls, mafe_hz, label='eshm20-hazard')
    plt.ylabel('Mean Annual Frequency of Exceedance')
    plt.xlabel('Intensity Measure, IM')
    plt.legend()
    plt.savefig(path / "hazard.svg", bbox_inches="tight", format="svg")
    plt.show()
    plt.close()

    # COMPUTE EAL
    eal_ratio, cache = get_eal(
        np.array(imls), np.array(tot_mean_losses), hazard, rc=rc
    )
    print(f"EALR = {eal_ratio:.2f}%")

    # SAVE DATA
    cache['EALR'] = eal_ratio
    cache['RC'] = rc
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
    with open(path / "loss.json", "w") as f:
        json.dump(data, f, indent=4)
