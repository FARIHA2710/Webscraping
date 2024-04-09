#download and generate latitude longitide in csv using the Object_URL column pregenetared, brings 12 decimals

#this script runs every 6 minutes to avoid error while data scraping also, it brings 800 data each time with maximum decimal point available
import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
import time
import os  # Import os module to check file existence

def read_urls_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    urls = df["Object_URL"].tolist()
    return urls

def scrape_address_latitude_longitude(url):
    try:
        headers_request = {'Accept-Language': 'en-US,en;q=0.9'}
        response = requests.get(url, headers=headers_request)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            address = soup.find('h1').text.strip()
            script_tags = soup.find_all('script')
            latitude = None
            longitude = None
            for script in script_tags:
                if 'initMap' in script.text:
                    # Modified to capture latitude and longitude without rounding
                    match = re.search(r'initMap\(([\d.-]+\.\d+),\s*([\d.-]+\.\d+)', script.text)
                    if match:
                        latitude = match.group(1)
                        longitude = match.group(2)
                        break
            return address, latitude, longitude
        else:
            return None, None, None
    except Exception as e:
        return None, None, None

def write_to_csv(data, csv_file_path):
    file_exists = os.path.exists(csv_file_path)
    with open(csv_file_path, mode='a', newline='', encoding='utf-8-sig') as csv_file:
        fieldnames = ['Address', 'Latitude', 'Longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

def chunk_urls(urls, chunk_size):
    for i in range(0, len(urls), chunk_size):
        yield urls[i:i + chunk_size]

input_csv_path = 'Building_data.csv'
output_csv_path = 'location_data_12deci.csv'  # Use a single output CSV file

urls = read_urls_from_csv(input_csv_path)

for index, chunk in enumerate(chunk_urls(urls, 800), start=1):
    scraped_data = []
    for url in chunk:
        address, latitude, longitude = scrape_address_latitude_longitude(url)
        # Ensure data is appended even if some fields are None
        scraped_data.append({'Address': address or 'Not Found', 'Latitude': latitude or 'Not Found', 'Longitude': longitude or 'Not Found'})
    write_to_csv(scraped_data, output_csv_path)
    processed_count = index * 800 if index * 800 < len(urls) else len(urls)
    print(f"Processed {processed_count} URLs.")

    if processed_count < len(urls):  # Check if there are more URLs to process
        print("Waiting 6 minutes before processing the next chunk...")
        time.sleep(360)  # Wait for 7 minutes

print("All data has been processed and written to the CSV file.")
