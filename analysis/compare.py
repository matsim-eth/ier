import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_iteration_times(path):
    df = pd.read_csv("%s/stopwatch.txt" % path, sep = "\t")

    start_times = np.array([
        np.dot(np.array([3600.0, 60.0, 1.0]), np.array(v.split(":"), dtype=np.int))
        for v in df["BEGIN iteration"].values
    ])

    end_times = np.array([
        np.dot(np.array([3600.0, 60.0, 1.0]), np.array(v.split(":"), dtype=np.int))
        for v in df["END iteration"].values
    ])

    return end_times - start_times[0]

def read_mode_shares(path):
    return pd.read_csv("%s/modestats.txt" % path, sep = "\t")

ier_times = read_iteration_times("../output")
ier_shares = read_mode_shares("../output")

standard_times = read_iteration_times("../output_standard")
standard_shares = read_mode_shares("../output_standard")

plt.figure(figsize = (6,4), dpi = 120)

for i, mode in enumerate(("car", "pt", "walk")):
    plt.plot(ier_times / 60, ier_shares[mode].values, '.-', color = "C%d" % i)
    plt.plot(standard_times / 60, standard_shares[mode].values, '.-', color = "C%d" % i, alpha = 0.25)
    plt.plot([np.nan, np.nan], [np.nan, np.nan], '-', color = "C%d" % i, label = mode)

plt.plot([np.nan, np.nan], [np.nan, np.nan], '.', color = "k", label = "IER")
plt.plot([np.nan, np.nan], [np.nan, np.nan], '.', color = "k", label = "Standard", alpha = 0.25)

plt.grid()
plt.legend(loc = "best", ncol = 2)
plt.ylabel("Mode share")
plt.xlabel("Runtime [min]")
plt.tight_layout()


plt.show()
