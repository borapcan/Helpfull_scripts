import pandas as pd

# Load the Excel table into a pandas DataFrame
df = pd.read_excel('input.xlsx', header=None)

# Define the size of each set of rows
set_size = 9

# Create an empty list to store the converted values
converted_values = []

# Iterate over each set of rows
for i in range(0, len(df), set_size):
    # Iterate over each column in the current set of rows
    for j in range(len(df.columns)):
        # Iterate over each row in the current column up to row 9
        for k in range(i, i+set_size):
            value = df.iloc[k, j]
            if pd.isna(value):
                # Skip NaN values
                pass
                print(f'Skip {value}, file{i//set_size}')
            elif isinstance(value, str) and (value.startswith('stan') or value.startswith('blank') or value.startswith('Blank')):
                #check if value is string, and if it is check if it starts with stan or Blank
                converted_values.append(175)
                print(f'Transfer {value} into {175}, file{i//set_size}' )
            elif value in [1,2,3,4,5,6,7,8,9,10,11,12,'A','B','C','D','E','F','G','H']:
                # Skip values in the range 1-12 or A-H
                pass
                print(f'Skip {value}, file{i//set_size}')
            elif value == 'n':
                converted_values.append(0)
                print(f'Transfer {value} into {0}, file{i//set_size}')
            else:
                converted_values.append(800)
                print(f'Transfer {value} into {800}, file{i//set_size}')

    # Write the converted values to a CSV file for the current set of rows
    with open(f'plate_input_{i//set_size+1}.csv', 'w') as f:
        for value in converted_values:
            f.write(str(value) + '\n')

    # Clear the list of converted values for the next set of rows
    converted_values = []
