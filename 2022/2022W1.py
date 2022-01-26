# Prepping Data 2020 Week 1

import pandas as pd
import numpy as np

data=pd.read_csv('data/PD 2022 Wk 1 Input - Input.csv')


data["Pupil's Name"]=data['pupil last name']+','+data['pupil first name']

data['Parental Contact Full Name']=data['pupil last name']+','+np.where(data['Parental Contact']==1,data['Parental Contact Name_1'],data['Parental Contact Name_2'])

data['Parental Contact Email Address']=np.where(data['Parental Contact']==1,data['Parental Contact Name_1'],data['Parental Contact Name_2'])+'.'+data['pupil last name']+'@'+data['Preferred Contact Employer']+'.com'

data['Date of Birth']=pd.to_datetime(data['Date of Birth'],format='%m/%d/%Y')
#https://stackoverflow.com/questions/35339139/what-values-are-valid-in-pandas-freq-tags
data=data.assign(Academic_Year=pd.PeriodIndex(data['Date of Birth'],freq='A-Aug'))

data['Academic_Year']=data['Academic_Year'].map(lambda x:int(x.strftime('%Y')))

data['Academic Year']=np.where(data['Academic_Year']>=2015,1,(2015-data['Academic_Year'])+1)

final=data[['Academic Year',"Pupil's Name","Parental Contact Full Name","Parental Contact Email Address"]]