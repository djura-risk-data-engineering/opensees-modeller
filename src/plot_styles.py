import random


FONTSIZE = 8
color_grid = ['#840d81', '#6c4ba6', '#407bc1', '#18b5d8', '#01e9f5',
              '#cef19d', '#a6dba7', '#77bd98', '#398684', '#094869']
color_grid1 = ["#2F8F9D", "#3BACB6", "#82DBD8", "#B3E8E5"]
grayscale = ['#111111', '#222222', '#333333', '#444444', '#555555',
             '#656565', '#767676', '#878787', '#989898', '#a9a9a9']
markers = ["o", "v", "^", "<", ">", "s", "*", "D", "+", "X", "p"]
gray = "#c4c1c0"
linestyles = ["solid", "dashed", "dashdot", "dotted"]
marker_size = 16


def add_text(ax, x, y, text, ha='center', va='center', rotation=None,
             size=10, color='k'):
    ax.text(x, y, text, ha=ha, va=va, rotation=rotation,
            fontsize=size, color=color)


def randomize_color():
    return lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]


def get_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = []
    unique_handles = []
    for handle, label in zip(handles, labels):
        if label not in unique_labels:
            unique_labels.append(label)
            unique_handles.append(handle)
    return unique_handles, unique_labels
