import smtplib
import csv
import os
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

sender_email = "lewishacker4@gmail.com"
sender_password = "faixvssubgtmipvk"

with open('receivers.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    receivers = [row[0] for row in reader]

subject = "Check if this mail is useful."
body = '''
Dear sir/mam,

    I hope this email finds you well. It is to notify that my email 
    automation task has been completed.
'''

def automation(sender_email, sender_password, receivers, file_path1, file_path2):
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = ', '.join(receivers)
  msg['Subject'] = "Job Data Update"

  body = "Attached are the updated job data."
  msg.attach(MIMEText(body, 'plain'))

  # Open the files in binary mode and attach them to the message
  for file_path in [file_path1, file_path2]:
      with open(file_path, 'rb') as attachment:
          part = MIMEBase('application', 'octet-stream')
          part.set_payload((attachment).read())

      encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
      msg.attach(part)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(sender_email, sender_password)
  text = msg.as_string()
  server.sendmail(sender_email, receivers, text)
  server.quit()
