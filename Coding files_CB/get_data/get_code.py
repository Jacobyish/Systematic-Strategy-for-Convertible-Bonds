# To find what are the bonds for each day
try:
    from iFinDPy import *
except:
    pass
THS_iFinDLogin("dxzq2102", "412085")

import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime

THS_iFinDLogin("dxzq2102", "412085")

# Create an empty dictionary to hold the data
dt_daima = {}

# Start and finish time
start_date = pd.to_datetime('2018-06-30')
end_date = pd.to_datetime('2023-06-30')
sse = mcal.get_calendar('SSE')  # Shanghai Stock Exchange
trading_days = sse.valid_days(start_date=start_date, end_date=end_date)

for day in trading_days:
    # Convert the date to a string in the desired format
    str_date = day.strftime('%Y%m%d')

    # Call the function to get the data for the current date
    data = THS_DR('p00570', f'jyzt=未到期;sfdb=全部;jysc=全部;edate={str_date}', 'jydm:Y,jydm_mc:Y,p00570_f044:Y', 'format:dataframe').data

    # Extract the 'jydm' column values and store in the dictionary
    dt_daima[str_date] = data['jydm'].values.tolist()
    print(day)

# import json
# s = json.dumps(dt_daima)
# with open("daima_2018_2023.txt", "w") as f:
#      f.write(s)

# #read bond codes
# with open("daima_2018_2023.txt", "r") as f:
#     daima = f.read()
#
# daima = json.loads(daima)