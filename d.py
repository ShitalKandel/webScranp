# import requests
# from bs4 import BeautifulSoup

# def get_links(url):
    
#     response = requests.get(url)

    
#     if response.status_code == 200:
        
#         soup = BeautifulSoup(response.text, 'html.parser')

    
#         links = soup.find_all('a')

        
#         for link in links:
#             href = link.get('href')
#             if href:
#                 print(href)
#     else:
#         print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")


# url_to_scrape = 'https://www.jobsnepal.com/'
# get_links(url_to_scrape)

import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.jobsnepal.com/'
resp = requests.get(url).text

def get_job_details(job_url):
    job_resp = requests.get(job_url)
    if job_resp.status_code == 200:
        job_soup = BeautifulSoup(job_resp.text, 'html.parser')
        # Extract the posted date and deadline from the job detail page
        posted_date = job_soup.find('div', class_='date-posted').text.strip()
        deadline = job_soup.find('div', class_='deadline').text.strip()
        return posted_date, deadline
    else:
        print(f"Error: Unable to fetch job details. Status code: {job_resp.status_code}")
        return None, None

def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tags = soup.find_all('h2', class_='job-title')
        location_tags = soup.find_all('span', class_='location')
        date_tags = soup.find_all('h5', class_='deadline')
        
        # Extract and print the href attribute of each link
        for link in soup.find_all('a', href=True):
            href = link['href']
            print(href)

        return title_tags, location_tags, date_tags
    else:
        print(f"Error: Unable to fetch:{response.status_code}")
        return None, None, None

# Call get_links and unpack the returned values
title_tags, location_tags, date_tags = get_links(url)

def job_dcp():
    description = []

    for title_tag, location_tag, date_tag in zip(title_tags, location_tags, date_tags):
        title = title_tag.text.strip()
        location = location_tag.text.strip()
        job_detail_url = title_tag.find('a')['href']
        print(job_detail_url)

        posted_date, deadline = get_job_details(job_detail_url)

        values = {'title': title, 'location': location, 'Posted_On': posted_date, 'Deadline': deadline}
        description.append(values)

    return description

data = job_dcp()

csv_file_path = 'job_data.csv'

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'location', 'Posted_On', 'Deadline']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if csv_file.tell() == 0:
        writer.writeheader()

    for row in data:
        writer.writerow(row)

print(f'Data has been saved to {csv_file_path}')
