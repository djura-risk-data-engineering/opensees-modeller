# Import installed packages
import numpy as np  # used for array operations
import matplotlib.pyplot as plt  # used for plotting

# Import the method to run pushover analysis for the RC frame
from src.zagreb.model import run_nspa


# Perform Pushover Analyses
run_nspa(infills=1, outsdir='outputs-nspa-infilled-frame')  # Infilled frame
run_nspa(infills=0, outsdir='outputs-nspa-bare-frame')  # Bare frame
# Read the storey displacements
disp_infill = np.loadtxt('outputs-nspa-infilled-frame\\displacement.txt')
disp_bare = np.loadtxt('outputs-nspa-bare-frame\\displacement.txt')
# Read the support reactions
reactions_infill = np.loadtxt('outputs-nspa-infilled-frame\\reaction.txt')
reactions_bare = np.loadtxt('outputs-nspa-bare-frame\\reaction.txt')
# Compute the base shear
base_shear_infill = np.abs(-np.sum(reactions_infill, axis=1))
base_shear_bare = np.abs(-np.sum(reactions_bare, axis=1))
# Get the roof displacements
roof_disp_infill = disp_infill[:, 2]
roof_disp_bare = disp_bare[:, 2]
# Plot the pushover curves
plt.plot(roof_disp_infill, base_shear_infill, label='infilled-frame')
plt.plot(roof_disp_bare, base_shear_bare, label='bare-frame')
plt.xlabel('Roof Displacement [m]')
plt.ylabel('Base Shear [kN]')
plt.legend()
plt.show()

# Plot the displacement profile at peak force for the bare frame
storeys = [0, 1, 2, 3]  # storey IDs
step = np.argmax(base_shear_bare)  # step of peak base shear
disps_peak = disp_bare[step, :]  # storey displacements at peak base shear
disps_peak = np.append(0, disp_bare[step, :])  # append ground displacement, 0
plt.plot(disps_peak, storeys)
plt.step(disps_peak, storeys, where="post")
plt.xlabel('Displacement [m]')
plt.ylabel('Storey #')
plt.show()

# Plot the storey drift profile at peak force for the bare frame
h = 3  # storey height
drifts_peak = disps_peak / h * 100  # drifts at the peak base shear
plt.plot(drifts_peak, storeys)
plt.xlabel('Interstorey Drifts [%]')
plt.ylabel('Storey #')
plt.step(drifts_peak, storeys, where="post")
plt.show()
