# Import necessary libraries
import pandas as pd
import alphalens as al
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import warnings
warnings.filterwarnings("ignore")

# Load your dataset
path = '/Users/jacobyi/Desktop/工作/东兴证劵/可转债/Coding files/factor_engineering/data_2018_2023_ic_weighted_120.csv'
df = pd.read_csv(path)

# Convert 'time' column to datetime
df['time'] = pd.to_datetime(df['time'])
prices = df.pivot(index='time', columns='thscode', values='ths_close_daily_settle_bond')
factors = ['factor_3']

for factor_name in factors:
    print(f"Processing factor: {factor_name}")

    # Set current factor
    factor = df.set_index(['time', 'thscode'])[factor_name]

    # Get clean factor and forward returns
    factor_data = al.utils.get_clean_factor_and_forward_returns(factor=factor,
                                                                prices=prices,
                                                                quantiles=5,
                                                                periods=(1, 10, 20))

    al.tears.create_full_tear_sheet(factor_data, long_short=True, group_neutral=False, by_group=False)

#%%
