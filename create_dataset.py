import json
import numpy as np
from dateutil import parser
import pandas as pd


# Now I will create a dataframe where each column is a company name and each row is the date of the company's
# shareholder meeting in the format YYYYMMDD
def create_dataset():
    # Reloading the dates dictionary from the .txt file
    with open('all_dates.txt', 'r') as file:
        reloaded_all_dates = json.load(file)

    # Convert dates in the dictionary to 'YYYYMMDD' format and handle NaN
    for company in reloaded_all_dates.keys():
        reloaded_all_dates[company] = [
            parser.parse(date_str).strftime('%Y%m%d') if pd.notna(date_str) else np.nan
            for date_str in reloaded_all_dates[company]
        ]

    # Determine the maximum number of dates for any company
    max_dates = max(len(dates) for dates in reloaded_all_dates.values())

    # Pad each company's list of dates with NaNs to ensure equal length
    for company, dates in reloaded_all_dates.items():
        dates_length = len(dates)
        if dates_length < max_dates:
            reloaded_all_dates[company].extend([np.nan] * (max_dates - dates_length))

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(reloaded_all_dates, orient='index').transpose()

    return df
