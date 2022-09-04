import csv
import matplotlib.pyplot as plt
import os
from plotter_definitions import *

for instance in instances:
    for version in versions:
        plt.figure()
        plt.title(instance, fontsize = "xx-large")
        plt.xlabel("Time (s)", fontsize = "x-large")
        plt.ylabel("Number of elites", fontsize = "x-large")
        for solver in solvers:
            if solver.startswith("nsbrkga"):
                filename = "num_elites_snapshots/" + instance + "_" + solver + "_" + version + ".txt"
                if os.path.exists(filename):
                    x = []
                    y = []
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = " ")
                        for row in data:
                            x.append(float(row[1]))
                            y.append(float(row[2]))
                    plt.plot(x, y, label = solver_labels[solver])
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.legend(loc = 'best', fontsize = "large")
        plt.savefig("num_elites_snapshots/" + instance + "_" + version + ".png", format = "png")
        plt.close()
