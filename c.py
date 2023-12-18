import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


url = "https://www.jobsnepal.com/category"

def job_category(url):
    resp = requests.get(url)
    cate = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        categories = soup.find_all('a', class_='jobs-category', limit=8)
        for i in categories:
            cate.append(i.get_text())

        job_string = str(cate)
        job_cate = job_string.strip("[]").replace("\\n", "").strip().replace("       ","").strip()

        li = list([word.strip("'") for word in job_cate.split(",")])
        
        print("\t<--Job by categories-->")
        for i, item in enumerate(li, start=1):
            print(f"{i}: {item}")

        return li  

def job_category_links(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        a_links = soup.find_all('a', class_='jobs-category', limit=10)
        href_list = [link['href'] for link in a_links]

        job_categories = job_category(url)

        print("\n<--Associating job categories with URLs-->")
        for i, (item, url) in enumerate(zip(job_categories, href_list), start=1):
            print(f"{i}: {item} - {url}")

        job_type_input = int(input("\nEnter the index according to the list: "))
        if 1 <= job_type_input <= len(job_categories):
            selected_category = job_categories[job_type_input - 1]
            selected_link = href_list[job_type_input - 1]
            print(f"\nSelected Job Category: {selected_category}")
            print(f"Opening link: {selected_link}")

            join_job_category = urljoin(url, selected_link)

            job_details = fetch_job_details(join_job_category)
            return job_details
        else:
            print("Invalid index. Please enter a valid index.")


def get_tags(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        div_location_tags = soup.find_all("div", class_="d-flex align-items-center pl-1 pr-1 py-1")
        
        title_tags = []
        for div_tag in div_location_tags:
            h2_tag = div_tag.find('h2', class_='job-title')
            if h2_tag:
                title_tags.append(h2_tag.text.strip())

        location_tags = [
            div.find("div", class_="job-location").text.strip() if div.find("div", class_="job-location") else None
            for div in div_location_tags
        ]

        div_tags = soup.find_all("div", class_="card-body")
        links = [
            div.find("a")["href"] if div.find("a") else None
            for div in div_tags
        ]

        return title_tags, location_tags, links
    else:
        print(f"Error: Unable to fetch: {response.status_code}")
        return None, None, None


def get_job_details(url):
    job_resp = requests.get(url)
    if job_resp.status_code == 200:
        job_soup = BeautifulSoup(job_resp.text, "html.parser")
        job_open_on_tag = job_soup.find("span", class_="job-posted-on")
        deadline_tag = job_soup.find("span", class_="apply-deadline")

        if job_open_on_tag and deadline_tag:
            job_open_on = job_open_on_tag.text.strip()[3:]
            deadline = deadline_tag.text.strip()[3:]
            return job_open_on, deadline
        else:
            return None, None
    

def fetch_job_details(url):
    description = []
    processed_urls = set()

    tags = get_tags(url)

    if not tags:
        print("No tags found")

    title_tags, location_tags, links = tags

    for title_tag, location_tag, link in zip(title_tags, location_tags, links):
        title = title_tag.text.strip()
        location = location_tag.text.strip()
        job_detail_url = urljoin(url, link)

        if job_detail_url.startswith("http") and job_detail_url not in processed_urls:
            job_open, deadline_job = get_job_details(job_detail_url)

            if job_open and deadline_job:
                job_open = " ".join(job_open.split()[2:])
                deadline_job = " ".join(deadline_job.split()[2:])

                values = {
                    "title": title,
                    "location": location,
                    "Posted_On": job_open,
                    "Deadline": deadline_job,
                }
                description.append(values)
                processed_urls.add(job_detail_url)
            else:
                print(f"Skipping job_detail_url without details: {job_detail_url}")
        elif not job_detail_url.startswith("http"):
            print(f"Skipping invalid job_detail_url: {job_detail_url}")

    return description


data = fetch_job_details(url)
job_category_links(url)


csv_file_path = "dec_17.csv"

with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["title", "location", "Posted_On", "Deadline"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if csv_file.tell() == 0:
        writer.writeheader()

    for row in data:
        writer.writerow(row)

print(f"Data has been saved to {csv_file_path}")


