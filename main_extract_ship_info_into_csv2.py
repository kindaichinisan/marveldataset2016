import os
import csv

# Folder containing the text files
input_folder = r'D:\WJ_git\marveldataset2016\W'
output_csv = 'ships.csv'

# Fields to extract, starting with the filename
fields = [
    "Filename", "Title", "Photographer", "Photo Category", "Added", "Views", "Image Resolution",
    "Description", "Current name", "Current flag", "Home port", "Callsign",
    "IMO", "MMSI", "Build year", "Builder", "Manager", "Owner",
    "Class society", "Vessel Type", "Gross tonnage", "Summer DWT",
    "Length", "Beam", "Draught", "Former name"
]

# Normalize field keys for comparison
normalized_fields = {field.lower(): field for field in fields if field != "Filename"}

with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    idx = 0
    for filename in sorted(os.listdir(input_folder)):
        if not filename.lower().endswith('.dat'):
            continue

        filepath = os.path.join(input_folder, filename)
        row = {"Filename": filename}

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if ':' not in line:
                    continue
                key_part, value_part = line.split(':', 1)
                key = key_part.strip().lower()
                value = value_part.strip()
                if key in normalized_fields and value:
                    row[normalized_fields[key]] = value

        writer.writerow(row)

        idx += 1
        if idx > 1000:
            break

print(f"✅ Extraction complete. Data saved to {output_csv}")
