#Generates the whole table
import requests
from bs4 import BeautifulSoup
import csv
base_url = 'https://photobuildings.com'
list_url_pattern = '/list.php?uid=39955&page={}'
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
    # Loop through the desired range of pages
    for page_number in range(1, 3):  # Replace 3 with the total number of pages + 1
        page_url = base_url + list_url_pattern.format(page_number)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.select_one('.rtable table')

        if not table:  # If there is no table on the page, break the loop
            break
    # Loop through the desired range of pages
    for page_number in range(1, 3):  # Replace 3 with the total number of pages + 1
        page_url = base_url + list_url_pattern.format(page_number)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.select_one('.rtable table')

        if not table:  # If there is no table on the page, break the loop
            break

        for row in table.find_all('tr')[1:]:
            # Extract the desired columns
            photo_url_td = row.find_all('td')[0]
            building_url_td = row.find_all('td')[1]
            photo_url = base_url + photo_url_td.find('a')['href'] if photo_url_td.find('a') else ''
            building_url = base_url + building_url_td.find('a')['href'] if building_url_td.find('a') else ''
            street_building_nr_text = building_url_td.get_text(strip=True)
            project = row.find_all('td')[2].get_text(strip=True)
            floors = row.find_all('td')[4].get_text(strip=True)
            built = row.find_all('td')[6].get_text(strip=True)
            name_purpose = row.find_all('td')[7].get_text(strip=True)

            # Create a data row excluding 'Constr.start' and 'Architects'
            data = [photo_url, building_url, street_building_nr_text, project, floors, built, name_purpose]
            writer.writerow(data)

    print('Data has been successfully written to buildings_data.csv')
