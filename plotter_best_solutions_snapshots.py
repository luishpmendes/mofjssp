import csv
import matplotlib.pyplot as plt
import os
import seaborn as sns
from plotter_definitions import *

for instance in instances:
    for version in versions:
        min_ys = []
        max_ys = []
        for i in range(m):
            min_ys.append(-1)
            max_ys.append(-1)
        for solver in solvers:
            num_snapshots = 0
            while True:
                filename = "best_solutions_snapshots/" + instance + "_" + solver + "_" + version + "_" + str(num_snapshots) +  ".txt"
                if not os.path.exists(filename):
                    break
                with open(filename) as csv_file:
                    next(csv_file)
                    data = csv.reader(csv_file, delimiter = " ")
                    for row in data:
                        for i in range(m):
                            if min_ys[i] == -1 or min_ys[i] > float(row[i]):
                                min_ys[i] = float(row[i])
                            if max_ys[i] == -1 or max_ys[i] < float(row[i]):
                                max_ys[i] = float(row[i])
                    csv_file.close()
                num_snapshots += 1
        for i in range(m):
            delta_y = max_ys[i] - min_ys[i]
            min_ys[i] = min_ys[i] - round(0.025 * delta_y)
            max_ys[i] = max_ys[i] + round(0.025 * delta_y)
        for snapshot in range(num_snapshots):
            fig, axs = plt.subplots(nrows = m, ncols = m, figsize = (5.0 * m, 5.0 * m), squeeze = False, num = 1, clear = True)
            fig.set_size_inches(5.0 * m, 5.0 * m)
            fig.suptitle(instance, fontsize = "xx-large")
            for i in range(len(solvers)):
                filename = "best_solutions_snapshots/" + instance + "_" + solvers[i] + "_" + version + "_" + str(snapshot) +  ".txt"
                if os.path.exists(filename):
                    ys = []
                    for k in range(m):
                        ys.append([])
                    with open(filename) as csv_file:
                        next(csv_file)
                        data = csv.reader(csv_file, delimiter = " ")
                        for row in data:
                            for k in range(m):
                                ys[k].append(float(row[k]))
                        csv_file.close()
                    for k in range(m):
                        for l in range(m):
                            if (k == l):
                                axs[k][l].set_xlim(left = min_ys[l], right = max_ys[l])
                                axs[k][l].set_xlabel(xlabel = "$f_{" + str(l + 1) + "}$", fontsize = "x-large")
                                axs[k][k].set_yticks([])
                                axs[k][l].set_ylabel(ylabel = "Density", fontsize = "x-large")
                                sns.kdeplot(data = ys[l], ax = axs[k][l], color = colors[i], label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), alpha = 0.80)
                                axs[k][l].legend(loc = "best")
                            else:
                                axs[k][l].set_xlim(left = min_ys[l], right = max_ys[l])
                                axs[k][l].set_ylim(bottom = min_ys[k], top = max_ys[k])
                                axs[k][l].set_xlabel(xlabel = "$f_{" + str(l + 1) + "}$", fontsize = "x-large")
                                axs[k][l].set_ylabel(ylabel = "$f_{" + str(k + 1) + "}$", fontsize = "x-large")
                                axs[k][l].scatter(x = ys[l], y = ys[k], color = colors[i], label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), alpha = 0.80)
                                axs[k][l].legend(loc = "best")
            plt.subplots_adjust(wspace = 0.15 + 0.05 * m, hspace = 0.15 + 0.05 * m)
            plt.savefig("best_solutions_snapshots/" + instance + "_" + version + "_" + str(snapshot) + ".png", format = "png")
