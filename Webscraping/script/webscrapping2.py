import csv
import requests
from bs4 import BeautifulSoup

def read_urls_from_csv(csv_file_path):
    """Read URLs from a CSV file under the 'Building Nr URL' column."""
    urls = []
    # Specify UTF-8 encoding explicitly to handle a wider range of characters
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ensure this matches the column name in your CSV
            urls.append(row["Street, Building Nr URL"])
    return urls

def scrape_data(url):
    """Scrape data from the given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    data_ds_nw = soup.find_all('td', class_='ds nw')
    data_d = soup.find_all('td', class_='d')
    return {ds_nw.text.strip(): d.text.strip() for ds_nw, d in zip(data_ds_nw, data_d)}

def scrape_and_align_data(urls):
    """Scrape and align data from URLs, using the first URL's data as the header template."""
    if not urls:
        print("No URLs provided.")
        return []

    # Scrape data from the first URL to establish headers
    template_data = scrape_data(urls[0])
    if template_data is None:
        print("Failed to establish template data.")
        return []

    headers = list(template_data.keys())
    all_data = [headers]  # Initialize with headers

    # Scrape and align data for each URL
    for url in urls:
        current_data = scrape_data(url)
        if current_data is None:
            print(f"Skipping URL due to failure in data retrieval: {url}")
            continue

        # Align current data with headers, filling missing fields
        row = [current_data.get(header, "field missing") for header in headers]
        all_data.append(row)

    return all_data

def save_to_csv(data, csv_file_path):
    """Save the provided data to a CSV file."""
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:  # Specify UTF-8 encoding here too
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"Data has been successfully saved to {csv_file_path}")

# The CSV file path where the URLs are stored
urls_csv_path = 'buildings_data.csv'
# Read URLs from the CSV
urls = read_urls_from_csv(urls_csv_path)

# Scrape and align data from the URLs
aligned_data = scrape_and_align_data(urls)

# Specify the output CSV file path
output_csv_path = 'scraped_data_aligned.csv'
# Save the aligned data to the output CSV
save_to_csv(aligned_data, output_csv_path)
