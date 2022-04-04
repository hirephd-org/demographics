# this script will create a master dataframe of all events to date and look for ubc postdoc attendee trends
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

#concatenate all raw csv files
path = r'C:\Users\Kuma\Documents\Python\HirePhD\event_reports' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
for filename in all_files:
    files = pd.read_csv(filename, index_col=None, header=0)
    files['filename'] = filename
    li.append(files)
df_raw = pd.concat(li, axis=0, ignore_index=True)

#change filename to only the event_id by extracting the number from the filenames
df_raw['event_id'] = df_raw['filename'].str.extract('(\d+)', expand=False)

#create a subset to work with
df = df_raw[['First Name', 'Last Name', 'Job Title', 'Company', 'event_id']]
#filter rows for UBC students
df_ubc = df.loc[df['Company'].isin(['UBC', 'University of British Columbia', 'UBC Graduate Student Society']) ]
#df_ubc['Job Title'].unique()
#filter rows for postdocs
df_ubcpd = df_ubc.loc[df_ubc['Job Title'].isin(['Postdoc', 'Postdoctoral Researcher', 'Postdoctoral Research Fellow', 'Postdoc ', 'Postdoctoral Fellow'])]

#read in events data master to get event dates
master = pd.read_csv(r'C:\Users\Kuma\Documents\Python\HirePhD\demographics\Events_data_master - Sheet1.csv')
dates = master[['event_id', 'date']]
#change dtype of the 'event_id' column to str
dates['event_id']=dates['event_id'].astype('str')
df_ubcpd['event_id'] = df_ubcpd['event_id'].astype('str')

#join the 'dates' dataframe with 'df_ubcpd' dataframe
full = df_ubcpd.merge(dates, on= 'event_id', how = 'left')
full = full.drop_duplicates()

count = full['date'].value_counts().rename_axis('date').reset_index(name = 'counts')
count['date']= pd.to_datetime(count['date'])
count = count.sort_values(by = 'date')


#plot simple lineplot
plt.plot(count['date'], count['counts'])
plt.title('UBC Postdoc Attendance')
plt.xlabel('Date')
plt.ylabel('Tickets sold')
plt.xticks(rotation = 50)
y_ticks = np.arange(0, 5, 1)
plt.yticks(y_ticks)
plt.tight_layout()
#plt.show()\
plt.savefig('ubc_postdoc.png')