import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import math
from scipy.stats import linregress

# read Excel file into pandas DataFrame
df = pd.read_excel("10.xlsx")

date_range = pd.date_range(start="2012-01-01", end="2022-12-31", freq="23D")

df[["G0 total", "G1 total", "G2 total", "S total", "B total", "F total"]] = df[
    ["G0 total", "G1 total", "G2 total", "S total", "B total", "F total"]
].astype(float)
# assign the date range to the 'Date' column in df
df["Date"] = date_range

# convert Time column to numeric format, for regplot
df["Date_Num"] = mdates.date2num(df["Date"])

# create a figure with 2 rows and 3 columns of subplots
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))

# create a list of tuples, each containing a column name, the corresponding subplot index, and color
plots = [
    ("G0 total", (0, 0), "blue"),
    ("G1 total", (0, 1), "green"),
    ("G2 total", (0, 2), "red"),
    ("S total", (1, 0), "orange"),
    ("B total", (1, 1), "purple"),
    ("F total", (1, 2), "brown"),
]

# set the x-axis limits based on the min and max values of the Time column
min_time = df["Date"].min()
max_time = df["Date"].max()

# set the x-tick locations to be every other year between 2012 and 2022
xtick_locs = pd.date_range(start="2012-01-01", end="2022-12-31", freq="2AS")

# create a dictionary to store line formulas
line_formulas = {}

# iterate over the list of plots and create a lineplot with a trendline on each subplot
for column, subplot_index, color in plots:
    ax = axs[subplot_index[0], subplot_index[1]]

    # normalization by first point
    first_point = df[column].iloc[0]
    df[column] = df[column] / first_point

    sns.lineplot(data=df, x="Date", y=column, ax=ax, marker="o", color=color)

    # Fit a linear regression model
    x = df["Date_Num"]
    y = df[column]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Store the line formula in the dictionary with more decimal places
    line_formulas[column] = (
        f"{column} line formula: y = {slope:.6f} * x + {intercept:.6f}"
    )

    # Plot the regression line
    ax.plot(x, slope * x + intercept, color="black")

    ax.set_xlabel("")  # remove x-label
    ax.set_ylabel("")  # remove y-label
    ax.set_title(column)  # reinstating subplot title
    ax.set_xlim(min_time, max_time)
    ax.set_xticks(xtick_locs)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylim(
        math.floor(df[column].min() * 2) / 2, math.ceil(df[column].max() * 2) / 2
    )

# Add the global x-axis label below the bottom middle subplot

fig.text(0.5, 0.04, "Time point (date)", ha="center", fontsize=12)

# Add the global y-axis label to the left side of the subplot grid

fig.text(
    0.1,
    0.5,
    "Normalized value",
    ha="center",
    va="center",
    rotation="vertical",
    fontsize=16,
)


# save the figure
plt.savefig("Derived_traits_over_Time_10_norm.pdf", format="pdf")

# export line formulas to a text file
with open("time_eff_5.txt", "w") as f:
    for formula in line_formulas.values():
        f.write(f"{formula}\n")
plt.show()
