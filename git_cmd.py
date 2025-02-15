import subprocess
import shutil
import os


def useGit(*args):
    if not shutil.which("git"):
        print("git is not installed on your system or cannot be found in your path.")
        os._exit(-1)
    proc = subprocess.run(
        ["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if proc.returncode != 0:
        print(f"error(git): git has returned with the code {proc.returncode}")
        os._exit(proc.returncode)
