#In this script it fills the black series in Final EHR with Project column values only in the empty fiels

import pandas as pd

# Define the path to your Excel file
file_path = 'Datatest.xlsx'

# Load the Excel file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Fill in blank values in 'Series_Project' with values from 'Project'
df['Series_Project'] = df['Series_Project'].fillna(df['Project'])

# Save the modified DataFrame back to the same Excel file and sheet
# Please ensure the Excel file is closed before running this script to avoid errors
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)


