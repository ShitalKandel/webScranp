import requests
from bs4 import BeautifulSoup
import csv
import smtplib


url = 'https://www.jobsnepal.com/'

def get_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tags = soup.find_all('h2', class_='job-title')
        location_tags = soup.find_all('span', class_='location')
        links = soup.find_all('a', href=True)

        return title_tags, location_tags, links
    else:
        print(f"Error: Unable to fetch:{response.status_code}")
        return None, None, None

title_tags, location_tags, links = get_links(url)

def get_job_details(job_url):
    job_resp = requests.get(job_url)
    if job_resp.status_code == 200:
        job_soup = BeautifulSoup(job_resp.text, 'html.parser')
        job_open_on_tag = job_soup.find('span', class_='job-posted-on')
        deadline_tag = job_soup.find('span', class_='apply-deadline')

        if job_open_on_tag and deadline_tag:
            job_open_on = job_open_on_tag.text.strip()
            deadline = deadline_tag.text.strip()
            return job_open_on, deadline
        else:
            return None, None
    

def job_dcp():
    description = []
    processed_urls = set()

    for title_tag, location_tag, link in zip(title_tags, location_tags, links):
        title = title_tag.text.strip()
        location = location_tag.text.strip()
        job_detail_url = link['href']

        if job_detail_url.startswith('http') and job_detail_url not in processed_urls:
            job_open_on, deadline = get_job_details(job_detail_url)

            if job_open_on and deadline:
                values = {'title': title, 'location': location, 'Posted_On': job_open_on, 'Deadline': deadline}
                description.append(values)
                processed_urls.add(job_detail_url)
            else:
                print(f"Skipping job_detail_url without details: {job_detail_url}")
        elif not job_detail_url.startswith('http'):
            print(f"Skipping invalid job_detail_url: {job_detail_url}")

    return description

data = job_dcp()

csv_file_path = 'job_data1.csv'

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'location', 'Posted_On', 'Deadline']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if csv_file.tell() == 0:
        writer.writeheader()

    for row in data:
        writer.writerow(row)

print(f'Data has been saved to {csv_file_path}')


# smptlib = smptlib.conne
