# Prepping Data 2022 W17

import pandas as pd
import re

streaming=pd.read_excel('data/PD 2022W17 Input.xlsx',sheet_name='Streaming')
pricing=pd.read_excel('data/PD 2022W17 Input.xlsx',sheet_name='Avg Pricing')


pricing.rename(columns={'Content_Type':'content_type'},inplace=True)

#Check the location field for spelling errors
location_dict={'Edinurgh':'Edinburgh'}

streaming['location']=streaming['location'].map(location_dict).fillna(streaming['location'])

#Fix the date fields so they are recognised as date data types

streaming.rename(columns={'t':'timestamp'},inplace=True)

streaming['timestamp']=pd.to_datetime(streaming['timestamp'])

#We need to update the content_type field:
#For London, Cardiff and Edinburgh, the content_type is defined as "Primary"
#For other locations, maintain the "Preserved" content_type and update all others to have a "Secondary" content_type

streaming['content_type']=streaming.apply(lambda x:'Primary' if re.search('(London|Cardiff|Edinburgh)',x['location']) 
                                            else 'Secondary' if pd.isna(x['content_type']) else x['content_type'],axis=1)

#Aggregate the data to find the total duration of each streaming session (as identified by the timestamp)

streaming=streaming.groupby(['userID','timestamp','location','content_type'],as_index=False).agg({'duration':'sum'})

#To join to the Avg Pricing Table, we need to work out when each user's first streaming session was. However, it's a little more complex than that. 
#For "Primary" content, we take the overall minimum streaming month, ignoring location
#For all other content, we work out the minimum active month for each user, in each location and for each content_type


streaming['dummy_loc']=streaming.apply(lambda x:'dummy' if x['content_type']=='Primary' else x['location'],axis=1)


streaming['min_timestamp']=streaming['timestamp'].groupby([streaming['userID'],streaming['content_type'],streaming['dummy_loc']]).transform('min')

streaming['Month']=streaming['min_timestamp'].apply(lambda x:x.strftime('%m %Y'))

final=pd.merge(streaming,pricing,on=['Month','content_type'],how='left')
#For "Preserved" content, we manually input the Avg Price as £14.98
final['Avg_Price']=final.apply(lambda x:14.98 if x['content_type']=='Preserved' else x['Avg_Price'],axis=1)

