import pandas as pd
import requests
import os
import string


def download_image(url, ehr_kood, index):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Clean up the Series_Project and EHR_Kood for use in filenames
            #file_name_part1 = "_".join(str(series_project).split()).replace('/', '_')
            file_name_part2 = str(ehr_kood).replace('/', '_')

            # Combine parts to create a unique file name and add the image extension
            #file_name = f"{file_name_part1}_{file_name_part2}_{index}.jpg"
            file_name = f"{file_name_part2}.jpg"
            encoded_file_name = file_name.encode('utf-8')

            # Remove characters that are invalid for filenames
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            valid_file_name = "".join(char for char in file_name if char in valid_chars)

            # Save the image
            file_path = os.path.join('downloaded_images2', valid_file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_path}")
        else:
            print(f"Failed to download image from {url} - Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")


# Create the directory for downloaded images if it doesn't exist
os.makedirs('downloaded_images', exist_ok=True)

# Read the Excel file into a DataFrame
file_path = 'Data\FilteredUrls.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Iterate through the DataFrame and download images from each non-empty PhotoURL
for index, row in df.iterrows():
    photo_url = row['PhotoURL']
    if pd.notna(photo_url):
        # Extract Series_Project and EHR_Kood, using default values if they are not present
        #series_project = row['Series_Project'] if pd.notna(row['Series_Project']) else 'NoSeriesProject'
        ehr_kood = row['ehr_gid'] if pd.notna(row['ehr_gid']) else 'NoEHRKood'
        #download_image(photo_url, series_project, ehr_kood, index)
        download_image(photo_url,  ehr_kood, index)

print("Downloaded all images.")
