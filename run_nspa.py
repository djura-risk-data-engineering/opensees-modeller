# Import installed packages
import numpy as np  # used for array operations
import matplotlib.pyplot as plt  # used for plotting

# Import the method to run pushover analysis for the RC frame
from src.mdof2d.model import run_nspa


# Perform Pushover Analyses
run_nspa(outsdir='outputs\\NSPA')
# Read the storey displacements
disp = np.loadtxt('outputs\\NSPA\\displacement.txt')
# Read the support reactions
reactions = np.loadtxt('outputs\\NSPA\\reaction.txt')
# Compute the base shear
base_shear = np.abs(-np.sum(reactions, axis=1))
# Get the roof displacements
roof_disp = disp[:, 2]
# Plot the pushover curve
plt.plot(roof_disp, base_shear)
plt.xlabel('Roof Displacement [m]')
plt.ylabel('Base Shear [kN]')
plt.savefig("outputs\\NSPA\\nspa-1.png")
plt.show()
plt.close()

# Plot the pushover curve as max. drift vs base shear coeff.
tresholds = [0.4, 1.0, 1.8, 2.6]
colors = ['cyan', 'green', 'orange', 'red']
total_weight = 306
storey_height = 3  # storey height
shear_coeff = base_shear / total_weight
drifts = np.insert(disp, 0, 0, axis=1)
drifts = np.diff(drifts, axis=1) / storey_height
max_drifts = np.max(drifts, axis=1) * 100
plt.plot(max_drifts, shear_coeff)
for i in range(4):
    plt.axvline(x=tresholds[i], color=colors[i], linestyle=":",
                label=(f'DLS-{i + 1}'))
plt.legend()
plt.ylabel("Base Shear Coefficient [V/W]")
plt.xlabel("Maximum Interstorey Drift [%]")
plt.savefig("outputs\\NSPA\\nspa-2.png")  # saves in your remote folder
plt.show()
plt.close()

# Plot the displacement profile at peak force
storeys = [0, 1, 2, 3]  # storey IDs
step = np.argmax(base_shear)  # step of peak base shear
disps_peak = disp[step, :]  # storey displacements at peak base shear
disps_peak = np.append(0, disp[step, :])  # append ground displacement, 0
plt.plot(disps_peak, storeys)
# Re-organize to plot the profile as a step function
X = []
Y = []
for i in range(len(disps_peak) - 1):
    # vertical segment
    X.extend([disps_peak[i+1], disps_peak[i+1]])
    Y.extend([storeys[i], storeys[i+1]])
    # horizontal segment (skip the first one)
    if i > 0:
        X.append(disps_peak[i+1])
        Y.append(storeys[i+1])
plt.plot(X, Y)
plt.xlabel('Displacement [m]')
plt.ylabel('Storey #')
plt.savefig("outputs\\NSPA\\nspa-3.png")
plt.show()
plt.close()

# Plot the storey drift profile at peak force
plt.plot(disps_peak / storey_height * 100, storeys)
plt.xlabel('Interstorey Drifts [%]')
plt.ylabel('Storey #')
plt.plot(np.array(X) / storey_height * 100, Y)
plt.savefig("outputs\\NSPA\\nspa-4.png")
plt.show()
plt.close()
