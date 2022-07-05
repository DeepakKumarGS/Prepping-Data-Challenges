# Prepping Data 2022 Week 18

import pandas as pd
import re

data=pd.read_csv('data/PD 2022 W18 Input.csv')

data=data.melt(id_vars='Region',value_name='Metric',var_name='col_name')

data['Bike Type']=data['col_name'].apply(lambda x:re.search('(^[^_]+)(?=_+)',x).group(1))

data['Metric_Name']=data['col_name'].apply(lambda x:re.search('(\d+)_+(\w+$)',x).group(2))

data['Date']=data['col_name'].apply(lambda x:re.search('(^[^_]+)(?=_+)_+([A-Za-z]{3}_\d+)',x).group(2))

data['Date']=pd.to_datetime('01_'+data['Date'],format='%d_%b_%y')

data.drop('col_name',inplace=True,axis=1)

final=data.pivot_table(index=['Region','Bike Type','Date'],values='Metric',columns='Metric_Name',aggfunc='first').reset_index().rename_axis(None,axis=1)

