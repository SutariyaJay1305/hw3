import os 
import subprocess
import re

img_dir = "/home/ubuntu/hw3/libpng-1.6.40/testcase_dir"
o_dir = "temp_output"
file_list = []

for filename in os.listdir(img_dir):
    if os.path.isfile(os.path.join(img_dir, filename)):
        file_list.append(filename)

print(f"Total files: {len(file_list)}")

total_coverage = 0
final_files = []

for file in file_list:
    subprocess.run(f'./pngtest {os.path.join(img_dir, file)}', shell=True)
    coverage_command = "gcov *.c"
    output = subprocess.check_output(coverage_command, shell=True).decode('utf-8')
    lines = output.splitlines()
    last_line = lines[-1]

    cov_string = re.search(r':(.*?)(%)', last_line)
    if cov_string:
        value = float(cov_string.group(1))
        if value > total_coverage:
            total_coverage = value
            final_files = [file]
        elif value == total_coverage:
            final_files.append(file)
    else:
        print("No match found")

print(f"Total coverage: {total_coverage}%")

for f in file_list:
    if f not in final_files:
        try:
            os.remove(os.path.join(img_dir, f))
        except FileNotFoundError as e:
            print(f"File not found: {f}")
