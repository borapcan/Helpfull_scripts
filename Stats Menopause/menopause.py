import pandas as pd
import numpy as np

# Assuming that the Excel file is in the same folder as this script

file_name = "Menstrual cycle RA.xlsx"

# Read the Excel file and extract the required columns ('Name', 'S', 'B', 'F', 'G2', 'G1', 'G0')

df = pd.read_excel(
    file_name,
    usecols=[
        "Name",
        "GP1",
        "GP2",
        "GP3",
        "GP4",
        "GP5",
        "GP6",
        "GP7",
        "GP8",
        "GP9",
        "GP10",
        "GP11",
        "GP12",
        "GP13",
        "GP14",
        "GP15",
        "GP16",
        "GP17",
        "GP18",
        "GP19",
        "GP20",
        "GP21",
        "GP22",
        "GP23",
        "GP24",
        "S",
        "B",
        "F",
        "G2",
        "G1",
        "G0",
    ],
)

# Convert all relevant columns to numeric types, coercing errors to NaN

traits = [
    "GP1",
    "GP2",
    "GP3",
    "GP4",
    "GP5",
    "GP6",
    "GP7",
    "GP8",
    "GP9",
    "GP10",
    "GP11",
    "GP12",
    "GP13",
    "GP14",
    "GP15",
    "GP16",
    "GP17",
    "GP18",
    "GP19",
    "GP20",
    "GP21",
    "GP22",
    "GP23",
    "GP24",
    "S",
    "B",
    "F",
    "G2",
    "G1",
    "G0",
]

df[traits] = df[traits].apply(pd.to_numeric, errors="coerce")

# Create a function to extract the timepoint from the 'Name' column


def extract_timepoint(name):
    timepoint_str = name[2:4]
    try:
        return int(timepoint_str)
    except ValueError:
        return -1


# Extract timepoint and person number from the 'Name' column

df["Timepoint"] = df["Name"].apply(extract_timepoint)
df["Person"] = (
    df["Name"].str.extract(r"GM\d{2}(\d{2})_", expand=False).fillna(-1).astype(int)
)

# Filter out rows where the 'Name' column starts with 'stand' and '_S'

df = df[~df["Name"].str.startswith("stand")]
df = df[~df["Name"].str.contains("_S")]

# Format the 'Person' and 'Timepoint' columns with leading zeros

df["Person"] = df["Person"].apply(lambda x: f"{x:02d}")
df["Timepoint"] = df["Timepoint"].apply(lambda x: f"{x:02d}")

# Create a new DataFrame with 'GM Code', 'Person Code', 'Timepoint Code', and the traits

output_df = df[["Name", "Person", "Timepoint", *traits]].copy()

output_df.columns = ["GM Code", "Person Code", "Timepoint Code", *traits]

# Sort the table first by person and then by timepoint

output_df.sort_values(by=["Person Code", "Timepoint Code"], inplace=True)

# Calculate normalized values for all traits by the first timepoint ('01')

for trait in traits:
    trait_column_name = f"{trait}_Normalized"
    normalized_values_df = pd.DataFrame(
        columns=["Person Code", "Timepoint Code", trait_column_name]
    )

    for person in output_df["Person Code"].unique():
        person_df = output_df[output_df["Person Code"] == person]
        person_01_trait_df = person_df[person_df["Timepoint Code"] == "01"][trait]

        # Check if the person_df contains data for the '01' timepoint and trait before proceeding

        if not person_01_trait_df.empty:
            person_01_trait = person_01_trait_df.values[0]

            for timepoint in person_df["Timepoint Code"]:
                trait_value = person_df[person_df["Timepoint Code"] == timepoint][
                    trait
                ].values[0]
                normalized_trait = trait_value / person_01_trait
                normalized_values_df = pd.concat(
                    [
                        normalized_values_df,
                        pd.DataFrame(
                            {
                                "Person Code": [person],
                                "Timepoint Code": [timepoint],
                                trait_column_name: [normalized_trait],
                            }
                        ),
                    ]
                )

    # Merge normalized values back to the original output_df for the current trait

    output_df = pd.merge(
        output_df, normalized_values_df, on=["Person Code", "Timepoint Code"]
    )

# Save the output DataFrame to an Excel file

output_df.to_excel("output_data.xlsx", index=False)


# # Convert the 'Timepoint Code' column to numeric

# output_df["Timepoint Code"] = pd.to_numeric(output_df["Timepoint Code"])


