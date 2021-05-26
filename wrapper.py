import subprocess

while True:
    try:
        subprocess.run("py runner.py", shell=True)
    except:
        continue