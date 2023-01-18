import os

# 10 weeks
open("README.md", "w")
for i in range(10):
    os.mkdir(f"week-{i+1}")
    os.chdir(f"week-{i+1}")
    with open("README.md", "w") as f:
        f.write(f"# Week {i+1} \n\n To be updated")
    os.chdir("../")

