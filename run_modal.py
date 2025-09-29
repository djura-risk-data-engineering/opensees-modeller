from src.Zagreb.model import run_modal
import numpy as np
import matplotlib.pyplot as plt

run_modal(outsdir='outputs', num_modes=3)

for i in range(3):  # loop through each mode
    eigen_vectors = np.loadtxt(f'outputs\\EigenVectors_Mode{i+1}.txt',
                               delimiter=',')
    fi_x = np.append(0, eigen_vectors[:, 1])  # eigen vector in X-dir
    fi_x = fi_x / np.max(np.abs(fi_x))  # Normalisation
    storeys = [0, 1, 2, 3]  # storey numbers
    plt.plot(fi_x, storeys, label=f'Mode-{i+1}')
    plt.ylabel('Storey ID')
    plt.xlabel('Displacement in X-dir')

plt.legend()
plt.show()
