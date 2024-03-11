from create_url_and_dates_dictionaries import create_url_and_dates_dictionaries
from create_dataset import create_dataset
import pandas as pd

if __name__ == '__main__':
    # Load dataframe with company names and other information about our sample
    master = pd.read_csv(r"master.csv")

    # Filter to inlcude only firms for which we have created time series.
    filtered_master = master[master['time_series_created'] == 1]

    # Function to extract company names from the filtered_master df.
    def extract_words(x):
        if pd.notnull(x):
            words = x.split()
            # Check if the first two "words" are only letters and their combined length is <= 2
            if len(words) >= 2 and all(word.isalpha() and len(word) == 1 for word in words[:2]):
                # Take the first four words if they exist, else take as many as are available
                return ' '.join(words[:4 if len(words) >= 4 else len(words)])
            else:
                # Take the first two words if they exist, else take as many as are available
                return ' '.join(words[:2 if len(words) >= 2 else len(words)])
        else:
            return ''

    # Apply the function to each value in the 'Company_Name' column
    company_names_adjusted = filtered_master['Company_Name'].apply(extract_words)

    # Convert company names to a list.
    company_names_adjusted_list = company_names_adjusted.tolist()

    # Run the full process
    create_url_and_dates_dictionaries(company_names_adjusted_list)
    df = create_dataset()
    # Save the dataset
    df.to_csv("dataset.csv")
