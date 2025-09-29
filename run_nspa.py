from src.Zagreb.model import run_nspa
import numpy as np
import matplotlib.pyplot as plt


# Run nspa for the bare frame
run_nspa(infills=0, outsdir='outputs-nspa')
disp = np.loadtxt('outputs-nspa\\displacement.txt')
reactions = np.loadtxt('outputs-nspa\\reaction.txt')
base_shear = np.abs(-np.sum(reactions, axis=1))
roof_disp = disp[:, 2]
plt.plot(roof_disp, base_shear)
plt.xlabel('Roof Displacement [m]')
plt.ylabel('Base Shear [kN]')
plt.show()

# Run nspa for the frame with infills
run_nspa(infills=1, outsdir='outputs-nspa2')
disp = np.loadtxt('outputs-nspa2\\displacement.txt')
reactions = np.loadtxt('outputs-nspa2\\reaction.txt')
base_shear = np.abs(-np.sum(reactions, axis=1))
roof_disp = disp[:, 2]
plt.plot(roof_disp, base_shear)
plt.xlabel('Roof Displacement [m]')
plt.ylabel('Base Shear [kN]')
plt.show()

# The displacement profile at peak force
step = np.argmax(base_shear)  # step of peak base shear
disps_peak = disp[step, :]  # storey displacements at peak base shear
disps_peak = np.append(0, disp[step, :])  # append ground displacement, 0
storeys = [0, 1, 2, 3]  # storey IDs
plt.plot(disps_peak, storeys)
plt.step(disps_peak, storeys, where="post")
plt.xlabel('Displacement [m]')
plt.ylabel('Storey #')
plt.show()

# The store drift profile at peak force
h = 3  # storey height
drifts_peak = disps_peak / h * 100
plt.plot(drifts_peak, storeys)
plt.xlabel('Interstorey Drifts [%]')
plt.ylabel('Storey #')
plt.step(drifts_peak, storeys, where="post")
plt.show()
