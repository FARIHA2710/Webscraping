import csv
import requests
from bs4 import BeautifulSoup
import os

def download_image_from_url(url, output_folder, image_id='ph'):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.find('img', id=image_id)
        if img_tag and img_tag.get('src'):
            img_src = img_tag['src']
            if img_src.startswith('/'):
                img_src = f'https://{url.split("/")[2]}{img_src}'
            img_response = requests.get(img_src, stream=True)
            if img_response.status_code == 200:
                filename = os.path.basename(img_src).split('?')[0]
                if not filename.lower().endswith('.jpg'):
                    filename += '.jpg'
                save_path = os.path.join(output_folder, filename)
                with open(save_path, 'wb') as f:
                    f.write(img_response.content)
                print(f'Image downloaded: {filename}')
            else:
                print(f'Failed to download the image: {img_src}')
        else:
            print(f'No <img> tag with id="{image_id}" found.')
    else:
        print(f'Failed to retrieve the webpage: {url}')

def read_urls_from_csv(csv_file_path, column_name='Photo URL', limit=15):
    urls = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row[column_name].strip()
            if url:  # Only add non-empty URLs
                urls.append(url)
            if len(urls) == limit:  # Stop when the limit is reached
                break
    return urls

# Specify the CSV file path and output folder
csv_file_path = 'buildings_data.csv'
output_folder = 'downloaded_images'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the image URLs from the CSV file
image_urls = read_urls_from_csv(csv_file_path)

# Download the image for each URL
for url in image_urls[:15]:  # Limit to the first 10 URLs
    download_image_from_url(url, output_folder)
