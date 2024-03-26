import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def read_urls_from_csv(csv_file_path, start_index, end_index):
    # Use pandas to easily read the specific column from the CSV and slice the desired range
    df = pd.read_csv(csv_file_path)
    urls = df["Object_URL"].tolist()

    return urls[start_index-1:end_index]  # Adjust for zero-based indexing

def scrape_address_latitude_longitude(url):
    try:
        headers_request = {'Accept-Language': 'en-US,en;q=0.9'}  # Request English content
        response = requests.get(url, headers=headers_request)
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
                        latitude = round(float(match.group(1)), 12)
                        longitude = round(float(match.group(2)), 12)
                        break
                        #latitude, longitude = match.groups()
                        #break
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

# Define the range of URLs to process
start_index = 14600 # Start from the first URL
end_index =14769  # End at the 999th URL

# Input and output CSV file paths
input_csv_path = 'Building_data.csv'
#output_csv_path = 'location918_1300.csv'
output_csv_path = 'location2.csv'#1301-1800

# Read URLs from the input CSV file within the specified range
urls = read_urls_from_csv(input_csv_path, start_index, end_index)

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
