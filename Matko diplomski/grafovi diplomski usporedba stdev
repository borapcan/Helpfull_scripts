import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the first Excel file
df1 = pd.read_excel(r'C:\Users\Genos\Downloads\uzorci DIPLOMSKI.xlsx')

# Read the second Excel file
df2 = pd.read_excel(r'C:\Users\Genos\Desktop\uzorci diplomski manual.xlsx')

# Define the custom order of x-axis labels
x_labels = [f"GP{i}" for i in range(1, 31)]

# Create a subset DataFrame with the desired row and columns from the first file
subset_df1 = df1.iloc[75, 2:].rename_axis('GP AVG').reset_index(name='avg')
subset_df1['Source'] = 'Automatski'
print(subset_df1)

# Create a subset DataFrame with the desired row and columns from the second file
subset_df2 = df2.iloc[76, 2:].rename_axis('GP AVG').reset_index(name='avg')
subset_df2['Source'] = 'Manualno'
print(subset_df2)

# Concatenate the two subset DataFrames
combined_df = pd.concat([subset_df1, subset_df2])

# Reorder the combined DataFrame based on the custom order of x-axis labels
combined_df['GP AVG'] = pd.Categorical(combined_df['GP AVG'], categories=x_labels, ordered=True)
combined_df = combined_df.sort_values('GP AVG')
print(combined_df)

# Plot the bar plot with adjusted figure size and rotated x-axis labels
plt.figure(figsize=(16, 10))
sns.barplot(x='GP AVG', y='avg', hue='Source', data=combined_df, palette=['red', 'blue'])
plt.xticks(rotation=45, ha='right')  # Rotates x-axis labels by 45 degrees and aligns them to the right

# Save the plot as PDF
plt.savefig('diplomski_comparison_stdev.pdf')
