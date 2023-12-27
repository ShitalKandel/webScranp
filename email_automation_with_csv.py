import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import ssl

sender_email = 'lewishacker4@gmail.com'
receiver_email = input('Enter your gmail:')
sender_app_password = 'faixvssubgtmipvk'

subject = "Check if this mail is useful."
body = '''
Dear sir/mam,

    I hope this email finds you well. It is to notify that my email 
    automation task has been completed.
'''

def automation(em,sender_email, sender_app_password, receiver_email, csv_file_path):
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))


    with open(csv_file_path, 'r') as file:
        em.attach(MIMEApplication(file.read(),Name = csv_file_path))

    
    context = ssl.create_default_context()

    try:
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtpObj:
    
            smtpObj.login(sender_email, sender_app_password)
        
            smtpObj.sendmail(sender_email, receiver_email, em.as_string())
            print("Email sent successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

