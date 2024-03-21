import requests
from bs4 import BeautifulSoup
import csv

url = 'https://photobuildings.com/list.php?uid=39955'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.select_one('.rtable table')

# Define the headers, removing 'Constr.start' and 'Architects'
headers = ['Photo URL', 'Street, Building Nr URL', 'Street, Building Nr Text', 'Project', 'Floors', 'Built',
           'Name/purpose']

with open('buildings_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    for row in table.find_all('tr')[1:]:
        # Extract the desired columns
        photo_url = 'https://photobuildings.com' + row.find_all('td')[0].find('a')['href'] if row.find_all('td')[
            0].find('a') else ''
        building_url = 'https://photobuildings.com' + row.find_all('td')[1].find('a')['href'] if row.find_all('td')[
            1].find('a') else ''
        street_building_nr_text = row.find_all('td')[1].get_text(strip=True)
        project = row.find_all('td')[2].get_text(strip=True)
        floors = row.find_all('td')[4].get_text(strip=True)
        built = row.find_all('td')[6].get_text(strip=True)
        name_purpose = row.find_all('td')[7].get_text(strip=True)

        # Create a data row excluding 'Constr.start' and 'Architects'
        data = [photo_url, building_url, street_building_nr_text, project, floors, built, name_purpose]
        writer.writerow(data)

print('Data has been successfully written to buildings_data.csv')
