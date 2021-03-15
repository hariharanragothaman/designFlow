import os

home = os.path.expanduser("~")
print(home)

# Note: If '/' is there in the end of {path}, the behavior is different
path = "/home/cppygod/workspace"

# This give the head of the path
print(f"The dirname path is: {os.path.dirname(path)}")
# This gives the tail of the path
print(f"The basename path is: {os.path.basename(path)}")

# Incoming os.walk() fundamentals
# os.walk() - generates - dirpath, dirnames, filenames
"""
dirpath: <string> to the path to the directory
dirnames: <list> of sub-directories in dirpath
filenames: <list> to the names of the non-directory files in dirpath
"""

# So this is the general crawling
for root, dir_names, file_names in os.walk(path):
    print(f"The root is {root}")
    print(f"The directory name is: {dir_names}")
    print(f"The file names are: {file_names}")
    print(f"*"*10)

# After the general crawling - this is just DFS to be honest
complete_files = []
for root, dir_names, file_names in os.walk(path):
    for f in file_names:
        # This os.path.join() is the most crucial line of all.
        # This line internally implements something DFS style.
        complete_files.append(os.path.join(root, f))
print("The complete set of files are ", complete_files)

# Now, check if a specific file-type contains a regex pattern?
for root, dir_names, file_names in os.walk(path):
    for f in file_names:
        fname = os.path.join(root, f)
        if fname.endswith('.py'):
            with open(fname) as myfile:
                line = myfile.read()
                c = line.count('TODO')
                if c:
                    print(f"The file name is: {fname}")
                    print(f"The count is: {c}")


# A solution using glob?
import glob
for filename in glob.iglob(path + '**/**', recursive=True):
    print(filename)