#this script will compile all event reports and produce a graph for gender (using prefixes) 
import os
import glob
import pandas as pd
os.chdir("C:\Users\Kuma\Documents\Python\HirePhD\demographics")
from matplotlib import pyplot as plt



extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

#get only those datasets where we collected prefix info
prefixes = combined_csv[~combined_csv['Prefix'].isna()]
prefixes['Order Date'].max()
prefixes['Order Date'].min()
prefixes.info()
prefixes[['Order Date', 'Prefix']]


def convert_percent(report, column):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the percentages of each answer.
    The function will return a pandas dataframe.
    """
    df = report[column].value_counts(normalize = True) 
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'percent']
    df['percent'] = df['percent']*100
    #df.sort_values('answer')
    return df


all_prefixes = convert_percent(prefixes, 'Prefix')
all_prefixes

fig = plt.figure(figsize = [6,10])
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])    
patches, texts, pcts = ax.pie(df['percent'], autopct='%1.0f%%', pctdistance=1.2)
plt.legend(df['answer'], bbox_to_anchor=(1,0.15), loc="center right", fontsize=10, 
         bbox_transform=plt.gcf().transFigure)
plt.setp(pcts, fontweight='bold')
#plt.show()
fig.savefig(name, format='png', dpi=300, bbox_inches="tight")


