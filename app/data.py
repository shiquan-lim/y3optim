import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime

# pull in raw data file
file = '../data/data_final.csv'
transaction_df = pd.read_csv(file, engine='c',parse_dates={'transaction_datetime':[4,5]}, infer_datetime_format=True)

# creating customer table
customer_df = pd.DataFrame()

# Assigning existing values from data file
customer_df['customer_id'] = transaction_df['Customer ID']
customer_df['age'] = transaction_df['Age']
customer_df['gender'] = transaction_df['Gender'] # Gender not require
del customer_df['gender'] # Gender not required

# remove duplicates from customer_df
customer_df = customer_df.drop_duplicates(keep='first')

# change age to numeric
customer_df['age'] = pd.to_numeric(customer_df['age'])

# Fill NaNs with zeros
customer_df['age'] = customer_df['age'].fillna(value=0)

# Getting mean and SD of individuals aged >= 6 & <= 88
mean = customer_df["age"].ix[(customer_df["age"] >= 6) & (customer_df["age"] <= 88)].mean()
sd = customer_df["age"].ix[(customer_df["age"] >= 6) & (customer_df["age"] <= 88)].std()

# Replacing age 0 or > 88 with age generated as per normal distribution of mu and sd calculated above.
def assignAge(d):
    while(d < 6 or d > 88):
        d = np.random.normal(mean, sd, 1)[0]
    return int(d)

# Assigning age category.
def age_group(d):
    if d <= 18:
        return "YOUTH"
    elif d <= 35 and d > 18:
        return "ADULT"
    elif d <= 50 and d > 35:
        return "MIDDLE"
    else:
        return "SENIOR"

# Apply functions to 'age' column
customer_df['age'] = customer_df['age'].apply(assignAge)
customer_df['age_group'] = customer_df['age'].apply(age_group)

# merge customer and transaction,
merged_df = transaction_df.merge(customer_df, how="left",left_on="Customer ID", right_on='customer_id')

# remove unecessary columns
del merged_df['Customer ID']
del merged_df['Age']
del merged_df['Gender']

# rename columns
merged_df = merged_df.rename(columns={'Transact ID':'transaction_id','Outlet':'outlet','Outlet District':'outlet_district',
                                      'Transact Details ID':'transact_details_id','Item':'item','Item Description':'item_desc',
                                      'Quantity':'qty','Price':'price','Spending':'spending'})

# Time of day function
def tod(d):
    today6am = datetime(12, 1, 1, 6, 0, 0).time()
    today12pm = datetime(12, 1, 1, 12, 0, 0).time()
    today6pm = datetime(12, 1, 1, 18, 0, 0).time()
    today12am = datetime(12, 1, 1, 23, 59, 59).time()

    if d.time() > today6am and d.time() < today12pm:  # greater than 6am and less than 12pm:
        return "BREAKFAST"
    elif d.time() >= today12pm and d.time() < today6pm:  # greater than 12pm and less than 6pm
        return "LUNCH"
    elif d.time() >= today6pm and d.time() <= today12am:
        return "DINNER"
    else:
        return "SUPPER"

# Apply time of day function, create new column
merged_df["time_of_day"] = merged_df["transaction_datetime"].apply(tod)

# Get derived items
derivedItems_df = pd.read_csv("../data/item_table_w_cost.csv")

# Rename derivedItems dataframe for consistency
derivedItems_df = derivedItems_df.rename(columns={'Item':'item','Item Description':'item_desc','Item Type':'item_type','Item Category':'item_cat',
                                                 'Price':'d_price'})
derivedItems_df['item'] = derivedItems_df['item'].str.strip()
merged_df['item'] = merged_df['item'].str.strip()
merged_df = pd.merge(merged_df,derivedItems_df, 'left', 'item')

# remove extra columns, cleaning things up
del merged_df['item_desc_y']

# rename item_desc_x column to item_desc
merged_df = merged_df.rename(columns={'item_desc_x':'item_desc'})

# drop rows with 'TAKEAWAY'
merged_df = merged_df[merged_df['item_type'] != "TAKEAWAY"]

# Replace 'Beverage' with 'drink
merged_df['item_type'] = merged_df['item_type'].replace('Beverage','Drink')

