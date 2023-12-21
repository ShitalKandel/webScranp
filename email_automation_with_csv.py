#Import necessary modules 

import smtplib 
'''Used to send mail to any internet machine with an Simple Mail
Transport Protocol'''

from email.mime.multipart import MIMEMultipart
'''MIME(Multipart Mail Extension is an extension of SMTP that let's 
user to exchange different data through email)'''
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import ssl
'''Provides built in function and classes to use Secure Socket Layer
and Transport Security Layer to secure both communication server
including client side.'''


sender_email = 'lewishacker4@gmail.com'#sender email (host_name) from where we will send email
receiver_email = input('Enter your gmail:')#receiver email from input

sender_app_password = 'faixvssubgtmipvk'
'''app password generated by 2factor authentication allows secure approach for automation
'''


subject = "Check if this mail is useful."
body = '''
Dear sir/mam,

    I hope this email finds you well. It is to notify that my email 
    automation task has been completed.
'''

csv_file_path = 'dec 14.csv'#path of file to be sent

#creating mime object for email
em = MIMEMultipart()
em['From'] = sender_email
em['To'] = receiver_email
em['Subject'] = subject
em.attach(MIMEText(body, 'plain'))


#attach csv file to email
with open(csv_file_path, 'r') as file:
    em.attach(MIMEApplication(file.read(), Name='dec_14.csv'))

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtpObj:
        smtpObj.login(sender_email, sender_app_password)
        smtpObj.sendmail(sender_email, receiver_email, em.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
