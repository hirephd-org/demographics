# this script will create a master dataframe of all events to date and look for ubc postdoc attendee trends
import pandas as pd
import glob

#concatenate all raw csv files
path = r'C:\Users\Kuma\Documents\Python\HirePhD\event_reports' # use your path
all_files = glob.glob(path + "/*.csv")

li = []
for filename in all_files:
    files = pd.read_csv(filename, index_col=None, header=0)
    li.append(files)
df_raw = pd.concat(li, axis=0, ignore_index=True)

df_raw


df = df_raw[['First Name', 'Last Name', 'Job Title', 'Company']]

df_ubc = df.loc[df['Company'].isin(['UBC', 'University of British Columbia', 'UBC Graduate Student Society']) ]
df_ubc['Job Title'].unique()
df_ubcpd = df_ubc.loc[df_ubc['Job Title'].isin(['Postdoc', 'Postdoctoral Researcher', 'Postdoctoral Research Fellow', 'Postdoc ', 'Postdoctoral Fellow'])]
df_ubcpd