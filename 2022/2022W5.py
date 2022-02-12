# Prepping Data 2022 Week 5

import pandas as pd

data=pd.read_csv('data/PD 2022 Wk 5 Input.csv')

data=data.melt(id_vars=['Student ID'],value_name='Score',var_name='Subject')
#Divide the students grades into 6 evenly distributed groups 
#By evenly distributed, it means the same number of students gain each grade within a subject
data=data.sort_values(['Subject','Score','Student ID'],ascending=[True,False,True]).reset_index()

data['Dummy']=data.index
#The top scoring group should get an A, second group B etc through to the sixth group who receive an F
#An A is worth 10 points for their high school application, B gets 8, C gets 6, D gets 4, E gets 2 and F gets 1.
grade_pt={'A':10,'B':8,'C':6,'D':4,'E':2,'F':1}

data['Grade']=data.groupby(['Subject'])['Dummy'].transform(lambda x:pd.qcut(x,len(grade_pt),labels=list(grade_pt.keys())))

data['Points']=data['Grade'].map(grade_pt).astype('int')

data['Total Points per Student']=data.groupby('Student ID')['Points'].transform('sum')

#Work out the average total points per student by grade 
#ie for all the students who got an A, how many points did they get across all their subjects

data['Avg student total points per grade']=data.groupby(['Grade'])['Total Points per Student'].transform('mean')

#Take the average total score you get for students who have received at least one A and remove anyone who scored less than this. 

data['Student Total Score']=data.groupby(['Student ID'])['Score'].transform('sum')

data['Avg Total Score with one A']=data[data['Grade']=='A'][['Student ID','Student Total Score']].drop_duplicates()['Student Total Score'].mean()

data=data[(data['Student Total Score'] >= data['Avg Total Score with one A']) & (data['Grade']!='A')].copy()