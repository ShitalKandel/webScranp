import os
import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email_automation_with_csv import automation, sender_email, sender_password, receivers
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

base_url = "https://www.jobsnepal.com/"

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
     'Accept-Language': 'en-US,en;q=0.9',
     'Connection': 'keep-alive'
}

class JobScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.processed_urls = set()

    def get_tags(self, url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title_tags = soup.find_all("h2", class_="job-title")
            title_text = [title.text.strip() for title in title_tags]

            location_tags = soup.find_all("span", class_="location")
            location_text = [location.text.strip() for location in location_tags]

            div_tags = soup.find_all("div", class_="col-sm-6 col-md-6 col-lg-4 mb-3")
            links = [urljoin(self.base_url, div.find("a")["href"]) if div.find("a") else None for div in div_tags]

            return title_text, location_text, links
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
            title = title_tag
            location = location_tag
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
                    print(f"job_detail_url lists: {job_detail_url}")

        return descriptions

class ScrapFile:
    @staticmethod
    def create_csv_file():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_csv_file_path = f"job_{timestamp}.csv"
        with open(new_csv_file_path, "w", newline="", encoding="utf-8") as new_csv_file:
            fieldnames = ["title", "location", "Posted_On", "Deadline"]
            writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
            writer.writeheader()
        return new_csv_file_path

    @staticmethod
    def get_existing_csv_files():
        return [file for file in os.listdir() if file.startswith("job_") and file.endswith(".csv")]

    @staticmethod
    def write_to_csv(data, csv_file_path):
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, "w", newline="", encoding="utf-8") as new_csv_file:
                fieldnames = ["title", "location", "Posted_On", "Deadline"]
                writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open(csv_file_path, "a", newline="", encoding="utf-8") as existing_file:
            writer = csv.DictWriter(existing_file, fieldnames=["title", "location", "Posted_On", "Deadline"])
            writer.writerows(data)

class JobManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def compare_and_update(self, new_data, csv_file_path):
        existing_data = []
        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", newline="", encoding="utf-8") as existing_file:
                reader = csv.DictReader(existing_file)
                existing_data = [row for row in reader]

        unique_data = [job for job in new_data if job not in existing_data]
        if unique_data:
            with open(csv_file_path, "a", newline="", encoding="utf-8") as existing_file:
                writer = csv.DictWriter(existing_file, fieldnames=["title", "location", "Posted_On", "Deadline"])
                writer.writerows(unique_data)

    def log_job_scraps(self, job_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("job_scraps_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp}: Scraped {len(job_data)} jobs.\n")

    def run(self):
        job_scraper = JobScraper(self.base_url)
        job_data = job_scraper.scrape_jobs()

        if job_data:
            csv_file_path = ScrapFile.create_csv_file()
            ScrapFile.write_to_csv(job_data, csv_file_path)
            self.compare_and_update(job_data, csv_file_path)
            self.log_job_scraps(job_data)
            
            # Sending email
            em = MIMEMultipart()
            automation(sender_email, sender_password, receivers)
            print("Successfully sent email.")
        else:
            print("No job data scraped.")

if __name__ == "__main__":
    job_manager = JobManager(base_url)
    job_manager.run()
