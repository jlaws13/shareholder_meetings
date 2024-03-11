from get_def14a_urls import get_def14a_urls
from get_meeting_dates import get_meeting_dates
import json


# Function using the company names list to create dictionaries with urls and shareholder meeting dates.
def create_url_and_dates_dictionaries(list_of_company_names: list, retry=False):
    # Initialize empty dictionaries to store the company and associated urls, as well as to store the ones we need to
    # retry.
    all_urls = {}
    retry_urls = {}

    # Get the urls to archived def_14a forms for each company in our list.
    for company in list_of_company_names:
        try:
            urls = get_def14a_urls(company)
            if urls:
                all_urls[company] = urls  # Store the list of URLS under the company name
            else:
                print(f"No URLs found for {company}. Adding to retry dictionary.")
                retry_urls[company] = None  # Store the company in the retry dictionary.
        except Exception as e:
            print(f"Error: {company}: {e}")
            all_urls[company] = []
            retry_urls[company] = []  # Store the company in the retry dictionary.

    # Save the dictionary of urls.
    with open('all_urls.txt', 'w') as file:
        json.dump(all_urls, file)

    # Initialize an empty dictionary to store the company names and their associated meeting dates
    all_dates = {}
    retry_dates = {}

    # Use the url dictionary to scrape files for meeting dates.
    for company, urls in all_urls.items():  # Iterate through each company and its list of URLs
        try:
            dates = get_meeting_dates(urls)  # Assuming get_meeting_dates accepts a single URL
            all_dates[company] = dates  # Add the retrieved dates to the company's list
        except Exception as e:
            print(f"Error with {company}: {e}")
            all_dates[company] = []
            retry_dates[company] = []  # If unsuccessful, add company name to the retry list

    # Save the dictionary of dates.
    with open('all_dates.txt', 'w') as file:
        json.dump(all_dates, file)

    # Populate retry_urls based on empty lists in all_urls
    for company, urls in all_urls.items():
        if not urls:  # Check if the URL list is empty
            retry_urls[company] = []  # Indicates a need to retry URL fetching

    # Populate retry_dates based on empty lists in all_dates
    for company, dates in all_dates.items():
        if not dates:  # Check if the URL list is empty
            retry_dates[company] = []  # Indicates a need to retry URL fetching

    # Retry fetching URLs for companies that failed in the first attempt
    if retry:
        for company in retry_urls.keys():
            try:
                urls = get_def14a_urls(company)
                if urls:
                    all_urls[company] = urls
                    retry_urls[company] = urls
                    # # Attempt to fetch dates right after successful URL fetch
                    # try:
                    #     dates = get_meeting_dates(urls)
                    #     all_dates[company] = dates
                    # except Exception as e:
                    #     print(f"Error fetching dates for {company} on retry: {e}.")
                    #     all_dates[company] = []  # or a special marker
                else:
                    print(f"No URLs found for {company} on retry.")
            except Exception as e:
                print(f"Error fetching URLs for {company} on retry: {e}.")

        # Retry fetching dates for companies that failed in the first dates attempt
        for company, urls in retry_urls.items():
            try:
                dates = get_meeting_dates(urls)
                all_dates[company] = dates
                retry_dates[company] = dates
            except Exception as e:
                print(f"Error fetching dates for {company} on retry: {e}.")
                all_dates[company] = []  # or a special marker

    # Save the dictionary of urls.
    with open('all_urls.txt', 'w') as file:
        json.dump(all_urls, file)

    # Save the dictionary of dates.
    with open('all_dates.txt', 'w') as file:
        json.dump(all_dates, file)

    print("Dictionary containing urls of def 14a forms were saved at all_urls.txt.\n Dictionary containing all "
          "dates were saved at all_dates.txt")

# # Load dataframe with company names and other information about our sample
# master = pd.read_csv(r"master.csv")
#
# # Filter to inlcude only firms for which we have created time series.
# filtered_master = master[master['time_series_created'] == 1]
#
# # Function to extract company names from the filtered_master df.
# def extract_words(x):
#     if pd.notnull(x):
#         words = x.split()
#         # Check if the first two "words" are only letters and their combined length is <= 2
#         if len(words) >= 2 and all(word.isalpha() and len(word) == 1 for word in words[:2]):
#             # Take the first four words if they exist, else take as many as are available
#             return ' '.join(words[:4 if len(words) >= 4 else len(words)])
#         else:
#             # Take the first two words if they exist, else take as many as are available
#             return ' '.join(words[:2 if len(words) >= 2 else len(words)])
#     else:
#         return ''
#
# # Apply the function to each value in the 'Company_Name' column
# company_names_adjusted = filtered_master['Company_Name'].apply(extract_words)
#
# # Convert company names to a list.
# company_names_adjusted_list = company_names_adjusted.tolist()
#
# create_url_and_dates_dictionaries(company_names_adjusted_list)
