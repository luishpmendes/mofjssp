import csv
import matplotlib.pyplot as plt
import os
import statistics as stats
import itertools
from math import ceil, floor, sqrt
from plotter_definitions import *

num_rows = floor(sqrt(len(instances)))
num_cols = ceil(len(instances)/floor(sqrt(len(instances))))
fig = plt.figure(figsize = (5 * num_cols, 5 * num_rows), constrained_layout = True)
figs = fig.subfigures(nrows = num_rows, ncols = num_cols, wspace = 0.05, hspace = 0.05)
for i in range(len(instances)):
    row = floor(i/num_cols)
    col = i%num_cols
    figs[row][col].suptitle(instances[i], fontsize = "x-large")
    ax = figs[row][col].subplots()
    ax.set_ylabel("Hypervolume", fontsize = "large")
    ax.set_xlabel("Solver", fontsize = "large")
    ax.set_ylim(bottom = 0, top = 1)
    xs = []
    for solver in solvers:
        filename = "hypervolume/" + instances[i] + "_" + solver + ".txt"
        x = []
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                x.append(float(row[0]))
        xs.append(x)
    plt.boxplot(xs, labels = [solver_labels[solver] for solver in solvers])
fig.suptitle("Hypervolume", fontsize = "xx-large")
plt.savefig("hypervolume/hypervolume.png", format = "png")
plt.close(fig)

hypervolume_per_num_jobs = {}

for solver in solvers:
        hypervolume_per_num_jobs[solver] = {}
        for nums_job in nums_jobs:
            hypervolume_per_num_jobs[solver][nums_job] = []

for num_jobs in nums_jobs:
    for instance in instances_per_num_jobs[num_jobs]:
        for solver in solvers:
            for seed in seeds:
                filename = "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_num_jobs[solver][num_jobs].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("Hypervolume x Number of Jobs", fontsize = "xx-large")
plt.xlabel("Number of Jobs", fontsize = "x-large")
plt.ylabel("Hypervolume", fontsize = "x-large")
plt.xticks(nums_jobs)
for i in range(len(solvers)):
    y = []
    for num_jobs in nums_jobs:
        y.append(stats.mean(hypervolume_per_num_jobs[solvers[i]][num_jobs]))
    plt.plot(nums_jobs, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.8)
plt.xlim(left = min(nums_jobs), right = max(nums_jobs))
plt.ylim(bottom = 0.0, top = 1.0)
plt.legend(loc = 'best')
plt.savefig("hypervolume/hypervolume_per_num_jobs.png", format = "png")
plt.close()

hypervolume_per_num_machines = {}

for solver in solvers:
    hypervolume_per_num_machines[solver] = {}
    for num_machines in nums_machines:
        hypervolume_per_num_machines[solver][num_machines] = []

for num_machines in nums_machines:
    for instance in instances_per_num_machines[num_machines]:
        for solver in solvers:
            for seed in seeds:
                filename = "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_num_machines[solver][num_machines].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("Hypervolume x Number of Machines", fontsize = "xx-large")
plt.xlabel("Number of Machines", fontsize = "x-large")
plt.ylabel("Hypervolume", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y = []
    for num_machines in nums_machines:
        y.append(stats.mean(hypervolume_per_num_machines[solvers[i]][num_machines]))
    plt.plot(nums_machines, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.8)
plt.xlim(left = min(nums_machines), right = max(nums_machines))
plt.ylim(bottom = 0.0, top = 1.0)
plt.legend(loc = 'best')
plt.savefig("hypervolume/hypervolume_per_num_machines.png", format = "png")
plt.close()

hypervolume_per_total_num_operations = {}

for solver in solvers:
    hypervolume_per_total_num_operations[solver] = {}
    for total_num_operations in total_nums_operations:
        hypervolume_per_total_num_operations[solver][total_num_operations] = []

for total_num_operations in total_nums_operations:
    for instance in instances_per_total_num_operations[total_num_operations]:
        for solver in solvers:
            for seed in seeds:
                filename = "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_total_num_operations[solver][total_num_operations].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("Hypervolume x Total Number of Operations", fontsize = "xx-large")
plt.xlabel("Total Number of Operations", fontsize = "x-large")
plt.ylabel("Hypervolume", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y = []
    for total_num_operations in total_nums_operations:
        y.append(stats.mean(hypervolume_per_total_num_operations[solvers[i]][total_num_operations]))
    plt.plot(total_nums_operations, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.8)
plt.xlim(left = min(nums_machines), right = max(nums_machines))
plt.ylim(bottom = 0.0, top = 1.0)
plt.legend(loc = 'best')
plt.savefig("hypervolume/hypervolume_per_total_num_operations.png", format = "png")
plt.close()
