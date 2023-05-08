import csv
import requests
from bs4 import BeautifulSoup
import re

# Set the base URL and request headers
BASE_URL = "https://tomsk.richfamily.ru/catalog/igrushki/myagkie/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

def get_product_data(html):
    """
    Extracts the name, price, and size of each product from the HTML of a product page.

    Args:
        html (str): The HTML of a product page.

    Returns:
        list: A list of lists containing the name, price, and size of each product.
    """
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", class_="card")
    result = []
    for product in products:
        name = product.find("span", class_="name").get_text(strip=True)
        price = product.find("span", class_="actual").get_text(strip=True)
        size = product.find("span", class_="name").get_text(strip=True)
        price_digits = re.sub('\D', '', price)
        size_match = re.search(r'\d+\sсм', size)

        if size_match:
            size_1 = size_match.group(0)
        else:
            size_1 = ""

        result.append([name, price_digits, size_1])
    return result

def write_to_csv(data):
    """
    Writes the product data to a CSV file.

    Args:
        data (list): A list of lists containing the name, price, and size of each product.
    """
    with open("toys.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Price", "Size"])
        for product in data:
            writer.writerow(product)

if __name__ == "__main__":
    try:
        # Initialize a session and get the first page of products
        with requests.Session() as session:
            response = session.get(BASE_URL, headers=HEADERS)
            response.raise_for_status()
            html = response.text

        # Get data from all product pages
        soup = BeautifulSoup(html, "html.parser")
        pagination = soup.find("ul", class_="pagination")
        if pagination:
            last_page = int(pagination.find_all("a")[-2].text)
        else:
            last_page = 1

        result = []
        li_page = ['','antisrtress', 'igrushki-podushki', 'interaktivnye', 'kresla', 'do-24-sm', 'do-24-sm', 'do-24-sm', 'personazhi-multfilmov']
        for page in li_page:
            # Get the HTML of a product page
            url = f"{BASE_URL}{page}/"
            response = session.get(url, headers=HEADERS)
            response.raise_for_status()
            html = response.text

            # Get data from the page and add it to the result array
            page_data = get_product_data(html)
            result.extend(page_data)

        # Write the data to a CSV file
        write_to_csv(result)
    except Exception as ex:
        print(f"ERROR: {ex}")
