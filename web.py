import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

response = requests.get('https://www.jobsnepal.com/', headers=headers)
response = response.content
soup = BeautifulSoup(response, 'html.parser')

# Job option
itJob = soup.find_all('div', class_='col-sm-6 col-md-6 col-lg-4 mb-3')
title_tags = soup.find_all('h2', class_='job-title')
location_tags = soup.find_all('span', class_='location')

# use <a href = 'job-posting-detail__link'>

a_tag_response = requests.get('https://www.jobsnepal.com/{title_tags}',headers=headers)
a_tag_response = a_tag_response.content
a_soup = BeautifulSoup(a_tag_response, 'html.parser')

print(a_soup)

span_posted = a_soup.find('span', class_='job-posted-on')
span_deadlines = a_soup.find('span', class_='apply-deadlines')


# pass parameter for the function
def dcp():
    description = [] # try using dict data structure
    
    # zip ko research
    for ttl, lct in zip(title_tags, location_tags):
        title = ttl.text.strip()
        location = lct.text.strip()
        
        # split by which separator
        print(span_posted)
        posted_date_split = span_posted.text.strip().split()[-3:]
        posted_date_joined = " ".join(posted_date_split)

        if span_deadlines is not None:
            deadline_split = span_deadlines.text.strip().split()[-3:]
            deadline_joined = " ".join(deadline_split)
        else:
            deadline_joined = "N/A"


        description.append({title, location, posted_date_joined, deadline_joined})

    return description

data = dcp()

csv_file_path = 'job_data1.csv'

# Write data to CSV
with open(csv_file_path, 'w', newline='') as csv_file:   # use best file mode
    fieldnames = ['title', 'location', 'Posted_On', 'Deadline']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

        # Write data rows
    for row in data:
        writer.writerow(row)  # potential error

print(f'Data has been saved to {csv_file_path}')


# print(job_ttl())

'''
    location_tag = h2.find('span', class_='job-company')
    expiry = h2.find('h2',span = 'job-expiry-date')
    # print(title_tag)


    if title_tag and location_tag:
        title = title_tag.text.strip()
        location = location_tag.text.strip()
        a = expiry.text.strip()
        # print(f"Title: {title}, Location: {location}, Applied Untill: {a}")

        h2_title = title_tag.attrs('title')
    # print(h2_title)

# print(title_tag)'''
