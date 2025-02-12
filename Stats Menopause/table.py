import pandas as pd

# Assuming that the Excel file is in the same folder as this script
file_name = "Menstrual cycle RA.xlsx"

# Read the Excel file and extract the required columns ('Name', 'S', 'B', 'F', 'G2', 'G1', 'G0')
df = pd.read_excel(file_name, usecols=['Name','S', 'B', 'F', 'G2', 'G1', 'G0'])

# Create a function to extract the timepoint from the 'Name' column
def extract_timepoint(name):
    timepoint_str = name[2:4]
    try:
        return int(timepoint_str)
    except ValueError:
        return -1

# Extract timepoint and person number from the 'Name' column
df['Timepoint'] = df['Name'].apply(extract_timepoint)
df['Person'] = df['Name'].str.extract(r'GM\d{2}(\d{2})_', expand=False).fillna(-1).astype(int)

# Filter out rows where the 'Name' column starts with 'stand'
df = df[~df['Name'].str.startswith('stand')]

# Format the 'Person' and 'Timepoint' columns with leading zeros
df['Person'] = df['Person'].apply(lambda x: f"{x:02d}")
df['Timepoint'] = df['Timepoint'].apply(lambda x: f"{x:02d}")

# Create a new DataFrame with 'GM Code', 'Person Code', 'Timepoint Code', 'S', 'B', 'F', 'G2', 'G1', and 'G0'
output_df = df[['Name', 'Person', 'Timepoint', 'S', 'B', 'F', 'G2', 'G1', 'G0']].copy()
output_df.columns = ['GM Code', 'Person Code', 'Timepoint Code', 'S', 'B', 'F', 'G2', 'G1', 'G0']

# Sort the table first by person and then by timepoint
output_df.sort_values(by=['Person Code', 'Timepoint Code'], inplace=True)

# Save the DataFrame to an Excel file
output_file_path = "Sorted_Table_With_Data.xlsx"
output_df.to_excel(output_file_path, index=False)


