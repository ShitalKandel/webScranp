import smtplib
import ssl
from email.message import EmailMessage



sender_email = 'lewishacker4@gmail.com'
receiver_email = input('Enter your gmail:')
sender_app_password = 'faixvssubgtmipvk'  


subject = "Check if this mail is useful."
body = '''
Dear sir/mam,
    
    I hope this email finds you useful. It is to notify that my email 
    automation task has been completed.
'''


em = EmailMessage()
em ['From'] = sender_email
em ['To'] = receiver_email
em ['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)as smtp:
        smtp.login(sender_email,sender_app_password)
        smtp.sendmail(sender_email,receiver_email,em.as_string())
        print("email has been sent successfully")
except Exception:
    print("Unable to send email.")


