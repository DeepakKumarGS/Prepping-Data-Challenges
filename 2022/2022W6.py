# Prepping Data Week 6 2022
## This script is a copy of the solution posted by Arsene Xie (https://twitter.com/ArseneXie/status/1493878139701043200/photo/1)
## For learning the approach and process, the script was reproduced by me.

import pandas as pd
import re
import numpy as np
# Input the data:
data=pd.read_excel('data/PD 2021 Wk 6 7 letter words.xlsx',sheet_name='Scrabble Scores')

words=pd.read_excel('data/PD 2021 Wk 6 7 letter words.xlsx',sheet_name='7 letter words')
#Parse out the information in the Scrabble Scores Input so that there are 3 fields:
#Tile
#Frequency
#Points
data['Points']=data['Scrabble'].apply(lambda x:int(re.search('^(\d+)',x).group(1)))

data['TileFrequency']=data['Scrabble'].str.extract('(?<=:\s)(.*)')

data=pd.concat([data['Points'],
            pd.DataFrame([map(str.strip,x) for x in data['TileFrequency'].str.split(',').values.tolist()])],
            axis=1,sort=False)

data=data.melt(id_vars='Points',value_name='TileFrequency',var_name='ToDrop').dropna().drop('ToDrop',axis=1)

data['Tile']=data['TileFrequency'].apply(lambda x:re.search('^(\w)',x).group(1))

data['Frequency']=data['TileFrequency'].apply(lambda x:float(re.search('(\d+)$',x).group(1)))

data['LN Chance']=np.log(data['Frequency']/data['Frequency'].sum())

#Split each of the 7 letter words into individual letters and count the number of occurrences of each letter
words=pd.concat([words,
                pd.DataFrame([map(str.upper,x) for x in words['7 letter word'].str.split('').values.tolist()])],
                axis=1,sort=False)

words=words.melt(id_vars='7 letter word',value_name='Letter',var_name='ToDrop').drop('ToDrop',axis=1).replace('',np.NaN).dropna()

words['LetterCount'] = words['Letter'].groupby([words['7 letter word'],words['Letter']]).transform('count')

#Join each letter to its scrabble tile 
final=pd.merge(words,data,left_on='Letter',right_on='Tile')

final=final[final['Frequency']>=final['Letter Count']]

final['Match Letter']=final['Letter'].groupby(final['7 letter word']).transform('count')

final=final[final['Match Letter']==7]

final=final.groupby('7 letter word',as_index=False).agg({'Points':'sum','LN Chance':'sum'}).rename(columns={'Points':'Total Points'})

final['% Chance']=np.exp(final['LN Chance'])

final['Likelihood Rank']=np.round(final['% Chance'],15).rank(method='dense',ascending=False).astype(int)

final['Points Rank']=final['Total Points'].rank(method='dense',ascending=False).astype(int)









