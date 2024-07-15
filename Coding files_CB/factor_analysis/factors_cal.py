import pandas as pd


# 'time', 时间 'ths_stock_code_cbond_x',正股代码 'thscode_x'转债代码
# 'ths_close_daily_settle_bond',转债收盘return
# 'ths_conversion_premium_rate_cbond',转股溢价率 'ths_pure_bond_premium_rate_cbond',纯债溢价率
# 'ths_bond_balance_bond',债券余额 'ths_specified_date_bond_rating_bond，信用评级

# 'ths_stock_pb_cbond'正股pb, 'ths_stock_close_cbond'正股收盘价,'ths_stock_pe_cbond'正股pe,
# 'ths_chg_ratio_nd_stock', 正股前180日涨跌幅'ths_avg_close_nd_stock'正股前180日平均收盘价,

#  # 计算价格因子'price_factor'
# df = pd.read_csv('data_2018_2023_full.csv')
#
#
# df['price_factor'] = df['ths_stock_close_cbond'] / df['ths_avg_close_nd_stock']
# df.to_csv('data_2018_2023_full.csv')




# 计算cumulative return

# import numpy as np
#
# df = pd.read_csv('data_2018_2023_full.csv')
#
#
# # Add 1 to daily returns
# df['return_plus_one'] = df['ths_close_daily_settle_bond']*0.01 + 1
#
# # Calculate cumulative returns over 20 trading day periods
# df['cumulative_return_20'] = df.groupby('thscode_x')['return_plus_one'].apply(lambda x: x.shift(-19).rolling(20).apply(np.prod, raw=True) - 1)
#
# # Drop rows with NaN values in 'cumulative_return' column
# df.dropna(subset=['cumulative_return_20'], inplace=True)
#
# # Drop the 'return_plus_one' column
# df.drop(columns=['return_plus_one'], inplace=True)
#
# df.to_csv('data_2018_2023_full_cumulative_return.csv')
#








# 计算 ic



# df = pd.read_csv('data_2018_2023_full.csv')
# from scipy.stats import spearmanr
#
# def calculate_rank_ic(group, factor_column, return_column, period=20):
#     group['future_return'] = group[return_column].shift(-period) # shift return data to future
#     group = group.dropna()  # remove rows with NaN values
#
#     rank_ic_values = []
#     for i in range(period, len(group) - period):  # Skip the first and last `period` days
#         factor_values = group[factor_column].iloc[i-period:i]  # last `period` days' factor values
#         future_returns = group['future_return'].iloc[i:i+period]  # next `period` days' return values
#
#         rank_ic, _ = spearmanr(factor_values, future_returns)  # calculate Rank IC
#         rank_ic_values.append(rank_ic)
#
#     rank_ic_series = pd.Series(rank_ic_values, index=group['time'].iloc[period:-period], name='Rank IC_' + factor_column, dtype='float64')
#     return rank_ic_series
#
# # List of factors
# factors = ['ths_stock_pe_cbond', 'ths_stock_pb_cbond', 'price_factor','ths_chg_ratio_nd_stock','ths_conversion_premium_rate_cbond','ths_pure_bond_premium_rate_cbond' ]
#
# # Initialize empty dataframe
# all_rank_ic = pd.DataFrame()
#
# # Calculate Rank IC for each factor
# for factor in factors:
#     rank_ic_df = df.groupby('thscode_x').apply(calculate_rank_ic, factor_column=factor, return_column='ths_close_daily_settle_bond', period=20)
#     rank_ic_df = rank_ic_df.reset_index()
#     rank_ic_df.columns = ['thscode_x', 'time', 'Rank IC_' + factor]
#     rank_ic_df = rank_ic_df.groupby('time')['Rank IC_' + factor].mean().reset_index()  # calculate average IC for each day
#
#     # If all_rank_ic is empty, copy rank_ic_df to it. Else, merge new Rank IC column to all_rank_ic
#     if all_rank_ic.empty:
#         all_rank_ic = rank_ic_df
#     else:
#         all_rank_ic = pd.merge(all_rank_ic, rank_ic_df, on='time')
#
# # Save the final dataframe with all Rank ICs to a csv file
# all_rank_ic.to_csv('all_rank_ic_data.csv', index=False)








#画图
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
#
# # 1. Read the data
# df = pd.read_csv('all_rank_ic_data.csv')
#
# # 每20个交易日取一个ic值
# df = df.iloc[::20, :]
# df = df.head(30)
# # Convert the 'time' column to datetime
# df['time'] = pd.to_datetime(df['time'])
#
# # 2. Calculate the cumulative sum for all columns (except 'time')
# for col in df.columns:
#     if col != 'time':
#         df[col+'_cumulative'] = df[col].cumsum()
#
# # 3. Plot the accumulated values over time
# plt.figure(figsize=(14,7))
#
# for col in df.columns:
#     if '_cumulative' in col:
#         plt.plot(df['time'], df[col], label=col)
#
# plt.xlabel('Time')
# plt.ylabel('Cumulative Sum')
# plt.title('Accumulated IC Values Over Time')
# plt.legend()
# plt.grid(True)
# plt.show()
#
# df.mean()