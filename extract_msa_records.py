from pathlib import Path
import zipfile
import math


inv_t = 50
path = Path(__file__).parent

# Folder containing your .zip files
zip_folder = path / "data/MSA-Records-zip"
# Output folder where they will be extracted
extract_to = path / "data/MSA-Records"
extract_to.mkdir(parents=True, exist_ok=True)

# Step 1: Extract all zip files
for zip_path in zip_folder.glob("*.zip"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        subfolder = extract_to / zip_path.stem
        subfolder.mkdir(parents=True, exist_ok=True)
        zip_ref.extractall(subfolder)
        print(f"Extracted {zip_path.name} to {subfolder}")

    # Step 2: Collect all file names from extracted folders
    all_files = []
    dts = []
    for file_path in subfolder.rglob("*"):  # recursive glob to get all files
        if file_path.is_file():
            # Store relative path (from extract_to) or just file name
            relative_path = file_path.relative_to(subfolder)
            all_files.append(str(relative_path))

            # Try reading the first two rows of the first column
            with file_path.open("r") as f:
                first = f.readline().strip()
                second = f.readline().strip()
                v1 = float(first.split()[0])
                v2 = float(second.split()[0])
                dt = float(v2 - v1)
                dts.append(dt)

    # Step 3: Write all file names to GMR_filenames.txt
    output_file = subfolder / "GMR_filenames.txt"
    with output_file.open("w") as f:
        for filename in all_files:
            f.write(filename + "\n")

    # Step 4: Write all dt values to GMR_dts.txt
    dts_file = subfolder / "GMR_dts.txt"
    with dts_file.open("w") as f:
        for dt in dts:
            f.write(f"{dt}\n")

    # Step 4: Rename the folder names by return period
    poe = float(str(subfolder.relative_to(extract_to)).split('_')[1])
    rt = round(-inv_t / math.log(1 - poe))
    new_path = extract_to / str(rt)
    subfolder.rename(new_path)
