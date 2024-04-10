import pandas as pd
import os

# Path to your Excel file and the main directory containing the folders
excel_file_path = 'Data\FilteredUrls.xlsx'
main_directory_path = 'downloaded_images2'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name='Sheet1')

# Create a dictionary to map Series_Project to Series_Project_eng
mapping = pd.Series(df.Series_Project_eng.values,index=df.Series_Project).to_dict()

# Iterate over each folder in the main directory
for folder_name in os.listdir(main_directory_path):
    folder_path = os.path.join(main_directory_path, folder_name)
    # Check if it's actually a folder/directory
    if os.path.isdir(folder_path):
        # If the folder name is in our mapping, rename it
        if folder_name in mapping:
            new_folder_name = mapping[folder_name]
            new_folder_path = os.path.join(main_directory_path, new_folder_name)
            os.rename(folder_path, new_folder_path)
            print(f"Renamed '{folder_name}' to '{new_folder_name}'")

print("Folder renaming process is complete.")
