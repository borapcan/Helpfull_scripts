import pandas as pd

# Load the Excel file into a DataFrame
file_name = "Sorted_Table_With_Data.xlsx"
df = pd.read_excel(file_name, engine="openpyxl")

# Filter rows where 'GM Code' does not contain '_S'
filtered_df = df[~df['GM Code'].str.contains('_S')]

# Save the filtered DataFrame to a new Excel file
filtered_file_name = "Filtered_Table_Without_S.xlsx"
filtered_df.to_excel(filtered_file_name, index=False, engine="openpyxl")

print(f"Filtered data saved to {filtered_file_name}")