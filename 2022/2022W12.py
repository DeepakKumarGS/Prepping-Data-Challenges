# Prepping Data 2022 Week 12 

import pandas as pd
import re
import os
data=[]
#Extract the Report years from the file paths
#Create a Year field based on the the first year in the Report name
for file in os.listdir('data/PD 2022 Wk 12 Inputs'):
    df=pd.read_csv(os.path.join('data/PD 2022 Wk 12 Inputs',file))
    df['Year']=re.search('(\d+)',file).group(0)
    df['Report']=re.search('(\d+ to \d+)',file).group(0)
    data.append(df)

data=pd.concat(data)

#Keep only relevant fields
data=data[['Year',
        'Report',
        'EmployerName',
        'EmployerId',
        'EmployerSize',
        'DiffMedianHourlyPercent']]

#Some companies have changed names over the years. For each EmployerId, find the most recent report they submitted and apply this EmployerName across all reports they've submitted
data['LatestYear']=data.groupby('EmployerId')['Year'].transform('max')
data['EmployerName_New']=data.apply(lambda x:x['EmployerName'] if x['Year']==x['LatestYear'] else '',axis=1)
data['EmployerName']=data.groupby('EmployerId')['EmployerName_New'].transform('max')
#Create a Pay Gap field to explain the pay gap in plain English
# In this dataset, a positive DiffMedianHourlyPercent means the women's pay is lower than the men's pay, whilst a negative value indicates the other way around
# The phrasing should be as follows:
# In this organisation, women's median hourly pay is X% higher/lower than men's.
# In this organisation, men's and women's median hourly pay is equal.

data['Pay Gap']=data['DiffMedianHourlyPercent'].apply(lambda x:"In this organisation, men's and women's median hourly pay is equal" if x==0
                                                    else f"In this organisation, women's median hourly pay is {abs(x)} {('higher' if x<0 else 'lower')} than men's.")


data=data[['Year',
        'Report',
        'EmployerName',
        'EmployerId',
        'EmployerSize',
        'DiffMedianHourlyPercent','Pay Gap']]

