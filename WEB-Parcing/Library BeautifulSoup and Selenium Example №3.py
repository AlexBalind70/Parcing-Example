import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set options for headless browsing
chrome_options = Options()
chrome_options.add_argument('--headless')

# Initialize the webdriver with the options
driver = webdriver.Chrome(options=chrome_options)

# Set the URL to scrape
url = 'https://www.nbcomputers.ru/catalog/noutbuki/'

# Load the page with the driver
driver.get(url)

# Wait for 10 seconds until the page loads completely
driver.implicitly_wait(10)

# Set up the explicit wait with a timeout of 10 seconds
wait = WebDriverWait(driver, 10)

# Loop to keep clicking on the "load more" button until there are no more products to load
while True:
    try:
        # Find the load more button and wait until it is clickable
        load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-47746e2f-0')))
        # Click the load more button
        load_more_button.click()
        # Wait for 2 seconds to give the page time to load more products
        time.sleep(2)
    except:
        # If there are no more products to load, break the loop
        break

# Get the page source after all the products have loaded
html = driver.page_source

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the product list container
product_list = soup.find('div', {'class': 'ant-col-xl-offset-1'})

# Create an empty list to store the extracted data
notebooks = []

# Loop through each product in the product list
for product in product_list.find_all('article', {'class': 'sc-5133e97-0'}):
    # Extract the title of the product
    title = product.find('div', {'class': 'sc-5133e97-15 buPdmH'}).text.strip()
    # Extract the price of the product
    price = product.find('span', {'class': 'sc-96470d6e-2 chpWFX'}).text.strip()
    # Extract the product code
    code = product.find('p', {'class': 'sc-d9406361-0 cfXmWO'}).text.strip()
    # Extract the digits from the price string using regular expressions
    price_digits = re.sub('\D', '', price)
    # Append the extracted data to the notebooks list
    notebooks.append({'title': title, 'price': price_digits, 'code': code[5:]})

# Write the extracted data to a CSV file
with open('notebooks.csv', 'w', encoding='utf-8', newline='') as csvfile:
    # Set up the fieldnames for the CSV file
    fieldnames = ['title', 'price', 'code']
    # Create a DictWriter object to write the data to the CSV file
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write the header row to the CSV file
    writer.writeheader()
    # Loop through each notebook in the notebooks list and write its data to the CSV file
    for notebook in notebooks:
        writer.writerow(notebook)

# Quit the webdriver
driver.quit()
