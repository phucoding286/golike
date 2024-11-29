import os, sys

if sys.platform.startswith("win"):
    os.system("python ./instagram/main.py")
else:
    os.system("python3 ./instagram/main.py")