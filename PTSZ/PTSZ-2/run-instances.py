import os
from os import listdir
from os.path import isfile

files = [f for f in listdir() if isfile(f)]
files.sort()

for instance in files:
    if "-instance-" not in instance:
        continue

    instance_size = instance.split("-")
    instance_size = instance_size[-1]
    instance_size = instance_size[:-4]

    proper_solution = ""
    for solution in files:
        if "-solution-" not in solution:
            continue
        if solution.find("-" + str(instance_size) + ".txt") != -1:
            proper_solution = solution
            print(instance)
            print(solution)
            break
    os.system("python3 validator.py " + instance + " " + proper_solution)
