import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

sender_email = "lewishacker4@gmail.com"

sender_password = "faixvssubgtmipvk"
smtp_server = "smtp.gmail.com"
smtp_port = 587


with open('receivers.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    receivers = [row[0] for row in reader]


subject = "Subject of your email"
body = "Body of your email"

def automation(sender_email,sender_password,receivers):
    for receiver_email in receivers:

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        
        csv_attachment = MIMEApplication(open('dec_21.csv', 'rb').read())
        csv_attachment.add_header('Content-Disposition', 'attachment', filename='dec_21.csv')
        message.attach(csv_attachment)

        message.attach(MIMEText(body, 'plain'))

        try:

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email sent successfully to {receiver_email}")
        except smtplib.SMTPAuthenticationError as e:
            print(f"Failed to send email to {receiver_email}. Authentication error: {e}")
        except Exception as e:
            print(f"An error occurred while sending email to {receiver_email}: {e}")

    print("Email sending process completed.")
