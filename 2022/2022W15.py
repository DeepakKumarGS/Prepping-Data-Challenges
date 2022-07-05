# Prepping Data 2022 Week 15

import pandas as pd
import numpy as np

contracts=pd.read_excel('data/PD 2022 Wk 15 Rental Contracts.xlsx')
office_space=pd.read_excel('data/PD 2022 Wk 15 Office Space Prices.xlsx')

contracts['Contract Start']=pd.to_datetime(contracts['Contract Start'],format='%Y-%m-%d')
contracts['Contract End']=pd.to_datetime(contracts['Contract End'],format='%Y-%m-%d')

contracts['Contract Length']=round((contracts['Contract End']-contracts['Contract Start'])/np.timedelta64(1,'M'),0)

contracts['Today']=pd.to_datetime('2022-04-13',format='%Y-%m-%d')

contracts['Months Until Expiry']=round((contracts['Contract End']-contracts['Today'])/np.timedelta64(1,'M'),0)

rental_data=pd.merge(contracts,office_space,on=['City','Office Size'],how='inner')

rental_data['Month Divider']=[pd.date_range(s,e,freq='MS') for s,e in zip(rental_data['Contract Start'],rental_data['Contract End'])]

rental_data=rental_data.explode('Month Divider')

rental_data['Cumulative Monthly Cost']=rental_data.groupby(['ID','Company'],as_index=False)['Rent per Month'].cumsum()

output1=rental_data.drop(['Today'],axis=1)

rental_data['Year']=rental_data['Month Divider'].dt.year

rental_data['Flag']=np.where(rental_data['Month Divider']<rental_data['Today'],'EoY and Current','Lesser')


output2=pd.pivot_table(rental_data,index='Year',columns='Flag',values='Rent per Month',aggfunc='sum').reset_index().rename_axis(None,axis='columns').drop('Lesser',axis=1)

