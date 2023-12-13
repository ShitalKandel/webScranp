import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://www.jobsnepal.com/')
soup = BeautifulSoup(response.content, 'html.parser')

title_tags = soup.find_all('h2', class_='job-title')
location_tags = soup.find_all('span', class_='location')


def get_job_details(url):
    details_response = requests.get(url)
    details_soup = BeautifulSoup(details_response.content, 'html.parser')

    span_posted = details_soup.find('span', class_='job-posted-on')
    span_deadlines = details_soup.find('span', class_='apply-deadlines')

    posted_date = span_posted.text.strip() if span_posted else 'N/A'
    deadline = span_deadlines.text.strip() if span_deadlines else 'N/A'
    
    return posted_date, deadline


def job_dcp():
    description = []

    for title_tag, location_tag in zip(title_tags, location_tags):
        title = title_tag.text.strip()
        location = location_tag.text.strip()

        job_detail_url = 'https://www.jobsnepal.com/' + title_tag.find('a')['href']
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
