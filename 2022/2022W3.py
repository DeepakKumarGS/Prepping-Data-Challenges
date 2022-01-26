# Prepping Data 2022 Week 3

import pandas as pd
import numpy as np

data=pd.read_csv('data/PD 2022 Wk 1 Input - Input.csv')
grade=pd.read_csv('data/PD 2022 WK 3 Grades.csv')
#Join the data sets together to give us the grades per student
df=pd.merge(data,grade,left_on='id',right_on='Student ID',how='inner')

#Remove the parental data fields, they aren't needed for the challenge this week

df.drop(['Parental Contact Name_1','Parental Contact Name_2','Parental Contact','Preferred Contact Employer','id'],axis=1,inplace=True)

#Pivot the data to create one row of data per student and subject
#Rename the pivoted fields to Subject and Score 
df=pd.melt(df,id_vars=['pupil first name','pupil last name','gender','Date of Birth','Student ID'],value_name='Score',var_name='Subject')

#Create an average score per student based on all of their grades
#Round the average score per student to one decimal place
df["Student's Avg Score"]=np.round(df.groupby('Student ID',as_index=False)['Score'].transform('mean'),1)

#Create a field that records whether the student passed each subject
df['pass or fail']=np.where(df['Score']>75,1,0)
#Aggregate the data per student to count how many subjects each student passed
df['Passed Subjects']=df.groupby(['Student ID'])['pass or fail'].transform('sum')
#Remove any unnecessary fields and output the data
final=df[['Passed Subjects',"Student's Avg Score",'Student ID','gender']].drop_duplicates()

final.to_csv('output/PD 2022 W3 Output.csv',index=False)



