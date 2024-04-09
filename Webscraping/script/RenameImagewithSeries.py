#in the data downloaded with ehr code name, this script converts the data type and makes the name combines with series and ehr

import pandas as pd
import os

# Function to rename images based on ehr_gid and Series_Project
def rename_images(image_dir, excel_path):
    # Read the Excel file into a DataFrame and ensure ehr_gid is a string
    df = pd.read_excel(excel_path, sheet_name='Sheet1')
    df['ehr_gid'] = df['ehr_gid'].astype(str).str.strip()

    # Ensure the image directory exists
    if not os.path.isdir(image_dir):
        print(f"The specified image directory does not exist: {image_dir}")
        return

    # Dictionary to map ehr_gid to Series_Project
    ehr_gid_to_series = df.set_index('ehr_gid')['Series_Project'].to_dict()

    # Iterate over each file in the image directory
    for filename in os.listdir(image_dir):
        # Extract the EHR code from the filename (without the extension)
        ehr_code = os.path.splitext(filename)[0]

        # If the ehr_code is found in the DataFrame, rename the file
        if ehr_code in ehr_gid_to_series:
            series_project_safe = ehr_gid_to_series[ehr_code].replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
            new_filename = f"{series_project_safe}_{ehr_code}.jpg"
            os.rename(
                os.path.join(image_dir, filename),
                os.path.join(image_dir, new_filename)
            )
            print(f"Renamed {filename} to {new_filename}")
        else:
            print(f"No matching ehr_gid found for {filename}")

# Paths to the image directory and Excel file
image_directory_path = 'downloaded_images2'
excel_file_path = 'Data/FilteredUrls.xlsx'

# Call the function to start renaming images
rename_images(image_directory_path, excel_file_path)
