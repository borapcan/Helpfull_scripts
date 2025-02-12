import pandas as pd
from regress import PassingBablok

# Load the data from Excel files
man_data = pd.read_excel("man.xlsx")
tec_data = pd.read_excel("tec.xlsx")

# Open a file for writing
with open("passing.txt", "w") as file:
    # Iterate over each GP column and perform Passing-Bablok regression
    for gp_column in man_data.columns[1:]:
        # Select the relevant columns from both datasets
        man_gp = man_data[["Sample Name", gp_column]]
        tec_gp = tec_data[["Sample Name", gp_column]]

        # Merge the datasets based on the 'Sample Name' column
        merged_data = pd.merge(
            man_gp, tec_gp, on="Sample Name", suffixes=("_man", "_tec")
        )

        # Drop rows with missing values
        merged_data = merged_data.dropna()

        # Perform Passing-Bablok regression
        pb_result = PassingBablok(
            merged_data[gp_column + "_man"], merged_data[gp_column + "_tec"]
        )

        # Write the results to the file
        file.write(f"For {gp_column}:\n")
        file.write(f"Intercept: {pb_result.intercept:.4f}\n")
        file.write(f"Slope: {pb_result.slope:.4f}\n")
        file.write("=" * 30 + "\n")
