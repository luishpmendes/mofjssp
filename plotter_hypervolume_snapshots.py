import csv
import matplotlib.pyplot as plt
import os
import statistics as stats
from math import ceil, floor, sqrt
from plotter_definitions import *

for version in versions:
    num_rows = floor(sqrt(len(instances)))
    num_cols = ceil(len(instances)/floor(sqrt(len(instances))))
    fig = plt.figure(figsize = (5 * num_cols, 5 * num_rows), constrained_layout = True)
    figs = fig.subfigures(nrows = num_rows, ncols = num_cols, wspace = 0.05, hspace = 0.05)
    for i in range(len(instances)):
        row = floor(i/num_cols)
        col = i%num_cols
        figs[row][col].suptitle(instances[i], fontsize = "x-large")
        ax = figs[row][col].subplots()
        ax.set_ylabel("Hypervolume x Time", fontsize = "large")
        ax.set_xlabel("Time (s)", fontsize = "large")
        ax.set_ylim(bottom = 0, top = 1)
        for j in range(len(solvers)):
            filename = "hypervolume_snapshots/" + instances[i] + "_" + solvers[j] + "_" + version + ".txt"
            if os.path.exists(filename):
                x = []
                y = []
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = ",")
                    for row in data:
                        x.append(float(row[1]))
                        y.append(float(row[2]))
                ax.plot(x, y, label = solver_labels[solvers[j]], marker = (j + 3, 2, 0), color = colors[j], alpha = 0.80)
        ax.set_xlim(left = 0)
        ax.legend(loc = 'best')
    fig.suptitle("Hypervolume", fontsize = "xx-large")
    plt.savefig("hypervolume_snapshots/hypervolume_snapshots_" + version + ".png", format = "png")
    plt.close(fig)

hypervolume_per_solver = {}
time_per_solver = {}

for solver in solvers:
    hypervolume_per_solver[solver] = []
    time_per_solver[solver] = []
    for i in range(num_snapshots + 1):
        hypervolume_per_solver[solver].append([])
        time_per_solver[solver].append([])

for instance in instances:
    for solver in solvers:
        for seed in seeds:
            filename = "hypervolume_snapshots/" + instance + "_" + solver + "_" + str(seed) + ".txt"
            if os.path.exists(filename):
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = ",")
                    i = 0
                    for row in data:
                        time_per_solver[solver][i].append(float(row[1]))
                        hypervolume_per_solver[solver][i].append(float(row[2]))
                        i += 1
                    csv_file.close()

plt.figure(figsize=(5, 5), constrained_layout = True)
plt.title("Hypervolume x Time", fontsize = "xx-large")
plt.xlabel("Time (s)", fontsize = "x-large")
plt.ylabel("Hypervolume", fontsize = "x-large")
max_time = 0;
for i in range(len(solvers)):
    x = []
    y = []
    for k in range(num_snapshots + 1):
        x.append(stats.mean(time_per_solver[solvers[i]][k]))
        y.append(stats.mean(hypervolume_per_solver[solvers[i]][k]))
        if max_time < max(time_per_solver[solvers[i]][k]):
            max_time = max(time_per_solver[solvers[i]][k])
    plt.plot(x, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i + j], alpha = 0.80)
plt.xlim(left = 0, right = max_time)
plt.ylim(bottom = 0.0, top = 1.0)
plt.legend(loc = 'best')
plt.savefig("hypervolume_snapshots/hypervolume_snapshots.png", format = "png")
plt.close()
