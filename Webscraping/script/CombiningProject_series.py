#In this script it fills the black series in Final EHR with Project column values only in the empty fiels
#
# import pandas as pd
#
# # Define the path to your Excel file
# file_path = 'Data\Datatest.xlsx'
#
# # Load the Excel file
# df = pd.read_excel(file_path, sheet_name='Sheet1')
#
# # Fill in blank values in 'Series_Project' with values from 'Project'
# df['Series_Project'] = df['Series_Project'].fillna(df['Project'])
#
# # Save the modified DataFrame back to the same Excel file and sheet
# # Please ensure the Excel file is closed before running this script to avoid errors
# with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
#     df.to_excel(writer, sheet_name='Sheet1', index=False)
#
#
import pandas as pd

# Define the path to your Excel file
file_path = 'Data/Final EHR.xlsx'

# Read the entire Excel file
xls = pd.ExcelFile(file_path)

# Load the specific sheet into a DataFrame
df = pd.read_excel(xls, sheet_name='Sheet1')

# Perform the operation
df['Series_Project2'] = df['Series'].fillna(df['Project'])

# Prepare a writer object using pd.ExcelWriter
# and specify the engine and mode accordingly
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    # Write modified DataFrame back to its original sheet,
    # replacing its content. Loop through all sheets to ensure
    # no data is lost from other sheets.
    for sheet_name in xls.sheet_names:
        if sheet_name == 'Sheet1':
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            pd.read_excel(xls, sheet_name).to_excel(writer, sheet_name=sheet_name, index=False)



