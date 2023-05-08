# -*- coding: utf-8 -*-

# Import necessary libraries
import re
import csv
import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
URL = "https://tomsk.richfamily.ru/catalog/igrushki/myagkie/"

# Request headers to mimic browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}


# Function to get HTML content of a page given its URL
def get_html(url):
    # Send HTTP GET request to the URL with headers and raise exception if not successful
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    # Return the text content of the response
    return response.text


# Function to get the links of all pages to scrape
def get_pages(html):
    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(html, "html.parser")
    # Find the element containing links to all pages, if not found return the URL of the initial page
    pages = soup.find("li", class_="children")
    if not pages:
        return [URL]
    else:
        # Extract links to all pages
        links = pages.find_all("a", href=True)
        page_links = [f"{URL}{link['href'].split('catalog/igrushki/myagkie/')[1]}" for link in links]
        data = []
        # Scrape data from each page and append to a list
        for link in page_links:
            page_html = get_html(link)
            page_data = get_product_data(page_html)
            data.extend(page_data)
        return data


# Function to scrape product data from a page
def get_product_data(html):
    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(html, "html.parser")
    # Find all elements containing product information
    products = soup.find_all("div", class_="card")
    result = []
    # Extract product name, price and size (if available) and append to a list
    for product in products:
        name = product.find("span", class_="name").get_text(strip=True)
        price = product.find("span", class_="actual").get_text(strip=True)
        price_digits = re.sub('\D', '', price)
        size_match = re.search(r'\d+\sсм', name)

        if size_match:
            size_1 = size_match.group(0)
        else:
            size_1 = ""

        result.append([name, price_digits, size_1])
    return result


# Function to write the scraped data to a CSV file
def write_to_csv(data):
    with open("toys.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Price", "Size"])
        for product in data:
            writer.writerow(product)


# Main program
if __name__ == "__main__":
    try:
        # Get the HTML content of the initial page
        html = get_html(URL)
        # Get the links of all pages to scrape
        page_links = get_pages(html)
        data = []
        # Scrape data from each page and append to a list
        for link in page_links:
            page_html = get_html(link)
            page_data = get_product_data(page_html)
            data.extend(page_data)
            print(page_links)
        write_to_csv(data)
    except Exception as ex:
        print(f"ERROR: {ex}")
