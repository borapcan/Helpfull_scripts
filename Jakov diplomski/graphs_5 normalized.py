import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import math

# read Excel file into pandas DataFrame
df = pd.read_excel('5.xlsx')
df[['G0 total', 'G1 total', 'G2 total', 'S total', 'B total', 'F total']] = df[
    ['G0 total', 'G1 total', 'G2 total', 'S total', 'B total', 'F total']].astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# convert Date column to numeric format, for regplot
df['Date_Num'] = mdates.date2num(df['Date'])

# normalize data by first time point
df_norm = df.copy()
for column in ['G0 total', 'G1 total', 'G2 total', 'S total', 'B total', 'F total']:
    first_val = df_norm.at[0, column]
    df_norm[column] = df_norm[column] / first_val

# create a figure with 2 rows and 3 columns of subplots
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))

# create a list of tuples, each containing a column name, the corresponding subplot index, and color
plots = [('G0 total', (0, 0), 'blue'), ('G1 total', (0, 1), 'green'), ('G2 total', (0, 2), 'red'),
         ('S total', (1, 0), 'orange'), ('B total', (1, 1), 'purple'), ('F total', (1, 2), 'brown')]

# set the x-axis limits based on the min and max values of the Date column
min_date = df['Date'].min()
max_date = df['Date'].max()

# set the x-tick locations to be every other year
xtick_locs = pd.date_range(start=min_date, end=max_date, freq='2AS')

# iterate over the list of plots and create a lineplot with a trendline on each subplot
for column, subplot_index, color in plots:
    ax = axs[subplot_index[0], subplot_index[1]]
    sns.lineplot(data=df_norm, x='Date', y=column, ax=ax, marker='o', color=color)
    sns.regplot(data=df_norm, x='Date_Num', y=column, ax=ax, scatter=False, line_kws={'color': 'black'})
    ax.set_title(column)
    ax.set_xlabel('Date')
    ax.set_ylabel(column + " (normalized to first point)")
    ax.set_xlim(min_date, max_date)
    ax.set_xticks(xtick_locs)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylim(0.8, math.ceil(df_norm[column].max() * 2) / 2)

# adjust the spacing between subplots and title
plt.subplots_adjust(top=0.9)

# add a bit of extra space at the top for the title
fig.tight_layout(rect=[0, 0, 1, 0.95])

fig.suptitle('Total over time')

# save the figure
plt.savefig("Derived_traits_over_Time_5_normalized.pdf", format='pdf')
