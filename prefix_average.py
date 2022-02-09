#this script will compile all event reports and produce a graph for gender (using prefixes) 
import os
import glob
import pandas as pd
from matplotlib import pyplot as plt

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#loop through each csv file to create a separate dataframe 
all_csvs = []
for filename in all_filenames:
    df_raw = pd.read_csv(filename)
    df = df_raw[['Order Date', 'Prefix']]
    df['filename'] = filename
    prefixes = df[['Prefix', 'Order Date', 'filename']].fillna(value='Unknown')
    all_csvs.append(prefixes)


all_csvs = pd.concat(all_csvs)

all_prefix = all_csvs[['Prefix', 'filename']]

#change all Ms/Miss/Mrs to 'female' and all Mrs to 'male' and the rest to "Unknown"
all_gender = all_prefix.replace({'Prefix' : { 'Mr.' : 'Male', 'Ms.' : 'Female', 'Miss' : 'Female', 'Mrs.' : 'Female', 'Dr.' : 'Unknown','Rev.' : 'Unknown','Prof.' : 'Unknown' ,'Mx.' : 'Unknown'   }})

#Get the count of each prefix for each event
avg = all_gender.groupby(['filename', 'Prefix'], as_index=False).size()
#add new column for sum of all prefixes per event
avg['sum']=avg.groupby(['filename'])['size'].transform('sum')
#calculate the percentage per prefix for each event
avg['percentage'] = avg['size']/avg['sum']*100
#create a new column for event number
avg['event'] = avg['filename'].map(lambda x: x.rstrip('_report.csv'))

#prepare dataframe for creating chart
df_avg = avg[['event', 'Prefix', 'percentage']]
df_avg = df_avg.pivot(index = 'event', columns = 'Prefix', values = 'percentage')
df_avg = df_avg.reset_index()
df_avg['event'] = df_avg.event.astype(int)
df_avg = df_avg.sort_values(by=['event'])
df_avg = df_avg.set_index('event')

#df_avg.to_csv('gender_per_event.csv', index = True)

#create a stacked bar chart 
fig = df_avg.plot(kind='bar', stacked=True, figsize = (8,6)).legend(bbox_to_anchor=(1, 0.5))
plt.show()
fig.figure.savefig('gender_per_event.png', format='png', dpi=300, bbox_inches="tight")

   


