import pandas as pd
from deepeval import evaluate
from deepeval.metrics.ragas import RagasMetric
from deepeval.test_case import LLMTestCase
from datetime import datetime

# Read the Excel file
df = pd.read_excel('D:/MyITSAcademia2-Season1/PDST/fp-pdst-rag/combined_results/combined_cleaned_responses_llama3.2_markdownsplitter_titledchunk_docling_bge_2024-12-04_14-12-40.xlsx')

# Create a list to store test cases
test_cases = []

# Iterate through the dataframe rows and create test cases
for _, row in df.iterrows():
    test_case = LLMTestCase(
        input=row['inputs'],
        actual_output=row['actual_output'],
        expected_output=row['expected_output'],
        retrieval_context=[row['retrieval_context']]  
    )
    test_cases.append(test_case)

# Create the metric
metric = RagasMetric(threshold=0.5, model="gpt-4o-mini")

# Evaluate all test cases
results = evaluate(test_cases, [metric])

# Store results directly without breaking down the structure
results_data = []

for i, result in enumerate(results):
    results_data.append({
        'Test Case': i + 1,
        'Result': result  # Store the full result object or summary directly
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results_data)

# Generate a timestamp for the output filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'evaluation_results_{timestamp}.xlsx'

# Export the results to an Excel file
results_df.to_excel(output_filename, index=False)

print(f"Evaluation results have been saved to {output_filename}")
