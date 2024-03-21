import csv
import requests
from bs4 import BeautifulSoup


def read_urls_from_csv(csv_file_path):
    """Read URLs from a CSV file under the specified column header."""
    urls = []
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row["Street, Building Nr URL"])
    return urls


def scrape_data(url, headers=None):
    """Scrape data from the given URL, requesting the English version, including the Address."""
    base_url = 'https://photobuildings.com/'
    headers_request = {'Accept-Language': 'en-US,en;q=0.9'}  # Request English content
    response = requests.get(url, headers=headers_request)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    data = {'Address': soup.find('h1').text.strip()}  # Add Address data

    # Continue with other data extraction
    for header in soup.find_all('td', class_='ds nw'):
        header_text = header.text.strip()
        corresponding_value_td = header.find_next('td', class_='d')

        # Check for the 'Series:' header and if it has an <a> tag
        if header_text == 'Series:' and corresponding_value_td and corresponding_value_td.find('a'):
            # Extract the href attribute and create a hyperlink
            href = corresponding_value_td.find('a')['href']
            # Prepend the base URL if the href is a relative path
            href = base_url + href if not href.startswith(('http://', 'https://')) else href
            value = f'=HYPERLINK("{href}", "{corresponding_value_td.text.strip()}")'
        else:
            value = corresponding_value_td.text.strip() if corresponding_value_td else "field missing"

        data[header_text] = value

    return data


def scrape_and_align_data(urls):
    """Scrape and align data from URLs."""
    if not urls:
        print("No URLs provided.")
        return []

    # Use the first URL to establish headers, including the new Address header
    first_data = scrape_data(urls[0])
    if first_data is None:
        print("Failed to establish template data.")
        return []

    # Establish a set of headers including additional ones found in second type URLs
    all_headers = ['Address']  # Start with Address
    all_headers.extend(first_data.keys())

    # Add headers found in second type URLs
    for url in urls[1:]:
        current_data = scrape_data(url)
        if current_data:
            all_headers.extend(h for h in current_data.keys() if h not in all_headers)

    headers = list(dict.fromkeys(all_headers))  # Remove duplicates while preserving order
    all_data = [headers]  # Initialize with headers

    # Scrape and align data for each URL according to the full set of headers
    for url in urls:
        current_data = scrape_data(url, headers)
        if current_data is None:
            print(f"Skipping URL due to failure in data retrieval: {url}")
            continue
        row = [current_data.get(header, "field missing") for header in headers]
        all_data.append(row)

    return all_data


def save_to_csv(data, csv_file_path):
    """Save the provided data to a CSV file."""
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
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
