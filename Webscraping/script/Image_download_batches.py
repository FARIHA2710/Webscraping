#from created the photo urls from script Get_photourl_fromobject_url.py
import pandas as pd
import requests
import os
import string

# Function to download an image from a URL and save it with a specific filename
def download_image(url, address, local_gov, index):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Replace spaces with underscores and remove characters that are invalid for filenames
            file_name_part1 = "_".join(address.split())
            file_name_part2 = "_".join(local_gov.split())

            # Combine both parts with an index to ensure uniqueness and add the image extension
            file_name = f"{file_name_part1}_{file_name_part2}_{index}.jpg"

            # Define valid characters for filenames (including numbers)
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            valid_file_name = "".join(char for char in file_name if char in valid_chars)

            # Construct the full file path and write the image to a file
            file_path = os.path.join('downloaded_images', valid_file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded: {file_path}")
        else:
            print(f"Failed to download image from {url} - Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

# Ensure the directory for downloaded images exists
os.makedirs('downloaded_images', exist_ok=True)

# Read the Excel file into a DataFrame
file_path = 'FilteredUrls.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Iterate through the DataFrame, downloading images from each non-empty PhotoURL
for index, row in df.iterrows():
    photo_url = row['PhotoURL']
    if pd.notna(photo_url):
        # Ensure that 'Address' and 'Local_Government' are treated as strings and not numbers
        address = str(row['Address']) if pd.notna(row['Address']) else 'NoAddress'
        local_gov = str(row['Local_Government']) if pd.notna(row['Local_Government']) else 'NoLocalGov'
        download_image(photo_url, address, local_gov, index)


# # import requests
# #
# # # URL of the image to be downloaded
# # image_url = "https://photobuildings.com//photo/00/13/54/13548.jpg"
# #
# # # Send a GET request to the image URL
# # response = requests.get(image_url)
# #
# # # Check if the request was successful
# # if response.status_code == 200:
# #     # Open a file in binary write mode
# #     with open("downloaded_image.jpg", "wb") as file:
# #         # Write the content of the response to the file
# #         file.write(response.content)
# #     print("Image downloaded successfully.")
# # else:
# #     print("Failed to download the image.")


#
# 1. **Read Data**: The script opens an Excel file named 'FilteredUrls.xlsx', specifically the 'Sheet1' sheet, and reads the content into a pandas DataFrame, expecting two columns of interest: 'PhotoURL' for the image web address, and 'Address' and 'Local_Government' for constructing the filenames.
#
# 2. **Create Storage**: It checks for (and creates if necessary) a directory named 'downloaded_images' in the current working directory to store the downloaded images.
#
# 3. **Process Each Entry**: For each row in the DataFrame, the script checks if there's a valid URL in the 'PhotoURL' column; if there is, it proceeds to download the image, and if not, it skips to the next row.
#
# 4. **Save Images with Unique Names**: When downloading an image, it creates a filename from the 'Address' and 'Local_Government' fields by replacing spaces with underscores and appending a unique index number from the DataFrame row, ensuring the filename includes the full address and any numbers present.
#
# 5. **Handle Responses and Errors**: The script attempts to download the image and save it to the 'downloaded_images' directory, printing a success message with the file path for each download or an error message if something goes wrong, such as an HTTP error or a problem writing the file.