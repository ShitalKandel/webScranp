
import os
import csv
from datetime import datetime
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

    """
    This class scraps jobs details form the url and get's job details
    """
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
            else:
                job_open_on, deadline = None, None

            return job_open_on, deadline
        else:
            return None, None

   
    def scrape_jobs(self):
        descriptions = []

        tags = self.get_tags(self.base_url)

        if not tags:
            print("No tags found")
            return descriptions

        title_text, location_text, links = tags

        for title_tag, location_tag, link in zip(title_text, location_text, links):
            title = title_tag
            location = location_tag
            job_detail_url = link

            if job_detail_url and job_detail_url not in self.processed_urls:
                job_open, deadline_job = self.get_job_details(job_detail_url)
                values = {
                    "title": title,
                    "location": location,
                    "Posted_On": job_open,
                    "Deadline": deadline_job,
                }
                descriptions.append(values)
        return descriptions



class ScrapFile:
   def __init__(self):
       pass

   def get_existing_csv_files(self):
        return[file for file in os.listdir() if file.startswith("job_") and file.endswith(".csv")]

   def create_csv_file(self):
       timestamp = datetime.now().strftime("%Y%m%d")
       new_csv_file_path = f"job_{timestamp}.csv"
       with open(new_csv_file_path, "w", newline="", encoding="utf-8") as new_csv_file:
           fieldnames = ["title", "location", "Posted_On", "Deadline"]
           writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
           writer.writeheader()
       return new_csv_file_path

   def write_to_csv(self, data, csv_file_path):
       with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
           writer = csv.DictWriter(csv_file, fieldnames=["title", "location", "Posted_On", "Deadline"], extrasaction='ignore')
           writer.writerows(data)

   def write_unique_data(self, new_csv_file_path, scrap_data):
        list_files = self.get_existing_csv_files()
        for timestamp in new_csv_file_path:
            if timestamp in new_csv_file_path == new_csv_file_path in list_files:
                with open(csv_file_path,'r',newline="",encoding ="utf-8") as existing_file:
                    existing_reader = csv.reader(existing_file)
                    existing_data = list(existing_reader)

                unique_data = [row for row in scrap_data if row not in existing_data]

                with open(csv_file_path,'a',newline="",encoding ="utf-8") as append_file:
                    writer = csv.DictWriter(append_file,fieldnames=["title", "location", "Posted_On", "Deadline"],extrasaction="ignore")
                    writer.writerows(unique_data)


class JobManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def log_job_scraps(self, job_data):
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       try:
           with open("job_scraps_log.txt", "a", encoding="utf-8") as log_file:
               log_file.write(f"{timestamp}: Scraped {len(job_data)} jobs.\n")
       except IOError:
           print("Failed to write to log file.")


if __name__ == "__main__":
   base_url = "https://www.jobsnepal.com/"

   job_scraper = JobScraper(base_url)
   scrap_file_instance = ScrapFile()

   scraped_data = job_scraper.scrape_jobs()
   csv_file_path = scrap_file_instance.create_csv_file()
   scrap_file_instance.write_to_csv(scraped_data,csv_file_path)
   store_data = scrap_file_instance.write_unique_data(scraped_data, csv_file_path)

   job_manager = JobManager(base_url)
   job_manager.log_job_scraps(scraped_data)
   email = automation(sender_email, sender_password, receivers, store_data)

   print("Successfully sent email.")

