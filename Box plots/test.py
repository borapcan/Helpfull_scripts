import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import median


data = pd.read_excel(r'C:/Users/vajma/Desktop/Julija_plotovi/Box_plots/igg_box_plot_data.xlsx')

sns.set(style='whitegrid')

g=sns.boxplot(data=data, width=0.3)

plt.title('IgG derived traits box-plot', fontsize=28, y=1.08
)
plt.ylabel( 'Abundance of glycan traits (%)', fontsize=20)
plt.ylim(0,100)

xvalues = ["G0","G1","G2","S","B","F"] 
plt.xticks(np.arange(6), xvalues)

sns.despine(top=True,
            right=True,
            left=True,
            bottom=False)

# Text G0
mean = round(median(data['G0']),1)
sd = round(data['G0'].std(),1)
textstr = "$\~ {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(-0.2, 1.1, textstr, fontsize=12, bbox=props)


# Text p1
mean = round(median(data['G1']),1)
sd = round(data['G1'].std(),1)
textstr = "$\~ {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(0.81, 1.1, textstr, fontsize=12, bbox=props)

# Text p1
mean = round(median(data['G2']),1)
sd = round(data['G2'].std(),1)
textstr = "$\~  {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(1.81, 1.1, textstr, fontsize=12, bbox=props)

# Text p1
mean = round(median(data['S']),1)
sd = round(data['S'].std(),1)
textstr = "$\~  {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(2.81, 1.1, textstr, fontsize=12, bbox=props)


# Text p1
mean = round(median(data['B']),1)
sd = round(data['B'].std(),1)
textstr = "$\~ {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(3.81, 1.1, textstr, fontsize=12, bbox=props)


# Text p1
mean = round(median(data['F']),1)
sd = round(data['F'].std(),1)
textstr = "$\~ {x}$" + f" = {mean} \ns = {sd}"
props = dict(boxstyle='round', facecolor='plum', alpha=0.2)
g.text(4.81, 1.1, textstr, fontsize=12, bbox=props)


plt.tight_layout()
plt.show()
g.figure.savefig("output.png")