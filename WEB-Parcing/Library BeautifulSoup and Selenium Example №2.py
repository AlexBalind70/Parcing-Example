# Import necessary libraries
import csv
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize the browser with headless option
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

# Set the URL to scrape
url = 'https://galamart.ru/catalog/hoztovary/'
driver.get(url)

# Set implicit wait to give the page time to load
driver.implicitly_wait(10)

# Initialize explicit wait for the "More" button
wait = WebDriverWait(driver, 10)

# Set URL pattern for the pages to scrape
url_page = 'https://galamart.ru/catalog/hoztovary/page-'

# Loop through each page and scrape the data
for page_number in range(2, 31):
    # Build the full URL for each page
    url_full = url_page + str(page_number) + '/'
    driver.get(url_full)

    # Wait for the page to load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.col.main-content')))

    # Get the HTML code after all the cards have loaded
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find the card block
    product_list = soup.find('div', {'class': 'col main-content'})

    # Loop through each card and extract the title and price
    notebooks = []
    for product in product_list.find_all('div', {'class': 'catalog-card'}):
        title = product.find('span', {'itemprop': 'name'}).text.strip()
        price = product.find('div', {'class': 'product-price'}).text.strip()
        price_digits = int(re.sub('\D', '', price))
        notebooks.append({'title': title, 'price': price_digits})

    # Sort the list of notebooks by price in descending order
    notebooks_sorted = sorted(notebooks, key=lambda x: x['price'], reverse=True)

    # Write the notebook information to a CSV file
    with open('galamart.csv', 'a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for notebook in notebooks_sorted:
            writer.writerow(notebook)

# Close the browser
driver.quit()
