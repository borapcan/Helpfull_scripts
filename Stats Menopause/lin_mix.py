import pandas as pd
from scipy.stats import rankdata
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from calculate_df import process_excel_file
import scipy.stats as stats

# from batchglm import combat


file_name = "Menstrual cycle RA.xlsx"

# Process the Excel file
output_df = process_excel_file(file_name)

# Convert 'Timepoint' to integers
output_df["Timepoint"] = output_df["Timepoint"].astype(int)

# List of traits
traits_list = [
    "S",
    "B",
    "F",
    "G0",
    "G1",
    "G2",
]

# Define parameters

ps = []
i = 0
result_strs = []


# Function to perform inverse rank transformation
def inverse_rank_transform(rank, desired_mean=0, desired_std=1):
    Z = stats.norm.ppf((rank - 0.5) / len(rank))
    return desired_mean + desired_std * Z


# Open a text file for writing
with open("output_results.txt", "w") as text_file:
    for trait in traits_list:
        # Rank transform trait values for each timepoint
        output_df[trait + "_rank"] = output_df.groupby("Timepoint")[trait].rank()

        # Apply inverse rank transformation to the ranked values
        output_df[trait + "_normal"] = inverse_rank_transform(
            output_df[trait + "_rank"]
        )

        # Define the linear mixed model formula
        # formula2 = trait + "_rank ~ Timepoint"

        formula2 = trait + "_normal ~ Timepoint"

        # formula2 = trait + " ~ Timepoint"

        # Fit the linear mixed model
        mixedlm_model = sm.MixedLM.from_formula(
            formula2, data=output_df, groups=output_df["Person"]
        )
        result = mixedlm_model.fit()

        # Extract information from the result
        time_effect = result.params["Timepoint"]
        standard_error = result.bse["Timepoint"]
        p_value = result.pvalues["Timepoint"]

        ps.append(p_value)

        # Prepare output
        result_str = (
            f"Trait: {trait}\nTime effect: {time_effect}\n"
            f"Standard error: {standard_error}\npvalue: {p_value:}\n"
        )
        result_strs.append(result_str)

        # Write the results to the text file
    # Calculate Benjamini-Hochberg Correction
    adjusted_p_values = multipletests(ps, method="fdr_bh")[1]

    # Print out adjusted p values
    output = ""
    for result in result_strs:
        output += result + f"adj pvalue: {adjusted_p_values[i]}\n"
        output += f"===================================\n"
        i += 1
    # Close the text file
    text_file.write(output)
    print(output)
    text_file.close()


# Save the results to Excel using the current trait name
output_df.to_excel(f"data.xlsx", index=False)  # Use f-string to include trait name
