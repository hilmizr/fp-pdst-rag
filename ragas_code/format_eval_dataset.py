import os
import pandas as pd
from tqdm import tqdm
import time

# Define directories
source_dir = r"D:\MyITSAcademia2-Season1\PDST\fp-pdst-rag\cleaned_results"
ground_truth_path = r"D:\MyITSAcademia2-Season1\PDST\fp-pdst-rag\ground_truth.xlsx"
output_dir = r"D:\MyITSAcademia2-Season1\PDST\fp-pdst-rag\combined_results"
log_file_path = os.path.join(output_dir, "processed_files.log")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load ground truth data
ground_truth_data = pd.read_excel(ground_truth_path)

# Load the log of processed files
if os.path.exists(log_file_path):
    with open(log_file_path, "r") as log_file:
        processed_files = set(log_file.read().splitlines())
else:
    processed_files = set()

# Get list of files to process
all_files = [f for f in os.listdir(source_dir) if f.endswith(".xlsx")]
new_files = [f for f in all_files if f not in processed_files]

# Start the timer
start_time = time.time()

# Iterate over new Excel files in the source directory
with tqdm(total=len(new_files), desc="Processing files", unit="file") as pbar:
    for filename in new_files:
        file_path = os.path.join(source_dir, filename)
        
        # Load the current file
        current_data = pd.read_excel(file_path)
        
        # Merge with ground truth
        combined_data = current_data.merge(ground_truth_data, on="queries", how="inner")
        
        # Rename and reorder columns as per Task 1
        combined_data = combined_data.rename(
            columns={
                "queries": "inputs",
                "responses": "actual_output",
                "expected_output": "expected_output",
                "cleaned_contexts": "retrieval_context"
            }
        )[["inputs", "actual_output", "expected_output", "retrieval_context"]]
        
        # Create the output file name
        output_file_name = f"combined_{filename}"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        # Save the combined data to the new directory
        combined_data.to_excel(output_file_path, index=False)
        
        # Update the log file
        with open(log_file_path, "a") as log_file:
            log_file.write(filename + "\n")
        
        # Update progress bar
        pbar.update(1)

# Stop the timer
end_time = time.time()
print(f"Processing completed in {end_time - start_time:.2f} seconds.")
