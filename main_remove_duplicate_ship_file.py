import os
import re

# Folder to scan for duplicates
folder = r'D:\WJ_git\marveldataset2016\W'

# Regex to match filenames like "name_1.ext", "name_2.ext", etc.
pattern = re.compile(r'^(.*)_\d+\.(\w+)$')

for filename in os.listdir(folder):
    match = pattern.match(filename)
    if not match:
        continue

    base_name = f"{match.group(1)}.{match.group(2)}"
    base_path = os.path.join(folder, base_name)
    dup_path = os.path.join(folder, filename)

    if os.path.exists(base_path):
        print(f"Deleting duplicate: {filename}")
        os.remove(dup_path)
