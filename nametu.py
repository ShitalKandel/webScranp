import requests
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
from urllib.parse import urljoin
from email.mime.multipart import MIMEMultipart
from email_automation_with_csv import automation,sender_email,sender_password,receivers

class JobScraper:
    def __init__(self, base_url, csv_file_path):
        self.base_url = base_url
        self.csv_file_path = csv_file_path
        self.processed_urls = set()

    def get_tags(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_tags = soup.find_all("h2", class_="job-title")
            location_tags = soup.find_all("span", class_="location")
            div_tags = soup.find_all("h2", class_="job-title")

            links = [urljoin(self.base_url, div.find("a")["href"]) if div.find("a") else None for div in div_tags]
            return title_tags, location_tags, links
        else:
            print(f"Error: Unable to fetch: {response.status_code}")
            return None, None, None

    def get_job_details(self, job_url):
        job_resp = requests.get(job_url)
        if job_resp.status_code == 200:
            job_soup = BeautifulSoup(job_resp.text, "html.parser")
            job_open_on_tag = job_soup.find("span", class_="job-posted-on")
            deadline_tag = job_soup.find("span", class_="apply-deadline")

            if job_open_on_tag and deadline_tag:
                job_open_on = " ".join(job_open_on_tag.text.strip().split()[2:])
                deadline = " ".join(deadline_tag.text.strip().split()[2:])
                return job_open_on, deadline
            else:
                return None, None

    def scrape_jobs(self):
        descriptions = []

        tags = self.get_tags(self.base_url)

        if not tags:
            print("No tags found")
            return descriptions

        title_tags, location_tags, links = tags

        for title_tag, location_tag, link in zip(title_tags, location_tags, links):
            title = title_tag.text.strip()
            location = location_tag.text.strip()
            job_detail_url = link

            if job_detail_url and job_detail_url not in self.processed_urls:
                job_open, deadline_job = self.get_job_details(job_detail_url)

                if job_open and deadline_job:
                    values = {
                        "title": title,
                        "location": location,
                        "Posted_On": job_open,
                        "Deadline": deadline_job,
                    }
                    descriptions.append(values)
                    self.processed_urls.add(job_detail_url)
                else:
                    print(f"Skipping job_detail_url without details: {job_detail_url}")

        return descriptions
    

class ScrapFile:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

    def write_to_csv(self, data):
        with open(self.csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["title", "location", "Posted_On", "Deadline"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if csv_file.tell() == 0:
                writer.writeheader()

            for row in data:
                writer.writerow(row)

def create_csv_file(csv_file_path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    new_csv_file_path = f"job_{timestamp}.csv"
    with open(new_csv_file_path, "w", newline="", encoding="utf-8") as new_csv_file:
        fieldnames = ["title", "location", "Posted_On", "Deadline"]
        writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
        writer.writeheader()
    return new_csv_file_path

if __name__ == "__main__":
    base_url = "https://www.jobsnepal.com/"

    while True:
        csv_file_path = input("Enter a csv file name: ")

        if os.path.exists(csv_file_path):
            job_scraper = JobScraper(base_url, csv_file_path)
            scrap_file = ScrapFile(csv_file_path)
        else:
            print(f"CSV file not found: {csv_file_path}")
            create_new_file = input("Do you want to create a new CSV file? (yes/no): ").lower() == "yes"
            if create_new_file:
                csv_file_path = create_csv_file(csv_file_path)
                job_scraper = JobScraper(base_url, csv_file_path)
                scrap_file = ScrapFile(csv_file_path)
            else:
                print("Exiting program.")
                break

        job_data = job_scraper.scrape_jobs()
        scrap_file.write_to_csv(job_data)

        add_another_csv = input("Do you want to add another CSV file? (yes/no): ").lower() == "yes"
        if not add_another_csv:
            em = MIMEMultipart()
            automation(sender_email, sender_password, receivers)
            print("Successfully sent email.")
            break