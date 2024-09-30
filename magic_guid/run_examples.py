"""Generate examples in docs"""
from magic_guid import random, check, same
print(">>> from magic_guid import random, check, same")
with open("examples.py") as fin:
    for line in fin.readlines():
        line = line.strip()
        if line and not line.startswith("#"):
            print(">>>",line)
            print(eval(line),"\n")