import csv
import matplotlib.pyplot as plt
import os
from plotter_definitions import *

for instance in instances:
    for version in versions:
        plt.figure(figsize = (5, 5))
        plt.title(instance, fontsize = "xx-large")
        plt.xlabel("Time (s)", fontsize = "x-large")
        plt.ylabel("Non-dominated Solutions", fontsize = "x-large")
        for i in range(len(solvers)):
            filename = "num_non_dominated_snapshots/" + instance + "_" + solvers[i] + "_" + version + ".txt"
            if os.path.exists(filename):
                x = []
                y = []
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = " ")
                    for row in data:
                        x.append(float(row[1]))
                        y.append(float(row[2]))
                plt.plot(x, y, label = solver_labels[solvers[i]], color = colors[i], marker = (i + 3, 2, 0), alpha = 0.80)
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.legend(loc = 'best')
        plt.savefig("num_non_dominated_snapshots/" + instance + "_" + version + ".png", format = "png")
        plt.close()
