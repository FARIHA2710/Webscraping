import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def read_urls_from_csv(csv_file_path):
    # Use pandas to easily read the specific column from the CSV
    df = pd.read_csv(csv_file_path)
    return df["Street, Building Nr URL"].tolist()

def scrape_address_latitude_longitude(url):
    try:
        headers_request = {'Accept-Language': 'en-US,en;q=0.9'}  # Request English content
        response = requests.get(url, headers=headers_request)
        #response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            address = soup.find('h1').text.strip()
            script_tags = soup.find_all('script')
            latitude = None
            longitude = None
            for script in script_tags:
                if 'initMap' in script.text:
                    match = re.search(r'initMap\(([\d.-]+),\s*([\d.-]+)', script.text)
                    if match:
                        latitude, longitude = match.groups()
                        break
            return address, latitude, longitude
        else:
            print(f"Failed to retrieve content from {url}")
            return None, None, None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None, None

def write_to_csv(data, csv_file_path):
    fieldnames = ['Address', 'Latitude', 'Longitude']
    with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            if row['Address'] and row['Latitude'] and row['Longitude']:
                writer.writerow(row)

# Input and output CSV file paths
input_csv_path = 'buildings_data.csv'
output_csv_path = 'location.csv'

# Read URLs from the input CSV file
urls = read_urls_from_csv(input_csv_path)

# Initialize a list to store scraped data
scraped_data = []

# Iterate over each URL and scrape the required information
for url in urls:
    address, latitude, longitude = scrape_address_latitude_longitude(url)
    if address and latitude and longitude:
        scraped_data.append({'Address': address, 'Latitude': latitude, 'Longitude': longitude})

# Write the scraped information to an output CSV file
write_to_csv(scraped_data, output_csv_path)

print(f"Data has been written to {output_csv_path}.")
