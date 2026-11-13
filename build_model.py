# Import installed packages
import matplotlib.pyplot as plt  # used for plotting figures
import opsvis as opsv  # used for plotting the models in OpenSees

# Import the method to build the numerical model
from src.mdof2d.model import build_model

# Add the model to the OpenSees
build_model()

# Plot the model
fig = plt.figure()  # start the figure
ax = fig.add_subplot(111, projection='3d')  # add a plot to the figure
opsv.plot_model(node_labels=0, element_labels=0, ax=ax)  # plot the model
ax.view_init(elev=0, azim=90)  # set view to 2D
ax.set_axis_off()  # turn off axis visibility
plt.show()  # show the figure
