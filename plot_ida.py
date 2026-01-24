import pickle
import matplotlib.pyplot as plt

FONTSIZE = 10
grayscale = ['#111111', '#222222', '#333333', '#444444', '#555555',
             '#656565', '#767676', '#878787', '#989898', '#a9a9a9']
color_grid = ['#840d81', '#6c4ba6', '#407bc1', '#18b5d8', '#01e9f5',
              '#cef19d', '#a6dba7', '#77bd98', '#398684', '#094869']

with open("outputs/IDA/ida.pickle", "rb") as f:
    data = pickle.load(f)

data = data[1]

drift_range = data["mpsd"]
im_qtile = data["im_qtile_psd"]
im = data["im"]
im_spl = data["im_spl_psd"]
drifts = data["drift"]
label_i = "Ind. records"

for rec in range(im_spl.shape[0]):
    plt.plot(drifts[rec], im[rec], grayscale[-1],
             marker='o', linewidth=1, markersize=2)
    plt.plot(drift_range, im_spl[rec], grayscale[-1], linewidth=1,
             label=label_i)
    label_i = None
plt.plot(drift_range, im_qtile[2], color=color_grid[8],
         label="84th quantile", ls="-.", linewidth=2)
plt.plot(drift_range, im_qtile[1], color=color_grid[6],
         label="50th quantile", ls="--", linewidth=2)
plt.plot(drift_range, im_qtile[0],
         color=color_grid[3], label="16th quantile", ls="-", linewidth=2)

plt.xlabel("PSD, [%]", fontsize=FONTSIZE)
plt.ylabel("Sa, [g]", fontsize=FONTSIZE)
plt.rc('xtick', labelsize=FONTSIZE)
plt.rc('ytick', labelsize=FONTSIZE)
plt.grid(True, which="major", ls="--", lw=0.8, dashes=(5, 10))
plt.legend(frameon=False, loc='best',
           fontsize=FONTSIZE)
plt.show()
