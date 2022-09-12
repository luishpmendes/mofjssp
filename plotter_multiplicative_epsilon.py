import csv
import matplotlib.pyplot as plt
import os
import statistics as stats
import itertools
from math import ceil, floor, sqrt
from plotter_definitions import *

min_multiplicative_epsilon = 1.0
max_multiplicative_epsilon = 0.0
for instance in instances:
    for solver in solvers:
        filename = "multiplicative_epsilon/" + instance + "_" + solver + ".txt"
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                min_multiplicative_epsilon = min(min_multiplicative_epsilon, float(row[0]))
                max_multiplicative_epsilon = max(max_multiplicative_epsilon, float(row[0]))
delta_multiplicative_epsilon = max_multiplicative_epsilon - min_multiplicative_epsilon
min_multiplicative_epsilon = max(min_multiplicative_epsilon - round(0.025 * delta_multiplicative_epsilon), 0.00)
max_multiplicative_epsilon = min(max_multiplicative_epsilon + round(0.025 * delta_multiplicative_epsilon), 1.00)

num_rows = floor(sqrt(len(instances)))
num_cols = ceil(len(instances)/floor(sqrt(len(instances))))
fig = plt.figure(figsize = (5 * num_cols, 5 * num_rows), constrained_layout = True)
figs = fig.subfigures(nrows = num_rows, ncols = num_cols, wspace = 0.05, hspace = 0.05)
for i in range(len(instances)):
    row = floor(i/num_cols)
    col = i%num_cols
    figs[row][col].suptitle(instances[i], fontsize = "x-large")
    ax = figs[row][col].subplots()
    ax.set_ylabel("Multiplicative Epsilon", fontsize = "large")
    ax.set_xlabel("Solver", fontsize = "large")
    xs = []
    for solver in solvers:
        filename = "multiplicative_epsilon/" + instances[i] + "_" + solver + ".txt"
        x = []
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                x.append(float(row[0]))
        xs.append(x)
    bp = ax.boxplot(xs, labels = [solver_labels[solver] for solver in solvers], patch_artist = True)
    for j in range(len(solvers)) :
        bp["boxes"][j].set_facecolor(colors[j])
        bp["medians"][j].set_color("black")
    ax.set_ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
fig.suptitle("MOFJSSP", fontsize = "xx-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon.png", format = "png")
plt.close(fig)

multiplicative_epsilon = []

for solver in solvers:
    multiplicative_epsilon.append([])

for instance in instances:
    for i in range(len(solvers)):
        for seed in seeds:
            filename = "multiplicative_epsilon/" + instance + "_" + solvers[i] + "_" + str(seed) + ".txt"
            if os.path.exists(filename):
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = ",")
                    for row in data:
                        multiplicative_epsilon[i].append(float(row[0]))
                    csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Solver", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
bp = plt.boxplot(multiplicative_epsilon, labels = [solver_labels[solver] for solver in solvers], patch_artist = True)
for i in range(len(solvers)) :
    bp["boxes"][i].set_facecolor(colors[i])
    bp["medians"][i].set_color("black")
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.savefig("multiplicative_epsilon/multiplicative_epsilons.png", format = "png")
plt.close()

multiplicative_epsilon_per_num_jobs = {}

for solver in solvers:
        multiplicative_epsilon_per_num_jobs[solver] = {}
        for nums_job in nums_jobs:
            multiplicative_epsilon_per_num_jobs[solver][nums_job] = []

for num_jobs in nums_jobs:
    for instance in instances_per_num_jobs[num_jobs]:
        for solver in solvers:
            for seed in seeds:
                filename = "multiplicative_epsilon/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            multiplicative_epsilon_per_num_jobs[solver][num_jobs].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Jobs", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(nums_jobs)
for i in range(len(solvers)):
    y = []
    for num_jobs in nums_jobs:
        y.append(stats.mean(multiplicative_epsilon_per_num_jobs[solvers[i]][num_jobs]))
    plt.plot(nums_jobs, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(nums_jobs) - 1, 0), right = max(nums_jobs) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_mean_per_num_jobs.png", format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Jobs", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(nums_jobs)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(multiplicative_epsilon_per_num_jobs[solvers[i]][num_jobs])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_jobs, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(multiplicative_epsilon_per_num_jobs[solvers[i]][num_jobs])
        y1.append(quantiles[1])
    plt.plot(nums_jobs, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(nums_jobs) - 1, 0), right = max(nums_jobs) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "x-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_quartiles_per_num_jobs.png", format = "png")
plt.close()

multiplicative_epsilon_per_num_machines = {}

for solver in solvers:
    multiplicative_epsilon_per_num_machines[solver] = {}
    for num_machines in nums_machines:
        multiplicative_epsilon_per_num_machines[solver][num_machines] = []

for num_machines in nums_machines:
    for instance in instances_per_num_machines[num_machines]:
        for solver in solvers:
            for seed in seeds:
                filename = "multiplicative_epsilon/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            multiplicative_epsilon_per_num_machines[solver][num_machines].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Machines", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y = []
    for num_machines in nums_machines:
        y.append(stats.mean(multiplicative_epsilon_per_num_machines[solvers[i]][num_machines]))
    plt.plot(nums_machines, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(nums_machines) - 1, 0), right = max(nums_machines) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "x-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_mean_per_num_machines.png", format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Machines", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(multiplicative_epsilon_per_num_machines[solvers[i]][num_machines])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_machines, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(multiplicative_epsilon_per_num_machines[solvers[i]][num_machines])
        y1.append(quantiles[1])
    plt.plot(nums_machines, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(nums_machines) - 1, 0), right = max(nums_machines) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "x-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_quartile_per_num_machines.png", format = "png")
plt.close()

multiplicative_epsilon_per_total_num_operations = {}

for solver in solvers:
    multiplicative_epsilon_per_total_num_operations[solver] = {}
    for total_num_operations in total_nums_operations:
        multiplicative_epsilon_per_total_num_operations[solver][total_num_operations] = []

for total_num_operations in total_nums_operations:
    for instance in instances_per_total_num_operations[total_num_operations]:
        for solver in solvers:
            for seed in seeds:
                filename = "multiplicative_epsilon/" + instance + "_" + solver + "_" + str(seed) + ".txt"
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            multiplicative_epsilon_per_total_num_operations[solver][total_num_operations].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Total Number of Operations", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(total_nums_operations)
for i in range(len(solvers)):
    y = []
    for total_num_operations in total_nums_operations:
        y.append(stats.mean(multiplicative_epsilon_per_total_num_operations[solvers[i]][total_num_operations]))
    plt.plot(total_nums_operations, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.8)
plt.xlim(left = max(min(total_nums_operations) - 1, 0), right = max(total_nums_operations) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "x-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_mean_per_total_num_operations.png", format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Total Number of Operations", fontsize = "x-large")
plt.ylabel("Multiplicative Epsilon", fontsize = "x-large")
plt.xticks(total_nums_operations)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(multiplicative_epsilon_per_total_num_operations[solvers[i]][total_num_operations])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(total_nums_operations, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(multiplicative_epsilon_per_total_num_operations[solvers[i]][total_num_operations])
        y1.append(quantiles[1])
    plt.plot(total_nums_operations, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(total_nums_operations) - 1, 0), right = max(total_nums_operations) + 1)
plt.ylim(bottom = min_multiplicative_epsilon, top = max_multiplicative_epsilon)
plt.legend(loc = 'best', fontsize = "x-large")
plt.savefig("multiplicative_epsilon/multiplicative_epsilon_quartile_per_total_num_operations.png", format = "png")
plt.close()
