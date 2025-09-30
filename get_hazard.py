from src.hazard import Hazard, analytical_mafe
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


poes = [0.999, 0.999, 0.999, 9.99E-01, 9.93E-01, 9.70E-01, 9.08E-01,
        7.89E-01, 6.20E-01, 4.36E-01, 2.76E-01, 1.57E-01, 8.19E-02, 3.88E-02,
        1.65E-02, 6.19E-03, 1.98E-03, 5.13E-04, 9.77E-05
        ]
imls = [0.0047287, 0.0068766, 0.01, 0.0145422, 0.0211474, 0.0307529, 0.0447214,
        0.0650345, 0.0945742, 0.1375312, 0.2, 0.2908431, 0.4229485, 0.6150582,
        0.8944272, 1.3006898, 1.8914832, 2.7506241, 4]

h = Hazard()
mafe = h.get_mafe(poe=poes)
out = h.fit_hazard_model(imls, mafe)
coefs = out['coef']

print("Coefficients", coefs)

# Test the fit through a plot
fig, ax = plt.subplots(figsize=(3, 2), dpi=100)
plt.scatter(out['s'], out['mafe'], c='r', label='Hazard')
plt.loglog(out['s_fit'], out['mafe_fit'], c='b', label='Fit')

plt.xlabel("IM")
plt.ylabel("MAFE")
plt.grid(True, which="major", axis='both', lw=0.5)
plt.legend(frameon=False, loc='best')

plt.show()


# Compute MAFC
eta = 4.75
beta = 0.63

k0, k1, k2 = coefs
s_fit = out['s_fit']
mafe_fit = out['mafe_fit']

# or we can create a new fit based on the coefficients for a larger range
# (losses a little bit of accuracy, but it all depends on the fitting quality)
s_fit = np.linspace(0.001, 8, 200)
mafe_fit = analytical_mafe(s_fit, *coefs)

interpolation = interp1d(s_fit, mafe_fit)
h_eta = interpolation(eta)

p = 1 / (1 + 2 * k2 * beta**2)

mafc = p**0.5 * k0**(1 - p) * h_eta**p * np.exp(0.5 * p * k1**2 * beta**2)

print("MAFC:", mafc)
