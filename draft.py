import os
import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, base_url, headers):
        self.BASE_URL = base_url
        self.HEADERS = headers

    def scrape_jobs(self):
        response = requests.get(self.BASE_URL, headers=self.HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_tags = soup.find_all("h2", class_="job-title")
            titles = [title.text.strip() for title in title_tags]
            location_tags = soup.find_all("span", class_="location")
            locations = [location.text.strip() for location in location_tags]
            return list(zip(titles, locations))
        else:
            print(f"Error: Unable to fetch: {response.status_code}")
            return []

class CsvWriter:
    @staticmethod
    def write_to_csv(data, file_path):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f"job_{timestamp}.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Location"])
            writer.writerows(data)

class DataComparator:
    @staticmethod
    def compare_and_write_diff(new_data, directory_path, file_path):
        existing_data = []

        for filename in os.listdir(directory_path):
            try:
                if filename.endswith(".csv"):
                    existing_data += pd.read_csv(os.path.join(directory_path, filename)).to_records(index=False).tolist()
            except FileNotFoundError as en :
                print("file not found")

        new_data_df = pd.DataFrame(new_data, columns=["Title", "Location"])
        existing_data_df = pd.DataFrame(existing_data, columns=["Title", "Location"])

        new_data_no_duplicates = new_data_df.drop_duplicates(subset=["Title", "Location"])
        existing_data_no_duplicates = existing_data_df.drop_duplicates(subset=["Title", "Location"])

        diff_data = new_data_no_duplicates[~new_data_no_duplicates.isin(existing_data_no_duplicates)].dropna()

        CsvWriter.write_to_csv(diff_data.to_records(index=False).tolist(), file_path)

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port, subject, body):
        self.SENDER_EMAIL = sender_email
        self.SENDER_PASSWORD = sender_password
        self.SMTP_SERVER = smtp_server
        self.SMTP_PORT = smtp_port
        self.SUBJECT = subject
        self.BODY = body

    def send_email(self, receivers, file_path):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        with open(file_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=file_path)
            part['Content-Disposition'] = f'attachment; filename="{file_path}"'

        for receiver_email in receivers:
            message = MIMEMultipart()
            message['From'] = self.SENDER_EMAIL
            message['To'] = receiver_email
            message['Subject'] = self.SUBJECT
            message.attach(MIMEText(self.BODY, 'plain'))
            message.attach(part)

            try:
                with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                    server.starttls()
                    server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
                    server.sendmail(self.SENDER_EMAIL, receiver_email, message.as_string())
                print(f"Email sent successfully to {receiver_email}")
            except smtplib.SMTPAuthenticationError as e:
                print(f"Failed to send email to {receiver_email}. Authentication error: {e}")
            except Exception as e:
                print(f"An error occurred while sending email to {receiver_email}: {e}")

        print("Email sending process completed.")

if __name__ == "__main__":
    BASE_URL = "https://www.jobsnepal.com/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }

with open('receivers.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    RECEIVERS = [row[0] for row in reader]

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SUBJECT = "Job Postings"
    BODY = "Dear sir/mam, I hope this email finds you well. It is to notify that my email automation task has been completed."


    EXISTING_DATA_DIRECTORY = "/path/to/existing/data"
    scraper = Scraper(BASE_URL, HEADERS)
    csv_writer = CsvWriter()
    data_comparator = DataComparator()
    email_sender = EmailSender("lewishacker4@gmail.com", "faixvssubgtmipvk", SMTP_SERVER, SMTP_PORT, SUBJECT, BODY)

    job_data = scraper.scrape_jobs()
    diff_file_path = "job_diff.csv"
    data_comparator.compare_and_write_diff(job_data, EXISTING_DATA_DIRECTORY, diff_file_path)

    email_sender.send_email(RECEIVERS, diff_file_path)

    print("Successfully sent emails.")
