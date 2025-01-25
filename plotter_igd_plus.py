import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
import ptitprince as pt
import os
import statistics as stats
from plotter_definitions import *

dirname = os.path.dirname(__file__)

min_igd_plus = 1.0
max_igd_plus = 0.0
for instance in instances:
    for solver in solvers:
        filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solver + ".txt")
        with open(filename) as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                min_igd_plus = min(min_igd_plus, float(row[0]))
                max_igd_plus = max(max_igd_plus, float(row[0]))
delta_igd_plus = max_igd_plus - min_igd_plus
min_igd_plus = max(min_igd_plus - round(0.025 * delta_igd_plus), 0.00)
max_igd_plus = min(max_igd_plus + round(0.025 * delta_igd_plus), 1.00)

# for instance in instances:
#     plt.figure(figsize = (11, 11))
#     plt.title(instance, fontsize = "xx-large")
#     plt.xlabel("Normalized Modified Inverted Generational Distance", fontsize = "x-large")
#     xs = []
#     for solver in solvers:
#         filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solver + ".txt")
#         x = []
#         with open(filename) as csv_file:
#             data = csv.reader(csv_file)
#             for row in data:
#                 x.append(float(row[0]))
#         xs.append(x)
#     pt.half_violinplot(data = xs, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
#     sns.stripplot(data = xs, palette = colors, orient = "h", size = 2, zorder = 0)
#     sns.boxplot(data = xs, orient = "h", width = 0.20, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
#     plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers], fontsize = "large")
#     filename = os.path.join(dirname, "igd_plus/" + instance + ".png")
#     plt.savefig(filename, format = "png")
#     plt.close()

igd_plus = []

for solver in solvers:
    igd_plus.append([])

for instance in instances:
    for i in range(len(solvers)):
        for seed in seeds:
            filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solvers[i] + "_" + str(seed) + ".txt")
            if os.path.exists(filename):
                with open(filename) as csv_file:
                    data = csv.reader(csv_file, delimiter = ",")
                    for row in data:
                        igd_plus[i].append(float(row[0]))
                    csv_file.close()

plt.figure()
plt.xlabel("Normalized Modified Inverted Generational Distance")
pt.half_violinplot(data = igd_plus, palette = colors, orient = "h", width = 0.6, cut = 0.0, inner = None)
sns.stripplot(data = igd_plus, palette = colors, orient = "h", size = 2, zorder = 0)
sns.boxplot(data = igd_plus, orient = "h", width = 0.2, color = "black", zorder = 10, showcaps = True, boxprops = {'facecolor' : 'none', "zorder" : 10}, showfliers = True, whiskerprops = {'linewidth' : 2, "zorder" : 10}, flierprops = {'markersize' : 2})
plt.yticks(ticks = list(range(len(solvers))), labels = [solver_labels[solver] for solver in solvers])
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus.png")
plt.savefig(filename, format = "png")
plt.close()

igd_plus_per_num_jobs = {}

for solver in solvers:
    igd_plus_per_num_jobs[solver] = {}
    for nums_job in nums_jobs:
        igd_plus_per_num_jobs[solver][nums_job] = []

for num_jobs in nums_jobs:
    for instance in instances_per_num_jobs[num_jobs]:
        for solver in solvers:
            for seed in seeds:
                filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            igd_plus_per_num_jobs[solver][num_jobs].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.xlabel("Number of Jobs")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y = []
    for num_jobs in nums_jobs:
        y.append(stats.mean(igd_plus_per_num_jobs[solvers[i]][num_jobs]))
    plt.plot(nums_jobs, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "upper left")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_mean_per_num_jobs.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.xlabel("Number of Jobs")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(igd_plus_per_num_jobs[solvers[i]][num_jobs])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_jobs, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_jobs in nums_jobs:
        quantiles = stats.quantiles(igd_plus_per_num_jobs[solvers[i]][num_jobs])
        y1.append(quantiles[1])
    plt.plot(nums_jobs, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_quartiles_per_num_jobs.png")
plt.savefig(filename, format = "png")
plt.close()

igd_plus_per_num_machines = {}

for solver in solvers:
    igd_plus_per_num_machines[solver] = {}
    for num_machines in nums_machines:
        igd_plus_per_num_machines[solver][num_machines] = []

for num_machines in nums_machines:
    for instance in instances_per_num_machines[num_machines]:
        for solver in solvers:
            for seed in seeds:
                filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            igd_plus_per_num_machines[solver][num_machines].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.xlabel("Number of Machines")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y = []
    for num_machines in nums_machines:
        y.append(stats.mean(igd_plus_per_num_machines[solvers[i]][num_machines]))
    plt.plot(nums_machines, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "best")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_mean_per_num_machines.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.xlabel("Number of Machines")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(igd_plus_per_num_machines[solvers[i]][num_machines])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(nums_machines, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for num_machines in nums_machines:
        quantiles = stats.quantiles(igd_plus_per_num_machines[solvers[i]][num_machines])
        y1.append(quantiles[1])
    plt.plot(nums_machines, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "upper center")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_quartiles_per_num_machines.png")
plt.savefig(filename, format = "png")
plt.close()

igd_plus_per_total_num_operations = {}

for solver in solvers:
    igd_plus_per_total_num_operations[solver] = {}
    for total_num_operations in total_nums_operations:
        igd_plus_per_total_num_operations[solver][total_num_operations] = []

for total_num_operations in total_nums_operations:
    for instance in instances_per_total_num_operations[total_num_operations]:
        for solver in solvers:
            for seed in seeds:
                filename = os.path.join(dirname, "igd_plus/" + instance + "_" + solver + "_" + str(seed) + ".txt")
                if os.path.exists(filename):
                    with open(filename) as csv_file:
                        data = csv.reader(csv_file, delimiter = ",")
                        for row in data:
                            igd_plus_per_total_num_operations[solver][total_num_operations].append(float(row[0]))
                        csv_file.close()

plt.figure()
plt.xlabel("Total Number of Operations")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y = []
    for total_num_operations in total_nums_operations:
        y.append(stats.mean(igd_plus_per_total_num_operations[solvers[i]][total_num_operations]))
    plt.plot(total_nums_operations, y, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.80)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "upper left")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_mean_per_total_num_operations.png")
plt.savefig(filename, format = "png")
plt.close()

plt.figure()
plt.xlabel("Total Number of Operations")
plt.ylabel("Normalized Modified Inverted Generational Distance")
plt.grid(alpha=0.5, color='gray', linestyle='dashed', linewidth=0.5, which='both')
for i in range(len(solvers)):
    y0 = []
    y2 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(igd_plus_per_total_num_operations[solvers[i]][total_num_operations])
        y0.append(quantiles[0])
        y2.append(quantiles[2])
    plt.fill_between(total_nums_operations, y0, y2, color = colors[i], alpha = 0.25)
for i in range(len(solvers)):
    y1 = []
    for total_num_operations in total_nums_operations:
        quantiles = stats.quantiles(igd_plus_per_total_num_operations[solvers[i]][total_num_operations])
        y1.append(quantiles[1])
    plt.plot(total_nums_operations, y1, label = solver_labels[solvers[i]], marker = (i + 3, 2, 0), color = colors[i], alpha = 0.75)
plt.yscale("log")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.gca().yaxis.set_minor_formatter(FormatStrFormatter('%.3f'))
plt.legend(loc = "upper left")
plt.tight_layout()
filename = os.path.join(dirname, "igd_plus/igd_plus_quartiles_per_total_num_operations.png")
plt.savefig(filename, format = "png")
plt.close()
