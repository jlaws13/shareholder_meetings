import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re


def get_meeting_dates(list_of_urls: list):
    driver_path = r'C:\Users\josh\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=driver_path)

    # Create a ChromeOptions object and set it to headless mode
    options = Options()
    options.add_argument("--headless")  # Specifies headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/90.0.4430.212 Safari/537.36")
    # options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration; sometimes necessary
    # options.add_argument("--window-size=1920x1080")  # Specifies window size, helpful for some sites

    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(service=service, options=options)

    # Define different search patterns focused on capturing just the date.
    # Pattern 1: "DATE AND TIME" followed by a date.
    pattern1 = r'DATE AND TIME[\s\S]*?(\w+ \d{1,2}, \d{4})'

    # Pattern 2: "will be held on" followed by a date.
    pattern2 = r'will be held on[\s\S]*?(\w+ \d{1,2}, \d{4})'

    # Pattern 3: "to be held on" followed by a date.
    pattern3 = r'to be held on[\s\S]*?(\w+ \d{1,2}, \d{4})'

    # Pattern 4: Either "Annual Meeting of Shareholders" or "Annual Shareholder Meeting" followed by a date.
    pattern4 = r'(?:Meeting of Shareholders|Shareholder Meeting)[\s\S]*?(\w+ \d{1,2}, \d{4})'

    # Pattern 5: "Annual Meeting" followed by a date.
    pattern5 = r'Annual Meeting[\s\S]*?(\w+ \d{1,2}, \d{4})'

    # Pattern 6: "to be held virtually on" followed by a date.
    pattern6 = r'to be held virtually on[\s\S]*?(\w+ \d{1,2}, \d{4})'

    patterns = [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6]

    # Initialize empty list for meeting dates
    meeting_dates = []

    # Loop through urls searching for the meeting date in each form.
    for url in list_of_urls:
        print(url)
        driver.get(url)
        date_found = False

        # Extract text from main body
        body_text = driver.find_element(By.TAG_NAME, 'body').text

        # Attempt to find a match using each pattern
        for pattern in patterns:
            match = re.search(pattern, body_text, re.IGNORECASE)
            if match:
                # Extracts the date, which is the captured group in these patterns
                meeting_date = match.group(1)
                print(f"Found Meeting Date: {meeting_date}")
                meeting_dates.append(meeting_date)
                date_found = True
                break  # Stop searching after the first match is found
        if not date_found:
            print("The date of the annual shareholders meeting wasn't found.")
            meeting_dates.append(np.nan)

    driver.quit()
    return meeting_dates


# urls = get_def14a_urls("Berkshire")
