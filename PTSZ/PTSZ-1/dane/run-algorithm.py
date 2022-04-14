import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

algorithms_folder = "algorithms"
algorithm_name = "136819-algorithm.exe"

instance_folder = "."
instance_files = [f for f in listdir(instance_folder) if isfile(join(instance_folder, f))]
to_remove = []
for file_name in instance_files:
    if "solution" in file_name:
        to_remove.append(file_name)

instance_files = [x for x in instance_files if x not in to_remove]
instance_files.sort()



for instance in instance_files:
    instance_size = instance.split("-")
    instance_size = instance_size[-1]
    instance_size = instance_size[:-4]

    path1 = Path(instance)
    path2 = Path(algorithm_name)

    os.system("python3 validator.py " + str(path1) + " " + str(path2))
