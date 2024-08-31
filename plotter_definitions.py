instances = ["mk01", "mk02", "mk03", "mk04", "mk05", "mk06", "mk07", "mk08", "mk09", "mk10", "mk11", "mk12", "mk13", "mk14", "mk15"]
solvers = ["nsga2", "nspso", "moead", "mhaco", "ihs", "nsbrkga"]
solver_labels = {"nsga2": "NSGA-II",
                 "nspso": "NSPSO",
                 "moead":
                 "MOEA/D-DE",
                 "mhaco": "MHACO",
                 "ihs": "IHS",
                 "nsbrkga": "NS-BRKGA"}
seeds = [305089489, 511812191, 608055156, 467424509, 944441939, 414977408, 819312498, 562386085, 287613914, 755772793]
versions = ["best", "median"]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#8c7e6e", "#738191"]
colors2 = ["#103c5a", "#804007", "#165016", "#6b1414", "#4a345f", "#462b26", "#723c61", "#404040", "#5e5f11", "#0c5f68", "#463f37", "#3a4149"]
nums_jobs = [10, 15, 20, 30]
instances_per_num_jobs = {10 : ["mk01", "mk02", "mk06"],
                          15 : ["mk03", "mk04", "mk05"],
                          20 : ["mk07", "mk08", "mk09", "mk10"],
                          30 : ["mk11", "mk12", "mk13", "mk14", "mk15"]}
nums_machines = [4, 5, 6, 8, 10, 15]
instances_per_num_machines = {4 : ["mk05"],
                              5 : ["mk07", "mk11"],
                              6 : ["mk01", "mk02"],
                              8 : ["mk03", "mk04"],
                              10 : ["mk08", "mk09", "mk12", "mk13"],
                              15 : ["mk06", "mk10", "mk14", "mk15"]}
total_nums_operations = [55, 58, 90, 100, 106, 150, 179, 193, 225, 231, 240, 277, 284]
instances_per_total_num_operations = {55 : ["mk01"],
                                      58 : ["mk02"],
                                      90 : ["mk04"],
                                      100 : ["mk07"],
                                      106 : ["mk05"],
                                      150 : ["mk03", "mk06"],
                                      179 : ["mk11"],
                                      193 : ["mk12"],
                                      225 : ["mk08"],
                                      231 : ["mk13"],
                                      240 : ["mk09", "mk10"],
                                      277 : ["mk14"],
                                      284 : ["mk15"]}
total_num_operations_per_instance = {"mk01" : 55,
                                     "mk02" : 58,
                                     "mk03" : 150,
                                     "mk04" : 90,
                                     "mk05" : 106,
                                     "mk06" : 150,
                                     "mk07" : 100,
                                     "mk08" : 225,
                                     "mk09" : 240,
                                     "mk10" : 240,
                                     "mk11" : 179,
                                     "mk12" : 193,
                                     "mk13" : 231,
                                     "mk14" : 277,
                                     "mk15" : 284}
num_snapshots = 30
m = 4
