from src.Zagreb.model import build_model

import matplotlib.pyplot as plt
import opsvis as opsv

print('Hello Zagreb!')

# Add the model to the OpenSees
build_model()

# Plot the model
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
opsv.plot_model(node_labels=0, element_labels=0, ax=ax)
ax.view_init(elev=0, azim=90)
ax.set_axis_off()
plt.show()
