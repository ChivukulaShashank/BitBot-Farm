import os
import glob

# 1. Inject Kaggle credentials directly
os.environ["KAGGLE_USERNAME"] = "ShashankCS123"
os.environ["KAGGLE_KEY"] = "KGAT_46da44ccd13167c85cd34537e0c7e0c4"

# 2. Create target directory
target_dir = "data"
os.makedirs(target_dir, exist_ok=True)

print("Initiating stable Kaggle CLI download...")

# 3. Execute the classic, stable CLI command
os.system(f"kaggle datasets download -d ehababoelnaga/anemia-types-classification --unzip -p {target_dir}")

# 4. Find and rename the CSV for our pipeline
csv_files = glob.glob(os.path.join(target_dir, "*.csv"))

if csv_files:
    target_path = os.path.join(target_dir, "raw_blood_tests.csv")
    if csv_files[0] != target_path:
        os.rename(csv_files[0], target_path)
    print(f"✅ Success! Dataset downloaded, unzipped, and locked in at: {target_path}")
else:
    print("❌ Error: Download failed. Check your API credentials.")