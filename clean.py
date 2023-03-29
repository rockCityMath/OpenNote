import os

path = os.getcwd()
files = os.listdir(path)

for file in files:
    if file.endswith(".on") or file.endswith(".ontemp"):
        os.remove(os.path.join(path, file))