# #Loads data from "Final EHR.xlsx" into a pandas DataFrame.
# Standardizes address fields ('Address' and 'ads_lahiaa') by removing punctuation, spaces, and converting to lowercase, saving the results in new columns ('Address_Clean' and 'ads_lahiaa_Clean').
#  Applies fuzzy matching between the cleaned address columns using `fuzz.ratio`, and stores the match scores in a new column ('Match_Score').
#  Filters rows in the DataFrame to only include those with a match score equal to or higher than a defined threshold (e.g., 90).
#  Saves the filtered DataFrame with high match scores to a new Excel file named "matched_addresses.xlsx".

import pandas as pd
from fuzzywuzzy import fuzz

# Load the Excel file into a pandas DataFrame
excel_path = 'Final EHR.xlsx'
df = pd.read_excel(excel_path)

# Define a function to standardize addresses
def clean_address(address):
    if pd.isnull(address):
        return ""
    return address.replace('.', '').replace(',', '').replace(' ', '').lower()

# Apply the function to clean both address fields
df['Address_Clean'] = df['Address'].apply(clean_address)
df['ads_lahiaa_Clean'] = df['ads_lahiaa'].apply(clean_address)

# Use fuzzy matching to compare addresses and create a match score
df['Match_Score'] = df.apply(lambda x: fuzz.ratio(x['Address_Clean'], x['ads_lahiaa_Clean']), axis=1)

# Define your own threshold for matching
some_threshold = 90  # For example, you may consider 80 as a good match score

# Filter the DataFrame to only include rows with a high match score
matched_df = df[df['Match_Score'] >= some_threshold]

# Save the matched results to a new Excel file
matched_excel_path = 'matched_addresses.xlsx'
matched_df.to_excel(matched_excel_path, index=False)


#
# import pandas as pd
# from fuzzywuzzy import fuzz
#
# # Load the Excel file into a pandas DataFrame
# excel_path = 'Final EHR.xlsx'  # Update this path to your actual Excel file location
# df = pd.read_excel(excel_path)
#
# # Define a function to standardize addresses
# def clean_address(address):
#     if pd.isnull(address):
#         return ""
#     # Remove punctuation, extra spaces, and make lowercase for standardization
#     return address.replace('.', '').replace(',', '').replace(' ', '').lower()
#
# # Apply the function to clean both address fields for comparison
# df['Address_Clean'] = df['Address'].apply(clean_address)
# df['ads_lahiaa_Clean'] = df['ads_lahiaa'].apply(clean_address)
#
# # Use fuzz.token_set_ratio for a more lenient comparison of addresses
# df['Match_Score'] = df.apply(lambda x: fuzz.token_set_ratio(x['Address_Clean'], x['ads_lahiaa_Clean']), axis=1)
#
# # Define your threshold for matching
# # You may need to adjust this based on the results you're getting
# match_threshold = 80  # Example threshold, can be adjusted
#
# # Filter the DataFrame to only include rows with a match score at or above the threshold
# matched_df = df[df['Match_Score'] >= match_threshold]
#
# # Save the matched results to a new Excel file
# matched_excel_path = 'matched_addresses2.xlsx'  # Update this path to where you want to save the results
# matched_df.to_excel(matched_excel_path, index=False)

