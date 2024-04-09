#creating urls using object_url column by webscraping , use Object_URL s generated from script filter_series.py

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the function to process each URL and return the final photo URL
def get_photo_url(object_url, base_url="https://photobuildings.com/"):
    try:
        # Send a GET request to the object URL
        response = requests.get(object_url)
        # Raise an HTTPError for bad responses (4XX, 5XX)
        response.raise_for_status()
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the first img tag with class 'f'
        img_tag = soup.find('img', class_='f')
        if img_tag and 'src' in img_tag.attrs:
            src_attr = img_tag['src']
            # Modify the src attribute to remove '_s' before '.jpg'
            modified_src = src_attr.replace('_s.jpg', '.jpg')
            # Combine the base URL with the modified src attribute
            final_url = base_url + modified_src
            print(f"Processed URL: {object_url} -> {final_url}")
            return final_url
    except Exception as e:
        print(f"Error processing URL {object_url}: {e}")
    return None

# Specify the path to your Excel file
file_path = 'FilteredUrls.xlsx'

try:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    # Apply the get_photo_url function to each URL in the Object_URL column
    df['PhotoURL'] = df['Object_URL'].apply(get_photo_url)
    print("Processing complete. Here's a preview:")
    print(df.head())  # Print the first few rows of the DataFrame as a preview

    # Write the modified DataFrame back to the same Excel file using the openpyxl engine
    with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    print(f"Updated Excel file saved: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")


# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
#
# # Function to process each URL and return the final photo URL
# def get_photo_url(object_url, base_url="https://photobuildings.com/"):
#     response = requests.get(object_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     img_tag = soup.find('img', class_='f')
#     if img_tag and 'src' in img_tag.attrs:
#         src_attr = img_tag['src']
#         modified_src = src_attr.replace('_s.jpg', '.jpg')
#         return base_url + modified_src
#     return None
#
# # Read the Excel file
# file_path = 'FilteredUrls.xlsx'
# df = pd.read_excel(file_path, sheet_name='Sheet1')
#
# # Process each URL and collect the results
# df['PhotoURL'] = df['Object_URL'].apply(get_photo_url)
#
# # Write the modified DataFrame back to the same Excel file
# with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
#     df.to_excel(writer, sheet_name='Sheet1', index=False)
#

# 1. The script reads a list of website URLs from the `Object_URL` column in the 'Sheet1' of an Excel file named 'FilteredUrls.xlsx', which contains links to specific pages on the "photobuildings.com" website.
#
# 2. For each website URL, it sends a request to fetch the corresponding web page, searches for a specific image tag (`img` with class 'f'), and extracts the image source URL (`src`) from it.
#
# 3. It modifies the extracted image source URL by removing a specific substring ('_s.jpg') to presumably convert it into a higher resolution image URL, creating a new list of modified image URLs.
#
# 4. This list of modified image URLs is added to the original DataFrame as a new column named `PhotoURL`, effectively pairing each original web page URL with its corresponding modified image URL.
#
# 5. Finally, the updated DataFrame, now containing both the original web page URLs and the new higher resolution image URLs, is written back to the same Excel file ('FilteredUrls.xlsx'), updating 'Sheet1' with the new information, thereby automating the process of enhancing a list of image links for further use.