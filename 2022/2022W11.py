# Prepping Data 2022 Week 11 

import pandas as pd

data=pd.read_csv('data/PD 2022 Wk 11 Fill the Blanks challenge.csv')

data[['Lesson Name','Subject']]=data.groupby(['Weekday','Teacher','Lesson Time'])[['Lesson Name','Subject']].transform('first')

data['Avg. Attendance per Subject & Lesson']=data.groupby(['Subject','Lesson Name'])['Attendance'].transform('mean')

