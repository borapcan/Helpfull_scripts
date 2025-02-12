import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Read the first Excel file
df1 = pd.read_excel(r'C:\Users\Genos\Downloads\uzorci DIPLOMSKI.xlsx')

# Read the second Excel file
df2 = pd.read_excel(r'C:\Users\Genos\Desktop\uzorci diplomski manual.xlsx')

# Define the custom order of x-axis labels
x_labels = [f"GP{i}" for i in range(1, 31)]

# Create a subset DataFrame with the desired row and columns from the first file
subset_df1 = df1.iloc[74, 2:].rename_axis('GP AVG').reset_index(name='avg')
subset_df1['Source'] = 'Automatski'

# Create a subset DataFrame with the desired row and columns from the second file
subset_df2 = df2.iloc[72, 2:].rename_axis('GP AVG').reset_index(name='avg')
subset_df2['Source'] = 'Manualno'

# Read error values for df1 from an Excel file
error_df1 = pd.read_excel(r'C:\Users\Genos\Downloads\uzorci DIPLOMSKI.xlsx', skiprows=75, usecols=range(2, 33))

# Read error values for df2 from an Excel file
error_df2 = pd.read_excel(r'C:\Users\Genos\Desktop\uzorci diplomski manual.xlsx', skiprows=range(76), usecols=range(2, 33))
print(error_df2)
# Concatenate the two subset DataFrames
combined_df = pd.concat([subset_df1, subset_df2])

# Reorder the combined DataFrame based on the custom order of x-axis labels
combined_df['GP AVG'] = pd.Categorical(combined_df['GP AVG'], categories=x_labels, ordered=True)
combined_df = combined_df.sort_values('GP AVG')

# Plot the bar plot with adjusted figure size and rotated x-axis labels
plt.figure(figsize=(20, 10))
sns.barplot(x='GP AVG', y='avg', hue='Source', data=combined_df, palette=['red', 'blue'])
plt.xticks(rotation=45, ha='right')  # Rotates x-axis labels by 45 degrees and aligns them to the right



# Generate x-values for error bars
x_values1 = np.arange(len(error_df1.columns))
x_values2 = np.arange(len(error_df2.columns))

# Add error bars for df1
error_values1 = error_df1.values.flatten()[:31]  # Select first 31 error values
plt.errorbar(x=x_values1 - 0.2, y=combined_df[combined_df['Source'] == 'Automatski']['avg'], yerr=error_values1, fmt='none', color='black', capsize=6, linewidth=3.5)

# Add error bars for df2
error_values2 = error_df2.values.flatten()[:31]  # Select first 31 error values
plt.errorbar(x=x_values2 + 0.2, y=combined_df[combined_df['Source'] == 'Manualno']['avg'], yerr=error_values2, fmt='none', color='black', capsize=6, linewidth=3.5)

# Increase font size of axis labels
plt.xlabel('X-axis Label', fontsize=14)
plt.ylabel('Y-axis Label', fontsize=14)

# Start y-axis at zero
plt.ylim(bottom=0)


# Save the plot as PDF
plt.savefig('diplomski_avg_stdev.pdf')