print(merged_df.groupby(['item_type']).size())

grouped_df = merged_df.groupby(['transaction_id','item_type']).size()

# Function to guess number of persons
def noPax(d):
    mains = d['Main']
    drinks = d['Drink']
    sides = d['Side']
    dessert = d['Dessert']
    soup = d["Soup"]
    # Number of mains shall be equal to the number of people.
    if mains > 0:
        return mains
    elif drinks > 0:
        return drinks
    elif sides > 0:
        return sides / 2
    elif soup > 0:
        return soup / 2
    elif dessert > 0:
        return dessert

output = {}
for transaction, subframe in grouped_df.groupby(level=0):
    temp_dict = subframe.to_dict()
    new_dict = {}
    for k1, k2 in temp_dict:
        val = temp_dict[(k1, k2)]
        new_dict[k2] = val

    if 'Main' not in new_dict:
        new_dict['Main'] = 0

    if 'Drink' not in new_dict:
        new_dict['Drink'] = 0

    if 'Side' not in new_dict:
        new_dict['Side'] = 0

    if 'Dessert' not in new_dict:
        new_dict['Dessert'] = 0

    if 'Soup' not in new_dict:
        new_dict['Soup'] = 0

    numPax = noPax(new_dict)
    numPax = np.ceil(numPax)
    if numPax < 1: numPax = 1
    output[transaction] = numPax

# Create numpax_df
numpax_df = pd.DataFrame(list(output.items()))
# Rename columns for readability
numpax_df  = numpax_df.rename(columns={0:'transaction_id',1:'numpax'})

# Set variable type as int, to be safe
numpax_df['transaction_id'] = numpax_df['transaction_id'].astype(int)
numpax_df['numpax'] = numpax_df['numpax'].astype(int)

# Function for getting groupCategory
def groupCategory(d):
    if d >= 3:
        return "GROUP"
    elif d == 2:
        return "COUPLE"
    else:
        return "SOLO"

# Apply group category function
numpax_df['group_category'] = numpax_df['numpax'].apply(groupCategory)

merged_df = pd.merge(merged_df, numpax_df, how='left', left_on='transaction_id', right_on='transaction_id')

# Create new dataframe of total quantity of items ordered for each age_group, tod, numpax profile
profile_item_total_df =  merged_df.groupby(['age_group','time_of_day','group_category'])['qty'].sum().reset_index()
item_total_df = merged_df.groupby(['age_group','time_of_day','group_category','item_desc','item_type', 'item_cat','d_price'])\
    .size().reset_index().rename(columns={0:'item_total'})

item_total_df = item_total_df.rename(columns={'d_price':'price'})

# Merge the two tables together
profile_and_item_total_df = pd.merge(profile_item_total_df,item_total_df,how='left',on=['age_group','time_of_day','group_category'])

temp_df = profile_and_item_total_df.ix[(profile_and_item_total_df.age_group == 'ADULT') &
                                       (profile_and_item_total_df.time_of_day == 'BREAKFAST') &
                                       (profile_and_item_total_df.group_category == 'COUPLE')]

# Calculate utility scores
profile_and_item_total_df['uscore'] = (profile_and_item_total_df['item_total'] / profile_and_item_total_df['qty']) * 10000

# Modify Utility Scores, If main +25%, if Drink -50%
main_mask = (profile_and_item_total_df['item_type'] == 'Main')
main_valid = profile_and_item_total_df[main_mask]
profile_and_item_total_df.loc[main_mask,'uscore'] = main_valid['uscore'] * 1.25

drink_mask = (profile_and_item_total_df['item_type'] == 'Drink')
drink_valid = profile_and_item_total_df[drink_mask]
profile_and_item_total_df.loc[drink_mask,'uscore'] = drink_valid['uscore'] * 0.5

# Round utility scores to nearest integer and set to type int
profile_and_item_total_df['uscore'] = profile_and_item_total_df['uscore'].round()
profile_and_item_total_df['uscore'] = profile_and_item_total_df['uscore'].astype(int)

