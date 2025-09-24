import subprocess

output = subprocess.check_output(['yapf', '-ir', '.'])
print("Formatting is done!")
