#this script will compile all event reports and produce a graph for gender (using prefixes) 
import os
import glob
import pandas as pd
from matplotlib import pyplot as plt

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

#get only those datasets where we collected prefix info
prefixes = combined_csv[['Order Date', 'Prefix']]
prefixes = prefixes[['Prefix']].fillna(value='Unknown')


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

#create a dataframe where we combine all Ms/Miss/Mrs and Dr/Rev/Prof/Mx as "other"
females = all_prefixes.iloc[['1', '4', '5']].sum()
males = all_prefixes.iloc[['0']].sum()
other = all_prefixes.iloc[['2', '3', '6', '7', '8']].sum()
#create a new dataframe with the sums
gender = pd.concat([females, males, other], axis =1).T

#change the name of the rows 
gender.at[0,'answer']='Female'
gender.at[1, 'answer'] = 'Male'
gender.at[2, 'answer'] = 'Unknown'

#gender.to_csv('all_events_gender.csv', index=False)

#create a pie chart
fig = plt.figure(figsize = [6,6])
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])    
patches, texts, pcts = ax.pie(gender['percent'], autopct='%1.0f%%', pctdistance=1.1)
plt.legend(gender['answer'], bbox_to_anchor=(1,0.15), loc="center right", fontsize=14, 
         bbox_transform=plt.gcf().transFigure)
plt.setp(pcts, fontweight='bold')
plt.title('All HirePhD. Events (except events 8, 9, 10)')
plt.show()
fig.savefig('all_events_gender.png', format='png', dpi=300, bbox_inches="tight")


