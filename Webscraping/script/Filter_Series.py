# Loads 'Series_Project' values from "Datatest.xlsx", collecting unique values.
# Loads URL data from "Urls.csv", URLS.csv have same data as "Datatest.xlsx" has in sheet1.
# Filters the "Urls.csv" data to include entries matching the 'Series_Project' values from "Datatest.xlsx".
#Saves the filtered data to a new Excel file named "FilteredUrls.xlsx".

import pandas as pd

def filter_urls_by_series_project(datatest_excel_path, urls_csv_path, output_excel_path):
    # Attempt to load the Series_Project data from the Excel file
    try:
        df_excel = pd.read_excel(datatest_excel_path, sheet_name='Sheet3', engine='openpyxl')
        print("Columns in Excel:", df_excel.columns)  # Debug: Print column names
        series_projects = df_excel['Series_Project'].unique().tolist()
    except Exception as e:
        print("Error reading Series_Project from Excel:", e)
        return

    # Attempt to load and filter the CSV data
    try:
        df_csv = pd.read_csv(urls_csv_path)
        print("Columns in CSV:", df_csv.columns)  # Debug: Print column names
        print("Total URLs:", len(df_csv))

        filtered_df = df_csv[df_csv['Series_Project'].isin(series_projects)]
    except Exception as e:
        print("Error filtering CSV data:", e)
        return

    # Save the filtered data to a new Excel file
    try:
        filtered_df.to_excel(output_excel_path, index=False, engine='openpyxl')
        print(f"Filtered data has been saved to {output_excel_path}")
        print("Filtered URLs:", len(filtered_df))
    except Exception as e:
        print(f"Error saving data to Excel file: {e}")

# Specify your file paths
datatest_excel_path = 'Datatest.xlsx'
urls_csv_path = 'Urls.csv'
output_excel_path = 'FilteredUrls.xlsx'

filter_urls_by_series_project(datatest_excel_path, urls_csv_path, output_excel_path)

