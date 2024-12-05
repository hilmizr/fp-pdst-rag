import os
import pandas as pd
import re
from tqdm import tqdm  
import time 

# Define the directory containing the files
input_directory = 'D:/MyITSAcademia2-Season1/PDST/fp-pdst-rag/rag_results/'
output_directory = 'D:/MyITSAcademia2-Season1/PDST/fp-pdst-rag/cleaned_results/'

# Define a log file to track processed files
log_file = 'processed_files_log.txt'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Ensure the log file exists
if not os.path.exists(log_file):
    with open(log_file, 'w') as file:
        pass  # Create an empty log file if it doesn't exist

# Load the log of processed files
with open(log_file, 'r') as file:
    processed_files = set(file.read().splitlines())

# Function to clean each context by removing Chunk ID and Relevance Score
def clean_context(context):
    # Remove lines starting with "### Chunk ID:" and "**Relevance Score:**"
    cleaned_context = re.sub(r"### Chunk ID:.*\n", "", context)
    cleaned_context = re.sub(r"\*\*Relevance Score:\*\*.*\n", "", cleaned_context)
    return cleaned_context.strip()

# Start timing
start_time = time.time()

# Get all .xlsx files in the directory
xlsx_files = [f for f in os.listdir(input_directory) if f.endswith('.xlsx')]

# Filter out already processed files
new_files = [f for f in xlsx_files if f not in processed_files]

# Process only new files with a progress bar
for filename in tqdm(new_files, desc="Processing new files"):
    # Load the Excel file
    file_path = os.path.join(input_directory, filename)
    data = pd.ExcelFile(file_path)
    
    # Load the first sheet (assumes relevant data is in the first sheet)
    df = data.parse(data.sheet_names[0])
    
    # Apply the cleaning function to the "contexts" column
    if 'contexts' in df.columns:
        df["cleaned_contexts"] = df["contexts"].apply(clean_context)
    
    # Save the result to the output directory with a 'cleaned_' prefix
    output_file_path = os.path.join(output_directory, f'cleaned_{filename}')
    df.to_excel(output_file_path, index=False)

    # Log the processed file
    with open(log_file, 'a') as log:
        log.write(filename + '\n')

# End timing
end_time = time.time()
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"\nProcessing completed in {elapsed_time:.2f} seconds.")
