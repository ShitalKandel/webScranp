import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


url = "https://www.jobsnepal.com/category"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

def job_category(url):
    resp = requests.get(url,header=headers)
    cate = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        categories = soup.find_all("a", class_="jobs-category", limit=8)
        for i in categories:
            cate.append(i.get_text())
            job_string = str(cate)
            job_cate = (
            job_string.strip("[]")
            .replace("\\n", "")
            .strip()
            .replace(" ", "")
            .strip()
            )
            li = list([word.strip("'") for word in job_cate.split(",")])
            print("\t<--Job by categories-->")
    for i, item in enumerate(li, start=1):
        print(f"{i}: {item}")
    return li


def get_jobs_from_category(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        a_links = soup.find_all("a", class_="jobs-category", limit=10)
        href_list = [link["href"] for link in a_links]

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

            join_job_category = selected_link
            job_details = get_job_urls_from_category(join_job_category)
            return job_details
        else:
            print("Invalid index. Please enter a valid index.")


def get_job_urls_from_category(category_url: str) -> list[str | None] | None:
    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        h2_tags = soup.find_all("h2", class_="job-title")

        links: list[str | None] = [
        div.find("a")["href"] if div.find_all("a") else None for div in h2_tags
        ]
        return links
    else:
        print(f"Error: Unable to fetch: {response.status_code}")
    return None


def get_job_details(url) -> dict[str, str] | None:
    job_resp = requests.get(url)
    if job_resp.status_code == 200:
        soup = BeautifulSoup(job_resp.text, "html.parser")

        title_tag = soup.find("h1", class_="job-title")
        location_tag = soup.find("span", class_="font-weight-semibold")

        posted_on_tags = soup.find("span", class_="job-posted-on")
        deadline_tag = soup.find("span", class_="apply-deadline")

    if not (posted_on_tags and deadline_tag and title_tag and location_tag):
        print(f"job details not found for {url}")
        return None
    posted_on = "".join(posted_on_tags.text.strip()[3:].split()[2:])
    deadline = "".join(deadline_tag.text.strip()[3:].split()[2:])

    return {
    "title": title_tag.text.strip(),
    "location": location_tag.text.strip(),
    "Posted_On": posted_on,
    "Deadline": deadline,
    }


def write_data(jobs: list[dict[str, str]]) -> None:
    csv_file_path = "dec_17.csv"

    with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["title", "location", "Posted_On", "Deadline"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if csv_file.tell() == 0:
            writer.writeheader()

        for job_detail in jobs:
            writer.writerow(job_detail)


def main() -> None:
    job_links = get_jobs_from_category(url)

    if not job_links:
        print("no jobs found")
        return

    jobs_details = list()

    for job_link in job_links:
        job_detail = get_job_details(job_link)
        jobs_details.append(job_detail)

    write_data(jobs_details)



main()