import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://www.gctc.ru/main.php?id=98.1'

# Set the user agent in the headers to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # Create a session object and set headers
    with requests.Session() as s:
        response = s.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if status code is not 200

        # Parse the HTML response with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html5lib')

        # Find the main div containing the info
        main_div = soup.find('div', {'class': 'ie_infoh'})

        # Find all the h2 tags in the main div
        h2_tags = main_div.select('h2')

        # Create a list to store the results
        result = []

        # Iterate over each h2 tag
        for tag in h2_tags:
            # Extract the year from the h2 tag
            year = tag.text[:-2]

            # Find the previous h1 tag
            h1_tag = tag.find_previous('h1')

            # Combine the date strings from the h1 and h2 tags
            date_str = h1_tag.text.strip() + ' ' + tag.text.strip()

            # Split the date string into month and day
            month_name, day = date_str.rsplit(maxsplit=1)[0].split(maxsplit=1)

            # Add the formatted date to the result list
            result.append(f"{month_name.strip()} {year}")

        # Print the result list
        print(result)

# Handle any exceptions
except requests.exceptions.RequestException as e:
    print('Error while requesting the website:', e)
