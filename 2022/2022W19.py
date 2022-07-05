# Prepping Data 2022 Week 19

import pandas as pd


product_set=pd.read_excel('data/PD 2022 Wk 19 Input.xlsx',sheet_name='Product Set')
sales=pd.read_excel('data/PD 2022 Wk 19 Input.xlsx',sheet_name='Sales')
size_table=pd.read_excel('data/PD 2022 Wk 19 Input.xlsx',sheet_name='Size Table')

#Change the Size ID to an actual Size value in the Sales table
product_set.rename(columns={'Size':'Product Size'},inplace=True)

product_set['Product Code']=product_set['Product Code'].str.replace('S','')

size_table.rename(columns={'Size':'Sales Size'},inplace=True)

sales=sales.merge(size_table,left_on='Size',right_on='Size ID')

sales=sales.merge(product_set,left_on='Product',right_on='Product Code')

correct_sales=sales.loc[sales['Sales Size']==sales['Product Size']][['Product Size','Scent','Product','Store']]

incorrect_sales=sales.loc[~(sales['Sales Size']==sales['Product Size'])][['Product Size','Scent','Product Code','Store']]

incorrect_sales=incorrect_sales.groupby(['Product Code','Product Size','Scent'],as_index=False).agg({'Store':'count'})

incorrect_sales.rename(columns={'Store':'Number of Sales with wrong size'},inplace=True)





