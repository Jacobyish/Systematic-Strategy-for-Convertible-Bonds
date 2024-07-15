# Part 1 Data
import pandas as pd
import os
# try:
#     from iFinDPy import
# except:
#     pass
# THS_iFinDLogin("dxzq2102", "412085")

# Read bond codes

import json
with open("daima_2018_2023.txt", "r") as f:
    daima = f.read()

daima = json.loads(daima)
#

# filename = 'data1_2018_2023_ori.csv'
#
# # Check if the file already exists
# if os.path.isfile(filename):
#     # If the file exists, read the data
#     df = pd.read_csv(filename)
#
#     # Get the last trading_date in the data (assuming your data has a column with dates)
#     last_trading_date = df.iloc[-1, 0]  # assuming the first column is the date
#
#     # Get the list of trading dates in daima after the last_trading_date
#     trading_dates = [date for date in daima.keys() if pd.to_datetime(date) > pd.to_datetime(last_trading_date)]
# else:
#     # If the file doesn't exist, we start from the beginning
#     trading_dates = list(daima.keys()) # get only the first 5 days
#
# for trading_day in trading_dates:
#     try:
#         # Get bond codes for the trading day
#         bond_codes = daima[trading_day]
#
#         df_day_full = pd.DataFrame()
#
#         df_day = THS_DS(bond_codes,
#                         'ths_close_daily_settle_bond;ths_stock_pe_cbond;ths_stock_pb_cbond;ths_stock_close_cbond;ths_conversion_premium_rate_cbond;ths_pure_bond_premium_rate_cbond;ths_bond_balance_bond;ths_specified_date_bond_rating_bond'
#                         ,'103;;;100;;;;100','',
#                         trading_day,
#                         trading_day).data
#
#         df_stock_code = THS_BD(bond_codes, 'ths_stock_code_cbond', '').data
#         df_day = pd.merge(df_day, df_stock_code, on='thscode')
#
#         df_day.to_csv(filename, mode='a', header=False, index=False)
#
#             方法二： # Save df to csv
#             if os.path.isfile(filename):
#                 # If the file exists, do not write the header
#                 df_day.to_csv(filename, mode='a', header=False, index=False)
#             else:
#                 # If the file doesn't exist, write the header
#                 df_day.to_csv(filename, mode='w', index=False)
#
#
#         print(trading_day)
#
#
#
#     except Exception as e:
#         print(f"Error on trading day {trading_day}: {str(e)}")
#
#

# 数据处理：drop NA，余额小于2，信用低于A-

# df = pd.read_csv('data1_2018_2023_ori.csv')
#
# # 1. Drop NA rows
# df = df.dropna()
#
# # 2. Drop rows where 'ths_bond_balance_bond' column value is less than 2
# df = df[df['ths_bond_balance_bond'] >= 2]
#
# # 3. Drop the credit rankings less than 'A-'
# credit_rankings = ['AA+', 'AA', 'AAA', 'AA-', 'A+', 'A-','A','AA+u']
#
# df = df[df['ths_specified_date_bond_rating_bond'].isin(credit_rankings)]
# df.to_csv('data1_2018_2023_full.csv')
# Count unique elements for one specific key
unique_elements_for_key1 = len(set(daima['20230630']))
print(f"Number of unique elements for 'key1': {unique_elements_for_key1}")

# Count unique elements for the entire dictionary
all_elements = []
for key, values in daima.items():
    all_elements.extend(values)

unique_elements_for_all_keys = len(set(all_elements))
print(f"Number of unique elements for the entire dictionary: {unique_elements_for_all_keys}")










# #Data Part 2
#
# import pandas as pd
#
# # Define your function here if it's not imported
#
# # Read the existing data
# df = pd.read_csv('data_2018_2023_v1.csv', index_col=0)
#
# # Keep only the required columns
# df = df[['time', 'ths_stock_code_cbond_x']]
#
# # Name of the file to save the updated data
# new_filename = 'data_2018_2023_v2.csv'
#
# # Get unique trading dates
# trading_dates = df['time'].unique()
#
# # Only take the first 5 days
# trading_dates = trading_dates[:5]
#
# for trading_day in trading_dates:
#     # Filter the dataframe for the trading day
#     df_day = df[df['time'] == trading_day]
#
#     # Get all the stock codes for the trading day
#     stock_codes = df_day['ths_stock_code_cbond_x'].unique()
#
#     # Convert the stock codes into a comma separated string
#     stock_codes_str = ','.join(stock_codes)
#
#     try:
#         # Get new data for the day
#         df_new = THS_DS(stock_codes_str,
#                         'ths_chg_ratio_nd_stock;ths_avg_close_nd_stock',
#                         '-180,100;-5,100',
#                         '',
#                         trading_day,
#                         trading_day).data
#
#         # Append the new data to df_day
#         df_day = pd.concat([df_day, df_new], axis=1)
#
#         # If the new file doesn't exist, write the header to it
#         if not os.path.isfile(new_filename):
#             df_day.to_csv(new_filename, index=False)
#         else:  # else it exists so append without writing the header
#             df_day.to_csv(new_filename, mode='a', header=False, index=False)
#
#     except Exception as e:
#         print(f"Error on trading day {trading_day}: {str(e)}")






