import csv
import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt
import os
import statistics as stats
from math import ceil, floor, sqrt
from plotter_definitions import *

dirname = os.path.dirname(__file__)

min_hypervolume = 1.0
max_hypervolume = 0.0
for instance in instances:
    for solver in solvers:
        filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solver + ".txt")
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                min_hypervolume = min(min_hypervolume, float(row[0]))
                max_hypervolume = max(max_hypervolume, float(row[0]))
delta_hypervolume = max_hypervolume - min_hypervolume
min_hypervolume = max(min_hypervolume - round(0.025 * delta_hypervolume), 0.00)
max_hypervolume = min(max_hypervolume + round(0.025 * delta_hypervolume), 1.00)

for instance in instances:
    plt.figure(figsize = (11, 11))
    plt.title(instance, fontsize = "xx-large")
    plt.xlabel("Hypervolume Ratio", fontsize = "x-large")
    xs = []
    for solver in solvers:
        filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solver + ".txt")
        x = []
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                x.append(float(row[0]))
        xs.append(x)
    pt.half_violinplot(data = xs, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
    sns.stripplot(data = xs, palette = colors, orient = "h", size = 2, zorder = 0)
    sns.boxplot(data = xs, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
    plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
    filename = os.path.join(dirname, "hypervolume/" + instance + ".png")
    plt.savefig(filename, format = "png")
    plt.close()

hypervolume = []

for solver in solvers:
    hypervolume.append([])

for instance in instances:
    for i in range(len(solvers)):
        for seed in seeds:
            filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solvers[i] + "_" + str(seed) + ".txt")
            if os.path.exists(filename):
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = ",")
                    for row in data:
                        hypervolume[i].append(float(row[0]))
                    csv_file.close()

plt.figure(figsize = (11, 11))
plt.title("Multi-Objective Flexible Job-Shop Scheduling Problem", fontsize = "xx-large")
plt.xlabel("Hypervolume Ratio", fontsize = "x-large")
pt.half_violinplot(data = hypervolume, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
sns.stripplot(data = hypervolume, palette = colors, orient = "h", size = 2, zorder = 0)
sns.boxplot(data = hypervolume, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume.png")
plt.savefig(filename, format = "png")
plt.close()

hypervolume_per_num_jobs = {}

for solver in solvers:
    hypervolume_per_num_jobs[solver] = {}
    for nums_job in nums_jobs:
        hypervolume_per_num_jobs[solver][nums_job] = []

for num_jobs in nums_jobs:
    for instance in instances_per_num_jobs[num_jobs]:
        for solver in solvers:
            for seed in seeds:
                filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_num_jobs[solver][num_jobs].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Jobs", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(nums_jobs)
for i in range(len(solvers)):
    y = []
    for num_jobs in nums_jobs:
        y.append(stats.mean(hypervolume_per_num_jobs[solvers[i]][num_jobs]))
    plt.plot(nums_jobs, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(nums_jobs) - 1, 0), right = max(nums_jobs) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume_mean_per_num_jobs.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Jobs", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(nums_jobs)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(hypervolume_per_num_jobs[solvers[i]][num_jobs])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_jobs, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(hypervolume_per_num_jobs[solvers[i]][num_jobs])
        y1.append(quantiles[1])
    plt.plot(nums_jobs, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(nums_jobs) - 1, 0), right = max(nums_jobs) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "x-large")
filename = os.path.join(dirname, "hypervolume/hypervolume_quartiles_per_num_jobs.png")
plt.savefig(filename, format = "png")
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
                filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_num_machines[solver][num_machines].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Machines", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y = []
    for num_machines in nums_machines:
        y.append(stats.mean(hypervolume_per_num_machines[solvers[i]][num_machines]))
    plt.plot(nums_machines, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(nums_machines) - 1, 0), right = max(nums_machines) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume_mean_per_num_machines.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Number of Machines", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(nums_machines)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(hypervolume_per_num_machines[solvers[i]][num_machines])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_machines, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(hypervolume_per_num_machines[solvers[i]][num_machines])
        y1.append(quantiles[1])
    plt.plot(nums_machines, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(nums_machines) - 1, 0), right = max(nums_machines) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume_quartiles_per_num_machines.png")
plt.savefig(filename, format = "png")
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
                filename = os.path.join(dirname, "hypervolume/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            hypervolume_per_total_num_operations[solver][total_num_operations].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Total Number of Operations", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(total_nums_operations)
for i in range(len(solvers)):
    y = []
    for total_num_operations in total_nums_operations:
        y.append(stats.mean(hypervolume_per_total_num_operations[solvers[i]][total_num_operations]))
    plt.plot(total_nums_operations, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.xlim(left = max(min(total_nums_operations) - 1, 0), right = max(total_nums_operations) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume_mean_per_total_num_operations.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.title("MOFJSSP", fontsize = "xx-large")
plt.xlabel("Total Number of Operations", fontsize = "x-large")
plt.ylabel("Hypervolume Ratio", fontsize = "x-large")
plt.xticks(total_nums_operations)
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(hypervolume_per_total_num_operations[solvers[i]][total_num_operations])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(total_nums_operations, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(hypervolume_per_total_num_operations[solvers[i]][total_num_operations])
        y1.append(quantiles[1])
    plt.plot(total_nums_operations, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.xlim(left = max(min(total_nums_operations) - 1, 0), right = max(total_nums_operations) + 1)
plt.ylim(bottom = min_hypervolume, top = max_hypervolume)
plt.legend(loc = "best", fontsize = "large")
filename = os.path.join(dirname, "hypervolume/hypervolume_quartiles_per_total_num_operations.png")
plt.savefig(filename, format = "png")
plt.close()