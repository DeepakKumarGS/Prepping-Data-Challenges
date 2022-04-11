# Prepping Data 2022 Week 10

## Reproduced from @arseneXie

import pandas as pd
import html
import re

data=pd.read_excel('data/PD 2022 Wk 10 Bechdel Test.xlsx',sheet_name='Webscraping')

ranking={'Fewer than two women in this movie':5,
 'There are two or more women in this movie and they talk to each other about something other than a man':1,
 'There are two or more women in this movie and they talk to each other about something other than a man, although dubious':2,
 "There are two or more women in this movie, but they don't talk to each other":4,
 'There are two or more women in this movie, but they only talk to each other about a man':3}

data['Movies']=data['DownloadData'].apply(lambda x:html.unescape(re.search('(?<=>)(([^><])+)(?=<\/a>)',x).group(1)))

data['Categorization']=data['DownloadData'].apply(lambda x:re.search('(?<=title="\[)(.*)(?=\])',x).group(1))

data['Ranking']=data['Categorization'].apply(lambda x:ranking.get(x))

data['WorstRanking']=data['Ranking'].groupby([data['Movies'],data['Year']]).transform('max')

data=data[data['Ranking']==data['WorstRanking']].drop('DownloadData',axis=1).drop_duplicates()

data['Pass/Fail']=data['Ranking'].apply(lambda x:'Pass' if x<=2 else 'Fail')

data.drop('WorstRanking',axis=1,inplace=True)