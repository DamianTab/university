import os
import sys

path = os.getcwd() + "/" + sys.argv[1] + "/"
print(path)
filenames = os.listdir(path)

for filename in filenames:
    new_filename = filename
    new_filename = new_filename.lower()
    x = "_b_" if new_filename.find("p-") != -1 else "_e_"
    new_filename = new_filename[:1] + x + new_filename[1:]
    new_filename = new_filename.replace("p", "", new_filename.count("p") - 1)
    new_filename = new_filename.replace("-", "")
    new_filename = new_filename.replace(".", "_", new_filename.count(".") - 1)
    os.rename(path + filename, path + new_filename)
