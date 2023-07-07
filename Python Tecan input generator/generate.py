import pandas as pd
import numpy as np

# Load the Excel table into a pandas DataFrame
df = pd.read_excel('input1.xlsx', header=None)

# Create an empty list to store the converted values
converted_values = []

# Iterate over each column in the DataFrame
for column in df:
    for value in df[column]:
        if pd.isna(value):
            # Skip NaN values
            pass
        elif isinstance(value, str) and value.startswith('stan'):
            # append 175 ul if its a standard
            converted_values.append(175)
        elif value == 'blank_s':
            # append 200 ul if its a blank
            converted_values.append(200)
        elif value in ['',1,2,3,4,5,6,7,8,9,10,11,12,'A','B','C','D','E','F','G','H']:
            # skip if its plate markings
            pass
        elif value == 'blank_d':
            # append 800 ul if its a blank with an empty filter
            converted_values.append(800)
        elif value == 'n':
            # append 0 ul if its an empty spot
            converted_values.append(0)
        else:
            # append 800 if its a sample (no name restrictions)
            converted_values.append(800)

# Write the converted values to a CSV file
with open('output_file.csv', 'w') as f:
    for value in converted_values:
        f.write(str(value) + '\n')
