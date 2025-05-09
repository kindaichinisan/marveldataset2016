import os

# Folder containing the images
image_folder = r"D:\WJ_git\marveldataset2016\W0_1"

# Output file
output_file = "image_ids.txt"

# List to store IDs
image_ids = []

# Loop through files in the folder
for filename in os.listdir(image_folder):
    if filename.lower().endswith(".jpg") and filename[:-4].isdigit():
        image_ids.append(int(filename[:-4]))  # remove ".jpg" and convert to int

# Sort IDs
image_ids.sort()

# Save to file
with open(output_file, "w", encoding="utf-8") as f:
    for img_id in image_ids:
        f.write(f"{img_id}\n")

print(f"✅ Image IDs saved to {output_file}")