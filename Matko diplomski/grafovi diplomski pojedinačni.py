import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the Excel files
man_df = pd.read_excel("man.xlsx")
tec_df = pd.read_excel("tec.xlsx")

# Extract the columns related to GP from both DataFrames
man_gp_columns = man_df.columns[1:]
tec_gp_columns = tec_df.columns[1:]

# Create dictionaries for average values
avg_man = {gp: man_df[gp].mean() for gp in man_gp_columns}
avg_tec = {gp: tec_df[gp].mean() for gp in tec_gp_columns}

# Create dictionaries for standard deviations
std_man = {gp: man_df[gp].std() for gp in man_gp_columns}
std_tec = {gp: tec_df[gp].std() for gp in tec_gp_columns}

# Sort the keys numerically
sorted_mgp_keys = sorted(
    [key for key in avg_man.keys() if key.startswith("mGP")],
    key=lambda x: int("".join(filter(str.isdigit, x))),
)
sorted_tgp_keys = sorted(
    [key for key in avg_tec.keys() if key.startswith("tGP")],
    key=lambda x: int("".join(filter(str.isdigit, x))),
)

# Interweave the keys to create the desired order
ordered_keys = [item for pair in zip(sorted_mgp_keys, sorted_tgp_keys) for item in pair]

# Combine data into a DataFrame for plotting
avg_df_man = pd.DataFrame(
    {
        "GP": ordered_keys,
        "Average Value": [avg_man.get(gp, 0) for gp in ordered_keys],
        "Dataset": ["Ručno"] * len(ordered_keys),
    }
)

# Combine data for tec into a separate DataFrame
avg_df_tec = pd.DataFrame(
    {
        "GP": ordered_keys,
        "Average Value": [avg_tec.get(gp, 0) for gp in ordered_keys],
        "Dataset": ["Automatizirano"] * len(ordered_keys),
    }
)

# Concatenate the two DataFrames
avg_df = pd.concat([avg_df_man, avg_df_tec], ignore_index=True)

# Set the width of the bars
bar_width = 0.35  # Reduce bar width for spacing

# Set the figure size for a moderately wide plot
plt.figure(figsize=(14, 8))

# Use Seaborn to create a bar chart with a colorblind-friendly palette
sns.barplot(
    x="GP",
    y="Average Value",
    hue="Dataset",
    data=avg_df,
    palette="colorblind",
    dodge=False,
)

# Set plot labels and title
plt.xlabel("Glikanski vrh")
plt.ylabel("Prosječna vrijednost relativnog udjela")

# Calculate the positions for the x-ticks
tick_positions = np.arange(len(ordered_keys)) + bar_width / 2

# Override x-axis ticks with larger ticks for "P"
xtick_labels = [
    "P" + str(int(gp[3:])) if i % 2 == 0 else "" for i, gp in enumerate(ordered_keys)
]
# Calculate the positions for the x-ticks with a small offset
tick_positions = np.arange(len(ordered_keys)) + bar_width + 0.1

# Override x-axis ticks with larger ticks for "P"
plt.xticks(tick_positions, xtick_labels)

# Calculate standard deviations for man and tec
std_df_man = pd.DataFrame(
    {
        "GP": ordered_keys,
        "Standard Deviation": [std_man.get(gp, 0) for gp in ordered_keys],
        "Dataset": ["Ručno"] * len(ordered_keys),
    }
)

std_df_tec = pd.DataFrame(
    {
        "GP": ordered_keys,
        "Standard Deviation": [std_tec.get(gp, 0) for gp in ordered_keys],
        "Dataset": ["Automatizirano"] * len(ordered_keys),
    }
)

# Concatenate the two standard deviation DataFrames
std_df = pd.concat([std_df_man, std_df_tec], ignore_index=True)

# Add the "Standard Deviation" column to avg_df
avg_df["Standard Deviation"] = std_df["Standard Deviation"]

# Generate x-values for error bars
x_values1 = np.arange(len(std_df_man))
x_values2 = np.arange(len(std_df_tec))

# Add error bars for man dataset
plt.errorbar(
    x=x_values1,
    y=avg_df[avg_df["Dataset"] == "Ručno"]["Average Value"],
    yerr=avg_df[avg_df["Dataset"] == "Ručno"]["Standard Deviation"],
    fmt="none",
    color="black",
    capsize=1,
    linewidth=1,
)

# Add error bars for tec dataset
plt.errorbar(
    x=x_values2,
    y=avg_df[avg_df["Dataset"] == "Automatizirano"]["Average Value"],
    yerr=avg_df[avg_df["Dataset"] == "Automatizirano"]["Standard Deviation"],
    fmt="none",
    color="black",
    capsize=0.8,
    linewidth=0.6,
)

# Change the legend title
plt.legend(title="Rezultati")

# Save the plot as a PDF file
plt.savefig("plot.pdf", format="pdf", dpi=500)
plt.show()
