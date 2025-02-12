import pandas as pd

# Load your existing Excel file
input_file = 'All_1.xlsx'
df = pd.read_excel(input_file)

# Initialize a set to store unique samples
unique_samples = set()

# Extract the unique samples by splitting the "Sample Name" column on the dot and taking the first part
for index, row in df.iterrows():
    sample_name = str(row['Sample Name'])
    sample_parts = sample_name.split('.')
    if len(sample_parts) > 0:
        sample = sample_parts[0]
        unique_samples.add(sample)

# Sort the unique samples in ascending order
sorted_samples = sorted(list(unique_samples), key=lambda x: int(x))

# Create a new DataFrame with the sorted "Sample" column
result_df = pd.DataFrame({'Sample': sorted_samples})

# Define a function to extract the value based on a specific pattern for a given column
def extract_column_value(sample, pattern, column_name):
    matches = df['Sample Name'].str.contains(f'{sample}{pattern}')
    if any(matches):
        return df.loc[matches, column_name].values[0]
    else:
        return None

# Define the columns for which you want to extract values
columns_to_extract = ['S', 'B', 'F', 'G0', 'G1', 'G2']

# Loop through the columns and patterns to create new columns and populate them
for column_name in columns_to_extract:
    for pattern in ['.1', '.2', '.3']:
        result_df[f'{column_name}{pattern}'] = result_df['Sample'].apply(lambda x: extract_column_value(x, pattern, column_name))

# Print the new DataFrame
print("Modified DataFrame:")
print(result_df)

# Save the result to a new Excel file named "all_1s.xlsx"
output_file = 'all_1s.xlsx'
result_df.to_excel(output_file, index=False)

print(f"Filtered samples saved to {output_file}")
