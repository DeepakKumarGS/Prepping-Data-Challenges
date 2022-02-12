# Prepping Data 2022 Week 4 

import pandas as pd
import numpy as np


data=pd.read_csv('data/PD 2022 Wk 1 Input - Input.csv')
travel=pd.read_excel('data/PD 2021 WK 1 to 4 ideas - Preferences of Travel.xlsx')

data.rename(columns={'id':'Student ID'},inplace=True)
#Join the data sets together based on their common field
data=pd.merge(data,travel,how='inner',on='Student ID')
#Change the weekdays from separate columns to one column of weekdays and one of the pupil's travel choice
data=pd.melt(data,id_vars=['Student ID', 'pupil first name', 'pupil last name', 'gender',
       'Date of Birth', 'Parental Contact Name_1', 'Parental Contact Name_2',
       'Preferred Contact Employer', 'Parental Contact'],var_name='Weekday',value_name='Method of Travel')
#Group the travel choices together to remove spelling mistakes
replace_dict={'Bycycle':'Bicycle',
               'Scoter':'Scooter',
               'Scootr':'Scooter',
               'Helicopeter':'Helicopter',
                'Carr':'Car',
                'Walkk':'Walk',
                'Wallk':'Walk',
                'Waalk':'Walk',
                'WAlk':'Walk'}

data['Method of Travel']=data['Method of Travel'].map(replace_dict).fillna(data['Method of Travel'])
#Total up the number of pupil's travelling by each method of travel 
data=data.groupby(['Weekday','Method of Travel'],as_index=False).agg({'Student ID':'count'})

data.rename(columns={'Student ID':'Number of Trips'},inplace=True)

data['Trips per Day']=data['Number of Trips'].groupby(data['Weekday']).transform('sum')

#Work out the % of trips taken by each method of travel each day
#Round to 2 decimal places
data['% of trips per day']=np.round(data['Number of Trips']/data['Trips per Day'],2)

#reate a Sustainable (non-motorised) vs Non-Sustainable (motorised) data field 
sustainable=['Walk',
"Mum's Shoulders",
'Bicycle',
'Scooter',
"Dad's Shoulders",
'Hopped',
'Skipped',
'Jumped']

data['Sustainable?']=data['Method of Travel'].apply(lambda x:'Sustainable' if x in sustainable else 'Non-Sustainable' )

data=data[['Weekday', 'Method of Travel', 'Number of Trips', 'Trips per Day',
        '% of trips per day', 'Sustainable?']]

