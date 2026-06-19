import pandas as pd
import os
from typing import List

class CSVDataExtractor:
    """
    Stage 1 Component: Data Extraction
    Responsible exclusively for loading raw CSV datasets, isolating user-selected 
    features, forcing numerical integrity, sanitizing missing values, and saving the output.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Extraction Failure: Target CSV file missing at {file_path}")
        self.cleaned_df = None

    def extract_clean_dataframe(self, chosen_features: List[str], target_col: str) -> pd.DataFrame:
        """
        Loads the raw CSV, slices explicitly requested columns, forces numeric
        casting on feature inputs, and purges all incomplete records.
        """
        if not chosen_features:
            raise ValueError("Extraction Error: You must explicitly provide at least one feature column.")

        # 1. File Ingestion
        df = pd.read_csv(self.file_path)

        # 2. Explicit Slicing Verification
        required_columns = chosen_features + [target_col]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Schema Mismatch: Specified columns missing from CSV: {missing_cols}")

        df_sliced = df[required_columns].copy()

        # 3. Numeric Forcing (Features and Target Column Safeguard)
        for col in chosen_features:
            df_sliced[col] = pd.to_numeric(df_sliced[col], errors='coerce')
        
        # Ensure target column is evaluated as a consistent datatype
        df_sliced[target_col] = pd.to_numeric(df_sliced[target_col], errors='coerce')

        # 4. Sanitization Matrix
        self.cleaned_df = df_sliced.dropna()
        return self.cleaned_df

    def save_clean_dataframe(self, output_path: str):
        """
        Saves the sanitized matrix to disk. Protects against empty directory string evaluation.
        """
        if self.cleaned_df is None:
            raise RuntimeError("Save Error: You must run extract_clean_dataframe() before saving.")
        
        # Defensive check against empty path strings crashing os.makedirs
        directory_prefix = os.path.dirname(output_path)
        if directory_prefix:
            os.makedirs(directory_prefix, exist_ok=True)
            
        self.cleaned_df.to_csv(output_path, index=False)
        print(f"✅ Cleaned data matrix saved successfully to: {output_path}")