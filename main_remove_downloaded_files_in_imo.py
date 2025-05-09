input_file_1 = r'D:\WJ_git\marveldataset2016_run2\VesselClassification_no_duplicate.dat'  # contains IDs to exclude
input_file_2 = r'D:\WJ_git\marveldataset2016_run2\IMOTrainAndTest.dat'  # data to filter
output_file = r'D:\WJ_git\marveldataset2016_run2\IMOTrainAndTest_filtered.dat'

# Step 1: Read first column values from file1
with open(input_file_1, 'r', encoding='utf-8') as f1:
    ids_to_exclude = {line.strip().split(',')[0] for line in f1 if line.strip()}

# Step 2: Filter file2
with open(input_file_2, 'r', encoding='utf-8') as f2, \
     open(output_file, 'w', encoding='utf-8') as out:
    
    for line in f2:
        if not line.strip():
            continue  # skip empty lines
        first_col = line.strip().split(',')[0]
        if first_col not in ids_to_exclude:
            out.write(line)

print(f"✅ Done: Filtered data written to {output_file}")