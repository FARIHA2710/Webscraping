# import pandas as pd
#
# # Load the original Excel file
# original_file_path = 'matched_addresses2.xlsx'
# df = pd.read_excel(original_file_path)
#
# # Function to clean the "Series" values based on the given conditions
# def clean_series_value(value):
#     if pd.isnull(value):
#         return value  # Return None if value is already NaN
#     elif str(value).strip()[0].isdigit():
#         return value  # Return the value as is if it strictly starts with a number
#     else:
#         return None  # Replace with None if it doesn't start with a number
#
#
# # Apply the cleaning function to the "Series" column
# df['Series'] = df['Series'].apply(clean_series_value)
#
# # Save the cleaned DataFrame to a new Excel file
# cleaned_file_path = 'numeric series.xlsx'
# df.to_excel(cleaned_file_path, index=False)
#
# print(f"Data cleaned and saved to {cleaned_file_path}")
#
# import pandas as pd
#
# # Replace 'your_file.xlsx' with the path to your Excel file
# file_path = 'numeric series.xlsx'
#
# # Load the Excel file
# df = pd.read_excel(file_path)
#
# # Ensure there is a column named 'Series' in your Excel
# if 'Series' in df.columns:
#     # Find unique values in the 'Series' column
#     unique_series = df['Series'].unique()
#
#     # Print the count of unique values
#     print(f"Total unique series types: {len(unique_series)}")
#
#     # Print each unique value
#     print("Unique series values are:")
#     for series in unique_series:
#         print(series)
# else:
#     print("Column 'Series' not found in the Excel file.")
#
#
# # Assuming df is your DataFrame after applying the previous cleaning steps
#
# # Remove rows where the "Series" column is NaN or empty
# df.dropna(subset=['Series'], inplace=True)
#
# # Save the cleaned DataFrame to a new Excel file, ensuring rows with empty "Series" are not included
# cleaned_file_path = 'numeric series.xlsx'  # Update the path as needed
# df.to_excel(cleaned_file_path, index=False)
#
# print(f"Rows with NaN or empty 'Series' values removed. Data saved to {cleaned_file_path}")
#

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


