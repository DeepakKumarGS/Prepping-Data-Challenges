# Prepping Data 2022 Week 7 

import pandas as pd
import re

#Input the data
people=pd.read_excel('data/PD 2022 Wk 7 PeopleData.xlsx',sheet_name='People')
leaders=pd.read_excel('data/PD 2022 Wk 7 PeopleData.xlsx',sheet_name='Leaders')
location=pd.read_excel('data/PD 2022 Wk 7 PeopleData.xlsx',sheet_name='Location')
dates=pd.read_excel('data/PD 2022 Wk 7 PeopleData.xlsx',sheet_name='Date Dim')
goal=pd.read_excel('data/PD 2022 Wk 7 PeopleData.xlsx',sheet_name='Goals')

metric=pd.ExcelFile('data/PD 2022 Wk 7 MetricData2021.xlsx')
#Join the People, Location, and Leader data sets together


data=people.merge(leaders,left_on='Leader 1',right_on='id',how='inner')

data=data.merge(location,how='inner')

data['Agent Name']=data['last_name_x']+','+data['first_name_x']

data['Leader Name']=data['last_name_y']+','+data['first_name_y']

data.drop(['first_name_x','last_name_x',
            'Leader 1','Location ID',
            'id_y','first_name_y','last_name_y'],axis=1,inplace=True)

data.rename(columns={'id_x':'id'},inplace=True)

#union the worksheets in the input step
#merge the mismatched fields
#create a month start date
#remove the table names and file paths field
#join the data with the people - remember we need to show every agent for every month

df=[]
rename_cols={'Not Answered':'Calls Not Answered','Answered':'Calls Answered','AgentID':'id','Offered':'Calls Offered'}
for s in metric.sheet_names:
    sf=pd.read_excel(metric,sheet_name=s).rename(columns=rename_cols)
    sf.insert(0,'Month Start Date',pd.to_datetime(f'2021-{s}-01',format='%Y-%b-%d'))
    df.append(sf)

metric_df=pd.concat(df)

metric_df['Month Start Date']=metric_df['Month Start Date'].dt.date

#Limit the dates to just 2021 and join those to the People, Location, Leader step

dates=dates.loc[dates['Month Start Date']<'2022-01-01']
dates['Month Start Date']=dates['Month Start Date'].dt.date

data=data.merge(dates,how='cross')

data=data.merge(metric_df,on=['id','Month Start Date'],how='left')

#add the goals input to the flow
#clean the goal data to have the goal name & numeric value
#add the goals to the combined people & data step
#be sure that you aren't increasing the row count - the goals should be additional columns

goal=goal['Goals'].tolist()

for g in goal:
    data[g]=int(re.search('(\d+)$',g).group(1))

#create a calculation for the percent of offered that weren't answered (for each agent, each month)

data['Not Answered Rate']=round(data['Calls Not Answered']/data['Calls Offered'],3)

#create a calculation for the average duration by agent (for each agent, each month)

data['Agent Avg Duration']=round(data['Total Duration']/data['Calls Answered'])

data['Met Not Answered Rate']=(data['Not Answered Rate']*100 < data['Not Answered Percent < 5'])

data['Met Sentiment Goal']=(data['Sentiment'] >= data['Sentiment Score >= 0'])













