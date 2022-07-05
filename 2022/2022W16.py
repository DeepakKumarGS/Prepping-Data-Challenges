# Prepping Data 2022 Week 16

import pandas as pd

orders=pd.read_excel('data/PD 2022 Wk 16 Menu Input.xlsx',sheet_name='Orders')

lookup=pd.read_excel('data/PD 2022 Wk 16 Menu Input.xlsx',sheet_name='Lookup Table')


ord_cols=orders.columns

order_mapping={i:j for i,j in zip(ord_cols[:-1],ord_cols[1:]) if i[0:7]!='Unnamed'}

team=['Carl','Tom','Jenny','Jonathan']

orders['Course']=orders['Carl'].apply(lambda x:x if x in ['Starters','Mains','Dessert'] else None).ffill()

for t in team:
    orders[t]=orders.apply(lambda x:x[t] if pd.notna(x[order_mapping[t]]) else None,axis=1)

data=orders[['Course']+team].melt(id_vars='Course',value_name='Dish',var_name='Guest').dropna()

final=data.merge(lookup,on='Dish')[['Course','Guest','Recipe ID','Dish']]

final=final.sort_values(['Guest','Course'],ascending=[True,False])

