import re

input_file = "download.log"
output_file = "no_such_file_ids.txt"

with open(input_file, "r", encoding="utf-8", errors="ignore") as f, open(output_file, "w", encoding="utf-8") as out:
    for line in f:
        match = re.search(r"\)\s+(\d+)\s+- NO SUCH FILE", line)
        if match:
            out.write(match.group(1) + "\n")