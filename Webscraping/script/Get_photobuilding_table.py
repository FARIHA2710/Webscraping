import requests
from bs4 import BeautifulSoup
import csv

url = 'https://photobuildings.com/list.php?cid=5562/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Select the table within the 'rtable' div
table = soup.select_one('.rtable table')

# Extract table headers
headers = ['Photo', 'Street, Building Nr', 'Project', 'Architects', 'Floors', 'Constr.start', 'Built', 'Name/purpose']

# Open a CSV file to write to
with open('table_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the column headers

    # Iterate over each row in the table except the header row
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        # Extract data from each cell
        data = [
            'https://photobuildings.com' + col.find('a', href=True)['href'] if col.find('a', href=True) else '' for col
            in cols
        ]
        writer.writerow(data)

print('Data has been successfully written to table_data.csv')
