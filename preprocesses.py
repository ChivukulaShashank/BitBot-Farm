import pandas as pd
import os

def align_raw_dataset(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"❌ Cannot find source file at {input_path}")
        return

    # 1. Load data
    df = pd.read_csv(input_path)

    # 2. Rename columns to match pipeline architecture specifications
    rename_map = {
        "HGB": "Hemoglobin",
        "Diagnosis": "Result"
    }
    df = df.rename(columns=rename_map)

    # 3. Transform textual diagnoses to clear binary integers
    # 'Healthy' maps to 0; all variations of anemia/leukemia map to 1
    df["Result"] = df["Result"].apply(lambda val: 0 if str(val).strip() == "Healthy" else 1)

    # 4. Perform logical filtering to drop corrupt, impossible rows
    # Drops Row 5 (HCT 316) and Row 6 (MCHC 79.6)
    initial_count = len(df)
    df = df[df["MCHC"] <= 60.0]
    df = df[df["Hemoglobin"] >= 1.0]
    
    purged_count = initial_count - len(df)

    # 5. Commit aligned file to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print("================================================================")
    print("✨ DATA PREPROCESSING & ALIGNMENT SUCCESSFUL")
    print("   - Renamed features to match target schemas.")
    print("   - Converted 'Diagnosis' text classes to binary [0, 1] outcomes.")
    print(f"   - Filtered out {purged_count} physiologically corrupted data records.")
    print(f"💾 Clean file saved for pipeline use at: {output_path}")
    print("================================================================")

if __name__ == "__main__":
    align_raw_dataset("data/raw_blood_tests.csv", "data/raw_blood_tests.csv")