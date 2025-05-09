import os
import csv
import re

# Folder containing the text files
input_folder = r'D:\WJ_git\marveldataset2016\W'
output_csv = 'ships.csv'

# Fields to extract, starting with the filename
fields = [
    "Filename",  # Add this as first column
    "Title", "Photographer", "Photo Category", "Added", "Views", "Image Resolution",
    "Description", "Current name", "Current flag", "Home port", "Callsign",
    "IMO", "MMSI", "Build year", "Builder", "Manager", "Owner",
    "Class society", "Vessel Type", "Gross tonnage", "Summer DWT",
    "Length", "Beam", "Draught", "Former name"
]

# Compile regex patterns anchored at line start
patterns = {
    field: re.compile(rf'^{re.escape(field)}:\s*(.*)', re.IGNORECASE | re.MULTILINE)
    for field in fields if field != "Filename"  # No regex for Filename
}

# Open CSV file for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith('.dat'):
            continue

        filepath = os.path.join(input_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        row = {"Filename": filename}  # Add filename to row
        for field, pattern in patterns.items():
            match = pattern.search(content)
            row[field] = match.group(1).strip() if match else ''

        writer.writerow(row)

print(f"✅ Extraction complete. Data saved to {output_csv}")
