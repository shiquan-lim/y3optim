# Set utility score for each item.

# Imports
import pandas as pd
import numpy as np

file = '../data/merged_final.csv'

df_merged_final = pd.read_csv(file)

profile_item_total_df =  df_merged_final.groupby(['age_group',
                                                  'time_of_day',
                                                  'NumPax'])['Quantity'].sum().reset_index()

item_total_df = df_merged_final.groupby(['age_group',
                                            'time_of_day',
                                            'NumPax',
                                            'Item Description_y',
                                           'Item Type',
                                           'Item Category']).size().reset_index().rename(columns={0:'item_total'})

uscore_list = []
rownum = 0
for row in df_merged_final.iterrows():
    print("now processing row: ", row)
    rownum+=1
    row_details = row[1]
    t_details_id = row_details['Transact Details ID']
    age_group = row_details['age_group']
    tod = row_details['time_of_day']
    numpax = row_details['NumPax']
    item_desc = row_details['Item Description_y']
    item_type = row_details['Item Type']
    item_cat = row_details['Item Category']

    item_total = item_total_df['item_total'].ix[(item_total_df['age_group'] == age_group) &
                                               (item_total_df['time_of_day'] == tod) &
                                               (item_total_df['NumPax'] == numpax) &
                                               (item_total_df['Item Description_y'] == item_desc) &
                                               (item_total_df['Item Type'] == item_type) &
                                               (item_total_df['Item Category'] == item_cat)].item()

    profile_total = profile_item_total_df['Quantity'].ix[(profile_item_total_df['age_group'] == age_group) &
                                                         (profile_item_total_df['time_of_day'] == tod) &
                                                         (profile_item_total_df['NumPax'] == numpax)].item()
#     print(item_total)
#     print(profile_total)
    temp_dict = {t_details_id: item_total / profile_total}
    # uscore_dict[t_details_id] = item_total / profile_total
    uscore_list.append(temp_dict)

pd.DataFrame(uscore_list).to_csv('uscore.csv')
