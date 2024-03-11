from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def get_def14a_urls(company_name: str):
    # Path to your WebDriver executable
    driver_path = r'C:\Users\josh\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
    service = Service(executable_path=driver_path)

    # Create a ChromeOptions object and set it to headless mode
    options = Options()
    # options.add_argument("--headless")  # Specifies headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/122.0.6261.112 Safari/537.36")
    # options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration; sometimes necessary
    # options.add_argument("--window-size=1920x1080")  # Specifies window size, helpful for some sites

    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the SEC's EDGAR search page
    driver.get("https://www.sec.gov/edgar/searchedgar/companysearch")

    # Find the search input box by its name or other attribute
    search_input = driver.find_element("id", 'edgar-company-person')

    # Type the search term into the input box
    search_input.send_keys(company_name)

    # Wait for the suggestions to load and become visible
    wait = WebDriverWait(driver, 7)

    # Construct the CSS Selector for the first <tr> in the table of suggestions
    first_suggestion_selector = "table.smart-search-entity-hints > tbody > tr:first-child"
    first_suggestion = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, first_suggestion_selector)))

    # Click the first suggestion
    first_suggestion.click()

    # I noticed that sometimes, after entering the company name and clicking the first suggestion, the webpage acts as
    # if I have already clicked view filings, and the 'filingDateFrom' box is already available. In these cases, the
    # function is not working because I am waiting for the "View Filings" button to be clickable and it never appears.
    # Check if the "View Filings" button exists or if we're already at the filings page
    try:
        view_filings_button = wait.until(EC.element_to_be_clickable((By.ID, "btnViewAllFilings")))
        view_filings_button.click()
    except TimeoutException:
        print(f"'View Filings' button not found or not needed for {company_name}. Proceeding...")
        # If this exception occurs, it's assumed we're already on the page with the 'filingDateFrom' box visible.
        pass  # Continue as the page has already advanced.

    # Find the date box and clear contents
    from_date_box = wait.until(EC.element_to_be_clickable((By.ID, "filingDateFrom")))
    from_date_box.clear()
    from_date_box.send_keys("2003-01-01")

    # Wait for the search box to be visible
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchbox")))

    # Type 'def 14a' into the search box
    search_box.send_keys("def 14a")

    # Find all links for DEF 14a forms
    def14a_links = driver.find_elements(By.CSS_SELECTOR, "a.document-link")

    # Extract the href attributes of these links
    def14a_urls = [link.get_attribute('href') for link in def14a_links]
    def14a_filtered_urls = [url for url in def14a_urls if 'def14a' in url]

    driver.quit()

    print(f"Found {len(def14a_filtered_urls)} urls for {company_name}.")
    return def14a_filtered_urls

