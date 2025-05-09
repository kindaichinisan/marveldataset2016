import os
import shutil

# Create the destination folder if it doesn't exist
os.makedirs("W", exist_ok=True)

dirs = os.listdir(os.getcwd())
for eachDir in dirs:
    if 'W' in eachDir and eachDir != "W":
        if os.path.isdir(eachDir):
            for filename in os.listdir(eachDir):
                src_path = os.path.join(eachDir, filename)
                dst_path = os.path.join("W", filename)

                # If a file with the same name exists in destination, rename it
                if os.path.exists(dst_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dst_path):
                        dst_path = os.path.join("W", f"{base}_{counter}{ext}")
                        counter += 1

                shutil.move(src_path, dst_path)