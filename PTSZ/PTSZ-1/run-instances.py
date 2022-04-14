import os
from os import listdir
from os.path import isfile, join

instance_folder = "dane"
solution_folder = "solutions"
instance_files = [f for f in listdir(instance_folder) if isfile(join(instance_folder, f))]
solution_files = [f for f in listdir(solution_folder) if isfile(join(solution_folder, f))]
instance_files.sort()
solution_files.sort()

for instance in instance_files:
    instance_size = instance.split("-")
    instance_size = instance_size[-1]
    instance_size = instance_size[:-4]

    proper_solution = ""
    for solution in solution_files:
        if solution.find("-" + str(instance_size) + ".txt") != -1:
            proper_solution = solution
    #         todo new version of loading
    os.system(
        "python3 validator.py " + instance_folder + "/" + instance + " " + solution_folder + "/" + proper_solution)
