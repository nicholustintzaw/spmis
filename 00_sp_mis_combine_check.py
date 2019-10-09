#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:01:36 2019

@author: nicholustintzaw
"""

####################################################################################################
'''
project tite    :           social pension database - national level
purpose         :           data processing and data checking on national social pension data
developed by    :           Nicholus Tint Zaw             
modified date   :           29th Sept 2019
'''
####################################################################################################


# directory setting
import getpass
username = getpass.getuser()  # identify the user

if username == 'nicholustintzaw':
    print('this program is currently using from username ', username)
    sp      =   '/Users/nicholustintzaw/Dropbox/00_report_demo/'
    raw     =   sp + '01_raw/'
    output  =   sp + '02_outputs/'
    report  =   sp + '03_reports/'
    db      =   sp + '02_outputs/'
elif username == 'xxxx':
    print('this program is currently using from username ', username)
    sp      =   '/Users/nicholustintzaw/Dropbox/00_report_demo/'
    raw     =   sp + '01_raw/'
    output  =   sp + '02_outputs/'
    report  =   sp + '03_reports/'
    db      =   sp + '02_outputs/'
            
####################################################################################################

## office setting
    # prepare the list of office folders to combine data
offices = ['00_office', '01_office', '02_office', '03_office', '04_office', '05_office']

####################################################################################################

## Combined data from each office
import pandas as pd

df = pd.DataFrame()             # define empty data frame

col_names = ['to_check', 'record_day', 'record_month', 'record_year', 'dr', 'dr29S', 'mr', 'mrs', 'ys',
       'dob1tagu', 'sr_no', 'benef_id',
       'benef_name', 'benef_gender',
       'benef_dob_mm', 'benef_dob_eng', 'benef_age',
       'benef_nrc', 'benef_father_name', 'geo_state_region',
       'geo_district', 'geo_township', 'geo_ward_villtract', 'geo_village',
       'benef_status',
       'benef_status_date', 'transfer_amount',
       'benef_sign']        # define column name

# loop functions to open all excel files in list offices - append to empty data frame
for office in offices :
    file_office = office + "name_month.xlsx" 
    data = pd.read_excel(raw + office + '/' + file_office, sheet_name = "Eligible", skiprows = 6, \
                         header = None, names = col_names)
    df = df.append(data)

# drop unnecessary variable

df = df.drop(['to_check', 'record_day', 'record_month', 'record_year', 'dr', 'dr29S', 'mr', 'mrs', 'ys',
       'dob1tagu', 'sr_no',
       'benef_status',
       'benef_status_date', 'transfer_amount',
       'benef_sign'], axis = 1) 
 
    
# merge with MIMU Pcode dataset
col_mimu = ['sr_pcode	', 'sr_name_eng', 'district_pcode', 'district_name_eng', 'tsp_pcode', 'township_name_eng', 'town_pcode',
            'town_name_eng', 'town_name_mmr', 'longitude', 'latitude', 	'source', 'start_date', 'modified_end_date',
            'notification', 'notification_modified', 'town_status', 'change_type', 'remark' ]

df_mimu = pd.read_excel(raw + "Myanmar PCodes Release-IX_Sep2019_Countrywide.xlsx", sheet_name = "_04_Towns", skiprows = 2, \
                         header = None, names = col_mimu)

df_dsw = df_mimu.merge(df, left_on = 'town_name_mmr', right_on = 'geo_township', how = 'outer')

df_dsw = df_dsw.dropna(subset=['geo_township'])  # col_list is a list of column names to consider for nan values.


####################################################################################################

# data checking  
df.dtypes
df
df.columns      # took column name in console


## Duplicated Observation 
# duplicate by id - booleen var
dup_id = df.duplicated(subset =['benef_id'], keep = False)

# duplicate by beneficiares info - booleen var
dup_resp = df.duplicated(subset =['benef_name', 'benef_gender', 'benef_dob_eng', 'benef_age'], keep = False)

# duplciate by id and beneficiares info dataset
dup_id2 = df.loc[dup_id == True]
dup_benef_id = dup_id2['benef_id']   # keep only one variable in dataframe

dup_resp2 = df.loc[dup_resp == True]

# merge two duplicate dataframes
dup_both = dup_resp2.merge(dup_id2, left_on = 'benef_id', right_on = 'benef_id', how = 'outer')

# find duplciate rows in merged two duplciated dataframe
# concept - to remove the rows which were duplciated by benef_id
dup_both2 = dup_both.duplicated(subset =['benef_id'], keep = False)
dup_respinfo_only = dup_both.loc[dup_both2 == False] # final dataframe with only beneficaires info duplciated dataframe

dup_respinfo_only.describe()


# export excel
dup_respinfo_only.to_excel(output + 'duplicated_observation_personal_information.xlsx', index = False)
dup_id2.to_excel(output + 'duplicated_observation_benefid.xlsx', index = False)
df_dsw.to_excel(output + 'sp_combined_office1.xlsx', index = False)

