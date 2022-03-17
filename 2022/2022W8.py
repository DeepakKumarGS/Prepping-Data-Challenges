# Prepping Data 2022 Week 8 

import pandas as pd

stats=pd.read_excel('data/PD 2022 Wk 8 input_pkmn_stats_and_evolutions.xlsx',sheet_name='pkmn_stats')

evolution=pd.read_excel('data/PD 2022 Wk 8 input_pkmn_stats_and_evolutions.xlsx',sheet_name='pkmn_evolutions')
#If a Pokémon doesn't evolve remove it from the dataset
evolution=evolution.dropna(subset=['Stage_2']).reset_index().rename(columns={'index':'key'})
#From pkmn_stats dataset remove the columns height, weight and evolves from
stats.drop(['height','weight','evolves_from'],axis=1,inplace=True)

#Pivot (wide to long) pkmn stats so that hp, attack, defense, special_attack, special_defense, and speed become a column called 'combat_factors'
stats_melt=pd.melt(stats,id_vars=['name','pokedex_number','gen_introduced'],var_name='combat_factors',value_name='power')

#Using the evolutions data look up the combat_factors for each Pokémon at each stage, making sure that the combat_factors match across the row, i.e. we should be able to see the hp for Bulbasaur, Ivysaur and Venusaur on one row
final=pd.merge(evolution,stats_melt,left_on='Stage_1',right_on='name').rename(columns={'power':'initial_combat_power'})

final=pd.merge(final.drop('name',axis=1),stats_melt[['name','combat_factors','power']],left_on=['Stage_2','combat_factors'],right_on=['name','combat_factors']).rename(columns={'power':'stage2_combat_power'})

final=pd.merge(final.drop('name',axis=1),stats_melt[['name','combat_factors','power']],left_on=['Stage_3','combat_factors'],right_on=['name','combat_factors'],how='left').rename(columns={'power':'stage3_combat_power'})

final.drop('name',axis=1,inplace=True)
#Sum together each Pokémon's combat_factors
final = final.groupby('key').agg({'Stage_1':'max','Stage_2':'max','Stage_3':'max','pokedex_number':'max','gen_introduced':'max',
                        'initial_combat_power':'sum','stage2_combat_power':'sum','stage3_combat_power':'sum'})

final['final_combat_power']=final.apply(lambda x:x['stage2_combat_power'] if pd.isna(x['Stage_3']) else int(x['stage3_combat_power']),axis=1)
#Find the percentage increase in combat power from the first & last evolution stage
final['combat_power_increase']=(final['final_combat_power']-final['initial_combat_power'])/final['initial_combat_power']
#Which Pokémon stats decrease from evolving?
final=final[['Stage_1','Stage_2','Stage_3','pokedex_number','gen_introduced','initial_combat_power',
                'final_combat_power','combat_power_increase']].sort_values('combat_power_increase')

#Nincada stats seems to decrease from evolving.  