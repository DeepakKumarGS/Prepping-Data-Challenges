# Prepping Data 2022 Week 13 

import pandas as pd

data=pd.read_csv('data/PD 2022 Wk 13 Pareto Input.csv')

#Aggregate the data to the total sales for each customer

data=data.groupby(['Customer ID','First Name','Surname'])['Sales'].sum().reset_index()

#Calculate the percent of total sales each customer represents

data['% of Total']=data['Sales']/data['Sales'].sum()*100

#Calculate the running total of sales across customers
#Order by the percent of total in a descending order
#Round to 2 decimal places

data['Running % Total Sales']=round(data.sort_values('Sales',ascending=False)['% of Total'].cumsum(),2)

data['Total Customers']=data['Customer ID'].nunique()

def pareto_perc(df,perc):
    pareto_details=df.loc[df['Running % Total Sales']<=perc].sort_values('Sales',ascending=False).copy()
    
    pareto_words=pd.DataFrame([f'{round(pareto_details.shape[0]/df.shape[0]*100,2)}% of customers account for {perc}% of sales'],columns=['outcomes'])

    return pareto_details,pareto_words
#Create a parameter that will allow the user to decide the percentage of sales they wish to filter to
perc_value=80
#Output the data, including the parameter in the output name
detail,words=pareto_perc(data,perc_value)