# Change price to cents and set to type int
profile_and_item_total_df['price'] = profile_and_item_total_df['price'].apply(lambda x: x * 100)
profile_and_item_total_df['price'] = profile_and_item_total_df['price'].astype(int)

# Remove unwanted columns, again
# del profile_and_item_total_df['group_category_y']
# profile_and_item_total_df = profile_and_item_total_df.rename(columns={'group_category_x':'group_category'})

# Output DataFrame
output_df = pd.DataFrame()
output_df['age_group'] = profile_and_item_total_df['age_group']
output_df['time_of_day'] = profile_and_item_total_df['time_of_day']
output_df['group_category'] = profile_and_item_total_df['group_category']
output_df['uscore'] = profile_and_item_total_df['uscore']
output_df['price'] = profile_and_item_total_df['price']
output_df['item_type'] = profile_and_item_total_df['item_type']
output_df['item_cat'] = profile_and_item_total_df['item_cat']
output_df['item_desc'] = profile_and_item_total_df['item_desc']

# print(output_df.head())

# output_group_df = output_df.groupby(['age_group','time_of_day','group_category']).size().groupby(level=0)

# loop through each sub category and generate csvs
age_group_list = output_df['age_group'].unique().tolist()
tod_list = output_df['time_of_day'].unique().tolist()
grp_cat_list = output_df['group_category'].unique().tolist()


dbname = 'y3optim'
user = 'limshiq'
pw = 'awesomeSQ'
host = 'y3optim.cnlc0eowtsp7.ap-southeast-1.rds.amazonaws.com'
port = '5432'
# Open db connection
engine = create_engine('postgresql+psycopg2://'+user+':'+pw+'@'+host+':'+port+'/'+dbname)
conn = engine.connect()

# Local path file
outputpath = '../data/output/'

# step through each category - sub category and query the table
for ag in age_group_list:
    for tod in tod_list:
        for grp_cat in grp_cat_list:
            temp_df = output_df.ix[(output_df.age_group == ag) &
                                      (output_df.time_of_day == tod) &
                                      (output_df.group_category == grp_cat)]

            file_name = str(ag)+"_"+str(tod)+"_"+str(grp_cat)+"_SUNNY"
            temp_df.ix[:,'uscore':'item_desc'].to_csv(outputpath+file_name+".csv",header=False, index=False)
            temp_df.ix[:, 'uscore':'item_desc'].to_sql(file_name,conn,if_exists='replace',index=False)

# Modify uscore values for Soup*, Noodlesoup*, Drink;Hot, Porridge* for 100% increase
# Soup;*
soup_mask = (output_df['item_cat'].str.contains(r'^Soup;'))
soup_valid = output_df[soup_mask]
output_df.loc[soup_mask,'uscore'] = soup_valid['uscore'] * 2
# Noodlesoup;*
noodlesoup_mask = (output_df['item_cat'].str.contains(r'^Noodlesoup;'))
noodlesoup_valid = output_df[noodlesoup_mask]
output_df.loc[noodlesoup_mask,'uscore'] = noodlesoup_valid['uscore'] * 2
# Drink;Hot*
hotdrink_mask = (output_df['item_cat'].str.contains(r'^Drink;Hot'))
hotdrink_valid = output_df[hotdrink_mask]
output_df.loc[hotdrink_mask,'uscore'] = hotdrink_valid['uscore'] * 2
# Porridge;*
porridge_mask = (output_df['item_cat'].str.contains(r'^Porridge;'))
porridge_valid = output_df[porridge_mask]
output_df.loc[porridge_mask,'uscore'] = porridge_valid['uscore'] * 2

for ag in age_group_list:
    for tod in tod_list:
        for grp_cat in grp_cat_list:
            temp_df = output_df.ix[(output_df.age_group == ag) &
                                      (output_df.time_of_day == tod) &
                                      (output_df.group_category == grp_cat)]

            file_name = str(ag)+"_"+str(tod)+"_"+str(grp_cat)+"_RAINY"
            temp_df.ix[:,'uscore':'item_desc'].to_csv(outputpath+file_name+".csv",header=False, index=False)
            temp_df.ix[:, 'uscore':'item_desc'].to_sql(file_name, conn, if_exists='replace', index=False)

# Close connection
conn.close()