import pandas as pd
import numpy as np


# path = '/Users/jacobyi/Desktop/工作/东兴证劵/可转债/data/get_data/data_2018_2023_v1.csv'
df = pd.read_csv('data.csv')

# Sort the DataFrame by time and asset
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values(by=['thscode', 'time'])

# 2. Calculate Daily Return of the Bond
df['bond_return_daily'] = df.groupby(['thscode'])['ths_close_daily_settle_bond'].apply(lambda x: np.log(x / x.shift(-1)))

# 6. Calculate bias_ratio_5days
# Define the function to calculate the 5-day bias ratio
def calculate_5_day_bias_ratio(group):
    group['5_day_MA'] = group['ths_close_daily_settle_bond'].rolling(window=5).mean()
    group['bias_ratio_5'] = (group['ths_close_daily_settle_bond'] - group['5_day_MA']) / group['5_day_MA'] *100
    return group

# Group by 'thscode' and apply the function
df = df.groupby('thscode').apply(calculate_5_day_bias_ratio)


# Define a function to standardize a series
def standardize(series):
    return (series - series.mean()) / series.std()

# Group by 'time' and apply the standardization function
standardized_cols = df.groupby('time').transform(lambda x: standardize(x) if x.name in ['ths_conversion_premium_rate_cbond', 'ths_close_daily_settle_bond', 'bias_ratio_5'] else x)

# Rename and add them to the original DataFrame
df['conversion_sd'] = standardized_cols['ths_conversion_premium_rate_cbond']
df['price_sd'] = standardized_cols['ths_close_daily_settle_bond']
df['bias_ratio_sd'] = standardized_cols['bias_ratio_5']


df['factor_3'] = (df['conversion_sd'] + df['price_sd'] +df['bias_ratio_sd']) / 3
df['factor_2'] = (df['conversion_sd'] + df['price_sd']) / 2


# 120天ic加权
# Calculate 10-day forward returns
df['cum_return_10d'] = df.groupby('thscode')['ths_close_daily_settle_bond'].apply(lambda x: (x.shift(-10) - x) / x)


# Spearman rank IC function
def rank_ic(group):
    factors = ['conversion_sd', 'price_sd', 'bias_ratio_sd']
    ic_dict = {}
    for factor in factors:
        ic = group[factor].corr(group['cum_return_10d'], method='spearman')
        ic_dict[f'IC_{factor}'] = ic
    return pd.Series(ic_dict)



# Group by time and apply the Spearman rank IC function
ic_df = df.groupby('time').apply(rank_ic).reset_index()

ic_df['IC_conversion_120'] = ic_df['IC_conversion_sd'].rolling(window=120).mean()
ic_df['IC_price_120'] = ic_df['IC_price_sd'].rolling(window=120).mean()
ic_df['IC_bias_ratio_120']  = ic_df['IC_bias_ratio_sd'].rolling(window=120).mean()
df = pd.merge(df, ic_df, on='time', how='left')

# Sum of absolute IC values
sum_ic_120 = abs(df['IC_conversion_120']) + abs(df['IC_price_120']) + abs(df['IC_bias_ratio_120'])

# Calculating the weighted factor
df['ic_weighted_factor'] = (abs(df['IC_conversion_120']) * df['conversion_sd'] + abs(df['IC_price_120']) * df['price_sd'] + abs(df['IC_bias_ratio_120']) * df['bias_ratio_sd']) / sum_ic_120

df['ic_weighted_factor_shifted'] = df.groupby('thscode')['ic_weighted_factor'].shift(10)

# Remove rows where 'ic_weighted_factor_shifted' is NaN
df.dropna(subset=['ic_weighted_factor_shifted'], inplace=True)

# save to csv
df.to_csv('data_2018_2023_ic_weighted_120.csv', index=False)






