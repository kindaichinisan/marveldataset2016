import csv
from collections import Counter

# Path to your input CSV file
input_csv = "ships2.csv"  # change this if your file has a different name

# Column name for vessel type
vessel_type_column = "Vessel Type"

# Counter for vessel types
vessel_type_counter = Counter()

# Read the CSV and count vessel types
with open(input_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        vessel_type = row.get(vessel_type_column, "").strip()
        if vessel_type:
            vessel_type_counter[vessel_type] += 1

# Print the results
print("📊 Vessel Type Frequency:")
for vessel_type, count in vessel_type_counter.most_common():
    print(f"{vessel_type}: {count}")