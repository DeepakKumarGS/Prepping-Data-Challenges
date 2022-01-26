# Prepping Data Week 2

import pandas as pd
import re
data=pd.read_csv('data/PD 2022 Wk 1 Input - Input.csv')

# Remove unnecessary fields,
data.drop(['id','gender','Parental Contact Name_1','Parental Contact Name_2','Preferred Contact Employer','Parental Contact'],axis=1,inplace=True)
#Format the pupil's name in First Name Last Name format
data['Pupil Name']=data['pupil first name']+" "+data['pupil last name']

data['Date of Birth']=pd.to_datetime(data['Date of Birth'],format='%m/%d/%Y')
#Create the date for the pupil's birthday in calendar year 2022 
data["This Year's Birthday"]=data['Date of Birth'].apply(lambda x:x.replace(year=2022))

#Work out what day of the week the pupil's birthday falls on
#Remember if the birthday falls on a Saturday or Sunday, we need to change the weekday to Friday
data['Cake Needed On']=data['Date of Birth'].dt.day_name()

data['Cake Needed On']=data['Cake Needed On'].apply(lambda x:'Friday' if x in ('Saturday','Sunday') else x )

#Work out what month the pupil's birthday falls within
data['Month']=data['Date of Birth'].dt.month_name()

#Count how many birthdays there are on each weekday in each month
data['BD per Weekday and Month']=data.groupby(['Month','Cake Needed On'])['Pupil Name'].transform('count')

final=data[['Date of Birth', 'Pupil Name',
       "This Year's Birthday", 'Month', 'Cake Needed On',
       'BD per Weekday and Month']]
