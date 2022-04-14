import os
from os import listdir
from os.path import isfile

files = [f for f in listdir() if isfile(f)]
files.sort()

for algorithm in files:
    if "-algorithm.exe" not in algorithm:
        continue

    for instance in files:
        if "-instance-" not in instance:
            continue
        else:
            os.system("python3 validator.py " + instance + " " + algorithm)