# # Create a DataFrame to store the results
# results_df = pd.DataFrame(
#     columns=[
#         "Glycan Trait",
#         "Time Effect",
#         "Standard Deviation",
#         "P-Value",
#         "Adjusted P-Value",
#     ]
# )

# # Perform linear regression for each trait and calculate time effect

# traits = ["G0", "G1", "G2", "B", "F", "S"]
# traits_n = [
#     "G0_Normalized",
#     "G1_Normalized",
#     "G2_Normalized",
#     "B_Normalized",
#     "F_Normalized",
#     "S_Normalized",
# ]
# print(output_df)
# adjusted_p_values = {}

# for trait in traits_n:
#     # Select columns for the regression
#     columns = ["Timepoint Code", trait]

#     # Fit linear regression model
#     X = sm.add_constant(output_df["Timepoint Code"])
#     y = output_df[trait]
#     model = sm.OLS(y, X).fit()

#     # Extract p-value and time effect
#     p_value = model.pvalues["Timepoint Code"]
#     time_effect = model.params["Timepoint Code"]
#     standard_deviation = y.std()

#     # Store p-value for multiple testing correction
#     adjusted_p_values[trait] = p_value

#     # Append results to the results DataFrame
#     results_df = results_df.append(
#         {
#             "Glycan Trait": trait,
#             "Time Effect": time_effect,
#             "Standard Deviation": standard_deviation,
#             "P-Value": p_value,
#             "Adjusted P-Value": None,
#         },
#         ignore_index=True,
#     )

# # Adjust p-values using the Benjamini-Hochberg procedure

# adjusted_p_values_list = list(adjusted_p_values.values())
# rejected, adjusted_p_values_bh, _, _ = multipletests(
#     adjusted_p_values_list, method="fdr_bh"
# )

# # Update the Adjusted P-Value column in the results DataFrame

# results_df["Adjusted P-Value"] = adjusted_p_values_bh

# # Save the results DataFrame to a text file

# results_df.to_csv("results_n.txt", sep="\t", index=False)


# # Create subplots for 'B_Normalized' and 'S_Normalized' and add 'F_Normalized', 'G0_Normalized', 'G1_Normalized', and 'G2_Normalized'

# fig, axs = plt.subplots(2, 3, sharex=True, gridspec_kw={"hspace": 0.3}, figsize=(12, 8))

# # Create a list of traits to plot

# traits = [
#     "G0_Normalized",
#     "G1_Normalized",
#     "G2_Normalized",
#     "S_Normalized",
#     "B_Normalized",
#     "F_Normalized",
# ]

# trendline_colors = ["red", "blue", "green", "orange", "purple", "brown"]


# # Set the common x-axis range

# common_x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# # Set y-axis ticks for all subplots

# y_ticks = [0.5, 0.75, 1, 1.25, 1.5, 1.75]

# # Plot each trait for each person

# for i, trait in enumerate(traits):
#     row, col = i // 3, i % 3
#     ax = axs[row, col]
#     for person in output_df["Person Code"].unique():
#         person_df = output_df[output_df["Person Code"] == person]
#         ax.plot(
#             person_df["Timepoint Code"],
#             person_df[trait],
#             marker="o",
#             color="gray",
#             alpha=0.5,
#             label=f"Person {person}",
#         )

#     # Calculate and plot the trendline for each trait

#     sns.regplot(
#         x="Timepoint Code",
#         y=trait,
#         data=output_df,
#         ci=None,
#         scatter=False,
#         ax=ax,
#         color=trendline_colors[i],
#         label=f"Trendline {trait[:-10]}",
#     )

#     # Set x-axis ticks for all subplots

#     ax.set_xticks(common_x_axis)

#     # Set y-axis ticks

#     ax.set_yticks(y_ticks)

#     # Set labels and titles for each subplot

#     ax.set_ylabel(f" ")
#     ax.set_xlabel(f" ")

#     # Set the background for the title

#     title_text = f"{trait[:-11]}"
#     ax.set_title(title_text)

# # Apply Seaborn styling

# sns.set_style("whitegrid")
# sns.set_palette("gray")

# # Remove legends for all subplots

# for ax in axs.flat:
#     ax.legend().set_visible(False)

# # Add the global x-axis label below the bottom middle subplo

# fig.text(0.5, 0.04, "Time point (weeks)", ha="center", fontsize=12)

# # Add the global y-axis label to the left side of the subplot grid

# fig.text(
#     0.1,
#     0.5,
#     "Normalized value",
#     ha="center",
#     va="center",
#     rotation="vertical",
#     fontsize=16,
# )


# plt.savefig("mc_figure.pdf", bbox_inches="tight")
# plt.show()
