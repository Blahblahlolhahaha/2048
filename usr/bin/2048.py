#! /usr/bin/env python3
import subprocess
import os

os.chdir("/usr/share/2048")

subprocess.Popen("python3 main.py",shell=True)